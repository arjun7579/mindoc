import os
from sentence_transformers import CrossEncoder


MODEL_ID = "cross-encoder/ms-marco-MiniLM-L-6-v2"
SAVE_PATH = os.path.join(os.getcwd(), "data", "models", "reranker")

def download_reranker():
    print(f"Downloading Reranker: {MODEL_ID}...")
    model = CrossEncoder(MODEL_ID)
    model.save(SAVE_PATH)
    print("Reranker saved to", SAVE_PATH)

if __name__ == "__main__":
    download_reranker()
