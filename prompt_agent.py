import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Forex Sniper", page_icon="💱")
st.title("💱 Forex Sniper")

# MANUAL KEY UPDATE
api_key = "AIzaSyCkdoiNYqaqSpOCRAB7l6oNL4NU_uemTZI"
genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-1.5-flash")

with st.form("trade_form"):
    pair = st.selectbox("Select Pair", ["EUR/USD", "GBP/JPY", "XAU/USD (Gold)"])
    timeframe = st.select_slider("Timeframe", options=["5m", "15m", "1H", "4H", "Daily"])
    submitted = st.form_submit_button("Analyze Market")

if submitted:
    with st.spinner("Analyzing..."):
        try:
            response = model.generate_content(f"Analyze {pair} on {timeframe}")
            st.markdown(response.text)
        except Exception as e:
            st.error(f"Error: {e}")