def chunk_text(text: str, chunk_size: int = 100, overlap: int = 40) -> list[str]:
    if not text.strip():
        return []
    
    words = text.split()
    
    if len(words) <= chunk_size:
        return [" ".join(words)]
    
    chunks = []
    start = 0
    text_length = len(words)
    
    while start < text_length:
        end = start + chunk_size
        
        chunk_words = words[start:end]
        
        chunk = " ".join(chunk_words).strip()
        
        if chunk:
            chunks.append(chunk)
            
        start += chunk_size - overlap
        
    return chunks