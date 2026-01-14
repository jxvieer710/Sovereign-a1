import streamlit as st
from agno.agent import Agent
from agno.models.groq import Groq

st.title("📈 Trading Sniper")
st.write("Live Market Zone & Trend Analysis")

symbol = st.text_input("Instrument (e.g., BTC, NVDA, Gold):", "BTC")
timeframe = st.selectbox("Timeframe:", ["5m", "15m", "1h", "4h", "Daily"])

if st.button("🔍 ANALYZE ZONES"):
    agent = Agent(
        model=Groq(id="llama-3.3-70b-versatile", api_key=st.secrets["GROQ_API_KEY"]),
        instructions=[
            f"Analyze {symbol} on the {timeframe} chart.",
            "Identify key Demand and Supply zones.",
            "Provide a probabilistic trend forecast based on current volume and RSI levels."
        ],
        markdown=True
    )
    with st.spinner("Calculating Zoned Analysis..."):
        st.markdown(agent.run(f"Full technical report for {symbol} on {timeframe}").content)