from .retrieval import retrieve_relevant_chunks
from .inference import generate_response


def build_context_from_chunks(chunks: list[dict]) -> str:
    
    context_parts = []
    
    
    for chunk in chunks:
        page_number = chunk["page_number"]
        text = chunk["text"]
        
        context_parts.append(f"Page {page_number}:\n{text}")
        
    return "\n\n---\n\n".join(context_parts)

def run_rag_pipeline(question: str, limit: int = 5) -> dict:
    retrieved_chunks = retrieve_relevant_chunks(question, limit)
    
    context = build_context_from_chunks(retrieved_chunks)
    
    answer = generate_response(question, context)
    
    return {
        "question": question,
        "context": context,
        "answer": answer,
        "sources": [
            {
                "score": chunk["score"],
                "page_number": chunk["page_number"],
                "chunk_id": chunk["chunk_id"],
                "text": chunk["text"]
            }
            for chunk in retrieved_chunks
        ]
    }