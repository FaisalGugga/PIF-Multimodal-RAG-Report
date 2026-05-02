from .embeddings import model
from .qdrant_service import client, COLLECTION_NAME


def retrieve_relevant_chunks(question: str, limit: int = 5) -> list[dict]:
    
    question_embedding = model.encode(question).tolist()
    
    result = client.query_points(
        collection_name=COLLECTION_NAME,
        query=question_embedding,
        limit=limit,
        with_payload=True
    )
    
    
    retrieved_chunks = []
    
    for point in result.points:
        retrieved_chunks.append({
            "score": point.score,
            "document_name": point.payload["document_name"],
            "page_number": point.payload["page_number"],
            "chunk_id": point.payload["chunk_id"],
            "text": point.payload["text"]
        })
        
    return retrieved_chunks