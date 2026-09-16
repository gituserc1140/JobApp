import re

import pandas as pd
import plotly.express as px
import streamlit as st

from careeros.services.database import init_db, list_saved_jobs

st.title("📈 Market Intelligence")

init_db()
jobs = list_saved_jobs(limit=1000)
if not jobs:
    st.info("Save jobs first to unlock market insights.")
    st.stop()

df = pd.DataFrame(jobs)

st.markdown("### Salary Trends")
if "salary" in df and df["salary"].notna().any():
    sal = df.dropna(subset=["salary"])
    st.plotly_chart(px.histogram(sal, x="salary", nbins=20, title="Salary distribution"), use_container_width=True)
else:
    st.info("Salary data not available yet.")

st.markdown("### Employer Demand")
employer = df.groupby("company", as_index=False).size().sort_values("size", ascending=False).head(15)
st.plotly_chart(px.bar(employer, x="company", y="size", title="Top hiring employers"), use_container_width=True)

st.markdown("### Role Demand")
roles = df.groupby("title", as_index=False).size().sort_values("size", ascending=False).head(15)
st.plotly_chart(px.bar(roles, x="title", y="size", title="Most frequent roles"), use_container_width=True)

st.markdown("### Location Analysis")
loc = df.groupby("location", as_index=False).size().sort_values("size", ascending=False).head(15)
st.plotly_chart(px.bar(loc, x="location", y="size", title="Top locations"), use_container_width=True)

st.markdown("### Skill Trends")
all_text = " ".join((df["title"].fillna("") + " " + df["description"].fillna(" ")).tolist()).lower()
keywords = re.findall(r"[a-zA-Z\+\#]{3,}", all_text)
skill_df = (
    pd.Series(keywords)
    .value_counts()
    .head(20)
    .reset_index()
    .rename(columns={"index": "skill", "count": "mentions"})
)
st.plotly_chart(px.bar(skill_df, x="skill", y="mentions", title="Top skill keywords"), use_container_width=True)
