import hmac
import hashlib
import time
from typing import Dict, Any, Tuple

class SecurityValidator:
    """
    GuardianX Core Security & Validation Engine
    Enterprise-grade defensive layer protecting autonomous connected systems (drones/IoT) against:
    - Out-of-bounds telemetry tampering
    - Replay attacks via timestamp drift checks
    - Unauthorized payload modifications via HMAC-SHA256 signatures
    """
    def __init__(self, secret_key: str = "guardianx-default-secret-key"):
        self.secret_key = secret_key.encode()
        self.max_allowed_drift_seconds = 30.0

    def validate_timestamp_drift(self, payload_timestamp: float) -> Tuple[bool, str]:
        """Validates that telemetry timestamp is within acceptable range (Replay attack defense)."""
        current_time = time.time()
        drift = abs(current_time - payload_timestamp)
        if drift > self.max_allowed_drift_seconds:
            return False, f"Replay attack detected or clock drift too high ({drift:.2f}s drift)."
        return True, "Timestamp valid."

    def verify_hmac_signature(self, payload_bytes: bytes, provided_signature: str) -> bool:
        """Verifies HMAC-SHA256 payload signature for tamper defense."""
        if not provided_signature:
            return False
        expected_signature = hmac.new(self.secret_key, payload_bytes, hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected_signature, provided_signature)

    def validate_telemetry_bounds(self, data: Dict[str, Any]) -> Tuple[bool, str]:
        """Sanitizes and checks telemetry numeric bounds for physical safety."""
        speed = data.get("speed", 0.0)
        altitude = data.get("altitude", 0.0)

        if speed < 0 or speed > 500.0:
            return False, f"Telemetry anomaly: speed {speed} out of physical bounds."
        if altitude < -100 or altitude > 15000.0:
            return False, f"Telemetry anomaly: altitude {altitude} out of valid operating range."

        return True, "Payload bounds valid."

    def evaluate_request(
        self, 
        data: Dict[str, Any], 
        payload_bytes: bytes = b"", 
        signature: str = ""
    ) -> Tuple[bool, str]:
        """Comprehensive multi-layer security evaluation."""
        bounds_ok, bounds_msg = self.validate_telemetry_bounds(data)
        if not bounds_ok:
            return False, bounds_msg

        if "timestamp" in data:
            ts_ok, ts_msg = self.validate_timestamp_drift(float(data["timestamp"]))
            if not ts_ok:
                return False, ts_msg

        if signature and not self.verify_hmac_signature(payload_bytes, signature):
            return False, "Tamper detected: HMAC signature verification failed."

        return True, "Security validation passed."