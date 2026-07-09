import streamlit as st

def show_ai_summary(career_score, match_percentage, missing_skills):
    summary = f"""
### 🤖 AI Career Summary

Your resume has a **Career Score of {career_score}/100** with a **{match_percentage}% match** for the selected role.

"""

    if len(missing_skills) == 0:
        summary += """
🎉 Excellent! Your resume already covers the required skills for this role.
"""
    else:
        summary += (
            "To improve your profile, focus on learning:\n\n"
            + ", ".join(missing_skills[:5])
            + ".\n\nAlso, add measurable achievements and keep your projects updated."
        )

    st.info(summary)