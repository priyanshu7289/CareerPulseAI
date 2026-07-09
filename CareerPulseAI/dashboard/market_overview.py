"""
dashboard/market_overview.py
CareerPulse AI v3 - Professional Dashboard
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# ----------------------------
# Mock Data
# Replace these functions with database queries later
# ----------------------------

def load_market_kpis():
    return {
        "jobs": 124832,
        "companies": 8470,
        "salary": 14.2,
        "remote": 31200,
    }


def hiring_trend():
    return pd.DataFrame({
        "Month": ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],
        "Jobs": [78,82,88,91,97,102,108,98,112,118,121,124]
    })


def industries():
    return pd.DataFrame({
        "Industry":["IT","Finance","Healthcare","EdTech","E-Commerce","AI"],
        "Jobs":[45,22,18,11,16,12]
    })


def cities():
    return pd.DataFrame({
        "City":["Bangalore","Hyderabad","Pune","Delhi NCR","Mumbai","Chennai"],
        "Jobs":[42,28,22,19,17,12]
    })


def trending_skills():
    return pd.DataFrame({
        "Skill":["Python","SQL","Power BI","Tableau","Machine Learning","Generative AI"],
        "Demand":[96,90,82,75,70,68]
    })


def top_companies():
    return pd.DataFrame({
        "Company":["Google","Microsoft","Amazon","Adobe","TCS","Infosys"],
        "Openings":[2100,1980,1840,1320,1180,980]
    })


# ----------------------------
# Dashboard
# ----------------------------

def render():

    st.title("📊 Market Overview")
    st.caption("AI Powered Job Market Intelligence")

    kpi = load_market_kpis()

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "💼 Jobs Available",
        f"{kpi['jobs']:,}",
        "+12%"
    )

    c2.metric(
        "🏢 Companies",
        f"{kpi['companies']:,}",
        "+5%"
    )

    c3.metric(
        "💰 Avg Salary",
        f"₹{kpi['salary']} LPA",
        "+8%"
    )

    c4.metric(
        "🌍 Remote Jobs",
        f"{kpi['remote']:,}",
        "+22%"
    )

    st.divider()

    left, right = st.columns(2)

    # Hiring Trend
    with left:

        st.subheader("📈 Hiring Trend")

        fig = px.line(
            hiring_trend(),
            x="Month",
            y="Jobs",
            markers=True,
        )

        fig.update_layout(
            height=350,
            margin=dict(l=10, r=10, t=20, b=10),
            template="plotly_white"
        )

        st.plotly_chart(fig, use_container_width=True)

    # Industry
    with right:

        st.subheader("🏢 Industry Distribution")

        fig = px.pie(
            industries(),
            values="Jobs",
            names="Industry",
            hole=0.45
        )

        fig.update_layout(
            height=350,
            margin=dict(l=10, r=10, t=20, b=10),
        )

        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    left, right = st.columns(2)

    # Cities
    with left:

        st.subheader("🌍 Top Hiring Cities")

        fig = px.bar(
            cities(),
            x="City",
            y="Jobs",
            text_auto=True,
        )

        fig.update_layout(
            height=350,
            margin=dict(l=10, r=10, t=20, b=10),
            template="plotly_white"
        )

        st.plotly_chart(fig, use_container_width=True)

    # Skills
    with right:

        st.subheader("🔥 Trending Skills")

        fig = px.bar(
            trending_skills(),
            x="Demand",
            y="Skill",
            orientation="h",
            text_auto=True,
        )

        fig.update_layout(
            height=350,
            margin=dict(l=10, r=10, t=20, b=10),
            template="plotly_white",
        )

        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.subheader("🏆 Top Hiring Companies")

    df = top_companies()

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.subheader("🤖 AI Market Insights")

    col1, col2 = st.columns(2)

    with col1:

        st.success("""
**Top Growing Skills**

• Python

• SQL

• Power BI

• Generative AI

• Machine Learning
""")

    with col2:

        st.info("""
**Hiring Insights**

• Bangalore remains #1 hiring hub.

• Remote jobs increased by 22%.

• AI & Data roles continue to grow rapidly.

• Average salary increased by 8%.
""")