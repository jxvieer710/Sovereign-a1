import streamlit as st

# 1. SETUP THE NAVIGATION (The Master Switchboard)
# This lists all your apps for the iPhone sidebar
pg = st.navigation([
    st.Page("app_sports.py", title="Vegas Sniper", icon="🎯", default=True),
    st.Page("app_trading.py", title="Trading Sniper", icon="📈"),
    st.Page("app_business.py", title="Business Agent", icon="💼"),
    st.Page("app_prompt.py", title="Prompt Master", icon="🪄")
])

# 2. SHARED CONFIGURATION
# This title and layout apply to all 4 apps
st.set_page_config(page_title="Sovereign AI", layout="wide")

# 3. RUN THE SELECTED PAGE
# This is the command that swaps the screen when you tap a menu item
pg.run()