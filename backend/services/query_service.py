from app.rag.vector_store import get_vector_store
from app.services.llm_service import generate_quick_answer, generate_deep_answer
from app.services.rerank_service import rerank_documents
def semantic_search(query_text: str, mode: str = "quick"):
    db = get_vector_store()
    
   
    initial_k = 10 
    results = db.similarity_search_with_score(query_text, k=initial_k)
    
    raw_docs = []
    for doc, score in results:
        raw_docs.append({
            "content": doc.page_content,
            "metadata": doc.metadata,
            "score": float(score) # Vector distance
        })
    
    
    ranked_docs = rerank_documents(query_text, raw_docs, top_k=3)
    
   
    if mode == "deep":
        ai_answer = generate_deep_answer(query_text, ranked_docs)
    else:
        ai_answer = generate_quick_answer(query_text, ranked_docs)
    
    return {
        "answer": ai_answer,
        "mode": mode,
        "results": ranked_docs 
    }
