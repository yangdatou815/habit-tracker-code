from __future__ import annotations

from datetime import UTC, date, datetime, timedelta

import structlog
from sqlalchemy.orm import Session, selectinload

from app.habits.models import Habit
from app.stats.schemas import StatsOverviewResponse

logger = structlog.get_logger()

WEEKDAY_ABBREV = ("mon", "tue", "wed", "thu", "fri", "sat", "sun")


def _today() -> date:
    return datetime.now(UTC).date()


def compute_stats_overview(
    db: Session,
    *,
    from_date: date,
    to_date: date,
) -> StatsOverviewResponse:
    today = _today()

    habits = (
        db.query(Habit)
        .options(
            selectinload(Habit.target_days),
            selectinload(Habit.completions),
        )
        .filter(Habit.is_active.is_(True))
        .all()
    )

    total_habits = len(habits)
    completed_today = 0
    total_today = 0
    total_done = 0
    total_expected = 0

    for habit in habits:
        scheduled_days = {td.day_of_week for td in habit.target_days}

        # --- today counts ---
        today_abbrev = WEEKDAY_ABBREV[today.weekday()]
        is_scheduled_today = len(scheduled_days) == 0 or today_abbrev in scheduled_days
        if is_scheduled_today:
            total_today += 1

        done_today = any(
            c.completed_date == today and c.status == "done"
            for c in habit.completions
        )
        if done_today:
            completed_today += 1

        # --- range rate ---
        done_dates_in_range = {
            c.completed_date
            for c in habit.completions
            if from_date <= c.completed_date <= to_date and c.status == "done"
        }

        effective_end = min(to_date, today)
        cursor = max(from_date, effective_end) if from_date > effective_end else from_date
        while cursor <= effective_end:
            day_abbrev = WEEKDAY_ABBREV[cursor.weekday()]
            if len(scheduled_days) == 0 or day_abbrev in scheduled_days:
                total_expected += 1
                if cursor in done_dates_in_range:
                    total_done += 1
            cursor += timedelta(days=1)

    completion_rate = (
        round((total_done / total_expected) * 100, 2) if total_expected > 0 else 0.0
    )

    logger.info(
        "stats.overview.computed",
        total_habits=total_habits,
        completed_today=completed_today,
        rate=completion_rate,
    )

    return StatsOverviewResponse(
        from_date=from_date,
        to_date=to_date,
        total_habits=total_habits,
        completed_today=completed_today,
        total_today=total_today,
        completion_rate=completion_rate,
    )
