from typing import Optional, List
import uuid
import re
import spacy
from spacy.cli import download
from spacy.matcher import Matcher
from spacy.util import is_package
from pydantic import BaseModel, Field

from constants import SKILL_POOL, TITLE_POOL


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
    name: str  # Full name of candidate
    email: str  # Primary contact email
    phone: Optional[str] = None  # Optional phone number
    location: Optional[str] = None  # City or region
    education: List[str]  # List of degrees, institutions
    experiences: List[str]  # List of past job experiences (text)
    skills: List[str]  # Normalized list of skills
    total_years_experience: Optional[float] = (
        None  # Summed from all jobs, if calculable
    )
    job_titles: List[str]  # Extracted past job titles

    @staticmethod
    def from_text(text: str) -> "CandidateProfile":
        text = text.replace("\r", "\n")
        text = re.sub(r"\n{2,}", "\n\n", text)  # collapse multiple newlines
        text = re.sub(r"\s{2,}", " ", text)  # collapse double spaces
        text = text.strip()
        doc = nlp(text)

        # Extract email
        email_match = re.search(
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", text
        )
        email = email_match.group(0) if email_match else "N/A"

        # Extract phone
        phone_match = re.search(r"(?:\+972[-\s]?|0)?5\d{1}[-\s]?\d{3}[-\s]?\d{4}", text)
        phone = phone_match.group(0) if phone_match else None

        # Extract name
        name = "N/A"
        matcher = Matcher(nlp.vocab)
        patterns = [
            [{"POS": "PROPN"}, {"POS": "PROPN"}],
            [{"POS": "PROPN"}, {"POS": "PROPN"}, {"POS": "PROPN"}],
            [{"POS": "PROPN"}, {"POS": "PROPN"}, {"POS": "PROPN"}, {"POS": "PROPN"}],
        ]
        for pattern in patterns:
            matcher.add("NAME", patterns=[pattern])
        matches = matcher(doc)
        for match_id, start, end in matches:
            span = doc[start:end]
            name = span.text
            break

        # Extract location (first GPE entity)
        location = next((ent.text for ent in doc.ents if ent.label_ == "GPE"), None)

        # Extract education-related lines
        lines = text.splitlines()
        education = []
        education_pattern = r"(?i)\b(?:b\.?sc|m\.?sc|ph\.?d|bachelor(?:'s)?|master(?:'s)?)\b[^,\n]{0,80}"
        matches = re.findall(education_pattern, text)
        for education_match_raw in matches:
            education_match: str = str(education_match_raw).strip()
            education.append(education_match)

        # Extract skills (match against known list)
        skills = []
        for skill in SKILL_POOL:
            skill_pattern = r"\b{}\b".format(re.escape(skill))
            skill_match = re.search(skill_pattern, text, re.IGNORECASE)
            if skill_match:
                skills.append(skill)

        # Estimate job titles (simple: look for known titles in lines)
        job_titles = [
            line.strip()
            for line in lines
            if any(t in line.lower() for t in [d.lower() for d in TITLE_POOL])
        ]

        # Experience block (extract paragraphs with years)
        paragraphs = [p.strip() for p in text.split("\n\n") if len(p.strip()) > 40]
        experiences = [p for p in paragraphs if re.search(r"\d{4}", p)]

        # Estimate total years of experience
        year_matches = re.findall(r"\b(20[0-9]{2}|19[8-9][0-9])\b", text)
        if len(year_matches) >= 2:
            years = max(map(int, year_matches)) - min(map(int, year_matches))
        else:
            years = None

        return CandidateProfile(
            name=name,
            email=email,
            phone=phone,
            location=location,
            education=education,
            experiences=experiences,
            skills=skills,
            total_years_experience=years,
            job_titles=job_titles,
        )

    @classmethod
    def from_dict(cls, data: dict) -> "CandidateProfile":
        return cls(**data)

    def summary(self) -> str:
        return f"{self.name} ({self.email}) — Titles: {', '.join(self.job_titles)} | Skills: {', '.join(self.skills[:5])}"
