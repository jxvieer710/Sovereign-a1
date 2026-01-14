from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.tools.yfinance import YFinanceTools
from agno.tools.duckduckgo import DuckDuckGoTools 
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reader.pdf_reader import PDFReader
from agno.vectordb.lancedb import LanceDb
from agno.knowledge.embedder.ollama import OllamaEmbedder

# 1. Setup Local Embeddings (Nomic)
local_embedder = OllamaEmbedder(id="nomic-embed-text", dimensions=768)

# 2. Setup the Knowledge Vault (Sovereign Memory)
knowledge_base = Knowledge(
    vector_db=LanceDb(
        uri="tmp/lancedb",
        table_name="sovereign_memory",
        embedder=local_embedder,
    ),
    # num_documents removed (deprecated in v2.0)
)

# 3. Add Content (This automatically queues/loads the file)
knowledge_base.add_content(path="vault", reader=PDFReader(chunk=True))

# 4. Final Master Agent: Sovereign Intelligence
agent = Agent(
    model=Ollama(id="llama3.2:3b"),
    tools=[YFinanceTools(), DuckDuckGoTools()], 
    knowledge=knowledge_base,
    add_knowledge_to_context=True, 
    markdown=True,
    description="You are the Sovereign God Mode Orchestrator for Javier Garcia.",
    instructions=[
        "IDENTITY: You possess the private trading edge of Javier Garcia.",
        "STEP 1: ALWAYS search the knowledge base for 'Sovereign Trading Protocol' PDF.",
        "STEP 2: Use DuckDuckGo to check for any high-impact news or economic calendar events.",
        "STEP 3: Check H1 Market Structure (HH/HL) and M15 Range breakouts.",
        "STEP 4: Output format: ## STRATEGY VALIDATION, ## NEWS FLASH, ## STRUCTURE ANALYSIS.",
        "WARNING: If high-impact news is within 15 minutes, warn the user to stay sidelined."
    ],
)

# NOTE: agent.knowledge.load() is removed as it is no longer needed.

print("--- Sovereign Intelligence: Total Domination Active ---")
user_query = input("Enter Asset (e.g. EURUSD=X) or Strategy Question: ")
agent.print_response(user_query, stream=True)