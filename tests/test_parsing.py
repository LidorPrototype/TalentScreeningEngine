import unittest
from backend.parsers.schema import CandidateProfile


class TestCandidateProfileParsing(unittest.TestCase):

    def test_minimal_resume_parsing(self):
        raw = (
            "John Doe\n"
            "Email: john.doe@example.com\n"
            "Phone: 052-1234567\n"
            "Skills: Python, Django, SQL\n"
            "Experience:\nSoftware Engineer at Acme Inc (2017-2022)"
        )

        profile = CandidateProfile.from_text(raw)

        self.assertEqual(profile.name.lower(), "john doe")
        self.assertEqual(profile.email, "john.doe@example.com")
        self.assertTrue("python" in profile.skills or "Python" in profile.skills)
        self.assertTrue("django" in profile.skills or "Django" in profile.skills)
        self.assertTrue("sql" in profile.skills or "SQL" in profile.skills)
        self.assertTrue("software engineer" in " ".join(profile.job_titles).lower())
        self.assertTrue(any("2017" in e for e in profile.experiences))
        self.assertIn("052", profile.phone)

    def test_fallback_name_email(self):
        raw = "Skills: Java, Spring\nExperience: Backend Engineer (2019-2022)"
        profile = CandidateProfile.from_text(raw)
        self.assertIsNotNone(profile.name)
        self.assertIsNotNone(profile.email)
        self.assertTrue("java" in profile.skills or "Java" in profile.skills)

    def test_education_detection(self):
        raw = """
        John Doe
        Education:
        B.Sc. in Computer Science, Tel Aviv University
        M.Sc. in AI
        Bachelor of Engineering Technion
        """
        profile = CandidateProfile.from_text(raw)
        self.assertTrue(any("computer science" in e.lower() for e in profile.education))


if __name__ == "__main__":
    unittest.main()
