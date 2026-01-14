import streamlit as st
from agno.agent import Agent
from agno.models.groq import Groq

st.title("💼 Business Agent")
if "GROQ_API_KEY" in st.secrets:
    agent = Agent(model=Groq(id="llama-3.3-70b-versatile", api_key=st.secrets["GROQ_API_KEY"]))
    task = st.text_area("What business task can I help with?")
    if st.button("🏗️ GENERATE PLAN"):
        st.markdown(agent.run(task).content)