"""Case Schemas"""

from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel

from app.constants import CaseType, CaseStatus, TimelineEventType


class CaseBase(BaseModel):
    title: str
    description: Optional[str] = None
    case_type: CaseType = CaseType.OTHER


class CaseCreate(CaseBase):
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    deposit_amount: Optional[float] = None
    jurisdiction: Optional[str] = None


class CaseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    case_type: Optional[CaseType] = None
    status: Optional[CaseStatus] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    deposit_amount: Optional[float] = None
    deposit_returned: Optional[float] = None
    jurisdiction: Optional[str] = None


class CaseResponse(CaseBase):
    id: str
    user_id: str
    status: CaseStatus
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    deposit_amount: Optional[float] = None
    deposit_returned: Optional[float] = None
    jurisdiction: Optional[str] = None
    extra_data: Optional[dict] = None
    created_at: datetime
    updated_at: datetime
    resolved_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class TimelineEventCreate(BaseModel):
    event_type: TimelineEventType
    event_date: datetime
    description: str
    document_id: Optional[str] = None
    extra_data: Optional[dict] = None


class TimelineEventResponse(TimelineEventCreate):
    id: str
    case_id: str
    source: str
    created_at: datetime

    class Config:
        from_attributes = True
