import streamlit as st

from resume_parser.file_parser import extract_resume_text
from resume_parser.skill_extractor import SkillExtractor


def render():

    st.title("📈 Skill Gap Analysis")
    st.write("Analyze your resume against your target role.")

    role = st.selectbox(
        "Target Role",
        [
            "Data Analyst",
            "Business Analyst",
            "Data Scientist",
            "Data Engineer",
            "ML Engineer",
        ],
    )

    uploaded_resume = st.file_uploader(
        "Upload Resume",
        type=["pdf", "docx"],
    )

    if uploaded_resume is None:
        return

    if st.button("Analyze Skill Gap"):

        with st.spinner("Analyzing Resume..."):

            try:

                resume_text = extract_resume_text(
    uploaded_resume,
    uploaded_resume.name
)

                extractor = SkillExtractor()

                current_skills = extractor.extract_skills(resume_text)

            except Exception as e:

                st.error(f"Resume Parsing Failed\n\n{e}")

                return

        role_skills = {

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

        required_skills = role_skills.get(role, [])

        current_skills = list(set(current_skills))

        missing_skills = [
            skill
            for skill in required_skills
            if skill.lower()
            not in [s.lower() for s in current_skills]
        ]

        score = int(
            (
                (len(required_skills) - len(missing_skills))
                / len(required_skills)
            )
            * 100
        )

        st.subheader("🎯 Skill Match")

        st.metric("Overall Match", f"{score}%")

        st.progress(score / 100)

        col1, col2 = st.columns(2)

        with col1:

            st.subheader("✅ Current Skills")

            if current_skills:

                for skill in sorted(current_skills):
                    st.success(skill)

            else:
                st.warning("No skills detected.")

        with col2:

            st.subheader("❌ Missing Skills")

            if missing_skills:

                for skill in missing_skills:
                    st.error(skill)

            else:

                st.success("Excellent! No missing skills.")

        st.divider()

        st.subheader("📚 Recommended Learning")

        recommendations = {

            "Tableau":
                "Tableau Desktop Specialist",

            "Machine Learning":
                "Machine Learning Specialization",

            "Spark":
                "Apache Spark Fundamentals",

            "AWS":
                "AWS Cloud Practitioner",

            "Airflow":
                "Apache Airflow Bootcamp",

            "Power BI":
                "Microsoft Power BI",

            "Statistics":
                "Statistics for Data Science",

            "SQL":
                "Advanced SQL",

            "Python":
                "Python for Data Analytics",
        }

        for skill in missing_skills:

            course = recommendations.get(skill, f"Learn {skill}")

            st.write(f"• **{skill}** → {course}")

        st.info(
            f"""
🤖 AI Recommendation

Your profile currently matches **{score}%** of the skills required
for a **{role}** role.

Focus on the missing skills above to improve your employability.
"""
        )
