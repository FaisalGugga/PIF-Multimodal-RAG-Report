from fastapi import FastAPI
from ..app.routes.upload import router as upload_router

app = FastAPI(title="PIF Multimodal RAG Document Analysis")

app.include_router(upload_router, prefix="/api")

@app.get('/')
def root():
    return {"message": "Welcome to the PIF Multimodal RAG Document Analysis API!"}

@app.get('/health')
def health():
    return {"status": "OK"}