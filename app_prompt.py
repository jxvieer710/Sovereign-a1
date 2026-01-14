import streamlit as st
from agno.agent import Agent
from agno.models.groq import Groq

st.title("🪄 Prompt Master")
if "GROQ_API_KEY" in st.secrets:
    agent = Agent(model=Groq(id="llama-3.3-70b-versatile", api_key=st.secrets["GROQ_API_KEY"]))
    prompt = st.text_area("Paste your rough prompt here:")
    if st.button("💎 OPTIMIZE"):
        st.markdown(agent.run(f"Rewrite this into a world-class AI prompt: {prompt}").content)