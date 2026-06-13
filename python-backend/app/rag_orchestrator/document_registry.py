
import json
import logging
from datetime import datetime, timezone

from typing import Any
from sqlalchemy import Select
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.document_record import DocumentRecord

from app.config import DOCUMENT_REGISTRY_FILE

logger = logging.getLogger(__name__)

# def load_documents_registry() -> list[dict]:
#     if not DOCUMENT_REGISTRY_FILE.exists():
#         return []
    
#     with open(DOCUMENT_REGISTRY_FILE, "r", encoding="utf-8") as file:
#         return json.load(file)
    
# def save_documents_registry(documents: list[dict]) -> None:
#     DOCUMENT_REGISTRY_FILE.parent.mkdir(parents=True, exist_ok=True)
    
#     with open(DOCUMENT_REGISTRY_FILE, 'w', encoding="utf-8") as file:
#         json.dump(documents, file, indent=2, ensure_ascii=False)
                
def document_record_to_dict(document: DocumentRecord) -> dict[str, Any]:
    return {
        "id": document.id,
        "document_id": document.document_id,
        "filename": document.filename,
        "document_name": document.document_name,
        "company_id": document.company_id,
        "year": document.year,
        "status": document.status,
        "created_at": document.created_at.isoformat(),
        "updated_at": document.updated_at.isoformat(),
    }
        
def upsert_document(document: dict[str, Any]) -> dict[str, Any]:
    db: Session = SessionLocal()
    
    try:
        document_id = document["document_id"]
        
        statement = Select(DocumentRecord).where(
            DocumentRecord.document_id == document_id
        )
        
        existing_document = db.execute(statement).scalar_one_or_none()
        
        if existing_document is None:
            document_to_save = DocumentRecord(
                document_id=document["document_id"],
                filename=document["filename"],
                document_name=document["document_name"],
                company_id=document["company_id"],
                year=document["year"],
                status=document.get("status", "uploaded"),
            )
        
            db.add(document_to_save)
        else:
            document_to_save = existing_document
            document_to_save.filename = document["filename"]
            document_to_save.document_name = document["document_name"]
            document_to_save.company_id = document["company_id"]
            document_to_save.year = document["year"]
            document_to_save.status = document.get("status", existing_document.status)
            
            
        db.commit()
        db.refresh(document_to_save)
        
        saved_document = document_record_to_dict(document_to_save)
        
        logger.info(
            "Document regisitry updated",
            extra={
                "event": "document_registry_updated",
                "document_id": document_id,
                "status": saved_document.get("status"),
            }
        )
        return saved_document
    
    except Exception as e:
        db.rollback()
        logger.error(
            "Error updating document registry",
            extra={
                "event": "document_registry_update_failed",
                "document_id": document.get("document_id"),
                "error": str(e),
            }
        )
        raise
    
    finally:
        db.close()

def list_registered_documents() -> list[dict[str, Any]]:
    db: Session = SessionLocal()
    
    try: 
        statement = Select(DocumentRecord).order_by(
            DocumentRecord.created_at.desc()
        )
        
        documents = db.execute(statement).scalars().all()
        document_dicts = [document_record_to_dict(doc) for doc in documents]
        
        return document_dicts
    
    finally:
        db.close()

def get_registered_document(document_id: str) -> dict[str, Any] | None:
    db: Session = SessionLocal()

    try: 
        statement = Select(DocumentRecord).where(
            DocumentRecord.document_id == document_id
        )
        
        document = db.execute(statement).scalar_one_or_none()
        
        if document is None:
            return None
        
        return document_record_to_dict(document)
    
    finally:
        db.close()
    
    # documents = load_documents_registry()
    
    # for document in documents:
    #     if document["document"] == document_id:
    #         return document
        
    return None


