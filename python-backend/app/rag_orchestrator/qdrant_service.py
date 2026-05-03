import uuid

from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct, Filter, FieldCondition, MatchValue

from app.config import QDRANT_COLLECTION_NAME, QDRANT_URL


COLLECTION_NAME = QDRANT_COLLECTION_NAME

client = QdrantClient(url=QDRANT_URL)

def create_collection(vector_size: int = 384):
    
    collections = client.get_collections().collections
    
    existing_collections = []
    for collection in collections:
        existing_collections.append(collection.name)
        
    if COLLECTION_NAME not in existing_collections:
        client.create_collection(
            collection_name = COLLECTION_NAME,
            vectors_config = VectorParams(
                size = vector_size,
                distance = Distance.COSINE
            )
        )
        
def create_point_id(document_name: str, chunk_id: str) -> str:
    unique_key = f"{document_name}:{chunk_id}"
    return str(uuid.uuid5(uuid.NAMESPACE_URL, unique_key))        

def delete_document_chunks(document_id: str):
    document_filter_document_id = Filter(
        must = [
            FieldCondition(
                key = "document_id",
                match = MatchValue(value=document_id)
            )
        ]
    )
    
    client.delete(
        collection_name = COLLECTION_NAME,
        points_selector = document_filter_document_id
    )
    
def upload_chunks_to_qdrant(embedded_chunks: list[dict]):
    
    points = []
    
    for index, chunk in enumerate(embedded_chunks):
        point_id = create_point_id(
            chunk["document_name"],
            chunk["chunk_id"]
        )
        
        point = PointStruct(
            id = point_id,
            vector = chunk["embedding"],
            payload = {
                "document_id": chunk["document_id"],
                "company_id": chunk["company_id"],
                "year": chunk["year"],
                "document_name": chunk["document_name"],
                "page_number": chunk["page_number"],
                "chunk_id": chunk["chunk_id"],
                "text": chunk["text"]
            }
        )
        
        
        points.append(point)
        

    client.upsert(
        collection_name = COLLECTION_NAME,
        points = points
    )