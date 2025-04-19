from typing import List

from fastapi import FastAPI
from backend.api.evaluator import evaluate_candidates
from backend.api.models import (
    ParseRequest,
    ParsedEvaluationRequest,
    RawEvaluationRequest,
    EvaluationResult,
)
from backend.matching.sbert_scorer import SBERTScorer
from backend.matching.tfidf_scorer import TFIDFScorer
from backend.parsers.schema import CandidateProfile
from constants import CODE_VERSION, PROJECT_NAME


app_name = f"{PROJECT_NAME} - API"
app = FastAPI(title=app_name)


@app.get("/")
def root():
    return "Nothing to see here ;)"


@app.get("/health", tags=["Meta"])
def health_check():
    return {"status": "OK", "message": "API is live and responsive"}


@app.get("/version", tags=["Meta"])
def version_info():
    return {
        "version": CODE_VERSION,
        "description": app_name,
        "build": "MVP",
        "components": {
            "scorers": ["TFIDFScorer", "SBERTScorer"],
            "bias_audit": "simple ruleset",
            "explanation": "keyword overlap",
        },
    }


@app.post("/parse_resume", response_model=CandidateProfile, tags=["Parsing"])
def parse_resume(req: ParseRequest):
    return CandidateProfile.from_text(req.raw_text)


@app.post(
    "/evaluate_parsed", response_model=List[EvaluationResult], tags=["Evaluation"]
)
def evaluate_parsed(req: ParsedEvaluationRequest, method: str = "tfidf"):
    if method == "sbert":
        sbert_scorer = SBERTScorer()
        return evaluate_candidates(req.candidates, req.job_description, sbert_scorer)
    else:
        tfidf_scorer = TFIDFScorer()
        return evaluate_candidates(req.candidates, req.job_description, tfidf_scorer)


@app.post("/evaluate_raw", response_model=List[EvaluationResult], tags=["Evaluation"])
def evaluate_raw(request: RawEvaluationRequest):
    parsed_candidates = [CandidateProfile.from_text(text) for text in request.resumes]
    scorer = TFIDFScorer() if request.method == "tfidf" else SBERTScorer()
    results = evaluate_candidates(parsed_candidates, request.job_description, scorer)
    return results


# if __name__ == "__main__":
#     import uvicorn
#     import logging
#
#     logging.basicConfig(level=logging.DEBUG)
#     uvicorn.run(
#         "main:app", host="127.0.0.1", port=8000, reload=False, log_level="debug"
#     )
