from __future__ import annotations


def test_habit_crud_flow(client) -> None:
    create_response = client.post(
        "/api/v1/habits",
        json={
            "name": "Exercise",
            "description": "30 min movement",
            "target_days": ["fri", "mon", "wed"],
            "is_active": True,
        },
    )
    assert create_response.status_code == 201
    created = create_response.json()
    habit_id = created["id"]
    assert created["name"] == "Exercise"
    assert created["target_days"] == ["mon", "wed", "fri"]
    assert created["is_active"] is True
    assert created["current_streak"] == 0
    assert created["longest_streak"] == 0

    list_response = client.get("/api/v1/habits")
    assert list_response.status_code == 200
    habits = list_response.json()
    assert len(habits) == 1
    assert habits[0]["id"] == habit_id

    detail_response = client.get(f"/api/v1/habits/{habit_id}")
    assert detail_response.status_code == 200
    detail = detail_response.json()
    assert detail["id"] == habit_id
    assert detail["completions"] == []

    patch_response = client.patch(
        f"/api/v1/habits/{habit_id}",
        json={"name": "Morning Exercise", "target_days": ["sun", "mon"]},
    )
    assert patch_response.status_code == 200
    patched = patch_response.json()
    assert patched["name"] == "Morning Exercise"
    assert patched["target_days"] == ["mon", "sun"]

    archive_response = client.patch(
        f"/api/v1/habits/{habit_id}",
        json={"is_active": False},
    )
    assert archive_response.status_code == 200
    assert archive_response.json()["is_active"] is False

    active_only_response = client.get("/api/v1/habits", params={"is_active": True})
    assert active_only_response.status_code == 200
    assert active_only_response.json() == []

    delete_response = client.delete(f"/api/v1/habits/{habit_id}")
    assert delete_response.status_code == 204

    post_delete_response = client.get(f"/api/v1/habits/{habit_id}")
    assert post_delete_response.status_code == 404
    assert post_delete_response.json() == {"detail": "Habit not found"}


def test_create_habit_rejects_blank_name(client) -> None:
    response = client.post(
        "/api/v1/habits",
        json={"name": "   ", "description": "bad payload"},
    )

    assert response.status_code == 422
