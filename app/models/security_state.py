from enum import Enum


class SecurityState(str, Enum):
    SECURE = "SECURE"
    WARNING = "WARNING"
    HIGH_RISK = "HIGH_RISK"
    CRITICAL = "CRITICAL"
    UNKNOWN = "UNKNOWN"


class SafetyState(str, Enum):
    SAFE = "SAFE"
    CAUTION = "CAUTION"
    UNSAFE = "UNSAFE"
    EMERGENCY = "EMERGENCY"
    UNKNOWN = "UNKNOWN"