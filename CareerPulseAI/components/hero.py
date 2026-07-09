"""
components/hero.py
CareerPulse AI v3 Hero Banner
"""

import streamlit as st


def render_hero():

    user = st.session_state.get("user")

    if user:
        name = user.get("name", "User")
        role = user.get("target_role", "Career Explorer")
    else:
        name = "Guest"
        role = "Career Explorer"

    st.markdown(
        f"""
        <style>

        .hero-container {{
            background: linear-gradient(135deg,#2563eb,#4f46e5,#7c3aed);
            border-radius:20px;
            padding:35px;
            color:white;
            margin-bottom:25px;
            box-shadow:0px 8px 25px rgba(0,0,0,.15);
        }}

        .hero-title {{
            font-size:38px;
            font-weight:700;
            margin-bottom:8px;
        }}

        .hero-subtitle {{
            font-size:18px;
            opacity:.92;
        }}

        .hero-card {{
            background:rgba(255,255,255,.15);
            padding:15px;
            border-radius:15px;
            text-align:center;
            margin-top:18px;
        }}

        .hero-number {{
            font-size:26px;
            font-weight:bold;
        }}

        </style>

        <div class="hero-container">

            <div class="hero-title">
                🚀 Welcome back, {name}
            </div>

            <div class="hero-subtitle">
                AI Powered Career Intelligence Platform
            </div>

            <br>

            <div style="display:flex;gap:20px;justify-content:space-between;flex-wrap:wrap;">

                <div class="hero-card">
                    <div class="hero-number">124K+</div>
                    Jobs
                </div>

                <div class="hero-card">
                    <div class="hero-number">8.4K+</div>
                    Companies
                </div>

                <div class="hero-card">
                    <div class="hero-number">₹14.2L</div>
                    Avg Salary
                </div>

                <div class="hero-card">
                    <div class="hero-number">{role}</div>
                    Target Role
                </div>

            </div>

        </div>

        """,
        unsafe_allow_html=True,
    )