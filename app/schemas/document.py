"""Document Schemas"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from app.constants import DocumentType


class DocumentCreate(BaseModel):
    filename: str
    mime_type: str
    size_bytes: int
    document_type: DocumentType = DocumentType.OTHER
    case_id: Optional[str] = None


class DocumentResponse(DocumentCreate):
    id: str
    user_id: str
    original_filename: str
    cloud_path: str
    overlay_id: Optional[str] = None
    extracted_at: Optional[datetime] = None
    extracted_data: Optional[dict] = None
    document_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    uploaded_via: str

    class Config:
        from_attributes = True
