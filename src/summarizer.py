import os
from typing import Dict


# Local fallback summarizer (works without OpenAI)
def local_dummy_summary(resume: Dict) -> str:
    name = resume.get("name", "Candidate")
    skills = resume.get("skills", [])[:6]  # first 6 skills
    years = resume.get("years_experience")

    summary = f"{name} has experience in {', '.join(skills)}."
    
    if years:
        summary += f" They have around {years} years of experience."

    return summary

# Optional: OpenAI-based summarizer
def openai_summary(resume: Dict, jd_text: str):
    try:
        import openai

        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            return local_dummy_summary(resume) + " (No OpenAI key found)"

        openai.api_key = api_key

        prompt = f"""
Summarize the following resume in 2-3 lines, focusing on role fit.

Job Description:
{jd_text}

Resume:
{resume.get('text', '')[:2000]}

Summary:
"""

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=70,
            temperature=0.4
        )

        return response.choices[0].text.strip()

    except Exception as e:
        return local_dummy_summary(resume) + f" (Error: {str(e)})"
