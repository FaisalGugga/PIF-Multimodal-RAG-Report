from pathlib import Path
import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ..rag_orchestrator.indexing import build_chunks_for_pdf
from ..rag_orchestrator.embeddings import embed_documents
from ..rag_orchestrator.qdrant_service import create_collection, upload_chunks_to_qdrant

router = APIRouter()
logger = logging.getLogger(__name__)
    
class IndexRequest(BaseModel):
    file_path: str
    max_chunks: int | None = None
    
PROJECT_ROOT = Path(__file__).resolve().parents[3]
UPLOAD_DIR = PROJECT_ROOT / "data" / "uploaded_pdfs"

@router.post("/index")
def index_pdf(request: IndexRequest):
    pdf_path = UPLOAD_DIR / request.file_path
    
    if not pdf_path.exists():
        raise HTTPException(detail=f"File '{request.file_path}' not found. PROJECT_ROOT: {PROJECT_ROOT}. UPLOAD_DIR: {UPLOAD_DIR}", status_code=404)
    
    try:
        chunks = build_chunks_for_pdf(pdf_path)
        
        if request.max_chunks is not None:
            chunks = chunks[:request.max_chunks]
            
        embedded_chunks = embed_documents(chunks)
        # logger.info(f"Built embedded_chunks: {embedded_chunks}.")
        
        create_collection()
        upload_chunks_to_qdrant(embedded_chunks)
        
        return {
            "message": "PDF indexed successfully",
            "file_name": request.file_path,
            "total_chunks": len(chunks),
            "indexed_chunks": len(embedded_chunks)
        }
        
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=404)