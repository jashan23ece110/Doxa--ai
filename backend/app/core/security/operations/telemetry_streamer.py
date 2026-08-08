"""
Real-Time Security Telemetry Streaming Engine.

Asynchronously streams security events, telemetry ticks, and live audit signals
to WebSocket producers and monitoring sub-systems.
"""

import asyncio
import threading
import time
from typing import Dict, Any, List, Callable, Optional
from pydantic import BaseModel, Field
from app.core.logging import security_logger


class TelemetryEvent(BaseModel):
    event_id: str
    event_type: str  # binary_scanned, ioc_detected, threat_blocked, sandbox_completed
    severity: str = "medium"
    payload: Dict[str, Any] = Field(default_factory=dict)
    timestamp: float = Field(default_factory=time.time)


class TelemetryStreamer:
    """Thread-safe Real-Time Security Telemetry Streaming Engine."""

    def __init__(self):
        self._lock = threading.Lock()
        self._subscribers: List[Callable[[TelemetryEvent], None]] = []
        self._event_buffer: List[TelemetryEvent] = []

    def subscribe(self, callback: Callable[[TelemetryEvent], None]):
        """Subscribes a listener or WebSocket stream producer."""
        with self._lock:
            self._subscribers.append(callback)
            security_logger.info("TelemetryStreamer: Added new telemetry stream subscriber.")

    async def emit_event(self, event_type: str, payload: Dict[str, Any], severity: str = "medium") -> TelemetryEvent:
        """Emits a new real-time security event."""
        event = TelemetryEvent(
            event_id=f"evt_{int(time.time() * 1000)}",
            event_type=event_type,
            severity=severity,
            payload=payload,
        )

        with self._lock:
            self._event_buffer.append(event)
            if len(self._event_buffer) > 1000:
                self._event_buffer.pop(0)
            subs = list(self._subscribers)

        for callback in subs:
            try:
                callback(event)
            except Exception as e:
                security_logger.error(f"TelemetryStreamer: Subscriber callback error: {e}")

        security_logger.debug(f"TelemetryStreamer: Emitted event '{event.event_type}' ({event.event_id}).")
        return event

    def get_recent_events(self, limit: int = 50) -> List[TelemetryEvent]:
        """Retrieves recent event buffer slice."""
        with self._lock:
            return list(self._event_buffer[-limit:])


# Global TelemetryStreamer instance
telemetry_streamer = TelemetryStreamer()
