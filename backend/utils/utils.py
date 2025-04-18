from backend.parsers.schema import CandidateProfile


def build_weighted_candidate_blob(candidate: CandidateProfile) -> str:
    """
    Builds a weighted string for TF-IDF where skills, titles, and education
    contribute at different levels.
    """
    skill_blob = " ".join(candidate.skills) * 3
    title_blob = " ".join(candidate.job_titles) * 2
    edu_blob = " ".join(candidate.education)

    return " ".join([skill_blob, title_blob, edu_blob])
