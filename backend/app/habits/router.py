from __future__ import annotations

from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.habits.models import Habit
from app.habits.dependencies import get_habit_or_404
from app.habits.schemas import (
    CompletionListResponse,
    CompletionResponse,
    CompletionUpsertRequest,
    HabitCreate,
    HabitDetailResponse,
    HabitResponse,
    HabitUpdate,
)
from app.habits.service import (
    create_habit,
    delete_habit,
    get_habit,
    list_completions_range,
    list_habits,
    update_habit,
    upsert_completion,
)

router = APIRouter(prefix="/habits", tags=["habits"])


@router.get("", response_model=List[HabitResponse])
def get_habits(
    is_active: Optional[bool] = Query(default=None),
    db: Session = Depends(get_db),
) -> List[HabitResponse]:
    return list_habits(db, is_active=is_active)


@router.post("", response_model=HabitResponse, status_code=status.HTTP_201_CREATED)
def create_habit_endpoint(
    payload: HabitCreate,
    db: Session = Depends(get_db),
) -> HabitResponse:
    return create_habit(db, payload)


@router.get("/{habit_id}", response_model=HabitDetailResponse)
def get_habit_endpoint(
    habit: Habit = Depends(get_habit_or_404),
    db: Session = Depends(get_db),
) -> HabitDetailResponse:
    return get_habit(db, habit)


@router.patch("/{habit_id}", response_model=HabitResponse)
def patch_habit_endpoint(
    payload: HabitUpdate,
    habit: Habit = Depends(get_habit_or_404),
    db: Session = Depends(get_db),
) -> HabitResponse:
    return update_habit(db, habit, payload)


@router.delete("/{habit_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_habit_endpoint(
    habit: Habit = Depends(get_habit_or_404),
    db: Session = Depends(get_db),
) -> Response:
    delete_habit(db, habit)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put(
    "/{habit_id}/completions/{completion_date}", response_model=CompletionResponse
)
def put_completion_endpoint(
    completion_date: date,
    payload: CompletionUpsertRequest,
    habit: Habit = Depends(get_habit_or_404),
    db: Session = Depends(get_db),
) -> CompletionResponse:
    return upsert_completion(
        db,
        habit_id=habit.id,
        completed_date=completion_date,
        status=payload.status,
    )


@router.get("/{habit_id}/completions", response_model=CompletionListResponse)
def get_completions_endpoint(
    from_date: Optional[date] = Query(default=None, alias="from"),
    to_date: Optional[date] = Query(default=None, alias="to"),
    habit: Habit = Depends(get_habit_or_404),
    db: Session = Depends(get_db),
) -> CompletionListResponse:
    try:
        completions = list_completions_range(
            db,
            habit_id=habit.id,
            from_date=from_date,
            to_date=to_date,
        )
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error

    return CompletionListResponse(
        habit_id=habit.id,
        from_date=from_date,
        to_date=to_date,
        completions=completions,
    )
