import uuid

from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct

COLLECTION_NAME = 'pif_reports_collection'

client = QdrantClient("localhost", port=6333)

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