import streamlit as st

from careeros.services.openrouter import generate_text

st.title("🤖 AI Career Coach")

if "coach_messages" not in st.session_state:
    st.session_state["coach_messages"] = []

for msg in st.session_state["coach_messages"]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("Ask for career strategy, CV review, or interview advice")
if user_input:
    st.session_state["coach_messages"].append({"role": "user", "content": user_input})
    answer = generate_text(user_input, system_prompt="You are a practical career coach.") or "I can help with role targeting, CV improvements, and interview prep."
    st.session_state["coach_messages"].append({"role": "assistant", "content": answer})
    st.rerun()

st.markdown("### Quick prompts")
col1, col2, col3 = st.columns(3)
if col1.button("CV Review"):
    prompt = "Review my CV and suggest top 5 improvements:\n" + st.session_state.get("cv_text", "")[:8000]
    st.write(generate_text(prompt) or "Upload CV in CV Studio to get a detailed review.")
if col2.button("Career Strategy"):
    st.write(generate_text("Create a 90-day career strategy plan.") or "Set target roles, build proof projects, and optimize outreach weekly.")
if col3.button("Interview Advice"):
    st.write(generate_text("Give me interview prep advice for product and consulting roles.") or "Use STAR answers, quantify impact, and practice role-specific cases.")
