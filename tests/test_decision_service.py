from app.models.enums import RiskLevel, SecurityDecision
from app.services.decision_service import DecisionService


def test_critical_security_risk_blocks():
    service = DecisionService()

    decision = service.decide(
        security_risk=RiskLevel.CRITICAL,
        safety_risk=RiskLevel.LOW,
    )

    assert decision == SecurityDecision.BLOCK


def test_high_safety_risk_blocks():
    service = DecisionService()

    decision = service.decide(
        security_risk=RiskLevel.LOW,
        safety_risk=RiskLevel.HIGH,
    )

    assert decision == SecurityDecision.BLOCK


def test_low_risk_allows():
    service = DecisionService()

    decision = service.decide(
        security_risk=RiskLevel.LOW,
        safety_risk=RiskLevel.LOW,
    )

    assert decision == SecurityDecision.ALLOW