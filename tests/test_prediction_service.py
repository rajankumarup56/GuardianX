from app.models.enums import RiskLevel
from app.services.prediction_service import PredictionService


def test_low_risk_stays_low():
    service = PredictionService()

    result = service.predict(
        current_risk=RiskLevel.LOW,
        anomaly_count=0,
    )

    assert result["predicted_risk"] == RiskLevel.LOW
    assert result["escalation_score"] == 0


def test_high_risk_with_increasing_trend_predicts_critical():
    service = PredictionService()

    result = service.predict(
        current_risk=RiskLevel.HIGH,
        anomaly_count=2,
        trend_increasing=True,
    )

    assert result["predicted_risk"] == RiskLevel.CRITICAL
    assert result["escalation_score"] == 4