import unittest
from backend.parsers.schema import CandidateProfile
from backend.matching.tfidf_scorer import TFIDFScorer


class TestTFIDFScorer(unittest.TestCase):

    def setUp(self):
        self.job_text = (
            "We are looking for a backend engineer with strong skills in Python, Django, "
            "PostgreSQL, and experience in building REST APIs and CI/CD pipelines."
        )

        self.good_candidate = CandidateProfile(
            name="Alice",
            email="alice@example.com",
            phone="0521234567",
            location="Tel Aviv",
            education=["B.Sc. in Computer Science"],
            experiences=["Built scalable APIs using Django"],
            skills=["Python", "Django", "PostgreSQL", "CI/CD"],
            total_years_experience=5,
            job_titles=["Backend Engineer"],
        )

        self.bad_candidate = CandidateProfile(
            name="Bob",
            email="bob@example.com",
            phone="0530000000",
            location="Haifa",
            education=["B.A. in History"],
            experiences=["Managed a bookstore"],
            skills=["Sales", "Excel", "Writing"],
            total_years_experience=2,
            job_titles=["Customer Support"],
        )

        self.scorer = TFIDFScorer()

    def test_good_candidate_scores_higher(self):
        good_score = self.scorer.score(self.good_candidate, self.job_text)
        bad_score = self.scorer.score(self.bad_candidate, self.job_text)

        self.assertGreater(good_score, bad_score)
        self.assertGreater(good_score, 0.1)
        self.assertLess(bad_score, 0.1)

    def test_score_range(self):
        score = self.scorer.score(self.good_candidate, self.job_text)
        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 1.0)


if __name__ == "__main__":
    unittest.main()
