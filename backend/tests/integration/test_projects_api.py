"""Integration tests for /api/v1/projects and /api/v1/checkins endpoints."""
from __future__ import annotations

from datetime import date

import pytest


@pytest.fixture
def _seed_projects(db_session):
    """Seed two projects for test use."""
    from app.projects.models import Project

    p1 = Project(name="打坐两小时", category="静功", sort_order=1)
    p2 = Project(name="拉筋", category="柔韧", sort_order=2)
    db_session.add_all([p1, p2])
    db_session.commit()
    return p1, p2


# ── Project CRUD ──────────────────────────────────────────────


def test_list_projects_empty(client):
    resp = client.get("/api/v1/projects")
    assert resp.status_code == 200
    assert resp.json() == []


@pytest.mark.smoke
def test_create_project(client):
    resp = client.post("/api/v1/projects", json={"name": "金刚功", "category": "动功"})
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "金刚功"
    assert data["category"] == "动功"
    assert data["is_active"] is True


def test_list_projects(client, _seed_projects):
    resp = client.get("/api/v1/projects")
    assert resp.status_code == 200
    names = [p["name"] for p in resp.json()]
    assert "打坐两小时" in names
    assert "拉筋" in names


def test_update_project(client, _seed_projects):
    resp = client.patch("/api/v1/projects/1", json={"name": "打坐三小时"})
    assert resp.status_code == 200
    assert resp.json()["name"] == "打坐三小时"


def test_delete_project(client, _seed_projects):
    resp = client.delete("/api/v1/projects/1")
    assert resp.status_code == 204
    resp2 = client.get("/api/v1/projects")
    assert len(resp2.json()) == 1


def test_update_nonexistent(client):
    resp = client.patch("/api/v1/projects/999", json={"name": "x"})
    assert resp.status_code == 404


def test_delete_nonexistent(client):
    resp = client.delete("/api/v1/projects/999")
    assert resp.status_code == 404


# ── Checkin Toggle ──────────────────────────────────────────


@pytest.mark.smoke
def test_toggle_checkin(client, _seed_projects):
    resp = client.put("/api/v1/checkins/1/2026-04-16", json={"status": "done"})
    assert resp.status_code == 200
    assert resp.json()["status"] == "done"


def test_toggle_checkin_upsert(client, _seed_projects):
    client.put("/api/v1/checkins/1/2026-04-16", json={"status": "done"})
    resp = client.put("/api/v1/checkins/1/2026-04-16", json={"status": "not_done"})
    assert resp.status_code == 200
    assert resp.json()["status"] == "not_done"


def test_toggle_nonexistent_project(client):
    resp = client.put("/api/v1/checkins/999/2026-04-16", json={"status": "done"})
    assert resp.status_code == 404


# ── Today / Date Checkins ────────────────────────────────────


@pytest.mark.smoke
def test_today_checkins(client, _seed_projects):
    today = date.today().isoformat()
    resp = client.get("/api/v1/checkins/today")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 2
    assert data["done_count"] == 0
    assert len(data["items"]) == 2


def test_today_with_done(client, _seed_projects):
    today = date.today().isoformat()
    client.put(f"/api/v1/checkins/1/{today}", json={"status": "done"})
    resp = client.get("/api/v1/checkins/today")
    data = resp.json()
    assert data["done_count"] == 1


def test_date_checkins(client, _seed_projects):
    client.put("/api/v1/checkins/1/2026-04-10", json={"status": "done"})
    resp = client.get("/api/v1/checkins/date/2026-04-10")
    assert resp.status_code == 200
    data = resp.json()
    assert data["date"] == "2026-04-10"
    assert data["done_count"] == 1


# ── History ──────────────────────────────────────────────────


def test_history(client, _seed_projects):
    client.put("/api/v1/checkins/1/2026-04-14", json={"status": "done"})
    client.put("/api/v1/checkins/2/2026-04-14", json={"status": "done"})
    client.put("/api/v1/checkins/1/2026-04-15", json={"status": "done"})

    resp = client.get("/api/v1/checkins/history", params={"from_date": "2026-04-14", "to_date": "2026-04-15"})
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 2
    day14 = next(d for d in data if d["date"] == "2026-04-14")
    assert day14["done_count"] == 2
    day15 = next(d for d in data if d["date"] == "2026-04-15")
    assert day15["done_count"] == 1
