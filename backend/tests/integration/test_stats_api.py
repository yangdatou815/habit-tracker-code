from __future__ import annotations

from datetime import UTC, date, datetime, timedelta


def _create_habit(client, name: str = "Read", target_days: list[str] | None = None) -> int:
    response = client.post(
        "/api/v1/habits",
        json={
            "name": name,
            "description": f"{name} description",
            "target_days": target_days or [],
            "is_active": True,
        },
    )
    assert response.status_code == 201
    return response.json()["id"]


def test_stats_overview_empty(client) -> None:
    response = client.get("/api/v1/stats/overview")
    assert response.status_code == 200

    payload = response.json()
    assert payload["total_habits"] == 0
    assert payload["completed_today"] == 0
    assert payload["total_today"] == 0
    assert payload["completion_rate"] == 0.0


def test_stats_overview_with_data(client) -> None:
    today = datetime.now(UTC).date().isoformat()

    habit_id = _create_habit(client, "Exercise")
    client.put(
        f"/api/v1/habits/{habit_id}/completions/{today}",
        json={"status": "done"},
    )

    response = client.get("/api/v1/stats/overview")
    assert response.status_code == 200

    payload = response.json()
    assert payload["total_habits"] == 1
    assert payload["completed_today"] == 1
    assert payload["total_today"] == 1
    assert payload["completion_rate"] > 0


def test_stats_overview_custom_date_range(client) -> None:
    habit_id = _create_habit(client, "Stretch")
    client.put(
        f"/api/v1/habits/{habit_id}/completions/2026-03-03",
        json={"status": "done"},
    )

    response = client.get(
        "/api/v1/stats/overview",
        params={"from": "2026-03-01", "to": "2026-03-05"},
    )
    assert response.status_code == 200

    payload = response.json()
    assert payload["from_date"] == "2026-03-01"
    assert payload["to_date"] == "2026-03-05"
    assert payload["total_habits"] == 1


def test_stats_overview_rejects_reversed_dates(client) -> None:
    response = client.get(
        "/api/v1/stats/overview",
        params={"from": "2026-03-10", "to": "2026-03-01"},
    )
    assert response.status_code == 422
    assert "from_date" in response.json()["detail"]


def test_stats_overview_defaults_to_7_day_range(client) -> None:
    response = client.get("/api/v1/stats/overview")
    assert response.status_code == 200

    payload = response.json()
    today = datetime.now(UTC).date()
    expected_from = (today - timedelta(days=6)).isoformat()
    expected_to = today.isoformat()

    assert payload["from_date"] == expected_from
    assert payload["to_date"] == expected_to
