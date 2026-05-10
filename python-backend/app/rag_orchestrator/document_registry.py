
import json
import logging
from datetime import datetime, timezone

from app.config import DOCUMENT_REGISTRY_FILE

logger = logging.getLogger(__name__)

def load_documents_registry() -> list[dict]:
    if not DOCUMENT_REGISTRY_FILE.exists():
        return []
    
    with open(DOCUMENT_REGISTRY_FILE, "r", encoding="utf-8") as file:
        return json.load(file)
    
def save_documents_registry(documents: list[dict]) -> None:
    DOCUMENT_REGISTRY_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    with open(DOCUMENT_REGISTRY_FILE, 'w', encoding="utf-8") as file:
        json.dump(documents, file, indent=2, ensure_ascii=False)
        
        
def upsert_document(document: dict) -> dict:
    documents = load_documents_registry()
    
    now = datetime.now().astimezone().isoformat()
    
    document_id = document["document_id"]
    
    existing_index = None
    
    for index, existing_document in enumerate(documents):
        if existing_document["document_id"] == document_id:
            existing_index = index
            break
        
    if existing_index is None:
        document_to_save = {
            **document,
            "created_at": now,
            "updated_at": now,
        }
        documents.append(document_to_save)
        
    else:
        old_document = documents[existing_index]
        document_to_save = {
            **old_document,
            **document,
            "created_at": old_document.get("created_at", now),
            "updated_at": now,
        }
        documents[existing_index] = document_to_save
    
    save_documents_registry(documents=documents)
    
    logger.info(
        "Document registry updated",
        extra={
            "event": "document_registry_updated",
            "document_id": document_id,
            "status": document_to_save.get("status"),
        }
    )
    
    return document_to_save

def list_registered_documents() -> list[dict]:
    return load_documents_registry()

def get_registered_document(document_id: str) -> dict | None:
    documents = load_documents_registry()
    
    for document in documents:
        if document["document"] == document_id:
            return document
        
    return None