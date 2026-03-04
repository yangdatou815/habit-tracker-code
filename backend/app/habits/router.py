from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.habits.schemas import HabitResponse
from app.habits.service import list_habits

router = APIRouter(prefix="/habits", tags=["habits"])


@router.get("", response_model=list[HabitResponse])
def get_habits(db: Session = Depends(get_db)) -> list[HabitResponse]:
    return list_habits(db)
