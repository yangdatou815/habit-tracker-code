from __future__ import annotations

from datetime import date

from app.stats.service import compute_stats_overview


def test_overview_returns_expected_shape(db_session) -> None:
    result = compute_stats_overview(
        db_session, from_date=date(2026, 3, 1), to_date=date(2026, 3, 7)
    )

    assert result.from_date == date(2026, 3, 1)
    assert result.to_date == date(2026, 3, 7)
    assert result.total_habits == 0
    assert result.completion_rate == 0.0
