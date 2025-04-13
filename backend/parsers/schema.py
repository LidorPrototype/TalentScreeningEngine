from typing import Optional, List
import uuid
import spacy
from spacy.cli import download
from spacy.util import is_package
from pydantic import BaseModel, Field

from constants import SKILL_POOL, TITLE_POOL, DEGREES

def ensure_spacy_model(model_name: str = "en_core_web_sm"):
    """Ensure spaCy model is installed and loaded."""
    if not is_package(model_name):
        print(f"[INFO] Downloading missing spaCy model: {model_name}")
        download(model_name)

    return spacy.load(model_name)

nlp = ensure_spacy_model()

class CandidateProfile(BaseModel):
    """
    Structured representation of a parsed resume for downstream use.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str                                       # Full name of candidate
    email: str                                      # Primary contact email
    phone: Optional[str] = None                     # Optional phone number
    location: Optional[str] = None                  # City or region
    education: List[str]                            # List of degrees, institutions
    experiences: List[str]                          # List of past job experiences (text)
    skills: List[str]                               # Normalized list of skills
    total_years_experience: Optional[float] = None  # Summed from all jobs, if calculable
    job_titles: List[str]                           # Extracted past job titles

    @staticmethod
    def from_text(text: str) -> "CandidateProfile":
        pass # TODO: Implement it later

    @classmethod
    def from_dict(cls, data: dict) -> "CandidateProfile":
        return cls(**data)

    def summary(self) -> str:
        return f"{self.name} ({self.email}) — Titles: {', '.join(self.job_titles)} | Skills: {', '.join(self.skills[:5])}"
