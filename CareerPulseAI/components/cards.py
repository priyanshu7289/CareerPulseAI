import streamlit as st

def metric_card(title, value, color="blue"):
    st.container(border=True)
    st.markdown(f"### {title}")
    st.metric("", value)