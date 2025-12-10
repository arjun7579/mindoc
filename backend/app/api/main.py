from fastapi import FastAPI
from app.api import ingest, query

app = FastAPI(title="Offline RAG Backend", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ingest.router)
app.include_router(query.router)

@app.get("/")
def health_check():
    return {"status": "ok", "system": "offline-rag"}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
