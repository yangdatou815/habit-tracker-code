from __future__ import annotations

from datetime import date, datetime, timezone
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.projects.schemas import (
    CheckinResponse,
    CheckinToggle,
    DayCheckinSummary,
    HistoryDaySummary,
    ProjectCreate,
    ProjectResponse,
    ProjectUpdate,
)
from app.projects.service import (
    create_project,
    delete_project,
    get_date_checkins,
    get_history,
    get_today_checkins,
    list_projects,
    toggle_checkin,
    update_project,
)

router = APIRouter(tags=["projects"])

# ── Project CRUD ──────────────────────────────────────────────

projects_router = APIRouter(prefix="/projects")


@projects_router.get("", response_model=List[ProjectResponse])
def get_projects(
    is_active: Optional[bool] = Query(default=None),
    db: Session = Depends(get_db),
) -> List[ProjectResponse]:
    return list_projects(db, is_active=is_active)


@projects_router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project_endpoint(
    payload: ProjectCreate,
    db: Session = Depends(get_db),
) -> ProjectResponse:
    return create_project(db, payload)


@projects_router.patch("/{project_id}", response_model=ProjectResponse)
def update_project_endpoint(
    project_id: int,
    payload: ProjectUpdate,
    db: Session = Depends(get_db),
) -> ProjectResponse:
    try:
        return update_project(db, project_id, payload)
    except ValueError:
        raise HTTPException(status_code=404, detail="Project not found")


@projects_router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project_endpoint(
    project_id: int,
    db: Session = Depends(get_db),
) -> Response:
    try:
        delete_project(db, project_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Project not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# ── Checkin endpoints ─────────────────────────────────────────

checkins_router = APIRouter(prefix="/checkins")


@checkins_router.put("/{project_id}/{checkin_date}", response_model=CheckinResponse)
def toggle_checkin_endpoint(
    project_id: int,
    checkin_date: date,
    payload: CheckinToggle,
    db: Session = Depends(get_db),
) -> CheckinResponse:
    try:
        checkin = toggle_checkin(db, project_id, checkin_date, payload.status)
    except ValueError:
        raise HTTPException(status_code=404, detail="Project not found")
    return CheckinResponse.model_validate(checkin)


@checkins_router.get("/today", response_model=DayCheckinSummary)
def today_checkins_endpoint(
    db: Session = Depends(get_db),
) -> DayCheckinSummary:
    today = datetime.now(timezone.utc).date()
    return get_today_checkins(db, today)


@checkins_router.get("/date/{target_date}", response_model=DayCheckinSummary)
def date_checkins_endpoint(
    target_date: date,
    db: Session = Depends(get_db),
) -> DayCheckinSummary:
    return get_date_checkins(db, target_date)


@checkins_router.get("/history", response_model=List[HistoryDaySummary])
def history_endpoint(
    from_date: date = Query(...),
    to_date: date = Query(...),
    db: Session = Depends(get_db),
) -> List[HistoryDaySummary]:
    if from_date > to_date:
        raise HTTPException(status_code=422, detail="from_date must be <= to_date")
    return get_history(db, from_date, to_date)


router.include_router(projects_router)
router.include_router(checkins_router)
