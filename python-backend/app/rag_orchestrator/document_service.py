import fitz
from pathlib import Path

def extract_text_from_pdf(pdf_path: Path) -> list[dict]:
    path = Path(pdf_path)
    
    if not path.exists():
        raise FileNotFoundError(f"File '{pdf_path}' does not exist.")
    
    doc = fitz.open(path)
    pages = []
    
    for page_index in range(len(doc)):
        page = doc.load_page(page_index)
        text = page.get_text("text")
        
        pages.append({
            "page_number": page_index + 1,
            "text": text.strip()
        })
        
    doc.close()
    return pages