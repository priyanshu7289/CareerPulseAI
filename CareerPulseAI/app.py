"""
CareerPulse AI — Main Application Entry Point
Run with: streamlit run app.py
"""

import streamlit as st

from components.hero import render_hero
from components.sidebar import render_sidebar
from auth.auth_page import show_auth_page

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------

st.set_page_config(
    page_title="CareerPulse AI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------------------------------------
# Session State
# -------------------------------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None

# -------------------------------------------------
# Authentication
# -------------------------------------------------

if not st.session_state.logged_in:
    show_auth_page()
    st.stop()

# -------------------------------------------------
# Dashboard
# -------------------------------------------------

page = render_sidebar()

render_hero()

# -------------------------------------------------
# Page Routing
# -------------------------------------------------

if page == "Dashboard":
    from dashboard.market_overview import render
    render()

elif page == "Resume Analyzer":
    from dashboard.resume_analyzer import render
    render()

elif page == "Salary Predictor":
    from dashboard.salary_predictor import render
    render()

elif page == "Job Listings":
    from dashboard.job_listings import render
    render()

elif page == "Career Roadmap":
    from dashboard.career_roadmap import render
    render()

elif page == "Skill Gap":
    from dashboard.skill_gap import render
    render()

elif page == "Settings":
    from dashboard.settings import render
    render()
