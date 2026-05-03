from sentence_transformers import SentenceTransformer

from app.config import EMBEDDING_MODEL_NAME

model = SentenceTransformer(EMBEDDING_MODEL_NAME)

def embed_documents(chunks: list[dict]) -> list[dict]:
    
    texts = []
    for chunk in chunks:
        text = chunk["text"]
        texts.append(text)
        
    embeddings = model.encode(texts)
    
    embedded_chunks = []
    for chunk, embedding in zip(chunks, embeddings):
        embedded_chunks.append({
            **chunk,
            "embedding": embedding.tolist()
        })
        
    return embedded_chunks
        