# 🧠 Mindoc — Private Offline RAG Assistant

Mindoc is a **fully offline, privacy-first AI assistant** that lets you **chat with your PDFs and PPTs** — without internet, API keys, or cloud services.  
Everything runs **entirely on your local CPU** using Small Language Models (SLMs).

---

## 🚀 Key Features

### 🔒 100% Offline
- No OpenAI  
- No cloud dependencies  
- No data leaves your device  
- All models stored locally  

### 📄 Multi-Document Ingestion
- Upload **multiple PDFs and PPTs**  
- Fully private, local processing  
- Fast and accurate extraction  

### 🧠 Local LLM
Powered by **LaMini-Flan-T5 (248M)** optimized for CPU inference.

### 🔎 Hybrid Search Engine
**Semantic Vector Search + Cross-Encoder Reranking**

- Vector Model: `all-MiniLM-L6-v2`  
- Reranker: `ms-marco-MiniLM-L12-v2`  

### ⚡ Dual Search Modes
- **Quick Mode:** Fast, short answers (Top-2 docs)  
- **Deep Research:** Multi-doc reasoning using Map-Reduce  

### 🔗 Smart Citations
- Evidence-based answers  
- Click on a citation → open PDF → auto-scroll to exact page  

---

## 🛠️ Technical Architecture

### 1. Ingestion Pipeline
- **Loader:** PyMuPDFLoader  
- **Chunking:** RecursiveCharacterTextSplitter  
  - Chunk size: 1000 chars  
  - Overlap: 200 chars  
- **Embeddings:** SentenceTransformer (384-dim)  
- **Storage:** ChromaDB (Local persistence)

### 2. Retrieval & Generation
1. Retrieve top-10 chunks with vector search  
2. Re-rank with cross-encoder, keep best 3  
3. Feed context → LaMini LLM → generate answer  

---
## 🏗️ System Architecture
           ┌────────────┐
           │   Files     │
           │ PDF / PPTX  │
           └──────┬─────┘
                  │
                  ▼
          ┌────────────────┐
          │ Document Loader │
          └──────┬─────────┘
                  │Chunks
                  ▼
      ┌────────────────────────┐
      │ Embeddings (Local Model)│
      └──────────┬────────────┘
                 │Vectors
                 ▼
        ┌──────────────────┐
        │ Vector Store      │
        │ FAISS / Chroma    │
        └────────┬─────────┘
                 │
                 ▼
        ┌───────────────────┐
        │ RAG Pipeline       │
        │ (Retrieve + LLM)   │
        └────────┬──────────┘
                 │
                 ▼
          ┌────────────┐
          │  FastAPI    │
          │  /query     │
          └────────────┘
---

## 📦 Installation Guide

### Prerequisites
- Python **3.10+** (3.12 recommended)  
- Node.js & npm  

---

## 🔧 Backend Setup (FastAPI)

```bash
cd backend

# Virtual environment
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download models (run once)
python download_model.py
python download_reranker.py

# Start backend server
uvicorn app.main:app --reload
```
## 🎨 Frontend Setup (React + Vite)

```bash
cd frontend

npm install
npm run dev
```

## 🖥️ Usage

### **Upload Documents**
- Drag & drop PDFs  
- Supports batch uploads  
- Wait for **“✅ Indexed”** confirmation  

### **Chat with Your Documents**

#### ⚡ **Quick Mode**
- Fast  
- Lightweight  
- Best for direct questions  

#### 🧠 **Deep Research**
- Reads many chunks  
- Map-Reduce summarization  
- Great for reports & summaries  

### **Verify Sources**
- Each answer includes clickable citations  
- Opens full PDF and auto-scrolls to correct page  

---

## 📂 Project Structure

```
mindoc/
├── backend/
│ ├── app/
│ │ ├── api/
│ │ ├── rag/
│ │ ├── services/
│ │ └── main.py
│ ├── data/
│ │ ├── chroma/
│ │ ├── models/
│ │ └── uploads/
│ ├── download_model.py
│ ├── download_reranker.py
│ └── requirements.txt
│
└── frontend/
├── src/
│ ├── App.jsx
│ ├── App.css
│ └── main.jsx
└── package.json

```

## ❗ Troubleshooting

### **sqlite3 errors (Python 3.12)**
Install SQLite shim:

```bash
pip install pysqlite3-binary
```
### **Context Window Errors**
Long chunks → crash.
Fixed by enabling:
```bash
truncation=True
```
### **500 Search Errors**
Usually caused by a missing reranker model.
Run again:
```bash
python download_reranker.py
```
---
## 🔮 Future Roadmap

- [ ] OCR for scanned documents  
- [ ] Model switching (LaMini ↔ Phi-2 ↔ Qwen 0.5B)  
- [ ] Persistent conversation history  
- [ ] Voice mode (offline ASR)
---
