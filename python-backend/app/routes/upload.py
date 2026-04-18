from fastapi import APIRouter, File, UploadFile, HTTPException
from pathlib import Path


router =APIRouter()

BASE_DIR = Path(__file__).resolve().parents[3]
UPLOAD_DIR = BASE_DIR / "data" / "uploaded_pdfs"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")
    
    file_location = UPLOAD_DIR / file.filename
    
    
    contents = await file.read()
    with open(file_location, "wb") as f:
        f.write(contents)
        
        
    return {"message": f"File '{file.filename}' uploaded successfully.", "file_path": str(file_location)}