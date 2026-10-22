from app.models.behaviour import BehaviourProfile
from app.models.enums import SecurityDecision
from app.services.behaviour_service import BehaviourService
from app.services.decision_service import DecisionService
from app.services.prediction_service import PredictionService
from app.services.risk_intelligence_service import RiskIntelligenceService


class IntelligenceService:
    """Runs GuardianX behaviour-to-decision intelligence flow."""

    def __init__(self) -> None:
        self.behaviour_service = BehaviourService()
        self.risk_service = RiskIntelligenceService()
        self.prediction_service = PredictionService()
        self.decision_service = DecisionService()

    def analyze(
        self,
        *,
        profile: BehaviourProfile,
        speed: float | None = None,
        altitude: float | None = None,
        temperature: float | None = None,
        trend_increasing: bool = False,
    ) -> dict:

        behaviour = self.behaviour_service.analyze(
            profile,
            speed=speed,
            altitude=altitude,
            temperature=temperature,
        )

        risk_level, risk_score = self.risk_service.evaluate_behaviour_risk(
            anomaly_count=behaviour["deviation_count"],
            confidence=1.0,
        )

        prediction = self.prediction_service.predict(
            current_risk=risk_level,
            anomaly_count=behaviour["deviation_count"],
            trend_increasing=trend_increasing,
        )

        decision = self.decision_service.decide(
            security_risk=risk_level,
            safety_risk=prediction["predicted_risk"],
        )

        return {
            "behaviour": behaviour,
            "risk_level": risk_level,
            "risk_score": risk_score,
            "prediction": prediction,
            "decision": decision,
        }