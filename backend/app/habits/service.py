from __future__ import annotations

from sqlalchemy.orm import Session

from app.habits.models import Habit


def list_habits(db: Session) -> list[Habit]:
    return db.query(Habit).order_by(Habit.id.asc()).all()
