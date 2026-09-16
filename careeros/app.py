import streamlit as st

if __package__:
    from careeros.services.database import get_application_stats, init_db, list_saved_jobs
else:
    from services.database import get_application_stats, init_db, list_saved_jobs


def main() -> None:
    st.set_page_config(page_title="CareerOS", page_icon="🧭", layout="wide")
    init_db()

    st.title("🧭 CareerOS")
    st.caption("AI-powered career operating system for job discovery, application optimization, and progress tracking.")

    stats = get_application_stats()
    saved_jobs = list_saved_jobs(limit=500)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Saved Jobs", len(saved_jobs))
    c2.metric("Applications", stats.get("total", 0))
    c3.metric("Interviews", stats.get("interview", 0))
    c4.metric("Offers", stats.get("offer", 0))

    st.markdown("### Workflows")
    st.markdown(
        """
        - **Jobs**: Search across Adzuna, Reed, and Remotive; save and match jobs.
        - **CV Studio**: Upload CV, generate role-specific versions, export as PDF/DOCX.
        - **Cover Letters**: Generate tailored letters from CV + role description.
        - **Skill Gap**: Identify missing skills and learning paths.
        - **Market Intelligence**: Explore salary, skill, role, and location trends.
        - **Application Tracker**: Track statuses and export your pipeline.
        - **AI Coach**: Career chat, strategy, CV review, and interview advice.
        - **LinkedIn Optimizer**: Build profile headline, summary, keywords, and experience edits.
        """
    )

    st.info("Use the left sidebar pages to navigate CareerOS modules.")


if __name__ == "__main__":
    main()
