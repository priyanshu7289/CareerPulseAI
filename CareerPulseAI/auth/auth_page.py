import streamlit as st

from auth.login import show_login
from auth.register import show_register


def show_auth_page():

    if "auth_page" not in st.session_state:
        st.session_state.auth_page = "login"

    if st.session_state.auth_page == "login":

        show_login()

        st.write("---")

        if st.button("Create New Account"):
            st.session_state.auth_page = "register"
            st.rerun()

    else:

        show_register()

        st.write("---")

        if st.button("Already have an account? Login"):
            st.session_state.auth_page = "login"
            st.rerun()