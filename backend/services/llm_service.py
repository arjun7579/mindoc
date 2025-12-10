import os
from transformers import pipeline

LOCAL_MODEL_DIR = os.path.join(os.getcwd(), "data", "models", "LaMini-Flan-T5-248M")

_llm_pipeline = None

def get_llm():
    global _llm_pipeline
    if _llm_pipeline is None:
        if not os.path.exists(LOCAL_MODEL_DIR):
            raise FileNotFoundError(f"Model not found at {LOCAL_MODEL_DIR}.")
        
        print(f"Loading Local LLM from: {LOCAL_MODEL_DIR}...")
        _llm_pipeline = pipeline(
            "text2text-generation",
            model=LOCAL_MODEL_DIR,
            tokenizer=LOCAL_MODEL_DIR,
            device=-1, 
            max_length=512
        )
    return _llm_pipeline

def generate_quick_answer(query: str, context_chunks: list):
    """
    Standard RAG: Truncates context to fit window. Fast but might lose details.
    """
    llm = get_llm()
    
    # Combined context (Safety truncated to 1000 chars)
    context_text = "\n\n".join([c['content'] for c in context_chunks])
    if len(context_text) > 1000:
        context_text = context_text[:1000]
        
    prompt = f"Question: {query}\nContext: {context_text}\nAnswer:"
    
    response = llm(prompt, truncation=True, max_length=512)
    return response[0]['generated_text']

def generate_deep_answer(query: str, context_chunks: list):
    """
    Map-Reduce RAG: Summarizes each chunk first, then answers.
    Allows using more documents (k=4) without crashing context window.
    """
    llm = get_llm()
    summaries = []
    
    print("Deep Search: Running Map Step...")
    for i, chunk in enumerate(context_chunks):

        content = chunk['content'][:800] 
        map_prompt = f"Extract key information about '{query}' from this text:\n{content}\nSummary:"

        res = llm(map_prompt, truncation=True, max_length=150)
        summaries.append(f"- {res[0]['generated_text']}")

    print("Deep Search: Running Reduce Step...")
    combined_summaries = "\n".join(summaries)
    
    final_prompt = f"""
    Based on these notes, answer the question: {query}
    
    Notes:
    {combined_summaries}
    
    Answer:
    """
    
    response = llm(final_prompt, truncation=True, max_length=512)
    return response[0]['generated_text']
