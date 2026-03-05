from __future__ import annotations

from datetime import date

from pydantic import BaseModel


class StatsOverviewResponse(BaseModel):
    from_date: date
    to_date: date
    total_habits: int
    completed_today: int
    total_today: int
    completion_rate: float
