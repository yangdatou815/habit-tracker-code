from __future__ import annotations

from datetime import date

from app.stats.service import overview


def test_overview_returns_expected_shape() -> None:
    result = overview(date(2026, 3, 1), date(2026, 3, 7))

    assert result["from"] == "2026-03-01"
    assert result["to"] == "2026-03-07"
    assert result["days"] == 7
    assert result["completion_rate"] == 0.0
