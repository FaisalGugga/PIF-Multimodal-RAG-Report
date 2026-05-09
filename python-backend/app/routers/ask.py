from typing import Literal

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.rag_orchestrator.ask_orchestrator import ask_single_document, ask_multiple_documents

router = APIRouter()

class AskRequest(BaseModel):
    question: str
    limit: int = 5
    mode: Literal["single","compare"] = "single"
    document_ids: list[str] = Field(default_factory=list)


@router.post("/ask")
def ask(request: AskRequest):
    if not request.question.strip():
        raise HTTPException(detail="Question cannot be empty", status_code=400)
    
    try:
        if request.mode == "single":
            if len(request.document_ids) != 1:
                raise HTTPException(status_code=400, detail="Single mode requires one document_id")
            
            document_id = request.document_ids[0]
            
            try:
                return ask_single_document(
                    question=request.question,
                    document_id=document_id,
                    limit=request.limit
                )
            
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to ask single document: {str(e)}")
            
    
        if request.mode == "compare":
            if len(request.document_ids) < 2:
                raise HTTPException(status_code=400, detail="Compare mode requires at least two document_ids")

            try:
                return ask_multiple_documents(
                    question=request.question,
                    document_ids=request.document_ids,
                    limit=request.limit
                )

            except Exception as error:
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to compare documents: {str(error)}"
                )
        
        # result = run_rag_pipeline(
        #     question=request.question,
        #     limit=request.limit,
        #     document_id=request.document_id,
        #     company_id=request.company_id,
        #     year=request.year
        # )
    
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=404)
    
    