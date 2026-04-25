"""
Document Model - File metadata and overlays
"""

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import String, DateTime, Integer, ForeignKey, Enum as SQLEnum, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.user import Base
from app.constants import DocumentType


class Document(Base):
    """Document model - file metadata in user's cloud storage."""
    
    __tablename__ = "documents"
    
    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=lambda: uuid.uuid4().hex[:16])
    user_id: Mapped[str] = mapped_column(String(32), ForeignKey("users.id"), nullable=False)
    case_id: Mapped[Optional[str]] = mapped_column(String(32), ForeignKey("cases.id"), nullable=True)
    
    # File details
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    original_filename: Mapped[str] = mapped_column(String(255), nullable=False)
    mime_type: Mapped[str] = mapped_column(String(100), nullable=False)
    size_bytes: Mapped[int] = mapped_column(Integer, nullable=False)
    
    # Document classification
    document_type: Mapped[DocumentType] = mapped_column(SQLEnum(DocumentType), default=DocumentType.OTHER)
    
    # Cloud storage path (relative to vault)
    cloud_path: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Overlay data (encrypted in cloud, metadata here)
    overlay_id: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    
    # Extraction status
    extracted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    extracted_data: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    
    # Document dates (extracted or manual)
    document_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Source info
    uploaded_via: Mapped[str] = mapped_column(String(50), default="web")  # web, mobile, email
