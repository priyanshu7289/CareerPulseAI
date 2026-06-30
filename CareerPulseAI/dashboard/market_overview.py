"""
dashboard/market_overview.py
Home/Market Dashboard page — KPIs, hiring trends, industry & city breakdowns.
"""

import streamlit as st
import pandas as pd
import plotly.express as px


def load_market_kpis() -> dict:
    """Replace with a real query: pd.read_sql(..., engine) against the jobs table."""
    return {
        "total_jobs": 124832, "companies": 8470, "avg_salary": 14.2, "remote_jobs": 31200,
    }


def load_monthly_trend() -> pd.DataFrame:
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    postings = [78, 82, 88, 91, 97, 102, 108, 98, 112, 118, 121, 124]
    return pd.DataFrame({"month": months, "postings_k": postings})


def load_industry_breakdown() -> pd.DataFrame:
    return pd.DataFrame({
        "industry": ["IT", "Finance", "Healthcare", "E-commerce", "EdTech", "Logistics"],
        "jobs_k": [45, 22, 18, 16, 11, 8],
    })


def load_city_breakdown() -> pd.DataFrame:
    return pd.DataFrame({
        "city": ["Bangalore", "Hyderabad", "Pune", "Delhi NCR", "Mumbai", "Chennai"],
        "jobs_k": [42, 28, 22, 19, 17, 12],
    })


def render():
    st.title("📊 Market Overview")
    st.caption("Real-time job market analytics across India's tech hubs")

    kpis = load_market_kpis()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total jobs", f"{kpis['total_jobs']:,}", "↑ 12% this month")
    c2.metric("Companies hiring", f"{kpis['companies']:,}", "↑ 5% this month")
    c3.metric("Avg salary", f"₹{kpis['avg_salary']} LPA", "↑ 8% YoY")
    c4.metric("Remote jobs", f"{kpis['remote_jobs']:,}", "↑ 22% vs last year")

    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Monthly hiring trend")
        trend_df = load_monthly_trend()
        fig = px.line(trend_df, x="month", y="postings_k", markers=True,
                      labels={"postings_k": "Postings (thousands)", "month": ""})
        fig.update_traces(line_color="#2a78d6")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Jobs by industry")
        ind_df = load_industry_breakdown()
        fig = px.bar(ind_df, x="industry", y="jobs_k", labels={"jobs_k": "Jobs (thousands)", "industry": ""})
        fig.update_traces(marker_color="#2a78d6")
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("City-wise opportunities")
    city_df = load_city_breakdown()
    fig = px.bar(city_df, x="city", y="jobs_k", labels={"jobs_k": "Jobs (thousands)", "city": ""})
    fig.update_traces(marker_color="#1baf7a")
    st.plotly_chart(fig, use_container_width=True)
