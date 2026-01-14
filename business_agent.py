from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reader.pdf_reader import PDFReader
from agno.vectordb.lancedb import LanceDb
from agno.knowledge.embedder.ollama import OllamaEmbedder

# 1. Setup Local Embeddings
local_embedder = OllamaEmbedder(id="nomic-embed-text", dimensions=768)

# 2. Setup the Business Vault (New Database)
knowledge_base = Knowledge(
    vector_db=LanceDb(
        uri="tmp/lancedb_biz",
        table_name="biz_memory",
        embedder=local_embedder,
    ),
)
# Create a 'biz_vault' folder later if you have PDF documents (leases/contracts)
# knowledge_base.add_content(path="biz_vault", reader=PDFReader(chunk=True))

# 3. The Sovereign Operations Director
agent = Agent(
    model=Ollama(id="llama3.2:3b"),
    tools=[DuckDuckGoTools()], 
    knowledge=knowledge_base,
    add_knowledge_to_context=True, 
    markdown=True,
    description="You are the Operations Director for OneStop Lawnscape Shop and Javier Garcia's Business Ventures.",
    instructions=[
        "IDENTITY: You are an expert in CA Small Business Grants, Commercial Real Estate (Valley Area), and Logistics.",
        "GOAL 1 (GRANTS): Periodically check 'Carl Moyer Program', 'CORE', and 'eL&G Pilot' for lawn equipment incentives.",
        "GOAL 2 (REAL ESTATE): Search for 'Industrial Flex Space' or 'Live/Work Warehouse' in zip codes 91331, 91340, 91352 (San Fernando/Pacoima/Sun Valley).",
        "GOAL 3 (CASH FLOW): Identify high-paying 'Medical Courier' contracts (BioTouch, Dropoff) that accept personal vehicles.",
        "OUTPUT FORMAT: ## OPPORTUNITY ALERT, ## DEADLINE/ACTION, ## ESTIMATED VALUE."
    ],
)

# 4. Continuous Fire Loop
print("--- Sovereign Intelligence: Business Director Active (Type 'exit' to quit) ---")

while True:
    try:
        user_query = input("\n>> Enter Business Task: ")
        if user_query.lower() in ["exit", "quit", "q"]:
            print("Shutting down Operations...")
            break
        agent.print_response(user_query, stream=True)
    except KeyboardInterrupt:
        break