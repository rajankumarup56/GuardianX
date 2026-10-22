from app.models.enums import RiskLevel
from app.services.risk_intelligence_service import RiskIntelligenceService


def test_no_anomaly_is_low_risk():
    service = RiskIntelligenceService()

    level, score = service.evaluate_behaviour_risk(
        anomaly_count=0,
    )

    assert level == RiskLevel.LOW
    assert score == 0


def test_single_anomaly_is_medium_risk():
    service = RiskIntelligenceService()

    level, score = service.evaluate_behaviour_risk(
        anomaly_count=1,
    )

    assert level == RiskLevel.MEDIUM
    assert score == 25


def test_multiple_anomalies_are_critical():
    service = RiskIntelligenceService()

    level, score = service.evaluate_behaviour_risk(
        anomaly_count=3,
    )

    assert level == RiskLevel.CRITICAL
    assert score == 75