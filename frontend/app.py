import streamlit as st
import sys, os

from components.manual_input import manual_candidate_input
from components.upload_input import upload_candidate_input
from components.sidebar import construct_sidebar

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from constants import (
    PROJECT_NAME,
    SCORING_OPTIONS,
    INPUT_MODE_OPTIONS,
    API_URL,
    UPLOAD_FILE_OPTIONS,
)

st.set_page_config(page_title=PROJECT_NAME, layout="wide")
st.title(f"🎯 {PROJECT_NAME}")

if "candidate_data" not in st.session_state:
    st.session_state.candidate_data = []

# SIDEBAR
with st.sidebar:
    scoring_method, input_mode = construct_sidebar(
        scoring_options=SCORING_OPTIONS, input_options=INPUT_MODE_OPTIONS
    )

# MAIN PAGE
st.markdown("### Step 1: Job Description")
job_description = st.text_area("Paste Job Description", height=200)


if input_mode == "manual":
    manual_candidate_input()

elif input_mode == "upload":
    upload_candidate_input(api_url=API_URL, upload_options=UPLOAD_FILE_OPTIONS)

st.markdown("---")
disabled = len(st.session_state.candidate_data) == 0
if st.button("🔍 Evaluate Candidates", disabled=disabled):
    try:
        import requests

        with st.spinner("Evaluating..."):
            url = f"{API_URL}/evaluate_parsed?method={scoring_method}"
            resp = requests.post(
                url,
                json={
                    "job_description": job_description,
                    "candidates": st.session_state.candidate_data,
                },
            )
            resp.raise_for_status()
            results = resp.json()

        st.success(f"Evaluation Complete - {scoring_method}")

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
