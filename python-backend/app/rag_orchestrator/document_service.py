import fitz
from pathlib import Path
from app.config import UPLOAD_DIR, RENDERED_PAGES_DIR

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

def render_pdf_page_to_image(filename: str, page_number: int) -> str:
    pdf_path = UPLOAD_DIR / filename
    
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")
    
    RENDERED_PAGES_DIR.mkdir(parents=True, exist_ok=True)
    
    document_stem = Path(filename).stem
    document_output_dir = RENDERED_PAGES_DIR / document_stem
    document_output_dir.mkdir(parents=True, exist_ok=True)
    
    image_path = document_output_dir / f"page_{page_number}.png"
    
    if image_path.exists():
        return str(image_path)
    
    doc = fitz.open(pdf_path)
    
    page_index = page_number - 1
    
    if page_index < 0 or page_index >= len(doc):
        doc.close()
        raise ValueError(f"Page number {page_number} is out of range.")
    
    page = doc.load_page(page_index)
    
    pix = page.get_pixmap(matrix=fitz.Matrix(2,2))
    pix.save(image_path)
    
    
    return str(image_path)
    
    