from typing import Tuple, Dict, Any
from backend.parsers.schema import CandidateProfile
from copy import deepcopy
import gender_guesser.detector as gender

from constants import RISKY_CITIES, PRESTIGE_KEYWORDS

gender_detector = gender.Detector()

def audit_bias(candidate: CandidateProfile) -> Tuple[CandidateProfile, Dict[str, Any]]:
    """
    Detects potentially bias-inducing fields and removes them from the candidate profile.
    Returns a cleaned profile and a bias metadata report.
    """
    sensitive_fields = []
    report: Dict[str, Any] = {}
    cleaned = deepcopy(candidate)
    if candidate.name:
        first_name = candidate.name.split()[0]
        gender_guess = gender_detector.get_gender(first_name) if gender_detector else "unknown"
        if gender_guess not in ['unknown', 'andy']:  # 'andy' = androgynous
            report['gender'] = gender_guess
            sensitive_fields.append('name')
            cleaned.name = ""
    if candidate.total_years_experience:
        age_estimate = int(21 + candidate.total_years_experience)
        report['age_estimate'] = age_estimate
        if age_estimate <= 21 or age_estimate > 60:
            report['age_flag'] = "outlier"
    if candidate.location:
        loc = candidate.location.lower()
        if any(city in loc for city in RISKY_CITIES):
            report['location_bias_risk'] = "high"
            sensitive_fields.append('location')
            cleaned.location = ""
    flagged_edu = []
    for edu in candidate.education:
        if any(pk in edu.lower() for pk in PRESTIGE_KEYWORDS):
            flagged_edu.append(edu)
    if flagged_edu:
        report['education_bias_flag'] = flagged_edu
        sensitive_fields.append('education')
        cleaned.education = []

    report['sensitive_fields'] = sensitive_fields

    return cleaned, report
