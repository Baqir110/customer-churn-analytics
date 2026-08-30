from app.services.strategy import get_retention_strategy


def test_critical_risk_strategy():
    risk, strategy, ab_variant = get_retention_strategy(0.85)
    assert risk == "CRITICAL"
    assert "retention call" in strategy.lower()
    assert ab_variant == "Standard_Retention_Call"


def test_moderate_risk_strategy():
    risk, strategy, ab_variant = get_retention_strategy(0.50)
    assert risk == "MODERATE"
    assert "survey" in strategy.lower()
    assert ab_variant == "Control_Survey"


def test_low_risk_strategy():
    risk, strategy, ab_variant = get_retention_strategy(0.20)
    assert risk == "LOW"
    assert "standard" in strategy.lower()
    assert ab_variant == "None"
