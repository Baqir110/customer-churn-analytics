from app.ml.predict import predict_churn_risk

def test_predict_churn_risk_high():
    # Sample input data for high churn risk
    sample_data = {
        "tenure_months": 2,
        "monthly_charges": 115.0,
        "total_charges": 230.0,
        "support_tickets": 7
    }
    prediction, prob = predict_churn_risk(sample_data)
    
    assert isinstance(prediction, int)
    assert isinstance(prob, float)
    assert 0.0 <= prob <= 1.0

def test_predict_churn_risk_low():
    # Sample input data for low churn risk
    sample_data = {
        "tenure_months": 36,
        "monthly_charges": 40.0,
        "total_charges": 1440.0,
        "support_tickets": 0
    }
    prediction, prob = predict_churn_risk(sample_data)
    
    assert isinstance(prediction, int)
    assert isinstance(prob, float)
    assert 0.0 <= prob <= 1.0