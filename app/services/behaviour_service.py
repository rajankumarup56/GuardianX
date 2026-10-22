from app.models.behaviour import BehaviourProfile


class BehaviourService:
    """Detects deviations from a device's expected behaviour."""

    def analyze(
        self,
        profile: BehaviourProfile,
        *,
        speed: float | None = None,
        altitude: float | None = None,
        temperature: float | None = None,
    ) -> dict:
        deviations: list[str] = []

        if speed is not None:
            if speed < profile.expected_speed_min:
                deviations.append("Speed below expected range.")
            elif speed > profile.expected_speed_max:
                deviations.append("Speed above expected range.")

        if altitude is not None:
            if altitude < profile.expected_altitude_min:
                deviations.append("Altitude below expected range.")
            elif altitude > profile.expected_altitude_max:
                deviations.append("Altitude above expected range.")

        if temperature is not None:
            if temperature > profile.expected_temperature_max:
                deviations.append("Temperature above expected limit.")

        return {
            "anomaly_detected": bool(deviations),
            "deviation_count": len(deviations),
            "deviations": deviations,
        }