from __future__ import annotations

from datetime import date, datetime
from typing import List, Literal, Optional

from pydantic import BaseModel, Field


class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    category: str = Field(default="其他", max_length=50)
    sort_order: int = Field(default=0)


class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    category: Optional[str] = Field(default=None, max_length=50)
    sort_order: Optional[int] = None
    is_active: Optional[bool] = None


class ProjectResponse(BaseModel):
    id: int
    name: str
    category: str
    sort_order: int
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class CheckinToggle(BaseModel):
    status: Literal["done", "not_done"]


class CheckinResponse(BaseModel):
    id: int
    project_id: int
    checkin_date: date
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}


class TodayCheckinItem(BaseModel):
    project_id: int
    project_name: str
    category: str
    sort_order: int
    status: str  # "done" or "not_done"
    checkin_id: Optional[int] = None


class DayCheckinSummary(BaseModel):
    date: date
    items: List[TodayCheckinItem]
    total: int
    done_count: int


class HistoryDaySummary(BaseModel):
    date: date
    total: int
    done_count: int
