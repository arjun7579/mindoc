import os
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

MODEL_ID = "MBZUAI/LaMini-Flan-T5-248M"
SAVE_PATH = os.path.join(os.getcwd(), "data", "models", "lamini")

def download_lamini():
    print(f"Downloading LaMini Model: {MODEL_ID}...")

    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)

    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_ID)
    
    if not os.path.exists(SAVE_PATH):
        os.makedirs(SAVE_PATH)
        
    tokenizer.save_pretrained(SAVE_PATH)
    model.save_pretrained(SAVE_PATH)
    
    print("LaMini saved to:", SAVE_PATH)

if __name__ == "__main__":
    download_lamini()
