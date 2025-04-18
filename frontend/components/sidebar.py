import streamlit as st

def construct_sidebar(scoring_options, input_options):
    st.markdown("## ⚙️ Settings")

    scoring_method = st.radio(
        "Scoring Strategy",
        options=scoring_options,
        format_func=lambda x: "TF-IDF (keyword overlap)" if x == "tfidf" else "SBERT (semantic match)",
        index=0
    )

    input_mode = st.radio(
        "Candidate Input Mode",
        options=input_options,
        format_func=lambda x: "Manual Entry" if x == "manual" else "Resume Upload",
        index=0
    )

    st.markdown("---")
    st.markdown("Adjust global options for scoring and candidate ingestion.")

    return scoring_method, input_mode
