import re

import pandas as pd
import streamlit as st

from careeros.services.openrouter import generate_text

st.title("🧩 Skill Gap Analyzer")

cv_text = st.text_area("CV text", value=st.session_state.get("cv_text", ""), height=200)
role_desc = st.text_area("Target role description", height=240)


def _tokens(text: str) -> set[str]:
    return {w for w in re.findall(r"[a-zA-Z]{3,}", text.lower())}


if st.button("Analyze skill gap", type="primary"):
    if not cv_text.strip() or not role_desc.strip():
        st.warning("Provide both CV text and role description.")
    else:
        cv_words = _tokens(cv_text)
        role_words = _tokens(role_desc)
        missing = sorted(list(role_words - cv_words))[:30]

        st.markdown("### Missing Skills (keyword-level)")
        st.dataframe(pd.DataFrame({"skill": missing}), use_container_width=True, hide_index=True)

        prompt = (
            "Given this CV and target role, identify critical missing skills and create a 6-week learning path. "
            "Keep it concise and actionable.\n\n"
            f"CV:\n{cv_text[:7000]}\n\nRole:\n{role_desc[:7000]}"
        )
        path = generate_text(prompt) or "Week 1-2: Fill core domain gaps\nWeek 3-4: Build project evidence\nWeek 5-6: Interview prep"
        st.markdown("### Learning Path")
        st.write(path)
