import logging

from .pipeline import run_rag_pipeline
from .inference import synthesize_multi_document_answer

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

def build_document_evidence_question(question: str) -> str:
    return f"""
        The user is asking a question that may involve comparing multiple documents.

        Original user question:
        {question}

        For this selected document only:
        Find the information in this document that is relevant to the user's question.

        The relevant information may be:
        - a numeric metric or value
        - a fact
        - a statement
        - a policy
        - a strategy
        - a target
        - a change
        - a table row
        - a description
        - any context needed to answer the question

        If numeric data is available and relevant, include the number, unit, year, and label.
        If the answer is text-based, summarize the relevant statement clearly.

        Do not compare against other documents.
        Do not use outside knowledge.
        Answer only from this document.
        """

def ask_multiple_documents(
    question: str,
    document_ids: list[str],
    limit: int = 5
) -> dict:
    logger.info(
        "Multi document ask started",
        extra={
            "event": "ask_multi_document_started",
            "document_ids": document_ids,
            "documents_count": len(document_ids),
            "limit": limit,
        }
    )
    
    document_answers = []
    
    evidence_question = build_document_evidence_question(question)
    
    for document_id in document_ids:
        single_document_result = ask_single_document(
            question=evidence_question,
            document_id=document_id,
            limit=limit
        )
        
        single_document_result["original_question"] = question
        document_answers.append(single_document_result)
        
    final_answer = synthesize_multi_document_answer(
        question=question,
        document_answers=document_answers
    )
    
    response = {
        "mode": "compare",
        "question": question,
        "document_ids": document_ids,
        "final_answer": final_answer,
        "document_answers": document_answers
    }

    logger.info(
        "Multi document ask completed",
        extra={
            "event": "ask_multi_document_completed",
            "document_ids": document_ids,
            "document_answers": len(document_answers),
        }
    )
    
    return response