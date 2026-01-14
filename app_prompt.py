import streamlit as st
from agno.agent import Agent
from agno.models.ollama import Ollama

st.set_page_config(page_title="Sovereign Strategy", page_icon="🧠", layout="centered")
st.header("🧠 Strategy Translator")

agent = Agent(
    model=Ollama(id="llama3.2:3b"),
    description="You convert raw user thoughts into high-precision technical commands."
)

if "messages" not in st.session_state: st.session_state.messages = []
for msg in st.session_state.messages: st.chat_message(msg["role"]).markdown(msg["content"])

if prompt := st.chat_input("Your Rough Idea..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)
    with st.chat_message("assistant"):
        response = agent.run(prompt).content
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})