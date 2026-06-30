"""
resume_parser/skill_extractor.py
NLP-based skill extraction from job descriptions and resumes using spaCy
phrase matching + a curated skill taxonomy.
"""

import logging
from typing import List, Set, Optional

import spacy
from spacy.matcher import PhraseMatcher

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# Curated taxonomy — extend this as the market evolves
SKILL_TAXONOMY = [
    "Python", "SQL", "Excel", "Power BI", "Tableau", "Spark", "PySpark",
    "AWS", "Azure", "GCP", "Machine Learning", "Deep Learning",
    "Generative AI", "LLMs", "NLP", "Airflow", "Pandas", "NumPy",
    "Docker", "Kubernetes", "Git", "TensorFlow", "PyTorch", "Scikit-learn",
    "XGBoost", "R", "Java", "Scala", "MongoDB", "PostgreSQL", "MySQL",
    "Hadoop", "Kafka", "Looker", "Snowflake", "BigQuery", "Redshift",
    "REST API", "FastAPI", "Flask", "Django", "Statistics", "A/B Testing",
    "Data Visualization", "ETL", "Data Warehousing", "Business Intelligence",
]


class SkillExtractor:
    def __init__(self, model: str = "en_core_web_sm"):
        try:
            self.nlp = spacy.load(model)
        except OSError:
            logger.warning(f"spaCy model '{model}' not found — run: python -m spacy download {model}")
            self.nlp = spacy.blank("en")

        self.matcher = PhraseMatcher(self.nlp.vocab, attr="LOWER")
        patterns = [self.nlp.make_doc(skill) for skill in SKILL_TAXONOMY]
        self.matcher.add("SKILLS", patterns)

    def extract(self, text: str) -> List[str]:
        """Return a deduplicated, sorted list of skills found in the given text."""
        if not text or not text.strip():
            return []

        doc = self.nlp(text)
        matches = self.matcher(doc)
        found: Set[str] = set()

        for match_id, start, end in matches:
            span_text = doc[start:end].text
            # Map back to canonical casing from the taxonomy
            canonical = next(
                (s for s in SKILL_TAXONOMY if s.lower() == span_text.lower()), span_text
            )
            found.add(canonical)

        return sorted(found)

    def extract_with_confidence(self, text: str) -> dict:
        """
        Returns {skill: confidence} — confidence approximated by frequency
        of mention normalized against document length (simple heuristic;
        swap for a transformer-based NER + scoring model for production).
        """
        skills = self.extract(text)
        if not skills:
            return {}

        text_lower = text.lower()
        word_count = max(len(text.split()), 1)
        scores = {}
        for skill in skills:
            freq = text_lower.count(skill.lower())
            scores[skill] = round(min(1.0, 0.5 + (freq / word_count) * 20), 3)
        return scores

def compare_resume_to_job(
    resume_text: str,
    job_description: str,
    extractor: Optional[SkillExtractor] = None
) -> dict:
    """
    Core skill-gap analysis: compares resume skills against a job description's
    required skills and returns match percentage + missing skills.
    """
    extractor = extractor or SkillExtractor()

    resume_skills = set(extractor.extract(resume_text))
    job_skills = set(extractor.extract(job_description))

    if not job_skills:
        return {
            "resume_skills": sorted(resume_skills),
            "required_skills": [],
            "matched_skills": [],
            "missing_skills": [],
            "match_percentage": 0.0,
        }

    matched = resume_skills & job_skills
    missing = job_skills - resume_skills
    match_pct = round((len(matched) / len(job_skills)) * 100, 1)

    return {
        "resume_skills": sorted(resume_skills),
        "required_skills": sorted(job_skills),
        "matched_skills": sorted(matched),
        "missing_skills": sorted(missing),
        "match_percentage": match_pct,
    }


def compute_career_score(match_pct: float, years_experience: float, num_skills: int) -> float:
    """
    Weighted composite score (0-100) used across the dashboard and PDF report.
    40% resume match, 30% experience (capped at 10 yrs), 30% skill breadth (capped at 15 skills).
    """
    exp_score = min(years_experience / 10, 1.0) * 100
    breadth_score = min(num_skills / 15, 1.0) * 100
    score = (0.4 * match_pct) + (0.3 * exp_score) + (0.3 * breadth_score)
    return round(score, 1)


if __name__ == "__main__":
    resume = "Experienced analyst skilled in Python, SQL, Excel, Power BI, and basic Machine Learning."
    jd = "We need a Data Analyst with Python, SQL, Power BI, Spark, and Airflow experience."

    extractor = SkillExtractor()
    result = compare_resume_to_job(resume, jd, extractor)
    print(result)

    score = compute_career_score(result["match_percentage"], years_experience=3, num_skills=len(result["resume_skills"]))
    print(f"Career Score: {score}")
