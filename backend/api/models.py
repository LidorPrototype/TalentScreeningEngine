from typing import List, Literal, Dict, Any
from pydantic import BaseModel
from backend.parsers.schema import CandidateProfile


class ParsedEvaluationRequest(BaseModel):
    job_description: str
    candidates: List[CandidateProfile]


class RawEvaluationRequest(BaseModel):
    job_description: str
    resumes: List[str]
    method: Literal["tfidf", "sbert"] = "tfidf"


class ParseRequest(BaseModel):
    raw_text: str


class EvaluationResult(BaseModel):
    score: float
    explanation: str
    bias_report: Dict[str, Any]
    cleaned_candidate: CandidateProfile
