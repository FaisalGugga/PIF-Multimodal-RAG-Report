from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ..rag_orchestrator.pipeline import run_rag_pipeline

router = APIRouter()

class AskRequest(BaseModel):
    question: str
    limit: int = 5
    

@router.post("/ask")
def ask(request: AskRequest):
    if not request.question.strip():
        raise HTTPException(detail="Question cannot be empty")
    
    try:
        result = run_rag_pipeline(
            question=request.question,
            limit=request.limit
        )
        return result
    
    except Exception as e:
        raise HTTPException(detail=str(e))
    
    