import re
from typing import Dict, Any, List
from rapidfuzz import fuzz


# ----------------------------------------------------
# 1) Extract JD Skills (Fuzzy Matching – Correct & Robust)
# ----------------------------------------------------
def jd_extract_skills(jd_text: str) -> List[str]:
    jd_text = jd_text.lower()

    common_skills = [
        "python", "java", "sql", "javascript", "html", "css",
        "machine learning", "deep learning", "ai", "ml",
        "data analysis", "communication", "django", "flask",
        "react", "node", "cloud", "aws", "apis"
    ]

    extracted = []
    for skill in common_skills:
        score = fuzz.partial_ratio(skill, jd_text)
        if score >= 70:      # fuzzy threshold
            extracted.append(skill)

    return extracted


# ----------------------------------------------------
# 2) Normalize function
# ----------------------------------------------------
def normalize(value: float, max_value: float) -> float:
    if max_value == 0:
        return 0.0
    return min(value / max_value, 1.0)


# ----------------------------------------------------
# 3) Compute Final Resume Score
# ----------------------------------------------------
def compute_score(jd_text: str, resume: Dict[str, Any]) -> Dict[str, float]:
    # JD extracted skills
    jd_skills = jd_extract_skills(jd_text)

    # Resume extracted skills
    resume_skills = [s.lower() for s in resume.get("skills", [])]

    # Years of experience
    years = resume.get("years_experience", 0)

    # Text fields
    resume_text = resume.get("text", "").lower()
    jd_text_lower = jd_text.lower()

    # ----------------------------------------
    # A) Skill Score (50% weight)
    # ----------------------------------------
    if jd_skills:
        matched_skills = sum(1 for skill in jd_skills if skill in resume_skills)
        skill_score = normalize(matched_skills, len(jd_skills))
    else:
        skill_score = 0.0

    # ----------------------------------------
    # B) Experience Score (30% weight)
    # ----------------------------------------
    experience_score = normalize(years, 10)

    # ----------------------------------------
    # C) Title/Text Similarity Score (20% weight)
    # ----------------------------------------
    title_score = fuzz.partial_ratio(jd_text_lower, resume_text) / 100.0

    # ----------------------------------------
    # D) Weighted Total Score
    # ----------------------------------------
    total_score = (
        skill_score * 0.50 +
        experience_score * 0.30 +
        title_score * 0.20
    )

    return {
        "skill_score": round(skill_score, 3),
        "years_score": round(experience_score, 3),
        "title_score": round(title_score, 3),
        "total_score": round(total_score, 3)
    }
