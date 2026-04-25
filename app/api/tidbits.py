"""Tidbit API Endpoints"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db import get_db
from app.models import Tidbit
from app.schemas import TidbitResponse
from app.dependencies import get_current_user_optional

router = APIRouter(prefix="/api/tidbits", tags=["tidbits"])


@router.get("", response_model=List[TidbitResponse])
async def list_tidbits(
    limit: int = 10,
    featured: bool = False,
    db: AsyncSession = Depends(get_db)
):
    """List tenant rights tidbits."""
    query = select(Tidbit).where(Tidbit.active == True)
    
    if featured:
        query = query.where(Tidbit.featured == True)
    
    query = query.order_by(Tidbit.published_at.desc()).limit(limit)
    
    result = await db.execute(query)
    tidbits = result.scalars().all()
    return tidbits


@router.get("/{tidbit_id}", response_model=TidbitResponse)
async def get_tidbit(
    tidbit_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get a specific tidbit by ID."""
    result = await db.execute(
        select(Tidbit).where(Tidbit.id == tidbit_id, Tidbit.active == True)
    )
    tidbit = result.scalar_one_or_none()
    if not tidbit:
        raise HTTPException(status_code=404, detail="Tidbit not found")
    
    # Increment view count
    tidbit.view_count += 1
    await db.commit()
    
    return tidbit
