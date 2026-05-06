from .retrieval import retrieve_relevant_chunks
from .inference import generate_response

from urllib.parse import urlencode


def build_context_from_chunks(chunks: list[dict]) -> str:
    
    context_parts = []
    
    
    for chunk in chunks:
        # document_id = chunk["document_id"]
        company_id = chunk["company_id"]
        year = chunk["year"]
        document_name = chunk["document_name"]
        page_number = chunk["page_number"]
        text = chunk["text"]
        
        context_parts.append(f"Company {company_id} - Year {year}: - Document Name {document_name} - Page {page_number}:\n{text}")
        
    return "\n\n---\n\n".join(context_parts)

def build_page_image_url(document_name: str, page_number: int) -> str:
    query_params = urlencode({
        "filename": document_name,
        "page_number": page_number
    })
    
    return f"/page-image?{query_params}"

def run_rag_pipeline(question: str, limit: int = 5, document_id: str | None = None, company_id: str | None = None, year: int | None = None) -> dict:
    
    retrieved_chunks = retrieve_relevant_chunks(question, limit, document_id=document_id, company_id=company_id, year=year)
    
    context = build_context_from_chunks(retrieved_chunks)
    
    answer = generate_response(question, context)
    
    return {
        "question": question,
        "answer": answer,
        "context": context,
        "sources": [
            {
                "score": chunk["score"],
                "document_id": chunk["document_id"],
                "company_id": chunk["company_id"],
                "year": chunk["year"],
                "document_name": chunk["document_name"],
                "page_number": chunk["page_number"],
                "chunk_id": chunk["chunk_id"],
                "text": chunk["text"],
                "image_url": build_page_image_url(
                    document_name=chunk["document_name"],
                    page_number=chunk["page_number"]
                )
            }
            for chunk in retrieved_chunks
        ]
    }