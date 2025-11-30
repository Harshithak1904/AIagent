# app.py
import os
import tempfile
import streamlit as st
import pandas as pd

# Local modules
from src.parser import parse_resume, extract_text
from src.matcher import compute_score
from src.summarizer import local_dummy_summary, openai_summary

# ----------------------------------------------------------
# Try importing FAISS functions silently (NO messages shown)
# ----------------------------------------------------------
try:
    from src.vector import add_resume_to_faiss, query_similar_resumes
    faiss_enabled = True
except:
    faiss_enabled = False


# ----------------------------------------------------------
# STREAMLIT UI SETUP
# ----------------------------------------------------------
st.set_page_config(page_title="AI Resume Screening Agent", layout="wide")
st.title("📄 AI Resume Screening Agent")


# Sidebar
with st.sidebar:
    st.header("Options")
    use_openai = st.checkbox("Use OpenAI Summaries (optional)", value=False)
    show_semantic = st.checkbox("Show Semantic Search (if available)", value=False)
    top_k = st.slider("Semantic Search Top-K", 1, 10, 5)


# ----------------------------------------------------------
# JOB DESCRIPTION INPUT
# ----------------------------------------------------------
jd_text = st.text_area("Paste Job Description", height=200)

uploaded_jd = st.file_uploader("Upload JD file (Optional)", type=["txt", "pdf", "docx"])
if uploaded_jd and not jd_text.strip():
    tmpjd = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_jd.name)[1])
    tmpjd.write(uploaded_jd.getvalue())
    tmpjd.flush()
    tmpjd.close()
    try:
        jd_text = extract_text(tmpjd.name)
    except:
        st.error("Unable to read JD file.")


# ----------------------------------------------------------
# RESUME UPLOAD
# ----------------------------------------------------------
uploaded_resumes = st.file_uploader(
    "Upload Resumes (PDF, DOCX, TXT)",
    accept_multiple_files=True,
    type=["pdf", "docx", "txt"]
)


# ----------------------------------------------------------
# PROCESS BUTTON
# ----------------------------------------------------------
if st.button("Process"):

    if not jd_text.strip():
        st.error("Please provide a Job Description first.")
        st.stop()

    if not uploaded_resumes:
        st.error("Please upload at least one resume.")
        st.stop()

    os.makedirs("exports", exist_ok=True)

    st.info("Processing resumes...")

    parsed_resumes = []

    # Parse resumes
    for f in uploaded_resumes:
        try:
            suffix = os.path.splitext(f.name)[1] or ".txt"
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
            tmp.write(f.getvalue())
            tmp.flush()
            tmp.close()

            parsed = parse_resume(tmp.name)
            parsed_resumes.append(parsed)


            # Add to FAISS if enabled
            if faiss_enabled:
                try:
                    add_resume_to_faiss(parsed.get("name", f.name), parsed.get("text", ""))
                except:
                    pass

        except:
            st.error(f"Error reading {f.name}")


    # ------------------------------------------------------
    # SCORING + SUMMARIES
    # ------------------------------------------------------
    results = []

    for r in parsed_resumes:

        scores = compute_score(jd_text, r)

        # Summaries
        summary = local_dummy_summary(r)
        if use_openai:
            try:
                summary = openai_summary(r, jd_text)
            except:
                pass

        results.append({
            "name": r.get("name", "Unknown"),
            "skills": ", ".join(r.get("skills", [])),
            "years_experience": r.get("years_experience"),
            "summary": summary,
            "skill_score": scores["skill_score"],
            "years_score": scores["years_score"],
            "title_score": scores["title_score"],
            "score": scores["total_score"]
        })

    df = pd.DataFrame(results)

    # SORTING BY FINAL SCORE
    df = df.sort_values("score", ascending=False).reset_index(drop=True)


    # ------------------------------------------------------
    # DISPLAY RESULTS
    # ------------------------------------------------------
    st.subheader("🏆 Ranked Candidates")

    for i, row in df.iterrows():
        st.markdown(f"### {i+1}. {row['name']} — **Score: {row['score']}**")
        st.write(f"**Summary:** {row['summary']}")
        st.write(f"**Skills:** {row['skills']}")

        st.progress(min(max(float(row["score"]), 0.0), 1.0))

        cols = st.columns(3)
        # cols[].metric("Skill Score", row["skill_score"])
        # cols[1].metric("Experience Score", row["years_score"])
        cols[0].metric("Title Match Score", row["title_score"])
        st.markdown("---")


    # ------------------------------------------------------
    # SEMANTIC SEARCH (FAISS)
    # Only if user enabled it + FAISS installed
    # ------------------------------------------------------
    if show_semantic and faiss_enabled:
        st.subheader("🔍 Semantic Matches")

        try:
            sem = query_similar_resumes(jd_text, top_k=top_k)
            if sem:
                for idx, item in enumerate(sem):
                    st.markdown(f"**{idx+1}. {item['resume_id']} — distance: {item['distance']:.3f}**")
                    st.write(item['text'][:500] + "...")
                    st.markdown("---")
        except:
            st.info("Semantic search unavailable.")

    elif show_semantic and not faiss_enabled:
        st.info("Semantic search requires FAISS (not installed).")


    # ------------------------------------------------------
    # EXPORT
    # ------------------------------------------------------
    out_path = "exports/ranked_candidates.csv"
    df.to_csv(out_path, index=False)
    st.success("Results exported!")

    st.download_button(
        "⬇ Download CSV",
        df.to_csv(index=False).encode("utf-8"),
        file_name="ranked_candidates.csv"
    )

    st.balloons()
