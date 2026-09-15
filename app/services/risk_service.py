from app.models.enums import RiskLevel


class RiskService:
    """Calculates a deterministic risk level from security signals."""

    def calculate(
        self,
        *,
        denied: bool = False,
        repeated_denied: bool = False,
        privileged: bool = False,
        sensitive_resource: bool = False,
        non_local: bool = False,
    ) -> tuple[RiskLevel, int]:
        score = 0

        if denied:
            score += 20

        if repeated_denied:
            score += 30

        if privileged:
            score += 20

        if sensitive_resource:
            score += 20

        if non_local:
            score += 10

        if score >= 70:
            level = RiskLevel.CRITICAL
        elif score >= 50:
            level = RiskLevel.HIGH
        elif score >= 25:
            level = RiskLevel.MEDIUM
        else:
            level = RiskLevel.LOW

        return level, score