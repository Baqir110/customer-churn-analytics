from app.services.strategy import get_retention_strategy


def test_critical_risk_strategy():
    risk, strategy = get_retention_strategy(0.85)
    assert risk == "CRITICAL"
    assert "20% renewal discount" in strategy


def test_moderate_risk_strategy():
    risk, strategy = get_retention_strategy(0.50)
    assert risk == "MODERATE"
    assert "proactive service check-in" in strategy


def test_low_risk_strategy():
    risk, strategy = get_retention_strategy(0.20)
    assert risk == "LOW"
    assert "standard automated" in strategy
