from app.models.command import Command
from app.models.enums import SecurityDecision
from app.models.user import User


class PolicyService:
    """Evaluates whether a user is allowed to issue a command."""

    def evaluate(self, user: User, command: Command) -> SecurityDecision:
        if not user.active:
            return SecurityDecision.BLOCK

        if user.role.value == "VIEWER":
            return SecurityDecision.BLOCK

        return SecurityDecision.ALLOW