import streamlit as st

# Setup the Navigation Sidebar
pg = st.navigation([
    st.Page("app_sports.py", title="Vegas Sniper", icon="🎯", default=True),
    st.Page("app_trading.py", title="Trading Sniper", icon="📈"),
    st.Page("app_business.py", title="Business Agent", icon="💼"),
    st.Page("app_prompt.py", title="Prompt Master", icon="🪄")
])

st.set_page_config(page_title="Sovereign AI", layout="wide")
pg.run()