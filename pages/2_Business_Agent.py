import streamlit as st
from groq import Groq

st.set_page_config(page_title="Sovereign Business", page_icon="💼", layout="wide")

with st.sidebar:
    st.title("💼 Sovereign Business")
    mode = st.radio("Select Agent Mode:", ["Hidden Job Market Scanner", "Corporate Spy (Resume/Email)", "Side Hustle Strategist"])
    if st.button("New Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

prompts = {
    "Hidden Job Market Scanner": "You are a Career Strategist. Find high-paying niche roles for a user with 11 years logistics/labor experience. Focus on pivots to Tech, Safety, or Management.",
    "Corporate Spy (Resume/Email)": "You are a Corporate Consultant. Rewrite inputs to sound high-status and authoritative. Use punchy, direct language.",
    "Side Hustle Strategist": "You are a Lean Startup Consultant. Critique ideas ruthlessly and calculate margins."
}

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title(f"🚀 {mode}")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Type here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    client = Groq(api_key=st.secrets["GROQ_API_KEY"])

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": prompts[mode]}, *st.session_state.messages],
            stream=True,
        )
        
        # --- THE FIX: Extract only text ---
        def parse_stream(stream):
            for chunk in stream:
                content = chunk.choices[0].delta.content
                if content:
                    yield content
        
        response = st.write_stream(parse_stream(stream))
    
    st.session_state.messages.append({"role": "assistant", "content": response})