from faker import Faker
from random import randint, sample, uniform
from typing import List, Union
from backend.parsers.schema import CandidateProfile
from constants import DEGREES, SKILL_POOL, TITLE_POOL

fake = Faker()


def generate_fake_candidate(
    n: int = 1,
) -> Union[CandidateProfile, List[CandidateProfile]]:
    def create_one() -> CandidateProfile:
        ex_range = randint(2, 4)
        experiences = [fake.text(max_nb_chars=100) for _ in range(ex_range)]
        years_per_role = [round(uniform(1, 4.0), 1) for _ in range(ex_range)]
        total_years_experience = round(sum(years_per_role), 1)
        return CandidateProfile(
            name=fake.name(),
            email=fake.email(),
            phone=fake.phone_number(),
            location=fake.city(),
            education=sample(DEGREES, k=randint(1, 2)),
            experiences=experiences,
            skills=sample(
                SKILL_POOL, k=randint(min(6, len(SKILL_POOL) // 2), len(SKILL_POOL))
            ),
            total_years_experience=total_years_experience,
            job_titles=sample(TITLE_POOL, k=ex_range),
        )

    if n == 1:
        return create_one()
    return [create_one() for _ in range(n)]
