from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class HabitBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=255)


class HabitResponse(HabitBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_active: bool
    created_at: datetime


class CompletionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    habit_id: int
    completed_date: date
    status: str
    created_at: datetime
