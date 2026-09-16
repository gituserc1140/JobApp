# CareerOS

CareerOS is a modular Streamlit career operating system for job discovery, CV optimization, application tracking, and AI-assisted career planning.

## Features

- Dashboard with KPI cards and analytics
- Multi-source job search (Adzuna, Reed, Remotive) with filtering and save/match actions
- CV Studio: upload/parse CV, generate role-tailored versions, export PDF and DOCX
- Cover letter generation from CV + job description
- Skill gap analysis and learning path suggestions
- Market intelligence from saved jobs (salary, role, location, employer, skill trends)
- Application tracker with status updates and CSV export
- AI coach for career chat, CV review, strategy, and interview advice
- LinkedIn profile optimization

## Project structure

```text
app.py
pages/
  1_📊_Dashboard.py
  2_🔎_Jobs.py
  ...
careeros/
  app.py
  pages/
    dashboard.py
    jobs.py
    cv_studio.py
    cover_letters.py
    skill_gap.py
    market_intelligence.py
    application_tracker.py
    ai_coach.py
    linkedin_optimizer.py
  services/
    adzuna.py
    reed.py
    remotive.py
    openrouter.py
    database.py
  data/
  assets/
  requirements.txt
```

## Setup

1. Install dependencies (root or module requirements both work):

```bash
pip install -r requirements.txt
# or
pip install -r careeros/requirements.txt
```

2. Configure environment variables:

- `OPENROUTER_API_KEY`
- `ADZUNA_APP_ID`
- `ADZUNA_APP_KEY`
- `REED_API_KEY`
- optional: `OPENROUTER_MODEL`

3. Run locally:

```bash
streamlit run app.py
```

## Database

SQLite database is auto-created at `careeros/data/careeros.db`.

Tables:
- `jobs(id, title, company, location, salary, url, source, description, date_saved)`
- `applications(id, company, job_title, status, notes, date_created)`

## Streamlit Cloud deployment

- Main file path: `app.py`
- Add environment variables in Streamlit Cloud Secrets.
