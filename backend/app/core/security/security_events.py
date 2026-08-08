"""
Security Event Bus for Enterprise Zero-Trust Security Platform.

Publishes and routes security events: LOGIN, LOGOUT, ACCESS_DENIED, PERMISSION_GRANTED,
SECRET_ROTATED, API_KEY_CREATED, API_KEY_REVOKED, POLICY_UPDATED, AUDIT_LOG_CREATED.
"""

from typing import Dict, Any, List, Callable, Coroutine
from app.core.logging import security_logger
from app.core.security.security_models import SecurityEvent


class SecurityEventBus:
    """Async security event broker."""

    def __init__(self):
        self._listeners: Dict[str, List[Callable[[SecurityEvent], Coroutine[Any, Any, None]]]] = {}

    def subscribe(self, event_type: str, listener: Callable[[SecurityEvent], Coroutine[Any, Any, None]]) -> None:
        """Subscribes an async listener to a security event type."""
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(listener)

    async def publish(self, event: SecurityEvent) -> int:
        """Publishes a security event to all subscribed listeners."""
        listeners = self._listeners.get(event.event_type, [])
        for listener in listeners:
            try:
                await listener(event)
            except Exception as e:
                security_logger.error(f"Error handling security event '{event.event_type}': {e}")
        return len(listeners)


class SecurityResearchEventType:
    """Domain events for security research and reverse engineering."""
    FILE_UPLOADED = "FILE_UPLOADED"
    ANALYSIS_STARTED = "ANALYSIS_STARTED"
    STATIC_ANALYSIS_COMPLETED = "STATIC_ANALYSIS_COMPLETED"
    DYNAMIC_ANALYSIS_COMPLETED = "DYNAMIC_ANALYSIS_COMPLETED"
    THREAT_IDENTIFIED = "THREAT_IDENTIFIED"
    REPORT_GENERATED = "REPORT_GENERATED"
    FORENSICS_COMPLETED = "FORENSICS_COMPLETED"
    SESSION_FINISHED = "SESSION_FINISHED"


async def publish_security_event(event_type: str, details: Dict[str, Any], actor: str = "system") -> SecurityEvent:
    """Convenience helper to publish a SecurityEvent onto the bus."""
    event = SecurityEvent(
        event_type=event_type,
        actor=actor,
        details=details,
    )
    await security_event_bus.publish(event)
    return event


# Global SecurityEventBus instance
security_event_bus = SecurityEventBus()
