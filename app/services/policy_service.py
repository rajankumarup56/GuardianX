from app.models.enums import SecurityDecision


class PolicyService:
    """Applies deterministic security policies."""

    def evaluate(self, authenticated: bool) -> SecurityDecision:
        if not authenticated:
            return SecurityDecision.BLOCK

        return SecurityDecision.ALLOW