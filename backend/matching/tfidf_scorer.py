from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from backend.matching.scoring_strategy import ScoringStrategy
from backend.utils.utils import build_weighted_candidate_blob
from backend.parsers.schema import CandidateProfile


class TFIDFScorer(ScoringStrategy):
    """ TF-IDF is a very naive approach, I recommend using one of the other options """
    def score(self, candidate: CandidateProfile, job_text: str) -> float:
        candidate_blob = build_weighted_candidate_blob(candidate)
        docs = [job_text, candidate_blob]
        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform(docs)
        return round(cosine_similarity(vectors[0:1], vectors[1:2])[0][0], 4)