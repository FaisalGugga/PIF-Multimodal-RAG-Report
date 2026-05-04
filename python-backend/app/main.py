import logging

from fastapi import FastAPI
from .routers.ask import router as ask_router
from .routers.upload import router as upload_router
from .routers.index import router as index_router
from .routers.documents import router as documents_router
from .routers.page_image import router as page_image_router
# log from index.py

logging.basicConfig(level=logging.INFO)



app = FastAPI(title="PIF Multimodal RAG Document Analysis")

app.include_router(ask_router)
app.include_router(upload_router)
app.include_router(index_router)
app.include_router(documents_router)
app.include_router(page_image_router)

@app.get('/')
def root():
    return {"message": "Welcome to the PIF Multimodal RAG Document Analysis API!"}

@app.get('/health')
def health():
    return {"status": "OK"}