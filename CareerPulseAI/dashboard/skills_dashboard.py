"""
dashboard/skills_dashboard.py
Skills Dashboard page — top skills, emerging skills, demand growth.
"""

import streamlit as st
import pandas as pd
import plotly.express as px


def load_top_skills() -> pd.DataFrame:
    return pd.DataFrame({
        "skill": ["Python", "SQL", "Power BI", "Tableau", "Machine Learning", "Excel", "Azure", "Spark"],
        "demand_pct": [84, 76, 62, 54, 48, 44, 38, 31],
    })


def load_growth_skills() -> pd.DataFrame:
    return pd.DataFrame({
        "skill": ["Generative AI", "MLOps", "Spark", "Azure", "Airflow"],
        "growth_pct": [340, 180, 90, 75, 60],
    })


def render():
    st.title("💡 Skills Dashboard")
    st.caption("Which skills employers are actually hiring for, right now")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Top skill", "Python", "84% of jobs")
    c2.metric("Fastest growing", "Gen AI", "↑ 340% in 6mo")
    c3.metric("Highest paying", "LLMs", "Avg ₹28 LPA")
    c4.metric("Emerging", "MLOps", "↑ 180% YoY")

    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Top demanded skills")
        df = load_top_skills()
        fig = px.bar(df.sort_values("demand_pct"), x="demand_pct", y="skill", orientation="h",
                     labels={"demand_pct": "% of job postings", "skill": ""})
        fig.update_traces(marker_color="#2a78d6")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Skill demand growth")
        gdf = load_growth_skills()
        fig = px.bar(gdf, x="skill", y="growth_pct", labels={"growth_pct": "Growth %", "skill": ""})
        fig.update_traces(marker_color="#4a3aa7")
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Skill market heatmap")
    tags = {
        "Hot 🔥": ["Python", "SQL", "Generative AI"],
        "Rising 📈": ["LLMs", "MLOps", "Spark", "Azure", "Airflow", "Deep Learning"],
        "Stable": ["Power BI", "Excel", "Tableau", "AWS", "NLP", "XGBoost"],
    }
    for label, skills in tags.items():
        st.markdown(f"**{label}**")
        st.write(" · ".join(skills))
