# CareerPulse AI 📊
### Intelligent Job Market Analytics & Skill Gap Analyzer

> "Analyze the Job Market. Identify Skill Gaps. Build Smarter Careers."

An end-to-end data analytics platform that scrapes job postings, cleans and
warehouses them, mines in-demand skills with NLP, predicts salaries and hiring
trends with ML, and turns a candidate's resume into a personalized,
AI-generated career report.

---

## ✨ Features

- **Web scraping & ETL** — collect, clean, dedupe, and standardize job postings from multiple portals
- **PostgreSQL warehouse** — normalized schema for companies, jobs, skills, users, predictions
- **NLP skill extraction** — spaCy phrase matching pulls skills from job descriptions and resumes
- **Resume skill-gap analysis** — match % , missing skills, and a composite Career Score
- **Salary prediction** — XGBoost / Random Forest / Gradient Boosting regression
- **Hiring trend forecasting** — Prophet (or linear fallback) for 1/3/6-month forecasts
- **AI recommendation engine** — courses, certificates, projects, and next career step
- **PDF report generator** — polished, multi-page report (ReportLab)
- **Streamlit dashboard** — Market, Skills, Salary, Resume, Jobs, Roadmap pages
- **FastAPI backend** — REST endpoints for every core capability

## 🗂️ Project structure

```
CareerPulseAI/
├── app.py                      # Streamlit entry point
├── requirements.txt
├── dashboard/                  # Streamlit pages
│   ├── market_overview.py
│   ├── skills_dashboard.py
│   ├── salary_predictor.py
│   ├── resume_analyzer.py
│   ├── job_listings.py
│   └── career_roadmap.py
├── scraper/
│   └── job_scraper.py          # Naukri/LinkedIn/Indeed scraper templates
├── utils/
│   └── etl_pipeline.py         # Extract-Transform-Load
├── database/
│   ├── schema.sql              # PostgreSQL DDL
│   └── db_connection.py        # SQLAlchemy engine/session
├── resume_parser/
│   ├── file_parser.py          # PDF/DOCX text extraction
│   └── skill_extractor.py      # spaCy NLP skill extraction + gap analysis
├── models/
│   └── salary_predictor.py     # ML salary regression (RF/XGBoost/GBM)
├── forecasting/
│   └── hiring_trend_forecast.py # Prophet-based hiring demand forecasting
├── recommendation_engine/
│   └── career_recommender.py   # Course + career path recommendations
├── reports/
│   └── report_generator.py     # PDF career report (ReportLab)
├── api/
│   └── main.py                 # FastAPI backend
├── notebooks/                  # EDA / experimentation
└── documentation/              # SRS, ER diagrams, test plans
```

## 🚀 Setup

```bash
# 1. Clone and enter the project
cd CareerPulseAI

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# 4. Set up PostgreSQL
createdb careerpulse
psql careerpulse < database/schema.sql

# 5. Configure environment variables (create a .env file)
echo "DB_HOST=localhost
DB_PORT=5432
DB_NAME=careerpulse
DB_USER=postgres
DB_PASSWORD=postgres" > .env

# 6. Run the Streamlit dashboard
streamlit run app.py

# 7. (Optional) Run the FastAPI backend in a separate terminal
uvicorn api.main:app --reload --port 8000
```

## 🧪 Quick test of individual modules

```bash
python models/salary_predictor.py        # trains + tests the salary model
python utils/etl_pipeline.py              # runs the ETL transform on sample data
python resume_parser/skill_extractor.py   # tests NLP skill extraction
python reports/report_generator.py        # generates a sample PDF report
python forecasting/hiring_trend_forecast.py
```

## 📄 License

Educational/academic project — for placement and internship portfolio use.
