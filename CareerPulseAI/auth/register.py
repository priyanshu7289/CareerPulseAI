import streamlit as st

from auth.auth_service import register_user


def show_register():

    st.markdown(
        """
        <h1 style='text-align:center;'>🚀 CareerPulse AI</h1>
        <h4 style='text-align:center;color:gray;'>
        Create your CareerPulse account
        </h4>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    st.write("### 📝 Register")

    full_name = st.text_input(
        "👤 Full Name",
        placeholder="Enter your full name",
    )

    email = st.text_input(
        "📧 Email",
        placeholder="Enter your email",
    )

    password = st.text_input(
        "🔒 Password",
        type="password",
        placeholder="Create a password",
    )

    confirm_password = st.text_input(
        "🔐 Confirm Password",
        type="password",
        placeholder="Confirm your password",
    )

    target_role = st.selectbox(
        "🎯 Target Role",
        [
            "Data Analyst",
            "Data Scientist",
            "Data Engineer",
            "ML Engineer",
        ],
    )

    agree = st.checkbox(
        "I agree to the Terms & Conditions"
    )

    st.write("")

    if st.button("🚀 Create Account", use_container_width=True):

        if not full_name.strip():
            st.warning("Please enter your full name.")
            return

        if not email.strip():
            st.warning("Please enter your email.")
            return

        if not password:
            st.warning("Please enter a password.")
            return

        if password != confirm_password:
            st.error("Passwords do not match.")
            return

        if len(password) < 8:
            st.warning("Password must be at least 8 characters.")
            return

        if not agree:
            st.warning("Please accept the Terms & Conditions.")
            return

        success, message = register_user(
            full_name,
            email,
            password,
            target_role,
        )

        if success:
            st.success("🎉 Account created successfully!")

            st.balloons()

            st.info("Please login using your new account.")

            st.session_state.auth_page = "login"

            st.rerun()

        else:
            st.error(message)