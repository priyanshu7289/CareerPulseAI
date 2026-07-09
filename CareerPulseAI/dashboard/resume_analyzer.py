"""
dashboard/resume_analyzer.py
Resume Analyzer page — upload resume, run skill-gap analysis, generate PDF report.
"""
from ai.career_coach import generate_career_advice
from components.ats_gauge import show_ats_gauge
from components.ai_summary import show_ai_summary
import os
import sys
import streamlit as st

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from resume_parser.file_parser import extract_resume_text
from resume_parser.skill_extractor import SkillExtractor, compare_resume_to_job, compute_career_score
from recommendation_engine.career_recommender import generate_recommendations, suggest_career_path
from models.salary_predictor import predict_salary
from dashboard.salary_predictor import get_model
from reports.report_generator import generate_career_report

# A representative aggregate job description for the target role —
# in production this is built dynamically from the `jobs`/`job_skills` tables.
TARGET_ROLE_JD = {
    "Data Analyst": "Python SQL Power BI Tableau Excel Machine Learning Spark Azure Airflow Statistics",
    "Data Scientist": "Python SQL Machine Learning Deep Learning NLP Generative AI LLMs Spark Azure AWS",
    "Data Engineer": "Python SQL Spark Airflow AWS Azure ETL Docker Kafka Hadoop",
    "ML Engineer": "Python Deep Learning PyTorch TensorFlow Docker Kubernetes MLOps Generative AI LLMs",
}


def render():
    st.title("📄 Resume Analyzer")
    st.caption("Upload your resume to see your career score, skill gaps, and learning roadmap")

    col1, col2 = st.columns([2, 1])
    with col1:
        uploaded_file = st.file_uploader("Upload resume (PDF or DOCX)", type=["pdf", "docx"])
    with col2:
        target_role = st.selectbox("Target role", list(TARGET_ROLE_JD.keys()))
        years_exp = st.number_input("Years of experience", 0.0, 30.0, 2.0, step=0.5)

    if uploaded_file is not None:
        with st.spinner("Analyzing your resume..."):
            resume_text = extract_resume_text(uploaded_file, uploaded_file.name)
            extractor = SkillExtractor()
            jd_text = TARGET_ROLE_JD[target_role]
            result = compare_resume_to_job(resume_text, jd_text, extractor)
            career_score = compute_career_score(
                result["match_percentage"], years_exp, len(result["resume_skills"])
            )

        st.divider()

        c1, c2, c3 = st.columns(3)
        c1.metric("Career score", f"{career_score} / 100")
        c2.metric("Resume match", f"{result['match_percentage']}%")
        c3.metric(
            "Skills found",
            f"{len(result['matched_skills'])} / {len(result['required_skills'])}"
        )
        show_ats_gauge(career_score)
        show_ai_summary(
    career_score,
    result["match_percentage"],
    result["missing_skills"]
)

        col_a, col_b = st.columns(2)

        with col_a:
            st.subheader("✅ Matched skills")
            for s in result["matched_skills"]:
                st.success(s, icon="✅")

        with col_b:
            st.subheader("❌ Missing skills")
            for s in result["missing_skills"]:
                st.error(s, icon="❌")

        if result["missing_skills"]:
            st.subheader("📚 Recommended learning path")

            recs = generate_recommendations(result["missing_skills"])

            st.dataframe(
                [
                    {
                        "Skill": r["skill"],
                        "Course": r["name"],
                        "Platform": r["platform"],
                        "Cost": "Free" if r["is_free"] else "Paid",
                        "Duration": f"{r['weeks']} wks",
                        "Priority": r["priority"],
                    }
                    for r in recs
                ],
                use_container_width=True,
                hide_index=True,
            )

            path = suggest_career_path(target_role, result["missing_skills"])

            st.info(
                f"**Next career step:** {path['next_career_step']}\n\n"
                f"**Suggested project:** {path['suggested_projects'][0]}"
            )

        model = get_model()

        salary_result = predict_salary(
            model,
            years_exp,
            "Bangalore",
            "Python + ML",
            "B.Tech",
            target_role,
        )

        st.divider()

        if st.button("📥 Generate full PDF career report", type="primary"):

            with st.spinner("Generating your personalized PDF report..."):

                output_path = "career_report.pdf"

                trending = [
                    ("Python", 84),
                    ("SQL", 76),
                    ("Power BI", 62),
                    ("Generative AI", 58),
                ]

                generate_career_report(
                    output_path=output_path,
                    user_name="Candidate",
                    target_role=target_role,
                    career_score=career_score,
                    resume_match_pct=result["match_percentage"],
                    matched_skills=result["matched_skills"],
                    missing_skills=result["missing_skills"],
                    predicted_salary=salary_result,
                    recommendations=generate_recommendations(result["missing_skills"])
                    or [
                        {
                            "skill": "—",
                            "name": "Keep building on your strengths",
                            "platform": "—",
                            "is_free": True,
                            "weeks": 0,
                            "priority": "Low",
                        }
                    ],
                    trending_skills=trending,
                )

            with open(output_path, "rb") as f:
                st.download_button(
                    "Download career report (PDF)",
                    f,
                    file_name="CareerPulse_Report.pdf",
                    mime="application/pdf",
                )

    else:
        st.info("👆 Upload your resume to get started, or try the demo button below.")
        st.info("👆 Upload your resume to get started, or try the demo button below.")
