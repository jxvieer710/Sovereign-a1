import streamlit as st

# 1. THE NAVIGATION (The Hallway)
# This defines the "doors" in your sidebar
pg = st.navigation([
    st.Page("app_sports.py", title="Vegas Sniper", icon="🎯", default=True),
    st.Page("app_trading.py", title="Trading Sniper", icon="📈")
])

# 2. GLOBAL CONFIG (The Roof)
# This title and icon appear in your browser tab for every page
st.set_page_config(page_title="Sovereign AI", page_icon="🎯", layout="wide")

# 3. RUN THE SELECTED PAGE
# This executes the specific code for whichever page is currently selected
pg.run()

# --- CONTENT FOR VEGAS SNIPER ---
# This code only runs when "Vegas Sniper" is selected in the menu
st.title("🎯 Vegas Sniper Master")
st.info("January 2026 Sports Intelligence Protocol Active.")

# Safely check for your Groq Key in Streamlit Secrets
if "GROQ_API_KEY" in st.secrets:
    st.success("System Status: Online")
    # Your Vegas Sniper logic goes here...
else:
    st.error("Missing Key! Go to Streamlit Settings > Secrets and add GROQ_API_KEY.")