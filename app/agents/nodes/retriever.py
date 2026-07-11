import logfire 
from app.agents.state import AgentState
from app.services.retreival.qdrant_service import search_enterprise_knowledge
from app.services.retreival.ranking_service import rerank_documents 

def retreiver_node(state:AgentState): 

    query=state['messages'][-1]['content'] if state['messages'] else ""

    with logfire.span("🔍 Knowledge Retrieval"):
        logfire.info(f"Searching Qdrant for :{query}")
        raw_results = search_enterprise_knowledge(query, limit=15)
        logfire.info(f"Retreived {len(raw_results)}candiadates from vector db")

        doc_contents=[doc['content'] for doc in raw_results]

        with logfire.span("Reranking"): 
            reranked_docs=rerank_documents(query,doc_contents,top_n =5)
            logfire.info(
    f"Reranking completed. Selected {len(reranked_docs)} documents."
)
        formatted_docs = [f"CONTENT: {doc}" for doc in reranked_docs]
    
    return {
        "documents":formatted_docs,
        "status":f"Retrieved relevant enterprise documents",
        "plan":state['plan']+['Context Retrived']
    }