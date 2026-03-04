from __future__ import annotations

from contextlib import contextmanager
from datetime import date

import pytest
from sqlalchemy import event

from app.habits.models import Completion, Habit
from app.habits.schemas import HabitCreate, HabitUpdate
from app.habits.service import (
    create_habit,
    delete_habit,
    list_completions_range,
    list_habits,
    update_habit,
    upsert_completion,
)


@contextmanager
def capture_select_statements(db_session):
    statements: list[str] = []
    engine = db_session.get_bind()

    def before_cursor_execute(
        conn,
        cursor,
        statement,
        parameters,
        context,
        executemany,
    ) -> None:
        if statement.lstrip().upper().startswith("SELECT"):
            statements.append(statement)

    event.listen(engine, "before_cursor_execute", before_cursor_execute)
    try:
        yield statements
    finally:
        event.remove(engine, "before_cursor_execute", before_cursor_execute)


def test_create_and_list_habits(db_session) -> None:
    created = create_habit(
        db_session,
        HabitCreate(
            name="  Exercise  ",
            description="  30 min movement  ",
            target_days=["fri", "mon", "wed", "mon"],
            is_active=True,
        ),
    )

    assert created.name == "Exercise"
    assert created.description == "30 min movement"
    assert created.target_days == ["mon", "wed", "fri"]

    listed = list_habits(db_session)
    assert len(listed) == 1
    assert listed[0].id == created.id


def test_update_habit_replaces_target_days(db_session) -> None:
    created = create_habit(
        db_session,
        HabitCreate(
            name="Read",
            description="Read pages",
            target_days=["mon", "wed"],
            is_active=True,
        ),
    )

    orm_habit = db_session.query(Habit).filter(Habit.id == created.id).first()
    assert orm_habit is not None

    updated = update_habit(
        db_session,
        orm_habit,
        HabitUpdate(
            name="Read Daily",
            target_days=["sun", "tue"],
            is_active=False,
        ),
    )

    assert updated.name == "Read Daily"
    assert updated.target_days == ["tue", "sun"]
    assert updated.is_active is False


def test_upsert_completion_and_range_query(db_session) -> None:
    created = create_habit(
        db_session,
        HabitCreate(name="Stretch", description=None, target_days=[], is_active=True),
    )

    upsert_completion(
        db_session,
        habit_id=created.id,
        completed_date=date(2026, 3, 4),
        status="done",
    )
    upsert_completion(
        db_session,
        habit_id=created.id,
        completed_date=date(2026, 3, 4),
        status="not_done",
    )

    records = list_completions_range(
        db_session,
        habit_id=created.id,
        from_date=date(2026, 3, 1),
        to_date=date(2026, 3, 7),
    )
    assert len(records) == 1
    assert records[0].status == "not_done"

    with pytest.raises(ValueError, match="from_date"):
        list_completions_range(
            db_session,
            habit_id=created.id,
            from_date=date(2026, 3, 7),
            to_date=date(2026, 3, 1),
        )


def test_delete_habit_cascades_completions(db_session) -> None:
    created = create_habit(
        db_session,
        HabitCreate(name="Walk", description=None, target_days=[], is_active=True),
    )

    upsert_completion(
        db_session,
        habit_id=created.id,
        completed_date=date(2026, 3, 4),
        status="done",
    )

    orm_habit = db_session.query(Habit).filter(Habit.id == created.id).first()
    assert orm_habit is not None
    delete_habit(db_session, orm_habit)

    remaining = db_session.query(Completion).all()
    assert remaining == []


def test_list_habits_avoids_n_plus_one_queries(db_session) -> None:
    for index in range(3):
        created = create_habit(
            db_session,
            HabitCreate(
                name=f"Habit {index}",
                description="test",
                target_days=["mon", "wed"],
                is_active=True,
            ),
        )
        upsert_completion(
            db_session,
            habit_id=created.id,
            completed_date=date(2026, 3, 4 + index),
            status="done",
        )

    with capture_select_statements(db_session) as select_statements:
        habits = list_habits(db_session)

    assert len(habits) == 3
    assert len(select_statements) <= 3
