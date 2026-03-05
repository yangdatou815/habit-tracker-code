from __future__ import annotations

from datetime import date, timedelta
from unittest.mock import patch

from app.habits.schemas import HabitCreate
from app.habits.service import create_habit, upsert_completion
from app.stats.service import compute_stats_overview


def _today() -> date:
    return date(2026, 3, 5)


def _create_active_habit(db_session, name: str, target_days: list[str] | None = None):
    return create_habit(
        db_session,
        HabitCreate(
            name=name,
            description=None,
            target_days=target_days or [],
            is_active=True,
        ),
    )


@patch("app.stats.service._today", _today)
def test_overview_empty_database(db_session) -> None:
    result = compute_stats_overview(
        db_session,
        from_date=date(2026, 2, 27),
        to_date=date(2026, 3, 5),
    )

    assert result.total_habits == 0
    assert result.completed_today == 0
    assert result.total_today == 0
    assert result.completion_rate == 0.0


@patch("app.stats.service._today", _today)
def test_overview_with_habits_no_completions(db_session) -> None:
    _create_active_habit(db_session, "Exercise", ["mon", "wed", "fri"])
    _create_active_habit(db_session, "Read", [])

    result = compute_stats_overview(
        db_session,
        from_date=date(2026, 2, 27),
        to_date=date(2026, 3, 5),
    )

    assert result.total_habits == 2
    assert result.completed_today == 0
    assert result.completion_rate == 0.0


@patch("app.stats.service._today", _today)
def test_overview_with_completions(db_session) -> None:
    # 2026-03-05 is a Thursday
    habit = _create_active_habit(db_session, "Read", [])  # daily

    # Mark done for today and yesterday
    upsert_completion(
        db_session,
        habit_id=habit.id,
        completed_date=date(2026, 3, 5),
        status="done",
    )
    upsert_completion(
        db_session,
        habit_id=habit.id,
        completed_date=date(2026, 3, 4),
        status="done",
    )

    result = compute_stats_overview(
        db_session,
        from_date=date(2026, 3, 1),
        to_date=date(2026, 3, 5),
    )

    assert result.total_habits == 1
    assert result.completed_today == 1
    assert result.total_today == 1
    # 5 days expected (daily habit, Mar 1-5), 2 done -> 40%
    assert result.completion_rate == 40.0


@patch("app.stats.service._today", _today)
def test_overview_excludes_archived_habits(db_session) -> None:
    active = _create_active_habit(db_session, "Active Habit", [])
    archived = create_habit(
        db_session,
        HabitCreate(
            name="Archived Habit",
            description=None,
            target_days=[],
            is_active=False,
        ),
    )

    upsert_completion(
        db_session,
        habit_id=active.id,
        completed_date=date(2026, 3, 5),
        status="done",
    )
    upsert_completion(
        db_session,
        habit_id=archived.id,
        completed_date=date(2026, 3, 5),
        status="done",
    )

    result = compute_stats_overview(
        db_session,
        from_date=date(2026, 3, 1),
        to_date=date(2026, 3, 5),
    )

    assert result.total_habits == 1
    assert result.completed_today == 1


@patch("app.stats.service._today", _today)
def test_overview_date_range_filtering(db_session) -> None:
    habit = _create_active_habit(db_session, "Stretch", [])

    # Completion inside range
    upsert_completion(
        db_session,
        habit_id=habit.id,
        completed_date=date(2026, 3, 3),
        status="done",
    )
    # Completion outside range
    upsert_completion(
        db_session,
        habit_id=habit.id,
        completed_date=date(2026, 2, 25),
        status="done",
    )

    result = compute_stats_overview(
        db_session,
        from_date=date(2026, 3, 1),
        to_date=date(2026, 3, 5),
    )

    # 5 expected days, 1 done in range -> 20%
    assert result.completion_rate == 20.0


@patch("app.stats.service._today", _today)
def test_overview_target_days_schedule_correct(db_session) -> None:
    # 2026: Mar 1=Sun, Mar 2=Mon, Mar 3=Tue, Mar 4=Wed, Mar 5=Thu
    habit = _create_active_habit(db_session, "Gym", ["mon", "wed", "fri"])

    # Done on Mon (Mar 2) and Wed (Mar 4)
    upsert_completion(
        db_session,
        habit_id=habit.id,
        completed_date=date(2026, 3, 2),  # Monday
        status="done",
    )
    upsert_completion(
        db_session,
        habit_id=habit.id,
        completed_date=date(2026, 3, 4),  # Wednesday
        status="done",
    )

    result = compute_stats_overview(
        db_session,
        from_date=date(2026, 3, 1),
        to_date=date(2026, 3, 5),
    )

    # Range Mar 1-5: Sun, Mon, Tue, Wed, Thu
    # Scheduled days: Mon (Mar 2), Wed (Mar 4) = 2 expected
    # Done: Mon (Mar 2), Wed (Mar 4) = 2 done
    assert result.completion_rate == 100.0
    assert result.total_habits == 1
