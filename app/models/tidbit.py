"""
Tidbit Model - Tenant rights news/education content
"""

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import String, DateTime, Integer, Enum as SQLEnum, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base
from app.constants import TidbitCategory


class Tidbit(Base):
    """Tidbit - bite-sized tenant rights information."""
    
    __tablename__ = "tidbits"
    
    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=lambda: uuid.uuid4().hex[:16])
    
    # Content
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)  # 1-2 sentences
    extended_content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # Full article (optional)
    
    # Categorization
    category: Mapped[TidbitCategory] = mapped_column(SQLEnum(TidbitCategory), default=TidbitCategory.TIP)
    jurisdiction: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)  # e.g., "NYC", "CA", "Germany"
    tags: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)  # Comma-separated
    
    # Source
    source_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    source_name: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    
    # Publishing
    published_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    featured: Mapped[bool] = mapped_column(Boolean, default=False)  # Show on dashboard
    
    # Stats
    view_count: Mapped[int] = mapped_column(Integer, default=0)
    
    # Admin
    created_by: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
