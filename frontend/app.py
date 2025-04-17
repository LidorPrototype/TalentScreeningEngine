import streamlit as st
import requests, re

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from constants import API_URL, PROJECT_NAME

st.set_page_config(page_title=PROJECT_NAME, layout="wide")
st.title(f"🎯 {PROJECT_NAME}")

# SIDEBAR
with st.sidebar:
    st.markdown("## ⚙️ Settings")

    scoring_method = st.radio(
        "Scoring Strategy",
        options=["tfidf", "sbert"],
        format_func=lambda x: "TF-IDF (keyword overlap)" if x == "tfidf" else "SBERT (semantic match)",
        index=0
    )

    st.markdown("---")
    st.markdown("Adjust system-wide evaluation parameters here.")

# MAIN PAGE

st.markdown("### Step 1: Job Description")
job_description = st.text_area("Paste Job Description", height=200)

st.markdown("### Step 2: Candidates")

st.markdown("### 📤 Upload Resume (Text)")

uploaded_file = st.file_uploader("Upload a .txt resume file", type=["txt"])
if uploaded_file:
    raw_text = uploaded_file.read().decode("utf-8")
    st.text_area("📄 Extracted Resume Text", raw_text, height=200)

    raw_text = raw_text.replace("\r", "\n")
    raw_text = re.sub(r"\n{2,}", "\n", raw_text)
    raw_text = re.sub(r"\s{2,}", " ", raw_text)

    print("raw_text\n")
    print(raw_text)
    print("\nraw_text")

    if st.button("Parse Resume"):
        with st.spinner("Parsing resume..."):
            response = requests.post(f"{API_URL}/parse_resume", json={"raw_text": raw_text})
            if response.status_code == 200:
                parsed = response.json()
                st.success("Resume parsed successfully")
                st.json(parsed)

                # You can auto-add parsed candidate to candidate_data[] if desired
                # candidate_data.append(parsed)
            else:
                st.error(f"Failed to parse resume: {response.text}")

num_candidates = st.number_input("How many candidates?", min_value=1, max_value=10, value=1)

candidate_data = []

st.markdown("### Step 2: Candidate Entries")

for i in range(num_candidates):
    with st.container():
        st.markdown(f"---")
        st.markdown(f"### 🧾 Candidate #{i+1}")

        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input(f"Full Name #{i+1}", key=f"name_{i}")
            email = st.text_input(f"Email #{i+1}", key=f"email_{i}")
            phone = st.text_input(f"Phone #{i + 1}")
            location = st.text_input(f"Location #{i+1}", key=f"location_{i}")
            years = st.number_input(f"Years Experience #{i+1}", min_value=0.0, max_value=60.0, step=0.5, key=f"years_{i}")

        with col2:
            skills = st.text_area(f"Skills (comma-separated) #{i+1}", key=f"skills_{i}")
            titles = st.text_area(f"Job Titles (comma-separated) #{i+1}", key=f"titles_{i}")
            education = st.text_area(f"Education (comma-separated) #{i+1}", key=f"education_{i}")

        experiences = st.text_area(f"Experiences (new-line-separated) #{i+1}", key=f"exp_{i}")

        candidate_data.append({
            "name": name,
            "email": email,
            "phone": phone,
            "location": location,
            "education": [e.strip() for e in education.split(",") if e.strip()],
            "experiences": [e.strip() for e in experiences.split("\n") if e.strip()],
            "skills": [s.strip() for s in skills.split(",") if s.strip()],
            "total_years_experience": years,
            "job_titles": [t.strip() for t in titles.split(",") if t.strip()],
        })

if st.button("🔍 Evaluate Candidates"):
    payload = {
        "job_description": job_description,
        "candidates": candidate_data
    }

    try:
        with st.spinner("Evaluating..."):
            response = requests.post(f"{API_URL}/evaluate_parsed", json=payload)
            response.raise_for_status()
            results = response.json()

        st.success("Evaluation Complete")

        for i, res in enumerate(results):
            with st.expander(f"Candidate #{i+1} — Score: {res['score']}"):
                st.markdown("**Explanation**")
                st.code(res["explanation"])
                st.markdown("**Bias Report**")
                st.json(res["bias_report"])
                st.markdown("**Cleaned Candidate**")
                st.json(res["cleaned_candidate"])

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
