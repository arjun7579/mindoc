import shutil
import os
from typing import List
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.rag.loader import load_document
from app.rag.chunker import get_chunker
from app.rag.vector_store import add_documents_to_db

router = APIRouter()

UPLOAD_DIR = os.path.join(os.getcwd(), "data", "uploads")

@router.post("/ingest")
async def ingest_documents(files: List[UploadFile] = File(...)):

  ingestion_report = []

    try:
        chunker = get_chunker()
        
        for file in files:
            # 1. Save File Locally
            file_path = os.path.join(UPLOAD_DIR, file.filename)
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            # 2. Load & Chunk
            # Note: If one file fails, we catch it so others can still proceed
            try:
                raw_docs = load_document(file_path)
                chunks = chunker.split_documents(raw_docs)
                
                # 3. Add to DB
                add_documents_to_db(chunks)
                
                ingestion_report.append({
                    "filename": file.filename,
                    "status": "success",
                    "chunks": len(chunks)
                })
            except Exception as e:
                print(f"Error processing {file.filename}: {e}")
                ingestion_report.append({
                    "filename": file.filename,
                    "status": "failed",
                    "error": str(e)
                })

        return {
            "message": "Batch processing complete",
            "report": ingestion_report
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch ingestion failed: {str(e)}")
