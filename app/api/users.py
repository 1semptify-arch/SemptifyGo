"""User API Endpoints"""

from fastapi import APIRouter, Depends

from app.schemas import UserResponse
from app.dependencies import require_user

router = APIRouter(prefix="/api", tags=["users"])


@router.get("/me", response_model=dict)
async def get_me(
    current_user: dict = Depends(require_user),
):
    """Get current user info."""
    return current_user
