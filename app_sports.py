import streamlit as st
from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.lancedb import LanceDb
from agno.knowledge.embedder.ollama import OllamaEmbedder

st.set_page_config(page_title="Sovereign Sports", page_icon="🏈", layout="centered")
st.header("🏈 Sports Assassin")

# Load Sports Memory
embedder = OllamaEmbedder(id="nomic-embed-text", dimensions=768)
knowledge = Knowledge(vector_db=LanceDb(uri="tmp/lancedb_sports", table_name="sports_memory", embedder=embedder))

agent = Agent(
    model=Ollama(id="llama3.2:3b"),
    tools=[DuckDuckGoTools()],
    knowledge=knowledge,
    add_knowledge_to_context=True,
    description="You are a Ruthless Sports Handicapper. Focus on Props, EV+, and Injury impacts."
)

if "messages" not in st.session_state: st.session_state.messages = []
for msg in st.session_state.messages: st.chat_message(msg["role"]).markdown(msg["content"])

if prompt := st.chat_input("Check Player Prop..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)
    with st.chat_message("assistant"):
        response = agent.run(prompt).content
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})