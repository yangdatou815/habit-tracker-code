from __future__ import annotations

from datetime import date


def overview(from_date: date, to_date: date) -> dict[str, object]:
    days = (to_date - from_date).days + 1
    return {
        "from": from_date.isoformat(),
        "to": to_date.isoformat(),
        "days": max(days, 0),
        "completion_rate": 0.0,
    }
