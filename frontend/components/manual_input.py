import streamlit as st


def manual_candidate_input():
    st.markdown("### Step 2: 📝 Enter Candidate Profiles Manually")
    num_candidates = st.number_input(
        "How many candidates?", min_value=1, max_value=10, value=1
    )
    for i in range(num_candidates):
        with st.container():
            st.markdown(f"---")
            st.markdown(f"### 🧾 Candidate #{i + 1}")
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input(f"Full Name #{i + 1}", key=f"name_{i}")
                email = st.text_input(f"Email #{i + 1}", key=f"email_{i}")
                phone = st.text_input(f"Phone #{i + 1}")
                location = st.text_input(f"Location #{i + 1}", key=f"location_{i}")
                years = st.number_input(
                    f"Years Experience #{i + 1}",
                    min_value=0.0,
                    max_value=60.0,
                    step=0.5,
                    key=f"years_{i}",
                )
            with col2:
                skills = st.text_area(
                    f"Skills (comma-separated) #{i + 1}", key=f"skills_{i}"
                )
                titles = st.text_area(
                    f"Job Titles (comma-separated) #{i + 1}", key=f"titles_{i}"
                )
                education = st.text_area(
                    f"Education (comma-separated) #{i + 1}", key=f"education_{i}"
                )
            experiences = st.text_area(
                f"Experiences (new-line-separated) #{i + 1}", key=f"exp_{i}"
            )
            st.session_state.candidate_data.append(
                {
                    "name": name,
                    "email": email,
                    "phone": phone,
                    "location": location,
                    "education": [e.strip() for e in education.split(",") if e.strip()],
                    "experiences": [
                        e.strip() for e in experiences.split("\n") if e.strip()
                    ],
                    "skills": [s.strip() for s in skills.split(",") if s.strip()],
                    "total_years_experience": years,
                    "job_titles": [t.strip() for t in titles.split(",") if t.strip()],
                }
            )
