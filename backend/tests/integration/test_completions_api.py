from __future__ import annotations


def _create_habit(client) -> int:
    response = client.post(
        "/api/v1/habits",
        json={
            "name": "Read",
            "description": "Read 20 pages",
            "target_days": ["mon", "tue", "wed"],
            "is_active": True,
        },
    )
    assert response.status_code == 201
    return response.json()["id"]


def test_completion_upsert_is_idempotent(client) -> None:
    habit_id = _create_habit(client)

    first = client.put(
        f"/api/v1/habits/{habit_id}/completions/2026-03-04",
        json={"status": "done"},
    )
    assert first.status_code == 200
    first_payload = first.json()
    assert first_payload["status"] == "done"

    second = client.put(
        f"/api/v1/habits/{habit_id}/completions/2026-03-04",
        json={"status": "not_done"},
    )
    assert second.status_code == 200
    second_payload = second.json()
    assert second_payload["id"] == first_payload["id"]
    assert second_payload["status"] == "not_done"

    list_response = client.get(
        f"/api/v1/habits/{habit_id}/completions",
        params={"from": "2026-03-01", "to": "2026-03-10"},
    )
    assert list_response.status_code == 200
    payload = list_response.json()
    assert payload["habit_id"] == habit_id
    assert payload["from_date"] == "2026-03-01"
    assert payload["to_date"] == "2026-03-10"
    assert len(payload["completions"]) == 1
    assert payload["completions"][0]["completed_date"] == "2026-03-04"
    assert payload["completions"][0]["status"] == "not_done"


def test_completion_upsert_rejects_invalid_status(client) -> None:
    habit_id = _create_habit(client)

    response = client.put(
        f"/api/v1/habits/{habit_id}/completions/2026-03-04",
        json={"status": "skipped"},
    )

    assert response.status_code == 422


def test_completion_date_path_must_be_iso_date(client) -> None:
    habit_id = _create_habit(client)

    response = client.put(
        f"/api/v1/habits/{habit_id}/completions/not-a-date",
        json={"status": "done"},
    )

    assert response.status_code == 422


def test_completion_range_rejects_reversed_dates(client) -> None:
    habit_id = _create_habit(client)

    response = client.get(
        f"/api/v1/habits/{habit_id}/completions",
        params={"from": "2026-03-10", "to": "2026-03-01"},
    )

    assert response.status_code == 422
    assert "from_date" in response.json()["detail"]


def test_completion_requests_require_existing_habit(client) -> None:
    put_response = client.put(
        "/api/v1/habits/999/completions/2026-03-04",
        json={"status": "done"},
    )
    assert put_response.status_code == 404

    get_response = client.get(
        "/api/v1/habits/999/completions",
        params={"from": "2026-03-01", "to": "2026-03-05"},
    )
    assert get_response.status_code == 404
