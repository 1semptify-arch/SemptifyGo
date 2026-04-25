"""User Schemas"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from app.constants import UserRole, StorageProvider


class UserCreate(BaseModel):
    id: str
    email: Optional[str] = None
    provider: StorageProvider
    storage_user_id: Optional[str] = None


class UserResponse(BaseModel):
    id: str
    email: Optional[str] = None
    provider: StorageProvider
    role: UserRole
    storage_user_id: Optional[str] = None
    created_at: datetime
    last_seen_at: Optional[datetime] = None

    class Config:
        from_attributes = True
