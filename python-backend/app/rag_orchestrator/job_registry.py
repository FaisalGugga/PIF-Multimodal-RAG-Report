import logging
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.indexing_job import IndexingJob

logger = logging.getLogger(__name__)


def utc_now() -> datetime:
    return datetime.now(timezone.utc)

def indexing_job_to_dict(job: IndexingJob) -> dict[str, Any]:
    return {
        "id": job.id,
        "job_id": job.job_id,
        "document_id": job.document_id,
        "filename": job.filename,
        "status": job.status,
        "error_message": job.error_message,
        "created_at": job.created_at.isoformat(),
        "updated_at": job.updated_at.isoformat(),
        "started_at": job.started_at.isoformat() if job.started_at else None,
        "completed_at": job.completed_at.isoformat() if job.completed_at else None, 
    }
    
def create_indexing_job(document_id: str, filename: str) -> dict[str, Any]:
    db: Session = SessionLocal()
    
    try: 
        job = IndexingJob(
            job_id=str(uuid4()),
            document_id=document_id,
            filename=filename,
            status="queued",
        )
        
        db.add(job)
        db.commit()
        db.refresh(job)
        
        saved_job = indexing_job_to_dict(job)
        
        logger.info(
            "Indexing job created",
            extra={
                "event": "indexing_job_created",
                "job_id": saved_job["job_id"],
                "document_id": document_id,
                "status": saved_job["status"],
            },
        )
        
        return saved_job
    
    except Exception:
        db.rollback()
        raise
    
    finally:
        db.close()
        
def get_indexing_job(job_id: str) -> dict[str, Any] | None:
    db: Session = SessionLocal()
    
    try: 
        statement = select(IndexingJob).where(
            IndexingJob.job_id == job_id
        )
        
        job = db.execute(statement).scalar_one_or_none()
        
        if job is None:
            return None
        
        return indexing_job_to_dict(job)
    
    finally:
        db.close()
        
def mark_job_processing(job_id: str) -> dict[str, Any] | None:
    db: Session = SessionLocal()
    
    try: 
        statement = select(IndexingJob).where(
            IndexingJob.job_id == job_id
        )
        
        job = db.execute(statement).scalar_one_or_none()
        
        if job is None:
            return None
        
        job.status = "processing"
        job.started_at = utc_now()
        job.error_message = None
        
        db.commit()
        db.refresh(job)
        
        return indexing_job_to_dict(job)
    
    except Exception:
        db.rollback()
        raise
    
    finally:
        db.close()
        
        
def mark_job_completed(job_id: str) -> dict[str, Any] | None:
    db: Session = SessionLocal()
    
    try: 
        statement = select(IndexingJob).where(
            IndexingJob.job_id == job_id
        )
        
        job = db.execute(statement).scalar_one_or_none()
        
        if job is None:
            return None
        
        job.status = "completed"
        job.completed_at = utc_now()
        job.error_message = None
        
        db.commit()
        db.refresh(job)
        
        return indexing_job_to_dict(job)
    
    except Exception:
        db.rollback()
        raise
    
    finally:
        db.close()
        
def mark_job_failed(job_id: str, error_message: str) -> dict[str, Any] | None:
    db: Session = SessionLocal()
    
    try: 
        statement = select(IndexingJob).where(
            IndexingJob.job_id == job_id
        )   
        
        job = db.execute(statement).scalar_one_or_none()
        
        if job is None:
            return None
        
        job.status = "failed"
        job.completed_at = utc_now()
        job.error_message = error_message
        
        db.commit()
        db.refresh(job)
        
        return indexing_job_to_dict(job)
    
    except Exception:
        db.rollback()
        raise
    
    finally:
        db.close()