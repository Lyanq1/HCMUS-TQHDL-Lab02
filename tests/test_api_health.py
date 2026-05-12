from fastapi.testclient import TestClient

from api.main import app


def test_health():
    with TestClient(app) as client:
        r = client.get("/health")
    assert r.status_code == 200
    assert r.json().get("status") == "ok"


def test_logs_history_empty_ok():
    with TestClient(app) as client:
        r = client.get("/api/logs/history", params={"limit": 5})
    assert r.status_code == 200
    data = r.json()
    assert "items" in data
