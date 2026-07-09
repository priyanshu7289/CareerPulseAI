import streamlit as st

def render():

    st.title("📈 Skill Gap Analysis")
    st.write("Compare your current skills with your target role.")

    role = st.selectbox(
        "Target Role",
        [
            "Data Analyst",
            "Data Scientist",
            "ML Engineer",
            "Data Engineer",
            "Business Analyst",
        ],
    )

    uploaded_resume = st.file_uploader(
        "Upload Resume",
        type=["pdf", "docx"],
    )

    if st.button("Analyze Skill Gap"):

        # Temporary demo data
        current_skills = [
            "Python",
            "SQL",
            "Excel",
            "Power BI",
            "Statistics",
        ]

        required_skills = {
            "Data Analyst": [
                "Python",
                "SQL",
                "Excel",
                "Power BI",
                "Tableau",
                "Statistics",
                "Machine Learning",
            ],
            "Business Analyst": [
                "Excel",
                "SQL",
                "Power BI",
                "Tableau",
                "Communication",
            ],
            "Data Scientist": [
                "Python",
                "Machine Learning",
                "Deep Learning",
                "Statistics",
                "SQL",
            ],
            "Data Engineer": [
                "Python",
                "SQL",
                "Spark",
                "Airflow",
                "AWS",
            ],
            "ML Engineer": [
                "Python",
                "TensorFlow",
                "PyTorch",
                "Docker",
                "ML",
            ],
        }

        required = required_skills.get(role, [])

        missing = [
            skill
            for skill in required
            if skill not in current_skills
        ]

        score = int(
            ((len(required) - len(missing)) / len(required)) * 100
        )

        st.subheader("🎯 Skill Match")

        st.progress(score / 100)

        st.success(f"Overall Match : {score}%")

        c1, c2 = st.columns(2)

        with c1:
            st.subheader("✅ Current Skills")

            for skill in current_skills:
                st.success(skill)

        with c2:
            st.subheader("❌ Missing Skills")

            for skill in missing:
                st.error(skill)

        st.subheader("📚 Recommended Courses")

        for skill in missing:
            st.write(f"• Learn **{skill}**")

        st.info(
            "Complete the missing skills to improve your job readiness."
        )
