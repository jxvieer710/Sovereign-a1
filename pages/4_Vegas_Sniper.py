import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
import datetime

# 1. Page Config
st.set_page_config(page_title="Master Sniper v15", page_icon="🎯", layout="wide")

# 2. INTERNAL TRUTH ENGINE (Verified 2026 Reality)
# This overrides the internet's tendency to show old 2025 data.
VERIFIED_2026_INTEL = """
CURRENT DATE: Jan 14, 2026.
NEXT NFL ROUND: Divisional Round (Jan 17-18, 2026).
NEXT NBA: Regular Season games (Lakers vs Suns, etc.).
"""

# 3. Sidebar for Search
with st.sidebar:
    st.title("🎯 Master Sniper v15")
    query = st.text_input("Search Team or Player:", value="Bills")
    if st.button("🚀 EXECUTE DEEP SCAN"):
        st.rerun()

# 4. Main Interface
st.title("📊 Multi-Sport Master Sniper")

if not query:
    st.info("👈 Enter a team name to start.")
else:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    with st.spinner(f"Analyzing {query}..."):
        # We search specifically for 2026 depth charts and prop trends
        with DDGS() as ddgs:
            raw_data = "\n".join([r['body'] for r in list(ddgs.text(f"{query} player props 2026", max_results=5))])

        prompt = f"""
        Act as a DFS Analyst. TODAY: Jan 14, 2026. TARGET: {query}.
        TRUTH_ENGINE: {VERIFIED_2026_INTEL}
        DATA: {raw_data}

        INSTRUCTIONS:
        1. Identify the sport and the NEXT game.
        2. CATEGORIZE the roster: STARS, SECOND STRING, and BREAKOUTS (High field time/low prop lines).
        3. For EVERY player, provide sport-specific prop estimates (Yds, TDs for NFL | Pts, Reb for NBA).
        4. Include 'Last 5 Games Trend': Are they hitting their OVER or UNDER?
        5. SIGNAL: [OVER/UNDER] based on usage/injuries.
        6. NO TABLES. Use a clean list with emojis.
        """
        
        try:
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1
            )
            st.markdown(completion.choices[0].message.content)
        except Exception as e:
            st.error("AI Analysis failed. Check Groq Key.")