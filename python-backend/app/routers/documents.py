from pathlib import Path
from fastapi import APIRouter


router = APIRouter()

PROJECT_ROOT = Path(__file__).resolve().parents[3]
UPLOAD_DIR = PROJECT_ROOT / "data" / "uploaded_pdfs"


@router.get("/documents")
async def list_uploaded_documents():
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    
    documents = []
    
    for file_path in UPLOAD_DIR.iterdir():
        if file_path.is_file() and file_path.suffix.lower() == ".pdf":
            size_mb = file_path.stat().st_size / (1024 * 1024)
            
            documents.append({
                "filename": file_path.name,
                "size_mb": round(size_mb, 2)
            })
            
    return { 
        "total_documents": len(documents),
        "documents": documents
    }