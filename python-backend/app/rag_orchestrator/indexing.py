from app.rag_orchestrator.document_service import extract_text_from_pdf
from app.utils.chunking import chunk_text

def build_chunks_for_pdf(pdf_path: str) -> list[dict]:
    pages = extract_text_from_pdf(pdf_path)
    all_chunks = []
    
    for page in pages:
        page_number = page["page_number"]
        page_text = page["text"]
        
        chunks = chunk_text(page_text)
        
        for chunk_index, chunk in enumerate(chunks):
            all_chunks.append({
                "page_number": page_number,
                "chunk_id": f"{page_number}_{chunk_index}",
                "text": chunk
            })
            
    return all_chunks