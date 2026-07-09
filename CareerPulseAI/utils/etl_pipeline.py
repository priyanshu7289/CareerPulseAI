"""
utils/etl_pipeline.py
Extract → Transform → Load pipeline for CareerPulse AI.

Reads raw scraped JSON/CSV, cleans and standardizes it, then loads it
into the PostgreSQL warehouse (companies, jobs, skills, job_skills tables).
"""

import re
import logging
from typing import List, Dict

import pandas as pd
import numpy as np

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# Canonical skill vocabulary used to normalize free-text skill tags
SKILL_ALIASES = {
    "py": "Python", "python3": "Python", "pyspark": "Spark",
    "ms excel": "Excel", "msexcel": "Excel", "excel ": "Excel",
    "power-bi": "Power BI", "powerbi": "Power BI",
    "ml": "Machine Learning", "deep-learning": "Deep Learning",
    "genai": "Generative AI", "gen ai": "Generative AI", "gen-ai": "Generative AI",
    "llm": "LLMs", "large language models": "LLMs",
    "amazon web services": "AWS", "microsoft azure": "Azure",
    "google cloud": "GCP", "google cloud platform": "GCP",
    "sql server": "SQL", "mysql": "SQL", "postgresql": "SQL",
    "natural language processing": "NLP",
}


class ETLPipeline:
    def __init__(self, raw_df: pd.DataFrame):
        self.raw_df = raw_df.copy()
        self.clean_df: pd.DataFrame = pd.DataFrame()

    # ── EXTRACT ──────────────────────────────────────────────────────────────
    @staticmethod
    def extract_from_csv(path: str) -> "ETLPipeline":
        df = pd.read_csv(path)
        logger.info(f"Extracted {len(df)} raw rows from {path}")
        return ETLPipeline(df)

    @staticmethod
    def extract_from_json(records: List[Dict]) -> "ETLPipeline":
        df = pd.DataFrame.from_records(records)
        logger.info(f"Extracted {len(df)} raw rows from JSON records")
        return ETLPipeline(df)

    # ── TRANSFORM ────────────────────────────────────────────────────────────
    def transform(self) -> pd.DataFrame:
        df = self.raw_df.copy()

        df = self._drop_duplicates(df)
        df = self._handle_missing(df)
        df = self._standardize_company_names(df)
        df = self._standardize_salary(df)
        df = self._standardize_experience(df)
        df = self._normalize_skills(df)
        df = self._standardize_city(df)

        self.clean_df = df
        logger.info(f"Transform complete. Clean rows: {len(df)}")
        return df

    def _drop_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        before = len(df)
        subset = [c for c in ["job_title", "company_name", "city", "posted_date"] if c in df.columns]
        df = df.drop_duplicates(subset=subset or None).reset_index(drop=True)
        logger.info(f"Removed {before - len(df)} duplicate rows")
        return df

    def _handle_missing(self, df: pd.DataFrame) -> pd.DataFrame:
        df["company_name"] = df.get("company_name", pd.Series(dtype=str)).fillna("Unknown")
        df["city"] = df.get("city", pd.Series(dtype=str)).fillna("Not specified")
        if "job_description" in df.columns:
            df["job_description"] = df["job_description"].fillna("")
        # Drop rows with no job title — unusable record
        if "job_title" in df.columns:
            df = df.dropna(subset=["job_title"])
        return df

    def _standardize_company_names(self, df: pd.DataFrame) -> pd.DataFrame:
        if "company_name" not in df.columns:
            return df
        df["company_name"] = (
            df["company_name"]
            .astype(str)
            .str.strip()
            .str.replace(r"\s+(Pvt\.?\s*Ltd\.?|Limited|Inc\.?|LLC)$", "", regex=True, case=False)
            .str.title()
        )
        return df

    def _standardize_salary(self, df: pd.DataFrame) -> pd.DataFrame:
        """Parse free-text salary strings like '8-12 LPA' or '₹8,00,000 - ₹12,00,000' into numeric LPA."""
        def parse_salary(val):
            if pd.isna(val):
                return (np.nan, np.nan)
            s = str(val).lower().replace(",", "").replace("₹", "")
            nums = [float(n) for n in re.findall(r"\d+\.?\d*", s)]
            if not nums:
                return (np.nan, np.nan)
            if "lakh" in s or "lpa" in s:
                pass  # already in LPA units
            elif "k" in s:
                nums = [n / 100 for n in nums]  # thousands -> lakhs approx
            elif max(nums) > 1000:
                nums = [n / 100000 for n in nums]  # raw rupees -> lakhs
            if len(nums) == 1:
                return (nums[0], nums[0])
            return (min(nums), max(nums))

        if "salary" in df.columns:
            parsed = df["salary"].apply(parse_salary)
            df["salary_min"] = parsed.apply(lambda x: x[0])
            df["salary_max"] = parsed.apply(lambda x: x[1])
        return df

    def _standardize_experience(self, df: pd.DataFrame) -> pd.DataFrame:
        def parse_exp(val):
            if pd.isna(val):
                return (np.nan, np.nan)
            nums = [float(n) for n in re.findall(r"\d+\.?\d*", str(val))]
            if not nums:
                return (np.nan, np.nan)
            if len(nums) == 1:
                return (nums[0], nums[0])
            return (min(nums), max(nums))

        if "experience" in df.columns:
            parsed = df["experience"].apply(parse_exp)
            df["experience_min"] = parsed.apply(lambda x: x[0])
            df["experience_max"] = parsed.apply(lambda x: x[1])
        return df

    def _normalize_skills(self, df: pd.DataFrame) -> pd.DataFrame:
        def normalize_list(skills):
            if not isinstance(skills, list):
                return []
            normalized = []
            for s in skills:
                key = str(s).strip().lower()
                canonical = SKILL_ALIASES.get(key, str(s).strip().title())
                normalized.append(canonical)
            return sorted(set(normalized))

        if "skills" in df.columns:
            df["skills"] = df["skills"].apply(normalize_list)
        return df

    def _standardize_city(self, df: pd.DataFrame) -> pd.DataFrame:
        city_aliases = {
            "bengaluru": "Bangalore", "blr": "Bangalore",
            "ncr": "Delhi NCR", "new delhi": "Delhi NCR", "gurugram": "Delhi NCR", "gurgaon": "Delhi NCR", "noida": "Delhi NCR",
            "bombay": "Mumbai", "madras": "Chennai",
        }
        if "city" in df.columns:
            df["city"] = df["city"].astype(str).str.strip().str.lower().map(
                lambda c: city_aliases.get(c, c.title())
            )
        return df

    # ── LOAD ─────────────────────────────────────────────────────────────────
    def load_to_postgres(self, engine, if_exists: str = "append"):
        """Loads the cleaned dataframe into the staging table 'jobs_staging'."""
        if self.clean_df.empty:
            logger.warning("No clean data to load — run transform() first.")
            return
        self.clean_df.to_sql("jobs_staging", engine, if_exists=if_exists, index=False)
        logger.info(f"Loaded {len(self.clean_df)} rows into jobs_staging table.")


if __name__ == "__main__":
    sample = pd.DataFrame([
        {"job_title": "Data Analyst", "company_name": "Infosys Ltd.", "city": "Bengaluru",
         "salary": "6-9 LPA", "experience": "1-3 years", "skills": ["SQL", "ms excel", "Power-BI"]},
        {"job_title": "Data Scientist", "company_name": "Infosys Ltd.", "city": "Bengaluru",
         "salary": "6-9 LPA", "experience": "1-3 years", "skills": ["SQL", "ms excel", "Power-BI"]},  # duplicate
        {"job_title": "ML Engineer", "company_name": "TCS Limited", "city": "noida",
         "salary": "₹15,00,000 - ₹22,00,000", "experience": "3-5", "skills": ["py", "deep-learning", "AWS"]},
    ])
    pipeline = ETLPipeline(sample)
    cleaned = pipeline.transform()
    print(cleaned)
