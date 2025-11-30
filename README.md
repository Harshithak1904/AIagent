# AI Resume Screening Agent

An intelligent AI-powered HR assistant that automatically analyzes, scores, ranks, and summarizes resumes based on a provided Job Description (JD).  
This project is built as part of the **AI Agent Development Challenge** and demonstrates real-world AI automation skills.

## 🚀 Overview

The AI Resume Screening Agent can:

- Parse resumes (PDF, DOCX, TXT)
- Extract skills, experience, and candidate information
- Extract JD skills using fuzzy matching
- Score resumes based on:
  - Skill Matching (50%)
  - Experience (30%)
  - Title/Keyword Match (20%)
- Rank all candidates automatically
- Generate a short summary for each candidate
- Provide a clean UI using Streamlit
- Export results to CSV

## 🧠 Features

### Resume Extraction  
Extracts:
- Skills  
- Years of experience  
- Name  
- Keywords  
from PDF/DOCX/TXT files using pdfplumber + python-docx.

### JD Understanding  
Uses fuzzy matching to extract relevant skills from job description.

###  Scoring System  
Weighted scoring formula:

total_score = 
  (0.50 * skill_score) + 
  (0.30 * experience_score) + 
  (0.20 * title_score)

###  Ranking  
Ranks best-matched resumes at the top.

### Summaries  
Uses a local summary generator (optional OpenAI support for better summaries).

###  Streamlit UI  
User-friendly interface:
- Upload JD
- Upload multiple resumes
- View ranked list
- Export CSV

---

## 🏗 Architecture Diagram

```
       ┌──────────────────────┐
       │     User Uploads      │
       │    JD + Resumes       │
       └───────────┬──────────┘
                   │
                   ▼
       ┌──────────────────────┐
       │     Resume Parser     │
       │ (PDF / DOCX / TXT)    │
       └───────────┬──────────┘
                   │ Parsed Data
                   ▼
     ┌─────────────────────────────┐
     │     JD Skill Extractor       │
     │     (Fuzzy Matching)         │
     └─────────────┬───────────────┘
                   │
                   ▼
        ┌─────────────────────────┐
        │      Scoring Engine      │
        │ skill + exp + title      │
        └─────────────┬───────────┘
                      │
                      ▼
        ┌──────────────────────────┐
        │  Candidate Ranking        │
        └─────────────┬────────────┘
                      │
                      ▼
       ┌──────────────────────────┐
       │     Streamlit UI          │
       │   Display + CSV Export    │
       └──────────────────────────┘
```

---

## 🛠 Tech Stack

### Backend
- Python  
- pdfplumber  
- python-docx  
- rapidfuzz  

### Frontend
- Streamlit  

### AI Logic
- Custom scoring engine  
- Fuzzy skill extractor  
- Local summarizer / OpenAI (optional)

---

## 📁 Folder Structure

```
resume-screening-agent/
│── app.py
│── requirements.txt
│── README.md
│── exports/
│── samples/
└── src/
    │── parser.py
    │── matcher.py
    │── summarizer.py
```

---

## ⚙ Installation & Running

### 1. Clone repo
```
git clone <your-repo-url>
cd resume-screening-agent
```

### 2. Create virtual environment
```
python -m venv .venv
```

### 3. Activate environment  
**Windows**
```
.venv\Scripts\activate
```
**Mac/Linux**
```
source .venv/bin/activate
```

### 4. Install dependencies
```
pip install -r requirements.txt
```

### 5. Run app
```
streamlit run app.py
```

---

## 🔑 OpenAI Integration (Optional)

Set your key:

### Windows
```
set OPENAI_API_KEY=your_key
```

### Mac/Linux
```
export OPENAI_API_KEY="your_key"
```

---

## 📤 Outputs

The system automatically creates:

```
exports/ranked_candidates.csv
```

This includes:
- Name  
- Skills  
- Summary  
- Experience   
- Title Score  
- Total Score  

## 🚧 Limitations

- Experience detection is approximate  
- Depends on skill keyword lists  
- No multilingual support  
- Resume extraction accuracy varies by file quality  

---

## 📈 Future Improvements

- Add FAISS vector search  
- Train custom NER model  
- Cloud API backend  
- Multi-language support  
- Better UI with filters & search  
- Model-based skill extraction  

---

## 🎥 Demo Video




## 🏁 Challenge Submission Checklist

✔ Working AI Agent  
✔ Clean README  
✔ Architecture diagram  
✔ GitHub Repository  
✔ CSV output  
✔ Streamlit UI  
✔ Optional demo video  

---

## 🙌 HARSHITHA K
AI Resume Screening Agent  
Built for the AI Agent Development Challenge  
