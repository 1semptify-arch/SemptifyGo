"""
Case and Timeline Event Models
"""

import uuid
from datetime import datetime, date
from typing import Optional

from sqlalchemy import String, DateTime, Date, ForeignKey, Enum as SQLEnum, Text, Numeric, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.user import Base
from app.constants import CaseType, CaseStatus, TimelineEventType


class Case(Base):
    """Case model - tenant case/housing issue."""
    
    __tablename__ = "cases"
    
    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=lambda: uuid.uuid4().hex[:16])
    user_id: Mapped[str] = mapped_column(String(32), ForeignKey("users.id"), nullable=False)
    
    # Case details
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    case_type: Mapped[CaseType] = mapped_column(SQLEnum(CaseType), default=CaseType.OTHER)
    status: Mapped[CaseStatus] = mapped_column(SQLEnum(CaseStatus), default=CaseStatus.ACTIVE)
    
    # Tenancy dates
    start_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    
    # Deposit tracking
    deposit_amount: Mapped[Optional[float]] = mapped_column(Numeric(10, 2), nullable=True)
    deposit_returned: Mapped[Optional[float]] = mapped_column(Numeric(10, 2), nullable=True)
    
    # Metadata
    jurisdiction: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)  # State/city
    metadata: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    resolved_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    # Relationships
    user: Mapped["User"] = relationship(back_populates="cases")
    timeline_events: Mapped[list["TimelineEvent"]] = relationship(back_populates="case", lazy="selectin")


class TimelineEvent(Base):
    """Timeline event - chronological record of case activity."""
    
    __tablename__ = "timeline_events"
    
    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=lambda: uuid.uuid4().hex[:16])
    case_id: Mapped[str] = mapped_column(String(32), ForeignKey("cases.id"), nullable=False)
    
    # Event details
    event_type: Mapped[TimelineEventType] = mapped_column(SQLEnum(TimelineEventType), nullable=False)
    event_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Optional document link
    document_id: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    
    # Source (auto-extracted, manual, etc.)
    source: Mapped[str] = mapped_column(String(50), default="manual")
    metadata: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationships
    case: Mapped["Case"] = relationship(back_populates="timeline_events")
