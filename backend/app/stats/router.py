from __future__ import annotations

from typing import Optional

from datetime import date, datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.stats.schemas import StatsOverviewResponse
from app.stats.service import compute_stats_overview

router = APIRouter(prefix="/stats", tags=["stats"])


@router.get("/overview", response_model=StatsOverviewResponse)
def get_stats_overview(
    from_date: Optional[date] = Query(default=None, alias="from"),
    to_date: Optional[date] = Query(default=None, alias="to"),
    db: Session = Depends(get_db),
) -> StatsOverviewResponse:
    today = datetime.now(timezone.utc).date()

    if from_date is None:
        from_date = today - timedelta(days=6)
    if to_date is None:
        to_date = today

    if from_date > to_date:
        raise HTTPException(
            status_code=422,
            detail="from_date cannot be after to_date",
        )

    return compute_stats_overview(db, from_date=from_date, to_date=to_date)
