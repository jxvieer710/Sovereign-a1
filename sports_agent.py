from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.tools.duckduckgo import DuckDuckGoTools 
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reader.pdf_reader import PDFReader
from agno.vectordb.lancedb import LanceDb
from agno.knowledge.embedder.ollama import OllamaEmbedder

# 1. Setup Local Embeddings (Nomic)
local_embedder = OllamaEmbedder(id="nomic-embed-text", dimensions=768)

# 2. Setup the Sports Vault (Distinct Memory)
knowledge_base = Knowledge(
    vector_db=LanceDb(
        uri="tmp/lancedb_sports",
        table_name="sports_memory",
        embedder=local_embedder,
    ),
    # num_documents deprecated in v2.0
)
# Reads your Prop Protocol from the folder
knowledge_base.add_content(path="sports_vault", reader=PDFReader(chunk=True))

# 3. The Player Prop Specialist Agent
agent = Agent(
    model=Ollama(id="llama3.2:3b"),
    tools=[DuckDuckGoTools()], 
    knowledge=knowledge_base,
    add_knowledge_to_context=True, 
    markdown=True,
    description="You are a Player Prop Analyst specializing in NFL and NBA performance.",
    instructions=[
        "IDENTITY: You find inefficiencies in player prop lines by analyzing matchups and usage.",
        "STEP 1: ALWAYS check 'Prop_Protocol.pdf' for rules on Blowouts and Injury Correlations first.",
        "STEP 2: Use DuckDuckGo to find: 'Player Name last 5 games stats', 'Opponent Rank vs [Position]', and 'Current Prop Line'.",
        "STEP 3: Analyze the 'Script': Is the team likely to trail (more passing) or lead (more running)?",
        "OUTPUT FORMAT: ## PLAYER STATS (Last 5), ## DEFENSIVE MATCHUP (DvP), ## SCRIPT ANALYSIS, ## SUGGESTED PROP PLAY."
    ],
)

# 4. Continuous Fire Loop (The Chatbot)
print("--- Sovereign Intelligence: Prop Assassin Active (Type 'exit' to quit) ---")

while True:
    try:
        # Get your command
        user_query = input("\n>> Enter Player/Prop: ")

        # Allow you to quit
        if user_query.lower() in ["exit", "quit", "q"]:
            print("Shutting down Sovereign Intelligence...")
            break

        # Fire the agent
        agent.print_response(user_query, stream=True)
        
    except KeyboardInterrupt:
        break