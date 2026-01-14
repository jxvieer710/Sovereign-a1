import streamlit as st
from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.duckduckgo import DuckDuckGoTools

st.title("🎯 Vegas Sniper")
st.write("Real-time 2026 Sports Intelligence")

if "GROQ_API_KEY" in st.secrets:
    agent = Agent(
        model=Groq(id="llama-3.3-70b-versatile", api_key=st.secrets["GROQ_API_KEY"]),
        tools=[DuckDuckGoTools()],
        instructions=[
            "Today's date is January 14, 2026.",
            "Search for current NFL/NBA schedules for Jan 2026.",
            "Provide [OVER/UNDER] signals based on 2026 injury reports."
        ],
        markdown=True
    )
    query = st.text_input("Enter Player or Team (e.g. 'Lions vs Rams 2026'):")
    if st.button("🚀 EXECUTE SCAN"):
        with st.spinner("Searching 2026 Web Data..."):
            st.markdown(agent.run(query).content)
else: st.error("Add GROQ_API_KEY to Secrets")