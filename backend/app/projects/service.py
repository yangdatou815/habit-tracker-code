from __future__ import annotations

from datetime import date, timedelta

from sqlalchemy.orm import Session

from app.projects.models import Checkin, Project
from app.projects.schemas import (
    DayCheckinSummary,
    HistoryDaySummary,
    ProjectCreate,
    ProjectResponse,
    ProjectUpdate,
    TodayCheckinItem,
)


def list_projects(db: Session, is_active: bool | None = None) -> list[ProjectResponse]:
    query = db.query(Project).order_by(Project.sort_order.asc(), Project.id.asc())
    if is_active is not None:
        query = query.filter(Project.is_active == is_active)
    return [ProjectResponse.model_validate(p) for p in query.all()]


def create_project(db: Session, data: ProjectCreate) -> ProjectResponse:
    project = Project(
        name=data.name,
        category=data.category,
        sort_order=data.sort_order,
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return ProjectResponse.model_validate(project)


def update_project(db: Session, project_id: int, data: ProjectUpdate) -> ProjectResponse:
    project = db.query(Project).filter(Project.id == project_id).first()
    if project is None:
        raise ValueError("Project not found")
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(project, key, value)
    db.commit()
    db.refresh(project)
    return ProjectResponse.model_validate(project)


def delete_project(db: Session, project_id: int) -> None:
    project = db.query(Project).filter(Project.id == project_id).first()
    if project is None:
        raise ValueError("Project not found")
    db.delete(project)
    db.commit()


def toggle_checkin(db: Session, project_id: int, checkin_date: date, status: str) -> Checkin:
    project = db.query(Project).filter(Project.id == project_id).first()
    if project is None:
        raise ValueError("Project not found")
    checkin = (
        db.query(Checkin)
        .filter(Checkin.project_id == project_id, Checkin.checkin_date == checkin_date)
        .first()
    )
    if checkin is None:
        checkin = Checkin(
            project_id=project_id,
            checkin_date=checkin_date,
            status=status,
        )
        db.add(checkin)
    else:
        checkin.status = status
    db.commit()
    db.refresh(checkin)
    return checkin


def _build_day_checkins(db: Session, target_date: date) -> list[TodayCheckinItem]:
    projects = (
        db.query(Project)
        .filter(Project.is_active == True)  # noqa: E712
        .order_by(Project.sort_order.asc(), Project.id.asc())
        .all()
    )
    project_ids = [p.id for p in projects]
    checkins = (
        db.query(Checkin)
        .filter(Checkin.project_id.in_(project_ids), Checkin.checkin_date == target_date)
        .all()
    )
    checkin_map = {c.project_id: c for c in checkins}
    items = []
    for p in projects:
        c = checkin_map.get(p.id)
        items.append(
            TodayCheckinItem(
                project_id=p.id,
                project_name=p.name,
                category=p.category,
                sort_order=p.sort_order,
                status=c.status if c else "not_done",
                checkin_id=c.id if c else None,
            )
        )
    return items


def get_today_checkins(db: Session, today: date) -> DayCheckinSummary:
    items = _build_day_checkins(db, today)
    done_count = sum(1 for i in items if i.status == "done")
    return DayCheckinSummary(
        date=today, items=items, total=len(items), done_count=done_count
    )


def get_date_checkins(db: Session, target_date: date) -> DayCheckinSummary:
    return get_today_checkins(db, target_date)


def get_history(
    db: Session, from_date: date, to_date: date
) -> list[HistoryDaySummary]:
    active_projects = (
        db.query(Project)
        .filter(Project.is_active == True)  # noqa: E712
        .all()
    )
    total = len(active_projects)
    project_ids = [p.id for p in active_projects]

    checkins = (
        db.query(Checkin)
        .filter(
            Checkin.project_id.in_(project_ids),
            Checkin.checkin_date >= from_date,
            Checkin.checkin_date <= to_date,
        )
        .all()
    )

    done_by_date: dict[date, int] = {}
    for c in checkins:
        if c.status == "done":
            done_by_date[c.checkin_date] = done_by_date.get(c.checkin_date, 0) + 1

    result = []
    current = from_date
    while current <= to_date:
        result.append(
            HistoryDaySummary(
                date=current,
                total=total,
                done_count=done_by_date.get(current, 0),
            )
        )
        current += timedelta(days=1)
    return result
