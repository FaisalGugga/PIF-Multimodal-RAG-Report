import logging
from .logging_config import setup_logging

from fastapi import FastAPI
from .routers.ask import router as ask_router
from .routers.upload import router as upload_router
from .routers.index import router as index_router
from .routers.documents import router as documents_router
from .routers.page_image import router as page_image_router

from .request_id_middleware import RequestIdMiddleware


# log from index.py

setup_logging()

logger = logging.getLogger(__name__)

app = FastAPI(title="PIF Multimodal RAG Document Analysis")

app.add_middleware(RequestIdMiddleware)

app.include_router(ask_router)
app.include_router(upload_router)
app.include_router(index_router)
app.include_router(documents_router)
app.include_router(page_image_router)

@app.get('/')
def root():
    logger.info(
        "Root endpoint called",
        extra={"event": "root_endpoint_called"}
    )
    return {"message": "Welcome to the PIF Multimodal RAG Document Analysis API!"}

@app.get('/health')
def health():
    logger.info(
        "Health check called",
        extra={"event": "health_check_called"}
    )
    return {"status": "OK"}