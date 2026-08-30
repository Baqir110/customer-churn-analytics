from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

sample_payload = {
    "customer_id": "CUST-1001",
    "tenure_months": 3,
    "monthly_charges": 95.5,
    "total_charges": 286.5,
    "support_tickets": 5,
}


def test_explain_endpoint():
    res = client.post("/api/v1/churn/explain", json=sample_payload)
    assert res.status_code == 200
    assert "feature_contributions" in res.json()


def test_batch_prediction_endpoint():
    batch_payload = [sample_payload, {**sample_payload, "customer_id": "CUST-1002"}]
    res = client.post("/api/v1/churn/predict/batch", json=batch_payload)
    assert res.status_code == 200
    data = res.json()
    assert data["total_records"] == 2
    assert len(data["predictions"]) == 2


def test_prometheus_metrics():
    res = client.get("/metrics")
    assert res.status_code == 200
    assert "http_requests_total" in res.text
