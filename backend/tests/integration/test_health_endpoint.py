from __future__ import annotations

import pytest


@pytest.mark.smoke
def test_health_endpoint(client) -> None:
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "habit-tracker-api"}
