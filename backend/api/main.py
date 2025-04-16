from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from backend.parsers.schema import CandidateProfile
from constants import CODE_VERSION, PROJECT_NAME

app_name = f"{PROJECT_NAME} API"
app = FastAPI(title=app_name)

class ParsedEvaluationRequest(BaseModel):
    job_description: str
    candidates: List[CandidateProfile]

class ParseRequest(BaseModel):
    raw_text: str

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
        }
    }
