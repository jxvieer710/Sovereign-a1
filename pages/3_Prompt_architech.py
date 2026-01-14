import streamlit as st
from groq import Groq

st.set_page_config(page_title="Prompt Architect", page_icon="📝", layout="wide")

with st.sidebar:
    st.title("📝 Prompt Architect")
    if st.button("New Session", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

system_prompt = "You are a Master Prompt Engineer. Write a PERFECT, structured prompt that the user can paste into another AI. Format: 1. Context, 2. The Prompt."

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("📝 Master Prompt Architect")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What do you need a prompt for?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    client = Groq(api_key=st.secrets["GROQ_API_KEY"])

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_prompt}, *st.session_state.messages],
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