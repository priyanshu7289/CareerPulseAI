import streamlit as st

def render():

    st.title("⚙ Settings")

    user = st.session_state.get("user", {})

    st.subheader("👤 Profile")

    st.text_input(
        "Full Name",
        value=user.get("name", ""),
        disabled=True,
    )

    st.text_input(
        "Email",
        value=user.get("email", ""),
        disabled=True,
    )

    st.text_input(
        "Target Role",
        value=user.get("target_role", ""),
        disabled=True,
    )

    st.divider()

    st.subheader("🎨 Appearance")

    theme = st.radio(
        "Theme",
        ["Dark", "Light"],
    )

    st.divider()

    st.subheader("🔔 Notifications")

    st.checkbox("Email Notifications", value=True)

    st.checkbox("Weekly Career Report", value=True)

    st.divider()

    st.subheader("ℹ About")

    st.write("CareerPulse AI")

    st.write("Version 4.0")

    st.divider()

    if st.button("🚪 Logout"):

        st.session_state.logged_in = False
        st.session_state.user = None

        st.rerun()
