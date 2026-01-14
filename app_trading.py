import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from groq import Groq
import json
import re

# 1. Page Config
st.set_page_config(page_title="Sniper Terminal v4", page_icon="🦅", layout="wide")

# 2. Sidebar: Command Center
with st.sidebar:
    st.header("🦅 Sniper Command v4")
    
    # Custom Ticker Input
    st.info("ENTER TARGET ASSET")
    user_input = st.text_input("Symbol:", value="EUR/USD", help="Try: BTC-USD, EUR/USD, NVDA")
    
    # Timeframes
    timeframe_map = {
        "5 Minutes (Scalp)": "5m",
        "15 Minutes (Day Trade)": "15m",
        "30 Minutes": "30m",
        "1 Hour (Swing)": "1h",
        "4 Hours (Trend)": "1h", 
        "1 Day (Macro)": "1d"
    }
    selected_label = st.selectbox("Timeframe:", list(timeframe_map.keys()), index=1)
    interval = timeframe_map[selected_label]
    
    if st.button("⚡ RELOAD INTEL", use_container_width=True):
        st.rerun()

# --- SMART TICKER CORRECTION ---
ticker = user_input.upper().strip()
if "/" in ticker and "=X" not in ticker:
    ticker = ticker.replace("/", "") + "=X"
# -------------------------------

# 3. Main Logic
st.title(f"🦅 Target: {ticker}")

try:
    # A. Intelligent Data Fetching
    if interval in ["5m", "15m", "30m"]:
        period = "5d"
    elif interval == "1h":
        period = "1mo"
    else:
        period = "1y"

    data = yf.download(ticker, period=period, interval=interval)
    
    # B. News Fetching
    news_context = "No recent breaking news found."
    try:
        ticker_obj = yf.Ticker(ticker)
        news_list = ticker_obj.news
        latest_headlines = []
        if news_list:
            for item in news_list[:3]:
                headline = item.get('title') or item.get('headline')
                if headline:
                    latest_headlines.append(f"- {headline}")
        if latest_headlines:
            news_context = "\n".join(latest_headlines)
    except Exception:
        news_context = "News feed temporarily unavailable."

    if not data.empty:
        # C. Live Metrics
        current_price = data['Close'].iloc[-1].item()
        prev_price = data['Close'].iloc[-2].item()
        pct_change = ((current_price - prev_price) / prev_price) * 100
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Current Price", f"{current_price:,.4f}", f"{pct_change:.2f}%")
        col2.metric("Session High", f"{data['High'].max().item():,.4f}")
        col3.metric("Session Low", f"{data['Low'].min().item():,.4f}")
        
        # D. Base Chart
        fig = go.Figure(data=[go.Candlestick(x=data.index,
                        open=data['Open'].iloc[:,0],
                        high=data['High'].iloc[:,0],
                        low=data['Low'].iloc[:,0],
                        close=data['Close'].iloc[:,0])])
        fig.update_layout(
            title=f"{ticker} - LIVE FEED",
            height=500,
            template="plotly_dark",
            margin=dict(l=0, r=0, t=30, b=0)
        )
        
        # Placeholder
        chart_placeholder = st.empty()
        chart_placeholder.plotly_chart(fig, use_container_width=True)
        
        # E. The AI Sniper
        st.subheader("🤖 AI Tactical Grid")
        
        if st.button("GENERATE TACTICAL MAP"):
            with st.spinner("Calculating Ambush Zones..."):
                client = Groq(api_key=st.secrets["GROQ_API_KEY"])
                
                # We force it to give zones even if Waiting
                sniper_prompt = f"""
                Act as an elite algorithm. Analyze {ticker}.
                Price: {current_price}
                News: {news_context}
                
                CRITICAL INSTRUCTION:
                Even if the signal is WAIT, you MUST provide the "entry_price" that you are waiting for (the ambush level), along with hypothetical stop loss and take profit for that setup.
                
                Return a valid JSON OBJECT ONLY. No other text. Format:
                {{
                    "signal": "BUY / SELL / WAIT",
                    "entry_price": 0.0000,
                    "stop_loss": 0.0000,
                    "take_profit": 0.0000,
                    "reasoning": "Brief analysis string"
                }}
                """

                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": sniper_prompt}],
                    temperature=0.1 
                )
                
                raw_content = completion.choices[0].message.content
                
                try:
                    start = raw_content.find('{')
                    end = raw_content.rfind('}') + 1
                    json_str = raw_content[start:end]
                    
                    signal_data = json.loads(json_str)
                    
                    # --- DRAW LINES ON CHART ---
                    # Entry (Cyan) - Dashed if waiting, Solid if active
                    line_style = "dash" if "WAIT" in signal_data['signal'].upper() else "solid"
                    entry_text = "WATCH ZONE" if "WAIT" in signal_data['signal'].upper() else "ENTRY"
                    
                    fig.add_hline(y=signal_data['entry_price'], line_dash="dash", line_color="cyan", annotation_text=entry_text, annotation_position="top right")
                    fig.add_hline(y=signal_data['stop_loss'], line_dash="dot", line_color="red", annotation_text="SL", annotation_position="bottom right")
                    fig.add_hline(y=signal_data['take_profit'], line_dash="dot", line_color="#00FF00", annotation_text="TP", annotation_position="top right")
                    
                    # Update Chart
                    chart_placeholder.plotly_chart(fig, use_container_width=True)
                    
                    # Show Text Analysis
                    if "WAIT" in signal_data['signal'].upper():
                        st.warning(f"SIGNAL: {signal_data['signal']} (Waiting for price to hit Watch Zone)")
                    elif "BUY" in signal_data['signal'].upper():
                        st.success(f"SIGNAL: {signal_data['signal']}")
                    else:
                        st.error(f"SIGNAL: {signal_data['signal']}")
                        
                    st.write(f"**Strategy:** {signal_data['reasoning']}")
                    
                    # Data Table
                    st.table({
                        "Zone": ["Ambush/Entry", "Stop Loss", "Take Profit"],
                        "Price": [signal_data['entry_price'], signal_data['stop_loss'], signal_data['take_profit']]
                    })
                    
                except Exception as e:
                    st.error("Could not visualize zones. Raw Analysis:")
                    st.write(raw_content)

    else:
        st.error(f"Target '{ticker}' not found. Check spelling.")

except Exception as e:
    st.error(f"System Error: {e}")