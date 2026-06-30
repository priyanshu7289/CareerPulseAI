"""
CareerPulse AI — Main Application Entry Point
Run with: streamlit run app.py
"""

import streamlit as st

st.set_page_config(
    page_title="CareerPulse AI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Sidebar navigation ────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/combo-chart.png", width=60)
    st.title("CareerPulse AI")
    st.caption("Intelligent Job Market Analytics")
    st.divider()

    page = st.radio(
        "Navigate",
        [
            "🏠 Market Overview",
            "💡 Skills Dashboard",
            "💰 Salary Predictor",
            "📄 Resume Analyzer",
            "🏢 Job Listings",
            "🗺️ Career Roadmap",
        ],
    )
    st.divider()
    st.caption("Data refreshed daily from LinkedIn, Naukri, Indeed")

# ── Page routing ──────────────────────────────────────────────────────────────
if page == "🏠 Market Overview":
    from dashboard.market_overview import render
    render()

elif page == "💡 Skills Dashboard":
    from dashboard.skills_dashboard import render
    render()

elif page == "💰 Salary Predictor":
    from dashboard.salary_predictor import render
    render()

elif page == "📄 Resume Analyzer":
    from dashboard.resume_analyzer import render
    render()

elif page == "🏢 Job Listings":
    from dashboard.job_listings import render
    render()

elif page == "🗺️ Career Roadmap":
    from dashboard.career_roadmap import render
    render()
