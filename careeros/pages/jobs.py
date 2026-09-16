import re

import pandas as pd
import streamlit as st

from careeros.services import adzuna, reed, remotive
from careeros.services.database import init_db, save_job

st.title("🔎 Jobs Explorer")
init_db()

keyword = st.text_input("Keyword", placeholder="Product Manager, UX Designer, Data Analyst...")
location = st.text_input("Location", placeholder="London, New York, Remote...")
min_salary = st.number_input("Minimum salary", min_value=0, value=0, step=5000)
remote_only = st.checkbox("Remote only", value=False)
hybrid_ok = st.checkbox("Include hybrid roles", value=True)
sources = st.multiselect("Sources", ["Adzuna", "Reed", "Remotive"], default=["Remotive"])


def _match_score(cv_text: str, role_text: str) -> int:
    words = {w for w in re.findall(r"[a-zA-Z]{3,}", cv_text.lower())}
    role_words = {w for w in re.findall(r"[a-zA-Z]{3,}", role_text.lower())}
    if not role_words:
        return 0
    overlap = len(words.intersection(role_words))
    return int((overlap / max(len(role_words), 1)) * 100)


if st.button("Search jobs", type="primary"):
    results = []
    if "Remotive" in sources:
        try:
            results.extend(remotive.search_jobs(keyword=keyword, location=location))
        except Exception as exc:
            st.warning(f"Remotive search failed: {exc}")
    if "Adzuna" in sources:
        try:
            results.extend(adzuna.search_jobs(keyword=keyword, location=location, min_salary=int(min_salary) or None, remote=remote_only))
        except Exception as exc:
            st.warning(f"Adzuna search failed: {exc}")
    if "Reed" in sources:
        try:
            results.extend(reed.search_jobs(keyword=keyword, location=location, min_salary=int(min_salary) or None, remote=remote_only))
        except Exception as exc:
            st.warning(f"Reed search failed: {exc}")

    if min_salary:
        results = [r for r in results if (r.get("salary") or 0) >= min_salary]

    if not hybrid_ok:
        results = [r for r in results if "hybrid" not in (r.get("title", "") + " " + r.get("description", "")).lower()]

    st.session_state["job_results"] = results

results = st.session_state.get("job_results", [])
if results:
    st.success(f"Found {len(results)} jobs")
    df = pd.DataFrame(results)
    st.dataframe(df[["title", "company", "location", "salary", "source", "url"]], use_container_width=True, hide_index=True)

    cv_text = st.session_state.get("cv_text", "")
    for i, job in enumerate(results[:25]):
        with st.expander(f"{job.get('title', 'Untitled')} — {job.get('company', 'Unknown')}"):
            st.write(job.get("location", "Unknown"))
            st.write(job.get("url", ""))
            st.write((job.get("description", "") or "")[:800] + "...")

            col1, col2 = st.columns(2)
            if col1.button("Save job", key=f"save_{i}"):
                save_job(job)
                st.success("Saved job.")
            if col2.button("Match job", key=f"match_{i}"):
                role_text = f"{job.get('title', '')} {job.get('description', '')}"
                score = _match_score(cv_text, role_text) if cv_text else 0
                st.info(f"Match score: {score}%")
else:
    st.info("Run a search to load jobs.")
