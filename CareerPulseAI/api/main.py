"""
api/main.py

CareerPulse AI REST API
"""

import io
import os
import sys
from typing import List

from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.salary_predictor import (
    generate_synthetic_training_data,
    train_model,
    predict_salary,
)

from resume_parser.file_parser import extract_resume_text

from resume_parser.skill_extractor import (
    SkillExtractor,
    compare_resume_to_job,
    compute_career_score,
)

from recommendation_engine.career_recommender import (
    generate_recommendations,
    suggest_career_path,
)

# -------------------------------------------------------------------
# FastAPI
# -------------------------------------------------------------------

app = FastAPI(
    title="CareerPulse AI API",
    description="CareerPulse AI Backend",
    version="1.0.0",
)

# -------------------------------------------------------------------
# Globals
# -------------------------------------------------------------------

extractor = SkillExtractor()

salary_model = None


def get_salary_model():

    global salary_model

    if salary_model is None:

        data = generate_synthetic_training_data(5000)

        salary_model = train_model(
            data,
            model_name="xgboost",
        )

    return salary_model


# -------------------------------------------------------------------
# Schemas
# -------------------------------------------------------------------

class SalaryRequest(BaseModel):
    experience_years: float
    city: str
    primary_skill: str
    education: str
    job_role: str


class SkillGapRequest(BaseModel):
    resume_text: str
    job_description: str
    years_experience: float = 0


class RecommendationRequest(BaseModel):
    missing_skills: List[str]
    current_role: str = "Data Analyst"


# -------------------------------------------------------------------
# Routes
# -------------------------------------------------------------------

@app.get("/")
def home():

    return {
        "status": "ok",
        "service": "CareerPulse AI",
    }


# -------------------------------------------------------------------

@app.post("/predict-salary")
def predict_salary_api(req: SalaryRequest):

    model = get_salary_model()

    return predict_salary(
        model,
        req.experience_years,
        req.city,
        req.primary_skill,
        req.education,
        req.job_role,
    )


# -------------------------------------------------------------------

@app.post("/skill-gap")
def skill_gap_api(req: SkillGapRequest):

    result = compare_resume_to_job(
        req.resume_text,
        req.job_description,
        extractor,
    )

    score = compute_career_score(
        result["match_percentage"],
        req.years_experience,
        len(result["resume_skills"]),
    )

    result["career_score"] = score

    return result


# -------------------------------------------------------------------

@app.post("/skill-gap/upload")
async def upload_resume(
    job_description: str,
    file: UploadFile = File(...),
):

    filename = file.filename or ""

    if not filename.lower().endswith(
        (".pdf", ".docx")
    ):
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are supported.",
        )

    contents = await file.read()

    resume_text = extract_resume_text(
        io.BytesIO(contents),
        filename,
    )

    return compare_resume_to_job(
        resume_text,
        job_description,
        extractor,
    )


# -------------------------------------------------------------------

@app.post("/recommendations")
def recommendation_api(req: RecommendationRequest):

    recommendations = generate_recommendations(
        req.missing_skills
    )

    career_path = suggest_career_path(
        req.current_role,
        req.missing_skills,
    )

    return {
        "recommendations": recommendations,
        "career_path": career_path,
    }


# -------------------------------------------------------------------

@app.get("/skills/extract")
def extract_skills(text: str):

    skills = extractor.extract(text)

    return {
        "skills": skills,
        "count": len(skills),
    }