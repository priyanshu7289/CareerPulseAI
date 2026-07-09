import streamlit as st


def render_hero():
    user = st.session_state.get("user", {})

    name = user.get("name", "Guest")
    role = user.get("target_role", "Career Explorer")

    st.title(f"🚀 Welcome back, {name}")
    st.caption("AI Powered Career Intelligence Platform")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("Jobs", "124K+")

    with c2:
        st.metric("Companies", "8.4K+")

    with c3:
        st.metric("Avg Salary", "₹14.2L")

    with c4:
        st.metric("Target Role", role)

    st.divider()
