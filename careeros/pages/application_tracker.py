import pandas as pd
import streamlit as st

from careeros.services.database import STATUSES, add_application, list_applications, update_status

st.title("📌 Application Tracker")

with st.form("add_application"):
    company = st.text_input("Company")
    job_title = st.text_input("Job Title")
    status = st.selectbox("Status", STATUSES, index=0)
    notes = st.text_area("Notes")
    submitted = st.form_submit_button("Add application")

if submitted:
    if company and job_title:
        add_application(company, job_title, status, notes)
        st.success("Application added.")
    else:
        st.warning("Company and Job Title are required.")

apps = list_applications(limit=1000)
if apps:
    df = pd.DataFrame(apps)
    st.dataframe(df, use_container_width=True, hide_index=True)

    app_ids = df["id"].tolist()
    selected_id = st.selectbox("Select application ID to update", app_ids)
    new_status = st.selectbox("New status", STATUSES, index=0)
    if st.button("Update status"):
        update_status(int(selected_id), new_status)
        st.success("Status updated.")

    st.download_button("Export CSV", df.to_csv(index=False), file_name="applications.csv", mime="text/csv")
else:
    st.info("No applications tracked yet.")
