"""
User and Session Models
"""

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import String, DateTime, ForeignKey, Enum as SQLEnum, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base
from app.constants import UserRole, StorageProvider


class User(Base):
    """User model - storage-based identity."""
    
    __tablename__ = "users"
    
    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    provider: Mapped[StorageProvider] = mapped_column(SQLEnum(StorageProvider), nullable=False)
    role: Mapped[UserRole] = mapped_column(SQLEnum(UserRole), default=UserRole.TENANT)
    storage_user_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    last_seen_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    # Relationships
    sessions: Mapped[list["Session"]] = relationship(back_populates="user", lazy="selectin")
    cases: Mapped[list["Case"]] = relationship(back_populates="user", lazy="selectin")


class Session(Base):
    """Session model - JWT token storage."""
    
    __tablename__ = "sessions"
    
    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=lambda: uuid.uuid4().hex)
    user_id: Mapped[str] = mapped_column(String(32), ForeignKey("users.id"), nullable=False)
    
    # OAuth tokens (encrypted)
    access_token_encrypted: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    refresh_token_encrypted: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Expiry
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    last_used_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    # Relationships
    user: Mapped["User"] = relationship(back_populates="sessions")
