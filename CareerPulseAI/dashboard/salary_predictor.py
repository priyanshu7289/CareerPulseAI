"""
dashboard/salary_predictor.py
Salary Predictor page — wraps models/salary_predictor.py in a Streamlit UI.
"""

import os
import streamlit as st
import pandas as pd
import plotly.express as px

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.salary_predictor import (
    generate_synthetic_training_data, train_model, predict_salary, load_model, save_model,
)

MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "models", "salary_model.joblib")


@st.cache_resource
def get_model():
    if os.path.exists(MODEL_PATH):
        return load_model(MODEL_PATH)
    data = generate_synthetic_training_data(n=5000)
    model = train_model(data, model_name="xgboost")
    save_model(model, MODEL_PATH)
    return model


def render():
    st.title("💰 Salary Predictor")
    st.caption("AI-powered salary estimate based on experience, skills, and location")

    model = get_model()

    with st.form("salary_form"):
        col1, col2 = st.columns(2)
        with col1:
            job_role = st.selectbox("Job role", [
                "Data Analyst", "Data Scientist", "ML Engineer",
                "Business Analyst", "Data Engineer", "AI/LLM Engineer",
            ])
            experience = st.slider("Experience (years)", 0.0, 20.0, 2.0, step=0.5)
        with col2:
            city = st.selectbox("City", [
                "Bangalore", "Hyderabad", "Pune", "Delhi NCR", "Mumbai", "Chennai", "Remote",
            ])
            primary_skill = st.selectbox("Primary skill set", [
                "Python + ML", "SQL + Power BI", "Python + Deep Learning",
                "Gen AI / LLMs", "Spark + Cloud", "Data Engineering",
            ])
        education = st.selectbox("Education", ["B.Tech", "M.Tech", "MCA", "MBA", "B.Sc"])
        submitted = st.form_submit_button("Predict my salary →", type="primary")

    if submitted:
        result = predict_salary(model, experience, city, primary_skill, education, job_role)

        st.divider()
        c1, c2, c3 = st.columns(3)
        c1.metric("Predicted salary", f"₹{result['predicted_salary_lpa']} LPA")
        c2.metric("Range low", f"₹{result['range_low']} LPA")
        c3.metric("Range high", f"₹{result['range_high']} LPA")

        bench_df = pd.DataFrame({
            "role": ["Data Analyst", "Data Scientist", "ML Engineer", "Business Analyst", "Data Engineer", "AI/LLM Engineer"],
            "salary": [8, 14, 18, 10, 16, 24],
        })
        bench_df["highlight"] = bench_df["role"].apply(lambda r: "Selected" if r == job_role else "Market")
        fig = px.bar(bench_df, x="role", y="salary", color="highlight",
                     color_discrete_map={"Selected": "#2a78d6", "Market": "#888780"},
                     labels={"salary": "Avg salary (LPA)", "role": ""})
        st.plotly_chart(fig, use_container_width=True)
