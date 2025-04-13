from abc import ABC, abstractmethod
from backend.parsers.schema import CandidateProfile

class ScoringStrategy(ABC):
    @abstractmethod
    def score(self, candidate: CandidateProfile, job_text: str) -> float:
        pass
