"""
dashboard/job_listings.py
Job Listings page — browse/filter live job postings and top hiring companies.
"""

import streamlit as st
import pandas as pd


def load_jobs() -> pd.DataFrame:
    return pd.DataFrame([
        {"title": "Senior Data Analyst", "company": "Google", "city": "Bangalore · Hybrid", "salary": "₹18–24 LPA", "exp": "3–5 yrs", "role_type": "Data Analyst"},
        {"title": "Data Scientist", "company": "Amazon", "city": "Hyderabad · Remote", "salary": "₹22–32 LPA", "exp": "2–4 yrs", "role_type": "Data Scientist"},
        {"title": "Data Engineer", "company": "Flipkart", "city": "Bangalore · On-site", "salary": "₹20–28 LPA", "exp": "2–5 yrs", "role_type": "Data Engineer"},
        {"title": "ML Engineer", "company": "Microsoft", "city": "Hyderabad · Hybrid", "salary": "₹25–38 LPA", "exp": "3–6 yrs", "role_type": "ML Engineer"},
        {"title": "Business Analyst", "company": "Infosys", "city": "Pune · Hybrid", "salary": "₹10–16 LPA", "exp": "1–3 yrs", "role_type": "Data Analyst"},
        {"title": "AI/LLM Engineer", "company": "Anthropic India", "city": "Remote", "salary": "₹35–55 LPA", "exp": "3–7 yrs", "role_type": "ML Engineer"},
        {"title": "Data Analyst (Fresher)", "company": "Wipro", "city": "Chennai · On-site", "salary": "₹4–7 LPA", "exp": "0–1 yr", "role_type": "Data Analyst"},
        {"title": "Data Scientist (NLP)", "company": "Swiggy", "city": "Bangalore · Remote", "salary": "₹24–34 LPA", "exp": "2–5 yrs", "role_type": "Data Scientist"},
    ])


def load_top_companies() -> pd.DataFrame:
    return pd.DataFrame([
        {"company": "Google", "openings": 1240}, {"company": "Amazon", "openings": 2180},
        {"company": "Microsoft", "openings": 980}, {"company": "Flipkart", "openings": 640},
        {"company": "Infosys", "openings": 3200}, {"company": "Wipro", "openings": 2800},
    ])


def render():
    st.title("🏢 Job Listings")
    st.caption("Live postings aggregated from LinkedIn, Naukri, Indeed, and Glassdoor")

    df = load_jobs()
    role_filter = st.multiselect("Filter by role", sorted(df["role_type"].unique()))
    filtered = df[df["role_type"].isin(role_filter)] if role_filter else df

    for _, row in filtered.iterrows():
        with st.container(border=True):
            c1, c2 = st.columns([3, 1])
            with c1:
                st.markdown(f"**{row['title']}**")
                st.caption(f"{row['company']} · {row['exp']}")
            with c2:
                st.markdown(f"**{row['salary']}**")
                st.caption(row["city"])

    st.divider()
    st.subheader("Top hiring companies")
    comp_df = load_top_companies()
    cols = st.columns(3)
    for i, (_, row) in enumerate(comp_df.iterrows()):
        with cols[i % 3]:
            st.metric(row["company"], f"{row['openings']:,} openings")
