from fastapi import APIRouter, Query

from app.services.event_service import EventService


router = APIRouter(prefix="/events", tags=["security-events"])
event_service = EventService()


@router.get("")
def list_security_events(
    limit: int = Query(default=50, ge=1, le=100),
) -> list[dict]:
    """Return recent GuardianX security events."""
    return event_service.list_security_events(limit=limit)


@router.get("/audit")
def list_audit_logs(
    limit: int = Query(default=50, ge=1, le=100),
) -> list[dict]:
    """Return recent GuardianX audit records."""
    return event_service.list_audit_logs(limit=limit)