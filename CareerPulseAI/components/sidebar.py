"""
components/sidebar.py
CareerPulse AI v3 Sidebar
"""

import streamlit as st
from streamlit_option_menu import option_menu


def render_sidebar():

    with st.sidebar:

        user = st.session_state.get("user")

        st.markdown(
            """
            <div style="text-align:center;">
                <img src="https://img.icons8.com/color/96/artificial-intelligence.png" width="80">
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            "<h2 style='text-align:center;'>CareerPulse AI</h2>",
            unsafe_allow_html=True,
        )

        st.markdown(
            "<p style='text-align:center;color:gray;'>AI Career Intelligence Platform</p>",
            unsafe_allow_html=True,
        )

        st.divider()

        # ---------------- USER ----------------

        if user:

            st.markdown(
                f"""
                <div style="
                    background:#F5F7FA;
                    padding:18px;
                    border-radius:15px;
                    text-align:center;
                    margin-bottom:20px;
                ">

                <h3 style="margin-bottom:5px;">
                    👤 {user['name']}
                </h3>

                <p style="color:#666;margin-top:0;">
                    {user['target_role']}
                </p>

                </div>
                """,
                unsafe_allow_html=True,
            )

        # ---------------- MENU ----------------

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
                    "padding": "0!important",
                    "background-color": "#ffffff",
                },

                "icon": {
                    "color": "#2563EB",
                    "font-size": "18px",
                },

                "nav-link": {
                    "font-size": "16px",
                    "text-align": "left",
                    "margin": "4px",
                    "--hover-color": "#EEF4FF",
                    "border-radius": "10px",
                },

                "nav-link-selected": {
                    "background-color": "#2563EB",
                },
            },
        )

        st.divider()

        # ---------------- QUICK STATS ----------------

        st.markdown("### 📊 Quick Stats")

        c1, c2 = st.columns(2)

        c1.metric("Score", "84")

        c2.metric("Reports", "12")

        st.divider()

        st.success("🟢 All Systems Operational")

        st.caption("Version 3.0")

        st.divider()

        # ---------------- LOGOUT ----------------

        if st.button("🚪 Logout", use_container_width=True):

            st.session_state.logged_in = False
            st.session_state.user = None
            st.session_state.auth_page = "login"

            st.rerun()

    return selected