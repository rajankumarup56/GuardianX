from app.models.enums import RiskLevel


class RiskService:
    """Calculates deterministic risk levels from security and telemetry signals."""

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

    def calculate_telemetry_risk(
        self,
        *,
        battery: float | None = None,
        temperature: float | None = None,
        speed: float | None = None,
    ) -> tuple[RiskLevel, int]:
        score = 0

        if battery is not None and battery < 20:
            score += 30

        if temperature is not None and temperature >= 80:
            score += 30

        if speed is not None and speed >= 25:
            score += 20

        if score >= 70:
            level = RiskLevel.CRITICAL
        elif score >= 50:
            level = RiskLevel.HIGH
        elif score >= 25:
            level = RiskLevel.MEDIUM
        else:
            level = RiskLevel.LOW

        return level, score