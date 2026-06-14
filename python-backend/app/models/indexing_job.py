from datetime import datetime, timezone

from sqlalchemy import Integer, String, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column

from .models_helper import utc_now


from app.database import Base

class IndexingJob(Base):
    __tablename__ = "indexing_jobs"
    
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )
    
    job_id: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False
    )
    
    document_id: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False
    )
    
    filename: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )
    
    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="queued",
    )
    
    error_message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now,
        nullable=False,
    )

    started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    
    