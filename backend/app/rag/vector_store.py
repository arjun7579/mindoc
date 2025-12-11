import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

CHROMA_PATH = os.path.join(os.getcwd(), "data", "chroma")
MODEL_NAME = "all-MiniLM-L6-v2"

embedding_function = HuggingFaceEmbeddings(
    model_name=MODEL_NAME,
    model_kwargs={'device': 'cpu'}, # Use 'cuda' if GPU available
    encode_kwargs={'normalize_embeddings': True}
)

def get_vector_store():
    """
    Returns the persistent ChromaDB instance.
    """
    return Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embedding_function,
        collection_name="private_rag"
    )

def add_documents_to_db(chunks):
    db = get_vector_store()
    db.add_documents(chunks)
    # Chroma 0.4+ autosaves, but we ensure it persists
    return True
