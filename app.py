import streamlit as st
from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.yfinance import YFinanceTools

st.set_page_config(page_title="Sovereign AI Master", layout="wide")

# 1. INTERNAL TRUTH ENGINE (Hard-coded 2026 NFL Reality)
VERIFIED_2026_INTEL = """
TODAY: Wednesday, January 14, 2026.
OFFICIAL NFL DIVISIONAL ROUND (JAN 17-18, 2026):
- Bills @ Broncos | 49ers @ Seahawks | Texans @ Patriots | Rams @ Bears
INJURY UPDATES: George Kittle (OUT - Achilles), Trent Williams (GTD - Hamstring).
"""

# 2. SIDEBAR NAVIGATION
with st.sidebar:
    st.title("Sovereign AI 2026")
    mode = st.radio("SELECT MISSION:", [
        "🎯 Vegas Sniper (Truth Engine)", 
        "📈 Trading Sniper (Zoned Analysis)", 
        "💼 Hidden Job Market Scanner", 
        "🪄 Prompt Master"
    ])
    st.info("System: 2026 Truth Engine Active")

# 3. MISSION LOGIC
if mode == "🎯 Vegas Sniper (Truth Engine)":
    st.title("🎯 Vegas Sniper 2026")
    agent = Agent(
        model=Groq(id="llama-3.3-70b-versatile"), 
        tools=[DuckDuckGoTools()], 
        instructions=[f"Use Truth Engine: {VERIFIED_2026_INTEL}", "Provide prop estimates for yards/TDs."]
    )
    query = st.text_input("Enter Player or Team:", value="Bills")
    if st.button("🚀 EXECUTE SCAN"):
        st.markdown(agent.run(query).content)

elif mode == "📈 Trading Sniper (Zoned Analysis)":
    st.title("📈 Trading Sniper")
    symbol = st.text_input("Ticker (BTC-USD, NVDA):", "BTC-USD")
    tf = st.selectbox("Timeframe:", ["5m", "15m", "1h", "4h"])
    agent = Agent(
        model=Groq(id="llama-3.3-70b-versatile"), 
        tools=[YFinanceTools(technical_indicators=True)], 
        instructions=[f"Identify Demand/Supply zones for {symbol} on {tf} charts."]
    )
    if st.button("🔍 ANALYZE ZONES"):
        st.markdown(agent.run(f"Zoned report for {symbol}").content)

elif mode == "💼 Hidden Job Market Scanner":
    st.title("💼 Career Pivot Strategist")
    st.write("Target: 11 Years Logistics -> Safety Specialist")
    if st.button("🏗️ GENERATE STRATEGY"):
        agent = Agent(model=Groq(id="llama-3.3-70b-versatile"))
        st.markdown(agent.run("Provide a 5-step strategy for an 11-year logistics veteran to pivot to Safety.").content)

elif mode == "🪄 Prompt Master":
    st.title("🪄 Prompt Master")
    p = st.text_area("Paste draft:")
    if st.button("💎 OPTIMIZE"):
        agent = Agent(model=Groq(id="llama-3.3-70b-versatile"))
        st.markdown(agent.run(f"Rewrite as an elite prompt: {p}").content)