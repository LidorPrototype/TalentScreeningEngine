from typing import List

import requests
import streamlit as st

# For Streamlit run only, because of the way the project is structured
from utils import extract_text_from_file

def upload_bulk_candidate_input(api_url: str, upload_options: List, job_description: str, scoring_method: str):
    st.markdown("### Step 2: ⚡ Bulk Resume Evaluation (Evaluate Raw)")

    if "parsed_resumes" not in st.session_state:
        st.session_state.parsed_resumes = {}
    if "candidate_data" not in st.session_state:
        st.session_state.candidate_data = []

    raw_files = st.file_uploader(
        f"Upload Resumes [`{"`, `".join(upload_options)}`]",
        type=upload_options,
        accept_multiple_files=True
    )

    if raw_files and job_description and st.button("🚀 Evaluate Resumes"):
        st.session_state.parsed_resumes = {}
        st.session_state.candidate_data = []
        resumes = []
        filenames = []
        text_map = {}
        for file in raw_files:
            text = extract_text_from_file(file)
            if text:
                resumes.append(text)
                filenames.append(file.name)
                text_map[file.name] = text
            else:
                st.warning(f"❌ Could not extract text from {file.name}")
        with st.spinner("Scoring resumes..."):
            try:
                resp = requests.post(f"{api_url}/evaluate_raw", json={
                    "job_description": job_description,
                    "resumes": resumes,
                    "method": scoring_method
                })
                resp.raise_for_status()
                results = resp.json()
                for i, result in enumerate(results):
                    fname = filenames[i]
                    parsed = result["cleaned_candidate"]
                    if fname not in st.session_state.parsed_resumes:
                        st.session_state.parsed_resumes[fname] = {
                            "raw": text_map[fname],
                            "parsed": parsed,
                            "used": True
                        }
                    st.session_state.candidate_data.append(parsed)
                st.success("All resumes parsed, scored, and added to pool.")
                st.session_state.eval_results = results
            except Exception as e:
                st.error(f"Evaluation failed: {str(e)}")
