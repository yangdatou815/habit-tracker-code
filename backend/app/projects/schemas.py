from __future__ import annotations

from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, Field


class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    category: str = Field(default="其他", max_length=50)
    sort_order: int = Field(default=0)


class ProjectUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    category: str | None = Field(default=None, max_length=50)
    sort_order: int | None = None
    is_active: bool | None = None


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
    checkin_id: int | None = None


class DayCheckinSummary(BaseModel):
    date: date
    items: list[TodayCheckinItem]
    total: int
    done_count: int


class HistoryDaySummary(BaseModel):
    date: date
    total: int
    done_count: int
