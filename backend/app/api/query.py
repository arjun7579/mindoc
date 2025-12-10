from fastapi import APIRouter, HTTPException
from app.services.query_service import semantic_search

router = APIRouter()

@router.get("/query")
async def query_documents(q: str, mode: str = "quick"):
    """
    Accepts ?q=...&mode=quick OR ?q=...&mode=deep
    """
    if not q:
        raise HTTPException(status_code=400, detail="Query cannot be empty")
        
    try:
        response_data = semantic_search(q, mode)
        return response_data
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
