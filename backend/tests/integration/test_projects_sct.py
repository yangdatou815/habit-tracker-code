"""SCT (System Component Test) abnormal-path tests for V2 User Stories.

Each US from PRD V2.6 must have >= 1 normal + >= 3 abnormal test cases.
Normal cases are in test_projects_api.py. This file covers abnormal paths.
"""
from __future__ import annotations

from datetime import date

import pytest


@pytest.fixture
def _seed(db_session):
    from app.projects.models import Project

    p = Project(name="打坐", category="静功", sort_order=1)
    db_session.add(p)
    db_session.commit()
    return p


# ── US1: 今日打卡状态 ────────────────────────────────────────
# Normal: test_today_checkins (in test_projects_api.py)
# Abnormal below:


def test_us1_today_no_projects(client):
    """No projects exist → empty items list."""
    resp = client.get("/api/v1/checkins/today")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 0
    assert data["items"] == []


def test_us1_today_all_inactive(client, db_session):
    """All projects inactive → empty items list."""
    from app.projects.models import Project

    p = Project(name="x", category="其他", sort_order=1, is_active=False)
    db_session.add(p)
    db_session.commit()
    resp = client.get("/api/v1/checkins/today")
    data = resp.json()
    assert data["total"] == 0


def test_us1_today_idempotent(client, _seed):
    """Calling today endpoint twice returns same result."""
    r1 = client.get("/api/v1/checkins/today").json()
    r2 = client.get("/api/v1/checkins/today").json()
    assert r1 == r2


# ── US2: 一键打卡 ────────────────────────────────────────────
# Normal: test_toggle_checkin (in test_projects_api.py)
# Abnormal below:


def test_us2_toggle_nonexistent_project(client):
    """Toggle checkin for non-existent project → 404."""
    resp = client.put("/api/v1/checkins/999/2026-04-16", json={"status": "done"})
    assert resp.status_code == 404


def test_us2_toggle_invalid_date_format(client, _seed):
    """Invalid date format → 422."""
    resp = client.put("/api/v1/checkins/1/not-a-date", json={"status": "done"})
    assert resp.status_code == 422


def test_us2_toggle_invalid_status(client, _seed):
    """Invalid status value → 422."""
    resp = client.put("/api/v1/checkins/1/2026-04-16", json={"status": "invalid"})
    assert resp.status_code == 422


def test_us2_toggle_overwrite(client, _seed):
    """Toggle done→not_done overwrites correctly."""
    client.put("/api/v1/checkins/1/2026-04-16", json={"status": "done"})
    resp = client.put("/api/v1/checkins/1/2026-04-16", json={"status": "not_done"})
    assert resp.status_code == 200
    assert resp.json()["status"] == "not_done"


# ── US3: 进度显示 ────────────────────────────────────────────
# Normal: test_today_with_done (in test_projects_api.py)
# Abnormal below:


def test_us3_progress_all_done(client, _seed):
    """All projects done → done_count == total."""
    today = date.today().isoformat()
    client.put(f"/api/v1/checkins/1/{today}", json={"status": "done"})
    data = client.get("/api/v1/checkins/today").json()
    assert data["done_count"] == data["total"]


def test_us3_progress_all_undone(client, _seed):
    """No checkins → done_count == 0."""
    data = client.get("/api/v1/checkins/today").json()
    assert data["done_count"] == 0
    assert data["total"] > 0


def test_us3_progress_partial(client, db_session):
    """Multiple projects, only some done."""
    from app.projects.models import Project

    db_session.add_all([
        Project(name="A", category="静功", sort_order=1),
        Project(name="B", category="动功", sort_order=2),
        Project(name="C", category="养生", sort_order=3),
    ])
    db_session.commit()
    today = date.today().isoformat()
    client.put(f"/api/v1/checkins/1/{today}", json={"status": "done"})
    data = client.get("/api/v1/checkins/today").json()
    assert data["done_count"] == 1
    assert data["total"] == 3


# ── US4: 历史查看 ────────────────────────────────────────────
# Normal: test_date_checkins (in test_projects_api.py)
# Abnormal below:


def test_us4_date_no_data(client, _seed):
    """Query a date with no checkins → done_count 0."""
    resp = client.get("/api/v1/checkins/date/2020-01-01")
    assert resp.status_code == 200
    assert resp.json()["done_count"] == 0


def test_us4_date_invalid_format(client):
    """Invalid date format → 422."""
    resp = client.get("/api/v1/checkins/date/bad-date")
    assert resp.status_code == 422


def test_us4_date_future(client, _seed):
    """Future date → returns valid response with 0 done."""
    resp = client.get("/api/v1/checkins/date/2099-12-31")
    assert resp.status_code == 200
    assert resp.json()["done_count"] == 0


# ── US5: 日历完成比例 / 历史查询 ─────────────────────────────
# Normal: test_history (in test_projects_api.py)
# Abnormal below:


def test_us5_history_no_data_range(client, _seed):
    """Query range with no checkins → still returns day summaries."""
    resp = client.get("/api/v1/checkins/history", params={
        "from_date": "2020-01-01", "to_date": "2020-01-03"
    })
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)


def test_us5_history_from_after_to(client, _seed):
    """from_date > to_date → 422."""
    resp = client.get("/api/v1/checkins/history", params={
        "from_date": "2026-04-20", "to_date": "2026-04-10"
    })
    assert resp.status_code == 422


def test_us5_history_missing_params(client):
    """Missing from/to params → 422."""
    resp = client.get("/api/v1/checkins/history")
    assert resp.status_code == 422


# ── US6: 项目管理 ────────────────────────────────────────────
# Normal: test_create_project, test_update_project, test_delete_project
# Abnormal below:


def test_us6_create_empty_name(client):
    """Empty project name → 422."""
    resp = client.post("/api/v1/projects", json={"name": "", "category": "其他"})
    assert resp.status_code == 422


def test_us6_create_missing_name(client):
    """Missing name field → 422."""
    resp = client.post("/api/v1/projects", json={"category": "其他"})
    assert resp.status_code == 422


def test_us6_update_nonexistent(client):
    """Update non-existent project → 404."""
    resp = client.patch("/api/v1/projects/9999", json={"name": "x"})
    assert resp.status_code == 404


def test_us6_delete_nonexistent(client):
    """Delete non-existent project → 404."""
    resp = client.delete("/api/v1/projects/9999")
    assert resp.status_code == 404
