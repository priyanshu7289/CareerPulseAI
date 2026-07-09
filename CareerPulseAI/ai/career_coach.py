"""
AI Career Coach
Provides personalized career advice based on resume analysis.
"""

from typing import List


def generate_career_advice(
    target_role: str,
    career_score: int,
    missing_skills: List[str],
):
    advice = []

    if career_score >= 85:
        advice.append(
            "🎉 Excellent profile! Your resume is already competitive for this role."
        )

    elif career_score >= 70:
        advice.append(
            "👍 Good profile, but a few improvements can significantly increase your chances."
        )

    else:
        advice.append(
            "📚 Your profile needs improvement before applying confidently."
        )

    if missing_skills:
        advice.append(
            "📌 Focus on these skills first:\n\n• "
            + "\n• ".join(missing_skills[:5])
        )

    role_projects = {
        "Data Analyst": [
            "Sales Dashboard in Power BI",
            "Customer Churn Prediction",
            "SQL Business Analysis Project",
        ],
        "Data Scientist": [
            "House Price Prediction",
            "Image Classification",
            "LLM Chatbot",
        ],
        "Data Engineer": [
            "ETL Pipeline using Airflow",
            "Data Warehouse Project",
            "Kafka Streaming Pipeline",
        ],
        "ML Engineer": [
            "MLOps Pipeline",
            "Model Deployment with FastAPI",
            "Recommendation System",
        ],
    }

    projects = role_projects.get(target_role, [])

    return {
        "advice": advice,
        "projects": projects,
    }