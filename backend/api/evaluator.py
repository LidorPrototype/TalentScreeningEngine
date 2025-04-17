from typing import List, Dict, Any

from backend.matching.scoring_strategy import ScoringStrategy
from backend.parsers.schema import CandidateProfile
from backend.bias_audit.audit import audit_bias
from backend.explain.rationale import explain_match
from concurrent.futures import ThreadPoolExecutor # TODO: maybe import it inside the if statement

def evaluate_single(candidate: CandidateProfile, job_text: str, scorer) -> Dict[str, Any]:
    cleaned, audit = audit_bias(candidate)
    score = scorer.score(cleaned, job_text)
    explanation = explain_match(cleaned, job_text)

    return {
        "score": score,
        "explanation": explanation,
        "bias_report": audit,
        "cleaned_candidate": cleaned.dict(),
        "id": cleaned.id
    }

def evaluate_candidates(candidates: List[CandidateProfile], job_text: str, scorer: ScoringStrategy) -> List[Dict[str, Any]]:
    if len(candidates) > 50:
        with ThreadPoolExecutor() as executor:
            results = list(executor.map(lambda c: evaluate_single(c, job_text, scorer), candidates))
    else:
        results = [evaluate_single(c, job_text, scorer) for c in candidates]

    results.sort(key=lambda r: r["score"], reverse=True)
    return results