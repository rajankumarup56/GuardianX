from app.models.enums import SecurityDecision, RiskLevel


class DecisionService:
    """Converts security and safety risk into an operational decision."""

    def decide(
        self,
        *,
        security_risk: RiskLevel,
        safety_risk: RiskLevel,
    ) -> SecurityDecision:

        if security_risk == RiskLevel.CRITICAL:
            return SecurityDecision.BLOCK

        if safety_risk == RiskLevel.CRITICAL:
            return SecurityDecision.BLOCK

        if security_risk == RiskLevel.HIGH:
            return SecurityDecision.BLOCK

        if safety_risk == RiskLevel.HIGH:
            return SecurityDecision.BLOCK

        if (
            security_risk == RiskLevel.MEDIUM
            or safety_risk == RiskLevel.MEDIUM
        ):
            return SecurityDecision.ALLOW

        return SecurityDecision.ALLOW