from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse

from app.rag_orchestrator.document_service import render_pdf_page_to_image

router = APIRouter()



@router.get("/page-image")
def get_page_image(
    filename: str = Query(..., description="PDF filename stored in uploaded_pdfs"),
    page_number: int = Query(..., ge=1, description="Page number to render the image")
):
    try:
        image_path = render_pdf_page_to_image(filename=filename, page_number=page_number)
        
        return FileResponse(
            path=image_path,
            media_type="image/png",
            filename=f"Page_{page_number}.png"
        )
    
    except FileNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error))
    
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
    
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to render page image: {str(error)}"
        )