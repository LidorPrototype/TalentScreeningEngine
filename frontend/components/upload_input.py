from typing import List
import requests
import streamlit as st

# For Streamlit run only, because of the way the project is structured
from utils import extract_text_from_file


def upload_candidate_input(api_url: str, upload_options: List):
    st.markdown("### Step 2: 📤 Upload Multiple Resumes")

    if "candidate_data" not in st.session_state:
        st.session_state.candidate_data = []
    if "parsed_resumes" not in st.session_state:
        st.session_state.parsed_resumes = {}

    uploaded_files = st.file_uploader(
        f"Upload one or more resumes [`{"`, `".join(upload_options)}`]",
        type=upload_options,
        accept_multiple_files=True
    )
    if uploaded_files:
        for file in uploaded_files:
            file_id = file.name  # Unique per file
            if file_id not in st.session_state.parsed_resumes:
                raw_text = extract_text_from_file(file)

                if not raw_text:
                    st.warning(f"❌ Could not extract text from {file.name}")
                    continue

                with st.spinner(f"Parsing {file.name}..."):
                    res = requests.post("http://localhost:8000/parse_resume", json={"raw_text": raw_text})
                    if res.status_code == 200:
                        parsed = res.json()
                        st.session_state.parsed_resumes[file_id] = {
                            "raw": raw_text,
                            "parsed": parsed,
                            "used": False
                        }
                        st.success(f"Parsed {file.name} successfully.")
                    else:
                        st.warning(f"❌ Failed to parse {file.name}")

        # Display parsed resumes
    for fname, data in st.session_state.parsed_resumes.items():
        if not data["used"]:
            st.markdown(f"---\n### Parsed: {fname}")
            st.text_area(f"Raw Text – {fname}", data["raw"], height=200)
            st.json(data["parsed"])
            if st.button(f"💾 Use {fname}", key=f"use_{fname}"):
                st.session_state.candidate_data.append(data["parsed"])
                st.session_state.parsed_resumes[fname]["used"] = True
                st.success(f"{fname} added to evaluation pool.")

