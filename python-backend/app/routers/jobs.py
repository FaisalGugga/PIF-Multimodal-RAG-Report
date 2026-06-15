
from fastapi import APIRouter, HTTPException

from app.rag_orchestrator.job_registry import get_indexing_job

router = APIRouter()

@router.get("/jobs/{job_id}")
def get_job_status(job_id: str):
    job = get_indexing_job(job_id)
    
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return job