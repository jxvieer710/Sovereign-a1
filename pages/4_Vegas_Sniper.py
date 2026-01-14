import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
import datetime

# 1. Page Config
st.set_page_config(page_title="Master Sniper v15", page_icon="🎯", layout="wide")

# 2. INTERNAL TRUTH ENGINE (Verified 2026 Context)
VERIFIED_2026_INTEL = """
TODAY: Jan 14, 2026.
BILLS PLAYOFFS: Playing Denver Broncos on Sat, Jan 17, 2026.
49ERS PLAYOFFS: Playing Seattle Seahawks on Sat, Jan 17, 2026.
"""

# 3. Universal Search logic
def fetch_intel(target):
    try:
        with DDGS() as ddgs:
            return "\n".join([r['body'] for r in list(ddgs.text(f"{target} player props 2026 trends", max_results=5))])
    except:
        return "Search timed out."

# 4. Interface
st.title("📊 Multi-Sport Master Sniper")
query = st.text_input("Enter Team/Player:", value="Bills")

if st.button("🚀 EXECUTE SCAN"):
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    with st.spinner(f"Scanning 2026 data for {query}..."):
        raw_data = fetch_intel(query)
        prompt = f"DFS Analyst. Jan 14, 2026. Target: {query}. Truth: {VERIFIED_2026_INTEL}. Data: {raw_data}. Provide Stars, Second String, and Breakouts with sport-specific props and [OVER/UNDER] signals."
        completion = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}], temperature=0.1)
        st.markdown(completion.choices[0].message.content)