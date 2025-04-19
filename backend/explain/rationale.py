from backend.parsers.schema import CandidateProfile
import re
from typing import List, Dict
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
import nltk
from nltk.corpus import stopwords


def normalize(term: str) -> str:
    """
    Normalizes a string by lowercasing and removing non-alphanumeric characters.
    Example: 'CI/CD' → 'cicd', 'Node.js' → 'nodejs'
    """
    return re.sub(r"[^a-zA-Z0-9]", "", term.lower())


def extract_keywords(text: str, top_n: int = 10) -> List[str]:
    try:
        nltk.data.find("corpora/stopwords")
    except LookupError:
        nltk.download("stopwords")
    # Clean punctuation and lowercase
    tokens = text.lower().split()
    # Extend stopwords set
    custom_stopwords = set(ENGLISH_STOP_WORDS).union(
        set(stopwords.words("english")),  # get list of stopwords from nltk
        {
            "looking",
            "experience",
            "required",
            "preferred",
            "candidate",
            "will",
            "must",
            "ability",
            "skill",
            "skills",
            "year",
            "years",
            "etc",
            "job",
            "role",
            "responsibilities",
        },
    )
    filtered = [
        normalize(t) for t in tokens if t not in custom_stopwords and len(t) >= 2
    ]
    freq: Dict = {}
    for token in filtered:
        freq[token] = freq.get(token, 0) + 1
    ranked = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    return [token for token, _ in ranked[:top_n]]


def explain_match(candidate: CandidateProfile, job_text: str) -> str:
    candidate_terms_raw = set(
        t.lower() for t in candidate.skills + candidate.job_titles + candidate.education
    )
    candidate_terms = {normalize(t) for t in candidate_terms_raw}
    job_terms = extract_keywords(job_text, top_n=15)

    matched = [term for term in job_terms if term.lower() in candidate_terms]
    missing = [term for term in job_terms if term.lower() not in candidate_terms]

    output = [f"Matched {len(matched)} of {len(job_terms)} key terms:"]
    for term in matched:
        output.append(f"✓ {term}")
    for term in missing:
        output.append(f"✗ {term}")

    return "\n".join(output)
