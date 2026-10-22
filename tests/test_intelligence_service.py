from app.models.behaviour import BehaviourProfile
from app.models.enums import RiskLevel, SecurityDecision
from app.services.intelligence_service import IntelligenceService


def test_normal_device_is_allowed():
    service = IntelligenceService()

    profile = BehaviourProfile(
        device_id="GX-DRONE-01",
        expected_speed_min=0,
        expected_speed_max=25,
        expected_altitude_min=0,
        expected_altitude_max=120,
        expected_temperature_max=80,
    )

    result = service.analyze(
        profile=profile,
        speed=10,
        altitude=50,
        temperature=40,
    )

    assert result["risk_level"] == RiskLevel.LOW
    assert result["prediction"]["predicted_risk"] == RiskLevel.LOW
    assert result["decision"] == SecurityDecision.ALLOW


def test_abnormal_device_is_blocked():
    service = IntelligenceService()

    profile = BehaviourProfile(
        device_id="GX-DRONE-01",
        expected_speed_min=0,
        expected_speed_max=25,
        expected_altitude_min=0,
        expected_altitude_max=120,
        expected_temperature_max=80,
    )

    result = service.analyze(
        profile=profile,
        speed=50,
        altitude=200,
        temperature=100,
        trend_increasing=True,
    )

    assert result["behaviour"]["anomaly_detected"] is True
    assert result["risk_level"] == RiskLevel.CRITICAL
    assert result["decision"] == SecurityDecision.BLOCK