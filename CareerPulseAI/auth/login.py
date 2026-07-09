import streamlit as st

from auth.auth_service import login_user


def show_login():

    st.markdown(
        """
        <h1 style='text-align:center;'>🚀 CareerPulse AI</h1>
        <h4 style='text-align:center;color:gray;'>
        AI-Powered Career Intelligence Platform
        </h4>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    st.write("### 🔐 Login")

    email = st.text_input(
        "📧 Email",
        placeholder="Enter your email",
    )

    password = st.text_input(
        "🔒 Password",
        type="password",
        placeholder="Enter your password",
    )

    remember = st.checkbox("Remember Me")

    st.write("")

    if st.button("🚀 Login", use_container_width=True):

        if email.strip() == "" or password.strip() == "":
            st.warning("Please enter email and password.")
            return

        success, user = login_user(email, password)

        if success and user is not None:

            st.session_state.logged_in = True

            st.session_state.user = {
                "user_id": user.user_id,
                "name": user.full_name,
                "email": user.email,
                "target_role": user.target_role,
            }

            st.success(f"Welcome back, {user.full_name}! 👋")

            st.balloons()

            st.rerun()

        else:
            st.error("❌ Invalid email or password.")