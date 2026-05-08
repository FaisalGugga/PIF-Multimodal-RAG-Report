import logging

from .pipeline import run_rag_pipeline

logger = logging.getLogger(__name__)

def ask_single_document(
    question: str,
    document_id: str,
    limit: int = 5
) -> dict:
    logger.info(
        "Single document ask started",
        extra={
            "event": "ask_single_document_started",
            "document_id": document_id,
            "limit": limit,
        }
    )
    
    rag_result = run_rag_pipeline(
        question, 
        limit=limit, 
        document_id=document_id
        )

    response = {
        "mode": "single",
        "question": question,
        "document_id": document_id,
        "answer": rag_result["answer"],
        "sources": rag_result["sources"]
    }

    logger.info(
        "Single document ask completed",
        extra={
            "event": "ask_single_document_completed",
            "document_id": document_id,
            "sources_count": len(response["sources"]),
        }
    )
    
    return response