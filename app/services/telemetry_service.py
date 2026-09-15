from typing import Any


class TelemetryService:
    """Normalizes telemetry received from devices or simulators."""

    ALLOWED_FIELDS = {
        "battery",
        "altitude",
        "speed",
        "latitude",
        "longitude",
        "heading",
        "temperature",
        "flight_mode",
    }

    def normalize(self, telemetry: dict[str, Any]) -> dict[str, Any]:
        return {
            key: value
            for key, value in telemetry.items()
            if key in self.ALLOWED_FIELDS
        }