"""
dashboard/skill_gap.py
CareerPulse AI - Skill Gap Analysis
"""

import streamlit as st

from resume_parser.file_parser import extract_resume_text
from resume_parser.skill_extractor import SkillExtractor


ROLE_SKILLS = {

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
        "SQL",
        "Machine Learning",
        "Deep Learning",
        "Statistics",
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
        "Machine Learning",
    ],
}


COURSE_RECOMMENDATIONS = {

    "Python": "Python for Data Analytics",

    "SQL": "Advanced SQL",

    "Power BI": "Microsoft Power BI",

    "Tableau": "Tableau Desktop Specialist",

    "Machine Learning": "Machine Learning Specialization",

    "Statistics": "Statistics for Data Science",

    "Spark": "Apache Spark Fundamentals",

    "AWS": "AWS Cloud Practitioner",

    "Airflow": "Apache Airflow Bootcamp",

    "TensorFlow": "TensorFlow Developer",

    "PyTorch": "PyTorch Fundamentals",

    "Docker": "Docker Essentials",

    "Communication": "Business Communication",
}


def render():

    st.title("📈 Skill Gap Analysis")

    st.write(
        "Upload your resume and compare your skills with your target role."
    )

    role = st.selectbox(
        "Target Role",
        list(ROLE_SKILLS.keys()),
    )

    uploaded_resume = st.file_uploader(
        "Upload Resume",
        type=["pdf", "docx"],
    )

    if uploaded_resume is None:
        st.info("Upload your resume to begin analysis.")
        return

    if not st.button("Analyze Skill Gap", use_container_width=True):
        return

    with st.spinner("Analyzing your resume..."):

        try:

            resume_text = extract_resume_text(
                uploaded_resume,
                uploaded_resume.name,
            )

            extractor = SkillExtractor()

            # Compatible with both versions
            if hasattr(extractor, "extract_skills"):
                current_skills = extractor.extract_skills(resume_text)
            else:
                current_skills = extractor.extract(resume_text)

        except Exception as e:

            st.error(f"❌ Resume parsing failed\n\n{e}")

            return

    current_skills = sorted(set(current_skills))

    required_skills = ROLE_SKILLS[role]

    current_lower = {skill.lower() for skill in current_skills}

    missing_skills = [

        skill

        for skill in required_skills

        if skill.lower() not in current_lower

    ]

    matched_skills = [

        skill

        for skill in required_skills

        if skill.lower() in current_lower

    ]

    score = round(

        (len(matched_skills) / len(required_skills)) * 100

    )

    st.divider()

    st.subheader("🎯 Overall Skill Match")

    st.metric("Match Score", f"{score}%")

    st.progress(score / 100)

    if score >= 85:

        st.success("Excellent! Your profile matches this role very well.")

    elif score >= 65:

        st.warning("Good profile. Learn a few more skills to improve.")

    else:

        st.error("Significant skill gap detected.")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("✅ Skills Found")

        if current_skills:

            for skill in current_skills:

                st.success(skill)

        else:

            st.warning("No skills detected.")

    with col2:

        st.subheader("❌ Missing Skills")

        if missing_skills:

            for skill in missing_skills:

                st.error(skill)

        else:

            st.success("No missing skills!")

    st.divider()

    st.subheader("📚 Recommended Learning")

    if missing_skills:

        for skill in missing_skills:

            course = COURSE_RECOMMENDATIONS.get(

                skill,

                f"Learn {skill}",

            )

            st.write(f"**{skill}** → {course}")

    else:

        st.success("No additional courses required.")

    st.divider()

    st.info(
        f"""
### 🤖 AI Recommendation

**Target Role:** {role}

**Current Match:** {score}%

Continue improving the missing skills to increase your interview chances.

A skill match above **85%** is generally considered highly competitive for internship and entry-level roles.
"""
    )
