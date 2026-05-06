import logging

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse

from app.rag_orchestrator.document_service import render_pdf_page_to_image

router = APIRouter()

logger = logging.getLogger(__name__)

@router.get("/page-image")
def get_page_image(
    filename: str = Query(..., description="PDF filename stored in uploaded_pdfs"),
    page_number: int = Query(..., ge=1, description="Page number to render the image")
):
    logger.info(
        "Page image request received",
        extra={
            "event": "page_image_request_received",
            "document_filename": filename,
            "page_number": page_number
        }
                )
    
    try:
        image_path = render_pdf_page_to_image(filename=filename, page_number=page_number)
        
        logger.info(
            "Page image response returned",
            extra={
                "event": "page_image_response_returned",
                "document_filename": filename,
                "page_number": page_number,
                "image_path": image_path
            }
        )
        
        return FileResponse(
            path=image_path,
            media_type="image/png",
            filename=f"Page_{page_number}.png"
        )
    
    except FileNotFoundError as error:
        logger.warning(
            "PDF file not found while rendering page image",
            extra={
                "event": "page_image_pdf_not_found",
                "document_filename": filename,
                "page_number": page_number,
                "error": str(error),
            }
        )
        raise HTTPException(status_code=404, detail=str(error))
    
    except ValueError as error:
        logger.warning(
            "Invalid page number while rendering page image",
            extra={
                "event": "page_image_invalid_page_number",
                "document_filename": filename,
                "page_number": page_number,
                "error": str(error),
            }
        )
        raise HTTPException(status_code=400, detail=str(error))
    
    except Exception as error:
        logger.exception(
            "Unexpected page image rendering error",
            extra={
                "event": "page_image_unexpected_error",
                "document_filename": filename,
                "page_number": page_number,
            }
        )
        raise HTTPException(
            status_code=500,
            detail=f"Failed to render page image: {str(error)}"
        )