"""
models/salary_predictor.py
Trains and serves a salary prediction model (Random Forest / XGBoost /
Gradient Boosting) based on experience, location, skills, education, and company.
"""

import logging
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from xgboost import XGBRegressor

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

NUMERIC_FEATURES = ["experience_years"]
CATEGORICAL_FEATURES = ["city", "primary_skill", "education", "job_role"]
TARGET = "salary_lpa"

MODEL_REGISTRY = {
    "random_forest": RandomForestRegressor(n_estimators=200, max_depth=12, random_state=42),
    "xgboost": XGBRegressor(n_estimators=250, max_depth=6, learning_rate=0.08, random_state=42),
    "gradient_boosting": GradientBoostingRegressor(n_estimators=200, max_depth=4, random_state=42),
}


def build_preprocessor() -> ColumnTransformer:
    return ColumnTransformer(transformers=[
        ("num", StandardScaler(), NUMERIC_FEATURES),
        ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_FEATURES),
    ])


def generate_synthetic_training_data(n: int = 5000, seed: int = 42) -> pd.DataFrame:
    """
    Generates a realistic synthetic dataset for bootstrapping the model
    before real scraped/warehouse data is available. Replace with a
    `pd.read_sql("SELECT * FROM jobs ...", engine)` call once jobs/skills
    tables are populated.
    """
    rng = np.random.default_rng(seed)

    cities = ["Bangalore", "Hyderabad", "Pune", "Delhi NCR", "Mumbai", "Chennai", "Remote"]
    city_mult = {"Bangalore": 1.2, "Hyderabad": 1.1, "Pune": 1.05, "Delhi NCR": 1.1,
                 "Mumbai": 1.15, "Chennai": 1.0, "Remote": 1.1}

    roles = ["Data Analyst", "Data Scientist", "ML Engineer", "Business Analyst",
             "Data Engineer", "AI/LLM Engineer"]
    role_base = {"Data Analyst": 8, "Data Scientist": 14, "ML Engineer": 18,
                 "Business Analyst": 10, "Data Engineer": 16, "AI/LLM Engineer": 24}

    skills = ["Python + ML", "SQL + Power BI", "Python + Deep Learning",
              "Gen AI / LLMs", "Spark + Cloud", "Data Engineering"]
    skill_mult = {"Python + ML": 1.1, "SQL + Power BI": 1.0, "Python + Deep Learning": 1.2,
                  "Gen AI / LLMs": 1.4, "Spark + Cloud": 1.25, "Data Engineering": 1.15}

    educations = ["B.Tech", "M.Tech", "MCA", "MBA", "B.Sc"]

    rows = []
    for _ in range(n):
        role = rng.choice(roles)
        city = rng.choice(cities)
        skill = rng.choice(skills)
        edu = rng.choice(educations)
        exp = round(float(rng.uniform(0, 15)), 1)

        base = role_base[role] + exp * 0.8
        salary = base * city_mult[city] * skill_mult[skill]
        salary *= rng.normal(1.0, 0.08)  # noise
        salary = max(round(salary, 1), 2.5)

        rows.append({
            "experience_years": exp, "city": city, "primary_skill": skill,
            "education": edu, "job_role": role, "salary_lpa": salary,
        })

    return pd.DataFrame(rows)


def train_model(df: pd.DataFrame, model_name: str = "xgboost") -> Pipeline:
    if model_name not in MODEL_REGISTRY:
        raise ValueError(f"Unknown model '{model_name}'. Choose from {list(MODEL_REGISTRY)}")

    X = df[NUMERIC_FEATURES + CATEGORICAL_FEATURES]
    y = df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    pipeline = Pipeline(steps=[
        ("preprocessor", build_preprocessor()),
        ("regressor", MODEL_REGISTRY[model_name]),
    ])
    pipeline.fit(X_train, y_train)

    preds = pipeline.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    r2 = r2_score(y_test, preds)
    logger.info(f"[{model_name}] MAE: {mae:.2f} LPA | R²: {r2:.3f}")

    return pipeline


def save_model(pipeline: Pipeline, path: str = "models/salary_model.joblib"):
    joblib.dump(pipeline, path)
    logger.info(f"Model saved to {path}")


def load_model(path: str = "models/salary_model.joblib") -> Pipeline:
    return joblib.load(path)


def predict_salary(pipeline: Pipeline, experience_years: float, city: str,
                    primary_skill: str, education: str, job_role: str) -> dict:
    input_df = pd.DataFrame([{
        "experience_years": experience_years, "city": city,
        "primary_skill": primary_skill, "education": education, "job_role": job_role,
    }])
    predicted = float(pipeline.predict(input_df)[0])
    return {
        "predicted_salary_lpa": round(predicted, 1),
        "range_low": round(predicted * 0.82, 1),
        "range_high": round(predicted * 1.25, 1),
    }


if __name__ == "__main__":
    data = generate_synthetic_training_data(n=5000)
    model = train_model(data, model_name="xgboost")
    save_model(model)

    result = predict_salary(
        model, experience_years=3, city="Bangalore",
        primary_skill="Python + ML", education="B.Tech", job_role="Data Analyst",
    )
    print(result)
