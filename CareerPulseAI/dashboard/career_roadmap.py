"""
dashboard/career_roadmap.py
Career Roadmap page — step-by-step upskilling plan per target role.
"""

import streamlit as st

ROADMAPS = {
    "Data Analyst": [
        ("Excel & SQL fundamentals", "Master pivot tables, VLOOKUP, and complex SQL with JOINs, subqueries, window functions.", "4 weeks", "Free"),
        ("Python for data analysis", "Learn Pandas, NumPy, Matplotlib. Build your first EDA project.", "6 weeks", "Free"),
        ("Data visualization", "Power BI and Tableau dashboards — build and publish interactive reports.", "4 weeks", "Paid"),
        ("Statistics & probability", "Hypothesis testing, regression, A/B testing for business decisions.", "3 weeks", "Free"),
        ("Portfolio project", "Build an end-to-end analytics project — scrape, analyze, visualize, present.", "4 weeks", "Free"),
        ("Apply & crack interviews", "Resume prep, SQL interview questions, case studies, mock interviews.", "2 weeks", "Free"),
    ],
    "Data Scientist": [
        ("Python + math foundations", "Linear algebra, calculus basics, statistics with NumPy/SciPy.", "5 weeks", "Free"),
        ("Machine learning core", "Scikit-learn: regression, classification, clustering, evaluation, tuning.", "6 weeks", "Paid"),
        ("Deep learning", "TensorFlow/PyTorch, CNNs, RNNs, transfer learning, deployment.", "8 weeks", "Paid"),
        ("NLP & Gen AI", "spaCy, Transformers, LLMs, RAG pipelines, prompt engineering.", "6 weeks", "Paid"),
        ("MLOps & deployment", "Docker, MLflow, FastAPI, cloud deployment (AWS/GCP/Azure).", "4 weeks", "Paid"),
        ("Capstone project", "Build a production-grade ML system, publish to GitHub.", "4 weeks", "Free"),
    ],
    "Data Engineer": [
        ("SQL & databases", "Advanced SQL, PostgreSQL, query optimization, indexes, transactions.", "4 weeks", "Free"),
        ("Python + ETL", "Pandas, ETL pipelines, data cleaning, REST APIs, web scraping.", "5 weeks", "Free"),
        ("Big data with Spark", "PySpark, distributed computing, DataFrames, Spark SQL.", "6 weeks", "Paid"),
        ("Cloud & data warehouses", "AWS S3/Redshift or Azure/Snowflake architectures.", "5 weeks", "Paid"),
        ("Workflow orchestration", "Apache Airflow — DAG design, scheduling, monitoring.", "3 weeks", "Free"),
        ("Build a data lake project", "Design and implement a complete data engineering pipeline.", "4 weeks", "Free"),
    ],
    "ML Engineer": [
        ("Python + ML mastery", "Advanced Scikit-learn, feature engineering, model selection, tuning.", "5 weeks", "Free"),
        ("Deep learning frameworks", "PyTorch from scratch — tensors, autograd, CNNs, RNNs, attention.", "7 weeks", "Paid"),
        ("NLP & LLMs", "Hugging Face Transformers, fine-tuning LLMs, RAG, vector databases.", "6 weeks", "Paid"),
        ("MLOps & infrastructure", "Docker, Kubernetes basics, MLflow, CI/CD for ML, monitoring.", "5 weeks", "Paid"),
        ("System design for ML", "Scalable ML system design, feature stores, serving, A/B testing.", "4 weeks", "Paid"),
        ("Open-source contribution", "Contribute to a real ML library to build credibility.", "4 weeks", "Free"),
    ],
}


def render():
    st.title("🗺️ Career Roadmap")
    st.caption("AI-curated, step-by-step learning paths for your target role")

    target_role = st.selectbox("Choose your target role", list(ROADMAPS.keys()))
    steps = ROADMAPS[target_role]

    for i, (title, desc, duration, cost) in enumerate(steps, start=1):
        with st.container(border=True):
            badge = "🟢 Free" if cost == "Free" else "🟡 Paid"
            st.markdown(f"**{i}. {title}** &nbsp; `{badge}` &nbsp; ⏱ {duration}")
            st.caption(desc)

    total_weeks = sum(int(d.split()[0]) for _, _, d, _ in steps)
    st.success(f"Estimated total time to become job-ready: **{total_weeks} weeks** (~{round(total_weeks/4.3,1)} months)")
