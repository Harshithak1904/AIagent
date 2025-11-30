import re
import pdfplumber
import docx
from typing import Dict, Any, List


# ----------------------------------------------------
# 1) Extract raw text from any supported document
# ----------------------------------------------------
def extract_text(path: str) -> str:
    path_l = path.lower()

    # PDF
    if path_l.endswith(".pdf"):
        try:
            with pdfplumber.open(path) as pdf:
                pages = [page.extract_text() or "" for page in pdf.pages]
                return "\n".join(pages)
        except:
            return ""

    # DOCX  (Correct code)
    elif path_l.endswith(".docx"):
        try:
            document = docx.Document(path)
            return "\n".join([para.text for para in document.paragraphs])
        except:
            return ""

    # TXT
    elif path_l.endswith(".txt"):
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()
        except:
            return ""

    return ""


# ----------------------------------------------------
# 2) Extract skills from text
# ----------------------------------------------------
def extract_skills(text: str) -> List[str]:
    text = text.lower()

    possible_skills = [
        "python", "java", "sql", "javascript", "html", "css",
        "machine learning", "deep learning", "ai", "ml",
        "data analysis", "communication", "django", "flask",
        "react", "node", "cloud", "aws", "apis"
    ]

    found = [skill for skill in possible_skills if skill in text]
    return list(set(found))


# ----------------------------------------------------
# 3) Extract candidate name
# ----------------------------------------------------
def extract_name(text: str) -> str:
    for line in text.split("\n"):
        line = line.strip()
        if len(line.split()) <= 5 and len(line) > 1:
            return line
    return "Unknown"


# ----------------------------------------------------
# 4) Extract years of experience
# ----------------------------------------------------
def extract_years_experience(text: str):
    text = text.lower()
    match = re.search(r"(\d{1,2})\+?\s+years", text)
    if match:
        try:
            return int(match.group(1))
        except:
            return 0
    return 0


# ----------------------------------------------------
# 5) Main parse function
# ----------------------------------------------------
def parse_resume(path: str) -> Dict[str, Any]:
    text = extract_text(path)

    print("DEBUG TEXT LENGTH =", len(text))


    skills = [s.lower() for s in extract_skills(text)]

    name = extract_name(text)
    years = extract_years_experience(text)

    return {
        "path": path,
        "text": text,
        "name": name,
        "skills": skills,
        "years_experience": years
    }
