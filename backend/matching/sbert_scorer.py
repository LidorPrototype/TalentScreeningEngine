from sentence_transformers import SentenceTransformer, util
from backend.parsers.schema import CandidateProfile
from backend.matching.scoring_strategy import ScoringStrategy
from constants import SBERT_MODEL_NAME
from backend.utils.utils import build_weighted_candidate_blob

model = SentenceTransformer(SBERT_MODEL_NAME)


class SBERTScorer(ScoringStrategy):
    def score(self, candidate: CandidateProfile, job_text: str) -> float:
        candidate_blob = build_weighted_candidate_blob(candidate)
        embeddings = model.encode([job_text, candidate_blob], convert_to_tensor=True)
        sim = util.pytorch_cos_sim(embeddings[0], embeddings[1])
        return round(sim.item(), 4)
