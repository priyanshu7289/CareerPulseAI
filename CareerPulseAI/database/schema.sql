-- database/schema.sql
-- CareerPulse AI — PostgreSQL Data Warehouse Schema

DROP TABLE IF EXISTS reports CASCADE;
DROP TABLE IF EXISTS recommendation CASCADE;
DROP TABLE IF EXISTS learning_courses CASCADE;
DROP TABLE IF EXISTS salary_prediction CASCADE;
DROP TABLE IF EXISTS resume_skills CASCADE;
DROP TABLE IF EXISTS job_skills CASCADE;
DROP TABLE IF EXISTS skills CASCADE;
DROP TABLE IF EXISTS jobs CASCADE;
DROP TABLE IF EXISTS companies CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- ── Companies ────────────────────────────────────────────────────────────────
CREATE TABLE companies (
    company_id      SERIAL PRIMARY KEY,
    company_name    VARCHAR(255) NOT NULL UNIQUE,
    industry        VARCHAR(120),
    headquarters    VARCHAR(120),
    company_size    VARCHAR(50),
    website         VARCHAR(255),
    created_at      TIMESTAMP DEFAULT NOW()
);

-- ── Jobs ─────────────────────────────────────────────────────────────────────
CREATE TABLE jobs (
    job_id          SERIAL PRIMARY KEY,
    job_title       VARCHAR(255) NOT NULL,
    company_id      INTEGER REFERENCES companies(company_id),
    city            VARCHAR(120),
    state           VARCHAR(120),
    country         VARCHAR(120) DEFAULT 'India',
    salary_min       NUMERIC(12, 2),
    salary_max       NUMERIC(12, 2),
    salary_currency  VARCHAR(10) DEFAULT 'INR',
    experience_min  NUMERIC(4, 1),
    experience_max  NUMERIC(4, 1),
    education       VARCHAR(120),
    employment_type VARCHAR(50),          -- Full-time, Contract, Internship
    is_remote       BOOLEAN DEFAULT FALSE,
    source_portal   VARCHAR(50),          -- LinkedIn, Naukri, Indeed, Glassdoor
    job_description TEXT,
    posted_date     DATE,
    scraped_at      TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_jobs_city ON jobs(city);
CREATE INDEX idx_jobs_posted_date ON jobs(posted_date);
CREATE INDEX idx_jobs_company ON jobs(company_id);

-- ── Skills ───────────────────────────────────────────────────────────────────
CREATE TABLE skills (
    skill_id        SERIAL PRIMARY KEY,
    skill_name      VARCHAR(120) NOT NULL UNIQUE,
    category        VARCHAR(80)            -- Programming, BI Tool, Cloud, ML, Soft Skill
);

-- ── Job ↔ Skill mapping ────────────────────────────────────────────────────────
CREATE TABLE job_skills (
    job_skill_id    SERIAL PRIMARY KEY,
    job_id          INTEGER REFERENCES jobs(job_id) ON DELETE CASCADE,
    skill_id        INTEGER REFERENCES skills(skill_id) ON DELETE CASCADE,
    UNIQUE(job_id, skill_id)
);

CREATE INDEX idx_job_skills_skill ON job_skills(skill_id);

-- ── Users ────────────────────────────────────────────────────────────────────
CREATE TABLE users (
    user_id         SERIAL PRIMARY KEY,
    full_name       VARCHAR(150),
    email           VARCHAR(150) UNIQUE NOT NULL,
    password_hash   VARCHAR(255) NOT NULL,
    target_role     VARCHAR(120),
    created_at      TIMESTAMP DEFAULT NOW()
);

-- ── Resume ↔ Skill mapping (extracted via NLP) ─────────────────────────────────
CREATE TABLE resume_skills (
    resume_skill_id SERIAL PRIMARY KEY,
    user_id         INTEGER REFERENCES users(user_id) ON DELETE CASCADE,
    skill_id        INTEGER REFERENCES skills(skill_id) ON DELETE CASCADE,
    confidence_score NUMERIC(4, 3),        -- NLP extraction confidence 0–1
    extracted_at    TIMESTAMP DEFAULT NOW()
);

-- ── Salary predictions ──────────────────────────────────────────────────────
CREATE TABLE salary_prediction (
    prediction_id   SERIAL PRIMARY KEY,
    user_id         INTEGER REFERENCES users(user_id) ON DELETE CASCADE,
    predicted_role  VARCHAR(120),
    experience_years NUMERIC(4, 1),
    city            VARCHAR(120),
    predicted_salary NUMERIC(12, 2),
    salary_range_low  NUMERIC(12, 2),
    salary_range_high NUMERIC(12, 2),
    model_used      VARCHAR(50),           -- RandomForest, XGBoost, GradientBoosting
    predicted_at    TIMESTAMP DEFAULT NOW()
);

-- ── Learning courses (recommendation catalogue) ────────────────────────────────
CREATE TABLE learning_courses (
    course_id       SERIAL PRIMARY KEY,
    course_name     VARCHAR(255) NOT NULL,
    skill_id        INTEGER REFERENCES skills(skill_id),
    platform        VARCHAR(120),          -- Coursera, Udemy, YouTube, etc.
    is_free         BOOLEAN DEFAULT FALSE,
    duration_weeks  INTEGER,
    course_url      VARCHAR(500)
);

-- ── AI recommendations per user ────────────────────────────────────────────────
CREATE TABLE recommendation (
    recommendation_id SERIAL PRIMARY KEY,
    user_id         INTEGER REFERENCES users(user_id) ON DELETE CASCADE,
    missing_skill_id INTEGER REFERENCES skills(skill_id),
    recommended_course_id INTEGER REFERENCES learning_courses(course_id),
    priority        VARCHAR(20),           -- High, Medium, Low
    created_at      TIMESTAMP DEFAULT NOW()
);

-- ── Generated PDF reports log ──────────────────────────────────────────────────
CREATE TABLE reports (
    report_id       SERIAL PRIMARY KEY,
    user_id         INTEGER REFERENCES users(user_id) ON DELETE CASCADE,
    report_path     VARCHAR(500),
    career_score    NUMERIC(5, 2),
    resume_match_pct NUMERIC(5, 2),
    generated_at    TIMESTAMP DEFAULT NOW()
);

-- ── Seed: common skill categories ──────────────────────────────────────────────
INSERT INTO skills (skill_name, category) VALUES
 ('Python', 'Programming'), ('SQL', 'Programming'), ('Excel', 'BI Tool'),
 ('Power BI', 'BI Tool'), ('Tableau', 'BI Tool'), ('Spark', 'Big Data'),
 ('AWS', 'Cloud'), ('Azure', 'Cloud'), ('GCP', 'Cloud'),
 ('Machine Learning', 'ML'), ('Deep Learning', 'ML'), ('Generative AI', 'ML'),
 ('LLMs', 'ML'), ('NLP', 'ML'), ('Airflow', 'Big Data'),
 ('Pandas', 'Programming'), ('NumPy', 'Programming'), ('Docker', 'DevOps'),
 ('Kubernetes', 'DevOps'), ('Git', 'DevOps')
ON CONFLICT (skill_name) DO NOTHING;
