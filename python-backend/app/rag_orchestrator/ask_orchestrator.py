import logging

from .pipeline import run_rag_pipeline
from .inference import synthesize_multi_document_answer

logger = logging.getLogger(__name__)


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


def build_document_answer_title(document_id: str, sources: list[dict]) -> str:
    if sources:
        company = sources[0].get("company")
        year = sources[0].get("year")

        if company and year:
            return f"{company} {year} Analysis"
        
        if year:
            return f"{year} Document Analysis"
    
    return f"{document_id} Analysis"


def get_evidance_status(answer: str | None, sources: list[dict]) -> str:
    if not sources:
        return "not_found"
    if not answer:
        return "not_found"

    not_found_phrases = [
        "could not find",
        "not found",
        "not available",
        "does not contain",
        "provided context does not",
        "cannot determine",
        "insufficient information",
    ]
    
    normalized_answer = answer.lower()
    
    for phrase in not_found_phrases:
        if phrase in normalized_answer:
            return "not_found"
        
    return "found"


def format_document_answer_for_compare(
    single_document_result: dict,
    original_question: str,
) -> dict:
    sources = single_document_result.get("sources")
    document_id = single_document_result.get("document_id")
    answer = single_document_result.get("answer")
    
    evidence_status = get_evidance_status(answer=answer, sources=sources)


    return {
        "document_id": document_id,
        "title": build_document_answer_title(document_id, sources),
        "question": original_question,
        "evidence_status": evidence_status,
        "answer": answer,
        "sources": sources,
    }


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
        
        formatted_document_answer = format_document_answer_for_compare(
            single_document_result=single_document_result, 
            original_question=question
        )
        
        # single_document_result["original_question"] = question
        document_answers.append(formatted_document_answer)
        
        logger.info(
            "Compare document evidence status",
            extra={
                "event": "compare_document_evidence_status",
                "document_id": formatted_document_answer["document_id"],
                "title": formatted_document_answer["title"],
                "evidence_status": formatted_document_answer["evidence_status"],
                "sources_count": len(formatted_document_answer["sources"]),
            }
        )
    
    
    logger.info(
    "Comparison synthesis started",
    extra={
        "event": "comparison_synthesis_started",
        "document_ids": document_ids,
        "documents_count": len(document_answers),
        }
    )
        
        
    final_answer = synthesize_multi_document_answer(
        question=question,
        document_answers=document_answers
    )
    
    logger.info(
    "Comparison synthesis completed",
    extra={
        "event": "comparison_synthesis_completed",
        "document_ids": document_ids,
        "documents_count": len(document_answers),
        }
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