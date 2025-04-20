import streamlit as st
import pandas as pd
import sys, os

from components.manual_input import manual_candidate_input
from components.upload_input import upload_candidate_input
from components.sidebar import construct_sidebar
from components.bulk_input import upload_bulk_candidate_input
from front_utils import format_score_label

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
if "job_description" not in st.session_state:
    st.session_state["job_description"] = ""

# SIDEBAR
with st.sidebar:
    scoring_method, input_mode = construct_sidebar(
        scoring_options=SCORING_OPTIONS, input_options=INPUT_MODE_OPTIONS
    )

# MAIN PAGE
st.markdown("### Step 1: Job Description")
st.session_state["job_description"] = st.text_area("Paste Job Description", height=200)


if input_mode == "manual":
    manual_candidate_input()
elif input_mode == "upload":
    upload_candidate_input(api_url=API_URL, upload_options=UPLOAD_FILE_OPTIONS)
elif input_mode == "evaluate_raw":
    upload_bulk_candidate_input(
        api_url=API_URL,
        upload_options=UPLOAD_FILE_OPTIONS,
        job_description=st.session_state["job_description"],
        scoring_method=scoring_method,
    )

st.markdown("---")
if st.session_state.get("candidate_data"):
    with st.expander("🧾 Candidate Summary Table", expanded=True):
        summary = []
        for idx, cand in enumerate(st.session_state["candidate_data"], 1):
            summary.append(
                {
                    # "Index": idx,
                    "Name": cand.get("name", "—"),
                    "Email": cand.get("email", "—"),
                    "Titles": ", ".join(cand.get("job_titles", [])) or "—",
                    "Skills": ", ".join(cand.get("skills", [])[:6]) or "—",
                }
            )
        df = pd.DataFrame(summary)
        st.dataframe(df, use_container_width=True)

disabled = len(st.session_state.candidate_data) == 0
if input_mode != "evaluate_raw":
    if st.button("🔍 Evaluate Candidates", disabled=disabled):
        try:
            import requests

            with st.spinner("Evaluating..."):
                url = f"{API_URL}/evaluate_parsed?method={scoring_method}"
                resp = requests.post(
                    url,
                    json={
                        "job_description": st.session_state["job_description"],
                        "candidates": st.session_state.candidate_data,
                    },
                )
                resp.raise_for_status()
                results = resp.json()
                st.session_state.eval_results = results
            st.success(f"Evaluation Complete - {scoring_method}")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

if st.session_state.get("eval_results"):
    with st.container():
        st.markdown("### 🔍 Match Score Indicators")
        st.markdown(
            """
            - 🟢 **Green** = Strong match (Score ≥ 0.75)  
            - 🟡 **Yellow** = Moderate match (0.4 ≤ Score < 0.75)  
            - 🔴 **Red** = Poor match (Score < 0.4)
            """
        )
    for i, res in enumerate(st.session_state.eval_results):
        label = format_score_label(res["score"], i)
        with st.expander(label):
            st.markdown("**Explanation**")
            st.code(res["explanation"])
            st.markdown("**Bias Report**")
            st.json(res["bias_report"])
            st.markdown("**Cleaned Candidate**")
            st.json(res["cleaned_candidate"])
