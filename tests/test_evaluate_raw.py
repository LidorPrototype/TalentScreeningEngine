import unittest
from fastapi.testclient import TestClient
from backend.api.main import app

client = TestClient(app)


class TestEvaluateRawEndpoint(unittest.TestCase):

    def setUp(self):
        self.url = "/evaluate_raw"
        self.job_description = (
            "We are looking for a backend engineer with experience in Python, Django, "
            "PostgreSQL, and building RESTful APIs."
        )
        self.resumes = [
            "John Doe\nEmail: john@example.com\nSkills: Python, Django, PostgreSQL",
            "Jane Roe\nEmail: jane@example.com\nSkills: Excel, Admin, Writing",
        ]

    def test_raw_pipeline_scores_correctly(self):
        response = client.post(
            self.url,
            json={
                "job_description": self.job_description,
                "resumes": self.resumes,
                "method": "tfidf",
            },
        )
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertEqual(len(result), 2)
        score1 = result[0]["score"]
        score2 = result[1]["score"]
        self.assertGreater(score1, score2)
        self.assertGreaterEqual(score1, 0)
        self.assertLessEqual(score1, 1)

    def test_empty_resume_is_skipped_or_handled(self):
        bad_payload = {
            "job_description": self.job_description,
            "resumes": [""],
            "method": "tfidf",
        }
        response = client.post(self.url, json=bad_payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)


if __name__ == "__main__":
    unittest.main()
