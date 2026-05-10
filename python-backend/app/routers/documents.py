from pathlib import Path
from fastapi import APIRouter

from app.rag_orchestrator.document_registry import list_registered_documents

# from app.config import UPLOAD_DIR

router = APIRouter()


@router.get("/documents")
def get_documents():
#     UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    
#     documents = []
    
#     for file_path in UPLOAD_DIR.iterdir():
#         if file_path.is_file() and file_path.suffix.lower() == ".pdf":
#             size_mb = file_path.stat().st_size / (1024 * 1024)
            
#             documents.append({
#                 "filename": file_path.name,
#                 "size_mb": round(size_mb, 2)
#             })

    documents = list_registered_documents()     
    
    return { 
        "total_documents": len(documents),
        "documents": documents
    }

