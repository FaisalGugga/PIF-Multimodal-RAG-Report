from pathlib import Path
import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ..rag_orchestrator.indexing import build_chunks_for_pdf
from ..rag_orchestrator.embeddings import embed_documents
from ..rag_orchestrator.qdrant_service import create_collection, upload_chunks_to_qdrant, delete_document_chunks
from ..rag_orchestrator.document_registry import upsert_document

from ..rag_orchestrator.job_registry import (
    create_indexing_job,
    mark_job_processing,
    mark_job_completed,
    mark_job_failed,
)

from app.config import UPLOAD_DIR, PROJECT_ROOT

router = APIRouter()
logger = logging.getLogger(__name__)
    
class IndexRequest(BaseModel):
    filename: str
    document_id: str
    company_id: str
    year: int
    max_chunks: int | None = None


@router.post("/index")
def index_pdf(request: IndexRequest):
    pdf_path = UPLOAD_DIR / request.filename
    
    
    job = create_indexing_job(request.document_id, request.filename)
    job_id = job["job_id"]
    
    try:
        mark_job_processing(job_id)
        
        if not pdf_path.exists():
            raise HTTPException(detail={"status": "success",
                                        "job": job,
                                        "message": f"File '{request.filename}' not found. PROJECT_ROOT: {PROJECT_ROOT}. UPLOAD_DIR: {UPLOAD_DIR}"
                                        }, status_code=404)
    
        chunks = build_chunks_for_pdf(str(pdf_path), request.document_id, request.company_id, request.year)
        
        if request.max_chunks is not None:
            chunks = chunks[:request.max_chunks]
            
        embedded_chunks = embed_documents(chunks)
        # logger.info(f"Built embedded_chunks: {embedded_chunks}.")
        
        create_collection()
        delete_document_chunks(request.document_id)
        upload_chunks_to_qdrant(embedded_chunks)
        
        
        registered_document = upsert_document({
        "document_id": request.document_id,
        "filename": request.filename,
        "document_name": request.filename,
        "company_id": request.company_id,
        "year": request.year,
        "status": "indexed",
    })
        
        complete_job = mark_job_completed(job_id)
        
        return {
            "status": "success",
            "message": "PDF indexed successfully",
            "job": complete_job,
            "document": registered_document,
        }
        
    except Exception as e:
        failed_job = mark_job_failed(job_id, error_message=str(e))
        
        raise HTTPException(
            status_code=500,
            detail={
                "message": "Document indexing failed",
                "job": failed_job,
                "error": str(e),
            },
        )