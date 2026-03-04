from __future__ import annotations

from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

VALID_TARGET_DAYS = {"mon", "tue", "wed", "thu", "fri", "sat", "sun"}
TARGET_DAY_ORDER = {
    "mon": 0,
    "tue": 1,
    "wed": 2,
    "thu": 3,
    "fri": 4,
    "sat": 5,
    "sun": 6,
}


def normalize_target_days(target_days: list[str]) -> list[str]:
    normalized = [day.strip().lower() for day in target_days]
    invalid_days = [day for day in normalized if day not in VALID_TARGET_DAYS]
    if invalid_days:
        invalid_csv = ", ".join(sorted(set(invalid_days)))
        raise ValueError(f"Invalid target day(s): {invalid_csv}")

    return sorted(set(normalized), key=lambda day: TARGET_DAY_ORDER[day])


class HabitBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=255)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("name cannot be blank")
        return normalized

    @field_validator("description")
    @classmethod
    def normalize_description(cls, value: str | None) -> str | None:
        if value is None:
            return None

        normalized = value.strip()
        return normalized or None


class HabitCreate(HabitBase):
    target_days: list[str] = Field(default_factory=list)
    is_active: bool = True

    @field_validator("target_days")
    @classmethod
    def validate_target_days(cls, value: list[str]) -> list[str]:
        return normalize_target_days(value)


class HabitUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=255)
    target_days: list[str] | None = None
    is_active: bool | None = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str | None) -> str | None:
        if value is None:
            return None

        normalized = value.strip()
        if not normalized:
            raise ValueError("name cannot be blank")
        return normalized

    @field_validator("description")
    @classmethod
    def normalize_description(cls, value: str | None) -> str | None:
        if value is None:
            return None

        normalized = value.strip()
        return normalized or None

    @field_validator("target_days")
    @classmethod
    def validate_target_days(cls, value: list[str] | None) -> list[str] | None:
        if value is None:
            return None
        return normalize_target_days(value)


class HabitResponse(HabitBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    target_days: list[str] = Field(default_factory=list)
    is_active: bool
    created_at: datetime
    current_streak: int = 0
    longest_streak: int = 0
    completion_rate: float = 0.0


class CompletionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    habit_id: int
    completed_date: date
    status: str
    created_at: datetime


class HabitDetailResponse(HabitResponse):
    completions: list[CompletionResponse] = Field(default_factory=list)


class CompletionUpsertRequest(BaseModel):
    status: Literal["done", "not_done"]


class CompletionListResponse(BaseModel):
    habit_id: int
    from_date: date | None = None
    to_date: date | None = None
    completions: list[CompletionResponse] = Field(default_factory=list)
