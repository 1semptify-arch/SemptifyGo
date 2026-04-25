"""Document API Endpoints"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db import get_db
from app.models import Document
from app.schemas import DocumentCreate, DocumentResponse
from app.dependencies import require_user

router = APIRouter(prefix="/api/documents", tags=["documents"])


@router.get("", response_model=List[DocumentResponse])
async def list_documents(
    case_id: str = None,
    current_user: dict = Depends(require_user),
    db: AsyncSession = Depends(get_db)
):
    """List documents for the current user."""
    query = select(Document).where(Document.user_id == current_user["user_id"])
    
    if case_id:
        query = query.where(Document.case_id == case_id)
    
    query = query.order_by(Document.created_at.desc())
    
    result = await db.execute(query)
    documents = result.scalars().all()
    return documents


@router.post("", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def create_document(
    document_data: DocumentCreate,
    current_user: dict = Depends(require_user),
    db: AsyncSession = Depends(get_db)
):
    """Create document metadata record."""
    document = Document(
        user_id=current_user["user_id"],
        original_filename=document_data.filename,
        **document_data.model_dump()
    )
    db.add(document)
    await db.commit()
    await db.refresh(document)
    return document


@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: str,
    current_user: dict = Depends(require_user),
    db: AsyncSession = Depends(get_db)
):
    """Get a specific document by ID."""
    result = await db.execute(
        select(Document).where(
            Document.id == document_id,
            Document.user_id == current_user["user_id"]
        )
    )
    document = result.scalar_one_or_none()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(
    document_id: str,
    current_user: dict = Depends(require_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete a document."""
    result = await db.execute(
        select(Document).where(
            Document.id == document_id,
            Document.user_id == current_user["user_id"]
        )
    )
    document = result.scalar_one_or_none()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    await db.delete(document)
    await db.commit()
    return None
