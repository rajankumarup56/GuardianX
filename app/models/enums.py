from enum import Enum


class SecurityDecision(str, Enum):
    ALLOW = "ALLOW"
    ALERT = "ALERT"
    RESTRICT = "RESTRICT"
    BLOCK = "BLOCK"
    SAFE_RESPONSE = "SAFE_RESPONSE"


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class IncidentStatus(str, Enum):
    OPEN = "OPEN"
    REVIEWED = "REVIEWED"
    CONFIRMED = "CONFIRMED"
    FALSE_POSITIVE = "FALSE_POSITIVE"


class UserRole(str, Enum):
    SUPER_ADMIN = "SUPER_ADMIN"
    SECURITY_ADMIN = "SECURITY_ADMIN"
    SYSTEM_ADMIN = "SYSTEM_ADMIN"
    AUDITOR = "AUDITOR"
    VIEWER = "VIEWER"