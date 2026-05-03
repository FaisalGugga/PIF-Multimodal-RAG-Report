from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ..rag_orchestrator.pipeline import run_rag_pipeline

router = APIRouter()

class AskRequest(BaseModel):
    question: str
    limit: int = 5
    document_id: str | None = None
    company_id: str | None = None
    year: int | None = None

@router.post("/ask")
def ask(request: AskRequest):
    if not request.question.strip():
        raise HTTPException(detail="Question cannot be empty")
    
    try:
        result = run_rag_pipeline(
            question=request.question,
            limit=request.limit,
            document_id=request.document_id,
            company_id=request.company_id,
            year=request.year
        )
        return result
    
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=404)
    
    