import streamlit as st
from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.yfinance import YFinanceTools

# 1. PAGE SETUP
st.set_page_config(page_title="Sovereign AI Master", layout="wide")

# 2. INTERNAL TRUTH ENGINE (Jan 2026 NFL Reality)
# Hard-coded to stop the AI from hallucinating 2025 data.
VERIFIED_2026_INTEL = """
TODAY: Wednesday, January 14, 2026.
OFFICIAL NFL DIVISIONAL ROUND (JAN 17-18, 2026):
- Sat Jan 17: (6) Bills @ (1) Broncos (4:30 PM) | (6) 49ers @ (1) Seahawks (8:00 PM)
- Sun Jan 18: (5) Texans @ (2) New England (3:00 PM) | (5) Rams @ (2) Bears (6:30 PM)

WEATHER ALERT (JAN 2026):
- Denver: Partly Cloudy, 50°F. Winds minimal.
- Chicago: Frigid (18°F), Light Snow possible. Ball security is a major factor.
- New England: Cold (33°F), Favors the home team defense.

INJURY TRUTH:
- George Kittle (49ers): OUT (Achilles Surgery)
- Trent Williams (49ers): Questionable (Hamstring)
- James Cook (Bills): Star RB (1,621 Yds in 2025)
"""

# 3. SIDEBAR NAVIGATION
with st.sidebar:
    st.title("🎯 Sovereign Master 2026")
    mode = st.radio("SELECT MISSION:", [
        "🎯 Vegas Sniper (Truth Engine)", 
        "📈 Trading Sniper (Zoned Analysis)", 
        "💼 Hidden Job Market Scanner", 
        "🪄 Prompt Master"
    ])
    st.divider()
    st.info("System: 2026 Truth Engine Active")

# Check for API Key
if "GROQ_API_KEY" not in st.secrets:
    st.error("Please add GROQ_API_KEY to your Streamlit Secrets.")
    st.stop()

# 4. MISSION LOGIC
if mode == "🎯 Vegas Sniper (Truth Engine)":
    st.title("🎯 Vegas Sniper 2026")
    query = st.text_input("Enter Team/Player for Jan 2026 Props:", value="Bills")
    
    if st.button("🚀 EXECUTE DEEP SCAN"):
        agent = Agent(
            model=Groq(id="llama-3.3-70b-versatile"),
            tools=[DuckDuckGoTools()],
            instructions=[
                f"TRUTH_ENGINE: {VERIFIED_2026_INTEL}",
                "Identify the upcoming Jan 2026 game and provide prop estimates (Pass/Rush/Rec Yds).",
                "MANDATORY: Provide ONLY raw search queries to the search tool. No XML tags."
            ],
            markdown=True
        )
        with st.spinner(f"Validating 2026 Intel for {query}..."):
            st.markdown(agent.run(query).content)

elif mode == "📈 Trading Sniper (Zoned Analysis)":
    st.title("📈 Trading Sniper")
    symbol = st.text_input("Instrument (BTC-USD, NVDA, Gold):", "BTC-USD")
    tf = st.selectbox("Chart Timeframe:", ["5m", "15m", "1h", "4h"])
    
    if st.button("🔍 ANALYZE ZONES"):
        agent = Agent(
            model=Groq(id="llama-3.3-70b-versatile"),
            tools=[YFinanceTools(technical_indicators=True)],
            instructions=[
                f"Identify Demand and Supply zones for {symbol} on the {tf} chart.",
                "Provide a probabilistic forecast: BULLISH / BEARISH / NEUTRAL."
            ],
            markdown=True
        )
        with st.spinner(f"Analyzing {symbol} {tf} zones..."):
            st.markdown(agent.run(f"Zoned Market Report for {symbol} on {tf}").content)

elif mode == "💼 Hidden Job Market Scanner":
    st.title("💼 Career Pivot Strategist")
    st.write("Target: 11 Years Logistics -> Safety Specialist")
    
    if st.button("🏗️ GENERATE STRATEGY"):
        agent = Agent(model=Groq(id="llama-3.3-70b-versatile"))
        prompt = "Act as a Hidden Job Market Scanner. Create a 5-step strategic pivot for an 11-year logistics professional moving into a Safety role."
        st.markdown(agent.run(prompt).content)

elif mode == "🪄 Prompt Master":
    st.title("🪄 Prompt Master")
    p = st.text_area("Paste draft prompt:")
    if st.button("💎 OPTIMIZE"):
        agent = Agent(model=Groq(id="llama-3.3-70b-versatile"))
        st.markdown(agent.run(f"Rewrite into an elite, structured AI prompt: {p}").content)