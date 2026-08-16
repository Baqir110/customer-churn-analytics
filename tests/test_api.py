from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_churn_prediction_high_risk():
    payload = {
        "tenure_months": 2,
        "monthly_charges": 115.0,
        "total_charges": 230.0,
        "support_tickets": 7
    }
    response = client.post("/api/v1/churn/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "churn_prediction" in data
    assert data["risk_level"] in ["CRITICAL", "MODERATE"]

def test_churn_prediction_low_risk():
    payload = {
        "tenure_months": 60,
        "monthly_charges": 30.0,
        "total_charges": 1800.0,
        "support_tickets": 0
    }
    response = client.post("/api/v1/churn/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["churn_prediction"] == 0
    assert data["risk_level"] == "LOW"