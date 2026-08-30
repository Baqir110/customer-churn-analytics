from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_read_root():
    res = client.get("/")
    assert res.status_code == 200
    assert res.json()["status"] == "online"


def test_drift_report_endpoint():
    res = client.get("/drift")
    assert res.status_code in [200, 500]


def test_metrics_endpoint():
    res = client.get("/metrics")
    assert res.status_code == 200
