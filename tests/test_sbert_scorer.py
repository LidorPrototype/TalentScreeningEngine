import unittest
from backend.parsers.schema import CandidateProfile
from backend.matching.sbert_scorer import SBERTScorer


class TestSBERTScorer(unittest.TestCase):

    def setUp(self):
        self.job_text = (
            "Looking for a senior backend engineer experienced with Django, PostgreSQL, "
            "CI/CD, and containerized deployments."
        )

        self.matching_candidate = CandidateProfile(
            name="Sarah",
            email="sarah@example.com",
            phone="0529999999",
            location="Jerusalem",
            education=["M.Sc. Software Engineering"],
            experiences=["Worked on Django APIs and CI/CD using Docker"],
            skills=["Django", "PostgreSQL", "Docker"],
            total_years_experience=6,
            job_titles=["Senior Backend Engineer"],
        )

        self.random_candidate = CandidateProfile(
            name="Tom",
            email="tom@example.com",
            phone="0508888888",
            location="Eilat",
            education=["PhD in Linguistics"],
            experiences=["Published poetry"],
            skills=["Writing", "Editing"],
            total_years_experience=1,
            job_titles=["Poet"],
        )

        self.scorer = SBERTScorer()

    def test_semantic_relevance(self):
        score_good = self.scorer.score(self.matching_candidate, self.job_text)
        score_bad = self.scorer.score(self.random_candidate, self.job_text)

        self.assertGreater(score_good, score_bad)
        self.assertGreater(score_good, 0.3)
        self.assertLess(score_bad, 0.2)

    def test_score_bounds(self):
        score = self.scorer.score(self.matching_candidate, self.job_text)
        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 1.0)


if __name__ == "__main__":
    unittest.main()
