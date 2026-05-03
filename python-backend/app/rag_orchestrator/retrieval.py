from .embeddings import model
from .qdrant_service import client, COLLECTION_NAME

from qdrant_client.models import Filter, FieldCondition, MatchValue

def build_qdrant_filter(
    document_id: str | None = None,
    company_id: str | None = None,
    year: int | None = None
) -> dict:
    
    conditions = []
    
    if document_id:
        conditions.append(
            FieldCondition(
                key = "document_id",
                match = MatchValue(value=document_id)
            )
        )
        
    if company_id:
        conditions.append(
            FieldCondition(
                key = "company_id",
                match = MatchValue(value=company_id)
            )
        )
    
    if year:
        conditions.append(
            FieldCondition(
                key = "year",
                match = MatchValue(value=year)
            )
        )
        
    if not conditions:
        return None
    
    return Filter(must=conditions)



def retrieve_relevant_chunks(question: str, limit: int = 5, document_id: str | None = None, company_id: str | None = None, year: int | None = None) -> list[dict]:
    
    question_embedding = model.encode(question).tolist()
    
    qdrant_filter = build_qdrant_filter(document_id=document_id, company_id=company_id, year=year)
    
    result = client.query_points(
        collection_name=COLLECTION_NAME,
        query_filter=qdrant_filter,
        query=question_embedding,
        limit=limit,
        with_payload=True
    )
    
    
    retrieved_chunks = []
    
    for point in result.points:
        retrieved_chunks.append({
            "score": point.score,
            "document_id": point.payload["document_id"],
            "company_id": point.payload["company_id"],
            "year": point.payload["year"],
            "document_name": point.payload["document_name"],
            "page_number": point.payload["page_number"],
            "chunk_id": point.payload["chunk_id"],
            "text": point.payload["text"]
        })
        
    return retrieved_chunks