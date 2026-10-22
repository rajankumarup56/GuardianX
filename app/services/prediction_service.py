from app.models.enums import RiskLevel


class PredictionService:
    """Predicts near-term risk escalation from current risk signals."""

    def predict(
        self,
        *,
        current_risk: RiskLevel,
        anomaly_count: int,
        trend_increasing: bool = False,
    ) -> dict:
        escalation = 0

        if current_risk == RiskLevel.MEDIUM:
            escalation += 1
        elif current_risk == RiskLevel.HIGH:
            escalation += 2
        elif current_risk == RiskLevel.CRITICAL:
            escalation += 3

        if anomaly_count >= 2:
            escalation += 1

        if trend_increasing:
            escalation += 1

        if escalation >= 4:
            predicted_risk = RiskLevel.CRITICAL
        elif escalation >= 3:
            predicted_risk = RiskLevel.HIGH
        elif escalation >= 1:
            predicted_risk = RiskLevel.MEDIUM
        else:
            predicted_risk = RiskLevel.LOW

        return {
            "predicted_risk": predicted_risk,
            "escalation_score": escalation,
            "trend_increasing": trend_increasing,
        }
        