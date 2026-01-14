import streamlit as st
from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.duckduckgo import DuckDuckGoTools

st.title("🎯 Vegas Sniper")
if "GROQ_API_KEY" in st.secrets:
    agent = Agent(
        model=Groq(id="llama-3.3-70b-versatile", api_key=st.secrets["GROQ_API_KEY"]),
        tools=[DuckDuckGoTools()],
        instructions=[
            "Today is January 14, 2026. Search for current NFL/NBA schedules and injury reports.",
            "MANDATORY: When using search, provide ONLY the raw search query. Do NOT use XML tags like <function>."
        ],
        markdown=True
    )
    query = st.text_input("Analyze Player/Team:")
    if st.button("🚀 EXECUTE SCAN"):
        with st.spinner("Searching 2026 Web Data..."):
            st.markdown(agent.run(query).content)