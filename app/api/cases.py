"""Case API Endpoints"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db import get_db
from app.models import Case
from app.schemas import CaseCreate, CaseResponse, CaseUpdate
from app.dependencies import require_user

router = APIRouter(prefix="/api/cases", tags=["cases"])


@router.get("", response_model=List[CaseResponse])
async def list_cases(
    current_user: dict = Depends(require_user),
    db: AsyncSession = Depends(get_db)
):
    """List all cases for the current user."""
    result = await db.execute(
        select(Case).where(Case.user_id == current_user["user_id"])
    )
    cases = result.scalars().all()
    return cases


@router.post("", response_model=CaseResponse, status_code=status.HTTP_201_CREATED)
async def create_case(
    case_data: CaseCreate,
    current_user: dict = Depends(require_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new case."""
    case = Case(
        user_id=current_user["user_id"],
        **case_data.model_dump()
    )
    db.add(case)
    await db.commit()
    await db.refresh(case)
    return case


@router.get("/{case_id}", response_model=CaseResponse)
async def get_case(
    case_id: str,
    current_user: dict = Depends(require_user),
    db: AsyncSession = Depends(get_db)
):
    """Get a specific case by ID."""
    result = await db.execute(
        select(Case).where(Case.id == case_id, Case.user_id == current_user["user_id"])
    )
    case = result.scalar_one_or_none()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return case


@router.put("/{case_id}", response_model=CaseResponse)
async def update_case(
    case_id: str,
    case_update: CaseUpdate,
    current_user: dict = Depends(require_user),
    db: AsyncSession = Depends(get_db)
):
    """Update a case."""
    result = await db.execute(
        select(Case).where(Case.id == case_id, Case.user_id == current_user["user_id"])
    )
    case = result.scalar_one_or_none()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")

    update_data = case_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(case, field, value)

    await db.commit()
    await db.refresh(case)
    return case


@router.delete("/{case_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_case(
    case_id: str,
    current_user: dict = Depends(require_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete a case."""
    result = await db.execute(
        select(Case).where(Case.id == case_id, Case.user_id == current_user["user_id"])
    )
    case = result.scalar_one_or_none()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")

    await db.delete(case)
    await db.commit()
    return None
