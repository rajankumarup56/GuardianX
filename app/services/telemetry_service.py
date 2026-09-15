from typing import Any


class TelemetryService:
    """Receives and validates telemetry in the software simulation."""

    def validate(self, telemetry: dict[str, Any]) -> bool:
        required_fields = {"device_id", "timestamp"}

        return required_fields.issubset(telemetry)