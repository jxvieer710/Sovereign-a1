import streamlit as st
from agno.agent import Agent
from agno.models.groq import Groq

st.title("📈 Trading Sniper")
if "GROQ_API_KEY" in st.secrets:
    agent = Agent(model=Groq(id="llama-3.3-70b-versatile", api_key=st.secrets["GROQ_API_KEY"]))
    symbol = st.text_input("Enter Ticker (BTC, NVDA):")
    if st.button("🔍 SCAN MARKET"):
        st.markdown(agent.run(f"Analyze {symbol} for Jan 2026 trends.").content)