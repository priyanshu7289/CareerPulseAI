"""
recommendation_engine/career_recommender.py
Generates course, certificate, and career-path recommendations based on
a user's missing skills (from the resume skill-gap analysis).
"""

import logging
from typing import List, Dict

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# Course catalogue — in production this comes from the learning_courses table
COURSE_CATALOGUE: Dict[str, List[Dict]] = {
    "Spark": [
        {"name": "Apache Spark with PySpark", "platform": "Udemy", "is_free": False, "weeks": 6, "priority": "High"},
        {"name": "Big Data with Spark (freeCodeCamp)", "platform": "YouTube", "is_free": True, "weeks": 4, "priority": "High"},
    ],
    "Azure": [
        {"name": "Microsoft Azure Fundamentals (AZ-900)", "platform": "Microsoft Learn", "is_free": True, "weeks": 3, "priority": "High"},
        {"name": "Azure Data Engineer Associate (DP-203)", "platform": "Coursera", "is_free": False, "weeks": 8, "priority": "Medium"},
    ],
    "Airflow": [
        {"name": "Apache Airflow: The Hands-On Guide", "platform": "Udemy", "is_free": False, "weeks": 3, "priority": "Medium"},
    ],
    "AWS": [
        {"name": "AWS Cloud Practitioner Essentials", "platform": "AWS Skill Builder", "is_free": True, "weeks": 2, "priority": "High"},
        {"name": "AWS Certified Data Analytics", "platform": "Coursera", "is_free": False, "weeks": 8, "priority": "Medium"},
    ],
    "Machine Learning": [
        {"name": "Machine Learning Specialization", "platform": "Coursera (Andrew Ng)", "is_free": False, "weeks": 12, "priority": "High"},
    ],
    "Deep Learning": [
        {"name": "Deep Learning Specialization", "platform": "Coursera", "is_free": False, "weeks": 16, "priority": "Medium"},
    ],
    "Generative AI": [
        {"name": "Generative AI with LLMs", "platform": "Coursera / DeepLearning.AI", "is_free": False, "weeks": 4, "priority": "High"},
    ],
    "Tableau": [
        {"name": "Tableau 2024 A-Z", "platform": "Udemy", "is_free": False, "weeks": 4, "priority": "Medium"},
    ],
    "Power BI": [
        {"name": "Microsoft Power BI Desktop for Business", "platform": "Udemy", "is_free": False, "weeks": 4, "priority": "Medium"},
        {"name": "Power BI free learning path", "platform": "Microsoft Learn", "is_free": True, "weeks": 3, "priority": "Medium"},
    ],
    "NLP": [
        {"name": "NLP Specialization", "platform": "Coursera", "is_free": False, "weeks": 16, "priority": "Medium"},
    ],
    "Docker": [
        {"name": "Docker for Data Scientists", "platform": "YouTube", "is_free": True, "weeks": 2, "priority": "Low"},
    ],
}

DEFAULT_COURSE = {"name": "Search relevant courses on Coursera/Udemy", "platform": "Various", "is_free": True, "weeks": 4, "priority": "Medium"}


def recommend_courses_for_skill(skill: str) -> List[Dict]:
    return COURSE_CATALOGUE.get(skill, [DEFAULT_COURSE])


def generate_recommendations(missing_skills: List[str], top_n_per_skill: int = 1) -> List[Dict]:
    """
    Given a list of missing skills (typically from skill_extractor.compare_resume_to_job),
    returns a prioritized list of {skill, course, platform, is_free, weeks, priority}.
    """
    recommendations = []
    for skill in missing_skills:
        courses = recommend_courses_for_skill(skill)[:top_n_per_skill]
        for course in courses:
            recommendations.append({"skill": skill, **course})

    # Sort: High priority first, then shortest duration
    priority_order = {"High": 0, "Medium": 1, "Low": 2}
    recommendations.sort(key=lambda r: (priority_order.get(r["priority"], 1), r["weeks"]))
    return recommendations


def suggest_career_path(current_role: str, missing_skills: List[str]) -> Dict:
    """
    Maps a user's current role + skill gaps to a suggested next-step career path.
    """
    path_map = {
        "Data Analyst": "Senior Data Analyst → Analytics Manager, or pivot to Data Scientist",
        "Business Analyst": "Senior Business Analyst → Product Analyst, or pivot to Data Analyst",
        "Data Scientist": "Senior Data Scientist → ML Engineer / Applied Scientist",
        "Data Engineer": "Senior Data Engineer → Data Platform Architect",
        "ML Engineer": "Senior ML Engineer → AI/LLM Engineer / MLOps Lead",
    }

    suggested_projects = []
    if "Spark" in missing_skills or "Airflow" in missing_skills:
        suggested_projects.append("Build an end-to-end ETL pipeline using Airflow + Spark")
    if "Generative AI" in missing_skills or "LLMs" in missing_skills:
        suggested_projects.append("Build a RAG-based chatbot using an open-source LLM")
    if "Power BI" in missing_skills or "Tableau" in missing_skills:
        suggested_projects.append("Create a 3-page interactive BI dashboard from a public dataset")
    if not suggested_projects:
        suggested_projects.append("Contribute to an open-source data project on GitHub")

    return {
        "next_career_step": path_map.get(current_role, "Explore adjacent data roles based on your strongest skills"),
        "suggested_projects": suggested_projects,
        "estimated_upskilling_weeks": sum(c["weeks"] for c in generate_recommendations(missing_skills)),
    }


if __name__ == "__main__":
    missing = ["Spark", "Azure", "Airflow"]
    recs = generate_recommendations(missing)
    for r in recs:
        print(r)

    path = suggest_career_path("Data Analyst", missing)
    print(path)
