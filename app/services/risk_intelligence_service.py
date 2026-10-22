from app.models.enums import RiskLevel


class RiskIntelligenceService:
    """Converts behavioural anomalies into risk intelligence."""

    def evaluate_behaviour_risk(
        self,
        *,
        anomaly_count: int,
        confidence: float = 1.0,
    ) -> tuple[RiskLevel, int]:

        score = 0

        if anomaly_count >= 1:
            score += 25

        if anomaly_count >= 2:
            score += 25

        if anomaly_count >= 3:
            score += 25

        if confidence < 0.5:
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