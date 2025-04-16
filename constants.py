""" This file should not contain any secrets or sensitive data """
# GLOBAL
CODE_VERSION = "1.0.0"
PROJECT_NAME = "Talent Screening Engine"

# BACKEND
SBERT_MODEL_NAME = "all-MiniLM-L6-v2"
RISKY_CITIES = {'brooklyn', 'detroit', 'compton', 'oakland', 'camden'}
PRESTIGE_KEYWORDS = ['harvard', 'yale', 'princeton', 'stanford', 'mit']
SKILL_POOL = [
    "Python", "Java", "SQL", "Machine Learning", "Data Analysis", "Django", "FastAPI", "Flask",
    "Kubernetes", "AWS", "Docker", "JavaScript", "React", "CI/CD", "Git", "Linux"
]
DEGREES = [
    "B.Sc.", "M.Sc.", "B.A.", "Ph.D.", "M.Eng.", "B.Sc. Software Engineering", "B.Sc. Computer Science", "University", "Bachelor", "Master", "College", "School", "Academy"
]
TITLE_POOL = [
    "Software Engineer", "Backend Developer", "Data Scientist", "ML Engineer",
    "DevOps Specialist", "Tech Lead", "Full Stack Developer"
]

# FRONTEND
API_URL = "http://localhost:8000"