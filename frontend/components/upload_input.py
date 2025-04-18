from typing import List
import requests
import streamlit as st
# For Streamlit run only, because of the way the project is structured
from utils import extract_text_from_file


def upload_candidate_input(api_url: str, upload_options: List):
    st.markdown("### Step 2: 📤 Upload Resume and Evaluate")
    uploaded_file = st.file_uploader(f"Upload a [`{"`, `".join(upload_options)}`] CV file", type=upload_options)
    if uploaded_file:
        raw_text = extract_text_from_file(uploaded_file)
        if not raw_text:
            st.error("Failed to extract text from file.")
        else:
            st.text_area("📄 Extracted Resume Text", raw_text, height=200)
        if st.button("Parse Resume"):
            with st.spinner("Parsing resume..."):
                resp = requests.post(f"{api_url}/parse_resume", json={"raw_text": raw_text})
                resp.raise_for_status()
                parsed = resp.json()
                st.success("Resume parsed successfully")
                st.json(parsed)
                st.session_state.candidate_data.append(parsed)
