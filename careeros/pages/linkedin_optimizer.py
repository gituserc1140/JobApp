import streamlit as st

from careeros.services.openrouter import generate_text

st.title("💼 LinkedIn Optimizer")

source_text = st.text_area("Paste CV text or profile draft", value=st.session_state.get("cv_text", ""), height=260)
focus_role = st.text_input("Target role", value="Product Manager")

if st.button("Generate LinkedIn assets", type="primary"):
    if not source_text.strip():
        st.warning("Please add source text.")
    else:
        headline = generate_text(f"Generate a sharp LinkedIn headline for a {focus_role} profile based on:\n{source_text[:6000]}") or f"{focus_role} | Strategy | Delivery | Growth"
        about = generate_text(f"Write a LinkedIn About section for a {focus_role} candidate:\n{source_text[:6000]}") or "I build measurable business outcomes through customer-focused execution."
        keywords = generate_text(f"List 30 ATS and LinkedIn keywords for {focus_role} from:\n{source_text[:6000]}") or "product strategy, roadmap, stakeholder management, experimentation"
        experience = generate_text(f"Rewrite experience bullets for {focus_role} impact using STAR:\n{source_text[:6000]}") or "- Led cross-functional projects and improved KPI outcomes."

        st.session_state["linkedin_assets"] = {
            "headline": headline,
            "about": about,
            "keywords": keywords,
            "experience": experience,
        }

assets = st.session_state.get("linkedin_assets")
if assets:
    st.text_input("Headline", assets["headline"])
    st.text_area("About", assets["about"], height=170)
    st.text_area("Keywords", assets["keywords"], height=120)
    st.text_area("Optimized Experience", assets["experience"], height=220)
