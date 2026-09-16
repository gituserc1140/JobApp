import pandas as pd
import plotly.express as px
import streamlit as st

from careeros.services.database import get_application_stats, init_db, list_applications, list_saved_jobs

init_db()

st.title("📊 Dashboard")

stats = get_application_stats()
saved_jobs = list_saved_jobs(limit=500)
apps = list_applications(limit=500)

a, b, c, d = st.columns(4)
a.metric("Saved Jobs", len(saved_jobs))
b.metric("Applications", stats.get("total", 0))
c.metric("Interview Stage", stats.get("interview", 0))
d.metric("Offers", stats.get("offer", 0))

if apps:
    df = pd.DataFrame(apps)
    status_chart = (
        df.groupby("status", as_index=False)
        .size()
        .rename(columns={"size": "count"})
        .sort_values("count", ascending=False)
    )
    st.plotly_chart(
        px.bar(status_chart, x="status", y="count", title="Applications by Status"),
        use_container_width=True,
    )
else:
    st.info("No applications yet. Add entries in Application Tracker.")

if saved_jobs:
    jobs_df = pd.DataFrame(saved_jobs)
    st.markdown("### Career Overview")
    st.dataframe(
        jobs_df[["title", "company", "location", "salary", "source"]],
        use_container_width=True,
        hide_index=True,
    )
else:
    st.info("No saved jobs yet. Search and save jobs in Jobs page.")
