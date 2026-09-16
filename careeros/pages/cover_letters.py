import streamlit as st
from docx import Document
from pypdf import PdfReader
from io import BytesIO

from careeros.services.openrouter import generate_text

st.title("✉️ Cover Letter Generator")

if "cv_text" not in st.session_state:
    st.session_state["cv_text"] = ""

def _extract_text(uploaded_file) -> str:
    name = uploaded_file.name.lower()
    if name.endswith(".txt"):
        return uploaded_file.getvalue().decode("utf-8", errors="ignore")
    if name.endswith(".pdf"):
        pdf = PdfReader(BytesIO(uploaded_file.getvalue()))
        return "\n".join(page.extract_text() or "" for page in pdf.pages)
    if name.endswith(".docx"):
        doc = Document(BytesIO(uploaded_file.getvalue()))
        return "\n".join(p.text for p in doc.paragraphs)
    return uploaded_file.getvalue().decode("utf-8", errors="ignore")


cv_upload = st.file_uploader("Upload CV (optional)", type=["txt", "pdf", "docx"], key="cover_cv")
if cv_upload:
    st.session_state["cv_text"] = _extract_text(cv_upload)

job_desc = st.text_area("Paste job description", height=250)

if st.button("Generate cover letter", type="primary"):
    if not job_desc.strip():
        st.warning("Please paste a job description.")
    else:
        prompt = (
            "Create a one-page tailored cover letter from this CV and job description. "
            "Use a professional tone and measurable impact.\n\n"
            f"CV:\n{st.session_state.get('cv_text','')[:8000]}\n\nJob Description:\n{job_desc[:8000]}"
        )
        output = generate_text(prompt) or "Dear Hiring Manager,\n\nI am excited to apply for this role..."
        st.session_state["cover_letter"] = output

if st.session_state.get("cover_letter"):
    text = st.session_state["cover_letter"]
    st.text_area("Cover Letter", text, height=320)
    st.download_button("Download TXT", text, file_name="cover_letter.txt")
