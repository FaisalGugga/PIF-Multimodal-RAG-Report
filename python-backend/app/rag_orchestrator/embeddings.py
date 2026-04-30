from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

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
        