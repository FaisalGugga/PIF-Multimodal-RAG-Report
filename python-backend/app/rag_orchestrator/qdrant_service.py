from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct

COLLECTION_NAME = 'document_chunks'

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
        
    
def upload_chunks_to_qdrant(embedded_chunks: list[dict]):
    
    points = []
    for index, chunk in enumerate(embedded_chunks):
        point = PointStruct(
            id = index,
            vector = chunk["embedding"],
            payload = {
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