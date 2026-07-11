import time
import logfire
from flashrank import Ranker, RerankRequest

# Lazy initialization - Ranker is loaded on first use to ensure logfire.configure() has run
_ranker=None 

def _get_ranker()->Ranker:
    """
     Initializes the FlashRank engine lazily. 
    FlashRank uses a local ONNX model (ms-marco-MiniLM-L-6-v2) for ultra-fast reranking.
    """
    global _ranker 
    if _ranker is None: 
        logfire.info("Initializing flash rank model locally..")
        try:
            _ranker=Ranker(cache_dir="/tmp/flashrank")
        except Exception as e:
            _ranker=Ranker()
    return _ranker

def rerank_documents(query:str,documents:list[str],top_n:int =5)->list[str]:

    if not documents:
        return []
    
    start_time=time.time()
    logfire.info(f"Reranker sending {len(documents)} docs to Flashrank cross encoder")
    try:
        ranker=_get_ranker()
        passages=[
            {"id":i,"text":doc}
            for i,doc in enumerate(documents)
        ]
        request = RerankRequest(query=query, passages=passages)
        results = ranker.rerank(request)

        reranked_docs = []
        for res in results[:top_n]:
            reranked_docs.append(res['text'])

        duration=time.time()-start_time
        top_score = results[0]['score'] if results else 'N/A'
        logfire.info(f"✅ [Reranker] Done in {duration:.2f}s. Top semantic score: {top_score}")
        return reranked_docs
    
    except Exception as e:
        logfire.error(f"❌ [Reranker] Semantic Reranking Failed: {e}")

        return documents[:top_n]