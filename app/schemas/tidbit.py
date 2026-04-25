"""Tidbit Schemas"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from app.constants import TidbitCategory


class TidbitCreate(BaseModel):
    title: str
    content: str
    extended_content: Optional[str] = None
    category: TidbitCategory = TidbitCategory.TIP
    jurisdiction: Optional[str] = None
    tags: Optional[str] = None
    source_url: Optional[str] = None
    source_name: Optional[str] = None


class TidbitResponse(TidbitCreate):
    id: str
    published_at: datetime
    active: bool
    featured: bool
    view_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
