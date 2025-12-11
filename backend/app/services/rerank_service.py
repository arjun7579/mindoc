import os
from sentence_transformers import CrossEncoder

RERANKER_PATH = os.path.join(os.getcwd(), "data", "models", "reranker")

_reranker = None

def get_reranker():
    global _reranker
    if _reranker is None:
        _reranker = CrossEncoder(RERANKER_PATH)
    return _reranker

def rerank_documents(query: str, docs: list, top_k: int = 3):

    model = get_reranker()
    pairs = [[query, doc['content']] for doc in docs]
    
  
    scores = model.predict(pairs)
    
    for i, doc in enumerate(docs):
        doc['rerank_score'] = float(scores[i])
        
    ranked_docs = sorted(docs, key=lambda x: x['rerank_score'], reverse=True)
    
    return ranked_docs[:top_k]
