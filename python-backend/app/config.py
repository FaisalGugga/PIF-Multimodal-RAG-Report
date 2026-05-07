import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv('app/config.env')
load_dotenv('app/.env')

PROJECT_ROOT = Path(__file__).resolve().parents[2]

UPLOAD_DIR = PROJECT_ROOT / "data" / "uploaded_pdfs"
RENDERED_PAGES_DIR = PROJECT_ROOT / "data" / "rendered_pages"

LOG_DIR = PROJECT_ROOT / "logs"
LOG_FILE = LOG_DIR / "app.log"

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME")

EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL_NAME = os.getenv("OPENAI_MODEL_NAME")
OPENAI_URL = os.getenv("OPENAI_URL")
