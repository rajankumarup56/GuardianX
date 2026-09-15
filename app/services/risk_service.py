from app.models.enums import RiskLevel


class RiskService:
    """Calculates security risk from validated events."""

    def classify(self, score: int) -> RiskLevel:
        if score >= 80:
            return RiskLevel.CRITICAL

        if score >= 60:
            return RiskLevel.HIGH

        if score >= 30:
            return RiskLevel.MEDIUM

        return RiskLevel.LOW