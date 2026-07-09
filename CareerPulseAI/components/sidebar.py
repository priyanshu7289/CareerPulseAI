"""
components/sidebar.py
CareerPulse AI v4 Sidebar
"""

import streamlit as st
from streamlit_option_menu import option_menu


def render_sidebar():

    with st.sidebar:

        st.markdown("""
        <style>

        section[data-testid="stSidebar"]{
            background:#1E1E2E;
        }

        .user-card{
            background:#FFFFFF;
            padding:20px;
            border-radius:16px;
            text-align:center;
            margin-bottom:20px;
            box-shadow:0 5px 15px rgba(0,0,0,.15);
        }

        .user-card h3{
            color:#111827 !important;
            margin-bottom:5px;
            font-size:20px;
        }

        .user-card p{
            color:#4B5563 !important;
            margin-top:0;
            font-size:16px;
        }

        </style>
        """, unsafe_allow_html=True)

        user = st.session_state.get("user")

        st.image(
            "https://img.icons8.com/color/96/artificial-intelligence.png",
            width=90,
        )

        st.markdown(
            "<h2 style='text-align:center;'>CareerPulse AI</h2>",
            unsafe_allow_html=True,
        )

        st.markdown(
            "<p style='text-align:center;color:#9CA3AF;'>AI Career Intelligence Platform</p>",
            unsafe_allow_html=True,
        )

        st.divider()

        if user:

            st.markdown(
                f"""
                <div class="user-card">

                <h3>👤 {user['name']}</h3>

                <p>{user['target_role']}</p>

                </div>
                """,
                unsafe_allow_html=True,
            )

        selected = option_menu(
            menu_title=None,

            options=[
                "Dashboard",
                "Resume Analyzer",
                "Salary Predictor",
                "Job Listings",
                "Career Roadmap",
                "Skill Gap",
                "Settings",
            ],

            icons=[
                "speedometer2",
                "file-earmark-person",
                "graph-up-arrow",
                "briefcase",
                "map",
                "bar-chart",
                "gear",
            ],

            default_index=0,

            styles={
                "container": {
                    "padding": "0",
                    "background-color": "#FFFFFF",
                    "border-radius": "16px",
                },

                "icon": {
                    "color": "#2563EB",
                    "font-size": "20px",
                },

                "nav-link": {
                    "color": "#111827",
                    "font-size": "16px",
                    "font-weight": "600",
                    "text-align": "left",
                    "padding": "12px",
                    "margin": "5px",
                    "border-radius": "10px",
                    "--hover-color": "#EEF4FF",
                },

                "nav-link-selected": {
                    "background-color": "#2563EB",
                    "color": "#FFFFFF",
                    "font-weight": "700",
                },
            },
        )

        st.divider()

        st.markdown("### 📊 Quick Stats")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Score", "84")

        with col2:
            st.metric("Reports", "12")

        st.divider()

        st.success("🟢 All Systems Operational")

        st.caption("Version 3.0")

        st.divider()

        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.rerun()

    return selected
