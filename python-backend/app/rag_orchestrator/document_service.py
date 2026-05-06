import fitz
import logging
from pathlib import Path
from app.config import UPLOAD_DIR, RENDERED_PAGES_DIR

logger = logging.getLogger(__name__)

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
    
    logger.info(
        "Resolved PDF path for page rendering",
        extra={
            "event": "pdf_path_resolved",
            "document_filename": filename,
            "page_number": page_number,
            "upload_dir": str(UPLOAD_DIR),
            "pdf_path": str(pdf_path),
            "pdf_exists": pdf_path.exists(),
        }
    )
    
    if not pdf_path.exists():
        logger.warning(
            "PDF file does not exist",
            extra={
                "event": "pdf_file_missing",
                "document_filename": filename,
                "page_number": page_number,
                "pdf_path": str(pdf_path),
            }
        )
        raise FileNotFoundError(f"PDF not found: {pdf_path}")
    
    RENDERED_PAGES_DIR.mkdir(parents=True, exist_ok=True)
    
    document_stem = Path(filename).stem
    document_output_dir = RENDERED_PAGES_DIR / document_stem
    document_output_dir.mkdir(parents=True, exist_ok=True)
    
    image_path = document_output_dir / f"page_{page_number}.png"
    
    logger.info(
        "Resolved rendered image path",
        extra={
            "event": "rendered_image_path_resolved",
            "document_filename": filename,
            "page_number": page_number,
            "rendered_pages_dir": str(RENDERED_PAGES_DIR),
            "document_output_dir": str(document_output_dir),
            "image_path": str(image_path),
            "image_exists": image_path.exists(),
        }
    )
    
    # if the image exists already, return the path
    if image_path.exists():
        return str(image_path)
    
    doc = fitz.open(pdf_path)
    
    page_index = page_number - 1
    total_pages = len(doc)
    
    logger.info(
        "Opened PDF for page rendering",
        extra={
            "event": "pdf_opened_for_rendering",
            "document_filename": filename,
            "page_number": page_number,
            "page_index": page_index,
            "total_pages": total_pages,
        }
    )
    
    if page_index < 0 or page_index >= total_pages:
        doc.close()
        
        logger.warning(
            "Requested page number is out of range",
            extra={
                "event": "page_number_out_of_range",
                "document_filename": filename,
                "page_number": page_number,
                "page_index": page_index,
                "total_pages": total_pages,
            }
        )
        
        raise ValueError(f"Page number {page_number} is out of range.")
    
    page = doc.load_page(page_index)
    
    pix = page.get_pixmap(matrix=fitz.Matrix(2,2))
    pix.save(image_path)
    
    logger.info(
        "PDF page rendered successfully",
        extra={
            "event": "pdf_page_rendered_successfully",
            "document_filename": filename,
            "page_number": page_number,
            "page_index": page_index,
            "image_path": str(image_path),
        }
    )
    
    return str(image_path)
    
    