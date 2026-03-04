from __future__ import annotations

from datetime import UTC, date, datetime, timedelta

from sqlalchemy.dialects.sqlite import insert as sqlite_insert
from sqlalchemy.orm import Session, selectinload

from app.habits.models import Completion, Habit, HabitTargetDay
from app.habits.schemas import (
    CompletionResponse,
    HabitCreate,
    HabitDetailResponse,
    HabitResponse,
    HabitUpdate,
)


def _compute_streaks(completions: list[Completion]) -> tuple[int, int]:
    done_dates = sorted(
        {
            completion.completed_date
            for completion in completions
            if completion.status == "done"
        }
    )
    if not done_dates:
        return 0, 0

    longest_streak = 1
    current_run = 1
    for index in range(1, len(done_dates)):
        if done_dates[index] - done_dates[index - 1] == timedelta(days=1):
            current_run += 1
            longest_streak = max(longest_streak, current_run)
        else:
            current_run = 1

    today = datetime.now(UTC).date()
    current_streak = 0
    cursor = today
    done_set = set(done_dates)
    while cursor in done_set:
        current_streak += 1
        cursor -= timedelta(days=1)

    return current_streak, longest_streak


def _completion_rate(completions: list[Completion]) -> float:
    if not completions:
        return 0.0

    done_count = sum(1 for completion in completions if completion.status == "done")
    return round((done_count / len(completions)) * 100, 2)


def _serialize_target_days(habit: Habit) -> list[str]:
    order = {"mon": 0, "tue": 1, "wed": 2, "thu": 3, "fri": 4, "sat": 5, "sun": 6}
    days = [target_day.day_of_week for target_day in habit.target_days]
    return sorted(days, key=lambda day: order.get(day, 99))


def _build_habit_response(habit: Habit) -> HabitResponse:
    current_streak, longest_streak = _compute_streaks(habit.completions)
    return HabitResponse(
        id=habit.id,
        name=habit.name,
        description=habit.description,
        target_days=_serialize_target_days(habit),
        is_active=habit.is_active,
        created_at=habit.created_at,
        current_streak=current_streak,
        longest_streak=longest_streak,
        completion_rate=_completion_rate(habit.completions),
    )


def _build_habit_detail_response(habit: Habit) -> HabitDetailResponse:
    summary = _build_habit_response(habit)
    completions = [
        CompletionResponse(
            id=completion.id,
            habit_id=completion.habit_id,
            completed_date=completion.completed_date,
            status=completion.status,
            created_at=completion.created_at,
        )
        for completion in sorted(
            habit.completions,
            key=lambda completion: completion.completed_date,
        )
    ]

    return HabitDetailResponse(**summary.model_dump(), completions=completions)


def _habit_query_with_relationships(db: Session):
    return db.query(Habit).options(
        selectinload(Habit.target_days),
        selectinload(Habit.completions),
    )


def list_habits(db: Session, is_active: bool | None = None) -> list[HabitResponse]:
    query = _habit_query_with_relationships(db).order_by(Habit.id.asc())
    if is_active is not None:
        query = query.filter(Habit.is_active == is_active)

    habits = query.all()
    return [_build_habit_response(habit) for habit in habits]


def create_habit(db: Session, payload: HabitCreate) -> HabitResponse:
    habit = Habit(
        name=payload.name,
        description=payload.description,
        is_active=payload.is_active,
        target_days=[HabitTargetDay(day_of_week=day) for day in payload.target_days],
    )
    db.add(habit)
    db.commit()
    db.refresh(habit)
    return _build_habit_response(habit)


def get_habit(db: Session, habit: Habit) -> HabitDetailResponse:
    habit_with_relationships = (
        _habit_query_with_relationships(db).filter(Habit.id == habit.id).first()
    )
    if habit_with_relationships is None:
        db.refresh(habit)
        habit_with_relationships = habit

    return _build_habit_detail_response(habit_with_relationships)


def update_habit(db: Session, habit: Habit, payload: HabitUpdate) -> HabitResponse:
    updates = payload.model_dump(exclude_unset=True)

    if "name" in updates:
        habit.name = updates["name"]
    if "description" in updates:
        habit.description = updates["description"]
    if "is_active" in updates:
        habit.is_active = updates["is_active"]
    if "target_days" in updates:
        habit.target_days = [
            HabitTargetDay(day_of_week=day) for day in updates["target_days"]
        ]

    db.add(habit)
    db.commit()
    db.refresh(habit)
    return _build_habit_response(habit)


def delete_habit(db: Session, habit: Habit) -> None:
    db.delete(habit)
    db.commit()


def upsert_completion(
    db: Session,
    *,
    habit_id: int,
    completed_date: date,
    status: str,
) -> CompletionResponse:
    statement = sqlite_insert(Completion).values(
        habit_id=habit_id,
        completed_date=completed_date,
        status=status,
    )
    statement = statement.on_conflict_do_update(
        index_elements=[Completion.habit_id, Completion.completed_date],
        set_={"status": status},
    )

    db.execute(statement)
    db.commit()

    completion = (
        db.query(Completion)
        .filter(
            Completion.habit_id == habit_id,
            Completion.completed_date == completed_date,
        )
        .first()
    )
    assert completion is not None

    return CompletionResponse(
        id=completion.id,
        habit_id=completion.habit_id,
        completed_date=completion.completed_date,
        status=completion.status,
        created_at=completion.created_at,
    )


def list_completions_range(
    db: Session,
    *,
    habit_id: int,
    from_date: date | None,
    to_date: date | None,
) -> list[CompletionResponse]:
    if from_date is not None and to_date is not None and from_date > to_date:
        raise ValueError("from_date cannot be after to_date")

    query = db.query(Completion).filter(Completion.habit_id == habit_id)
    if from_date is not None:
        query = query.filter(Completion.completed_date >= from_date)
    if to_date is not None:
        query = query.filter(Completion.completed_date <= to_date)

    completions = query.order_by(Completion.completed_date.asc()).all()
    return [
        CompletionResponse(
            id=completion.id,
            habit_id=completion.habit_id,
            completed_date=completion.completed_date,
            status=completion.status,
            created_at=completion.created_at,
        )
        for completion in completions
    ]
