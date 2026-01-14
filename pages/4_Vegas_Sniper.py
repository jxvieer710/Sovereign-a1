import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
import datetime

# 1. Page Config
st.set_page_config(page_title="Vegas Sniper 2026", page_icon="🎯", layout="wide")

# 2. INTERNAL TRUTH ENGINE (Hard-coded 2026 Divisional Reality)
# This overrides the internet's tendency to show old 2025 data.
VERIFIED_2026_INTEL = """
CURRENT DATE: Wednesday, January 14, 2026.
OFFICIAL NFL DIVISIONAL ROUND (JAN 17-18, 2026):
- Sat Jan 17, 4:30 PM: (6) Buffalo Bills @ (1) Denver Broncos (CBS)
- Sat Jan 17, 8:00 PM: (6) San Francisco 49ers @ (1) Seattle Seahawks (FOX)
- Sun Jan 18, 3:00 PM: (5) Houston Texans @ (2) New England Patriots (ESPN)
- Sun Jan 18, 6:30 PM: (5) LA Rams @ (2) Chicago Bears (NBC)

2026 PLAYER DATA (BILLS):
- QB: Josh Allen (Star)
- RB: James Cook (Star - 1,621 Yds in 2025), Ray Davis (Role), Ty Johnson (Role)
- WR: Brandin Cooks, Khalil Shakir, Keon Coleman (Breakout)
- TE: Dalton Kincaid (Star), Dawson Knox

2026 PLAYER DATA (49ERS):
- QB: Brock Purdy (Star)
- RB: Christian McCaffrey (Star - 1,039 Rush / 849 Rec), Brian Robinson Jr. (Role)
- WR: Jauan Jennings, Ricky Pearsall (Breakout - Knee PCL Questionable), Kendrick Bourne
- TE: George Kittle (OUT - Achilles Surgery), Jake Tonges (Starter)
- OL: Trent Williams (Questionable - Hamstring)
"""

# 3. Sidebar
with st.sidebar:
    st.title("🎯 Sniper Master 2026")
    st.caption("VERIFIED DIVISIONAL DATA")
    query = st.text_input("Search Team (Bills, 49ers, Rams, etc.):", value="Bills")
    if st.button("🚀 EXECUTE DEEP SCAN", type="primary"):
        st.rerun()

# 4. Universal Data Fetcher
def fetch_data(target):
    try:
        # Forcing search for the Jan 17, 2026 game specifically
        full_query = f"{target} player props January 2026 site:espn.com OR site:fanduel.com"
        with DDGS() as ddgs:
            results = list(ddgs.text(full_query, max_results=5))
            return "\n".join([r['body'] for r in results])
    except:
        return "Using internal 2026 truth data."

# 5. Main Interface
st.title("📊 2026 Betting Intelligence")

if not query:
    st.info("👈 Enter a team name to start.")
else:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    
    with st.spinner(f"Validating 2026 Roster & Matchup for {query}..."):
        search_data = fetch_data(query)
        
        prompt = f"""
        Act as a Professional DFS Analyst. TODAY: Jan 14, 2026.
        TARGET: {query}
        TRUTH_ENGINE: {VERIFIED_2026_INTEL}
        SCRAPED_DATA: {search_data}

        INSTRUCTIONS:
        1. Identify the UPCOMING 2026 Divisional game from the TRUTH_ENGINE.
        2. Break the roster into STARS, ROLE PLAYERS, and BREAKOUTS.
        3. For EVERY player, provide these prop estimates:
           - PASSING: Yds, TDs
           - RUSHING: Yds, TDs
           - RECEIVING: Yds, Rec, Longest Catch
        4. Include '2026 Trend Analysis': Mention injuries (e.g. Kittle being OUT, Trent Williams questionable).
        5. NO TABLES. NO POSITIONS (QB/RB). Use a clean list with emojis.
        """
        
        try:
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1
            )
            st.markdown(completion.choices[0].message.content)
            
        except Exception as e:
            st.error("AI Analysis failed. Check connection.")