"""
Alert Engine for Enterprise Observability Platform.

Generates operational alerts across 4 severity levels (Info, Warning, Error, Critical)
for latency spikes, memory pressure, queue overload, and provider failures.
"""

import threading
from typing import Dict, Any, List
from app.core.logging import logger
from app.core.observability.observability_models import AlertRecord, AlertSeverity


class AlertEngine:
    """Manages operational alerts and severity escalation."""

    def __init__(self):
        self._lock = threading.Lock()
        self._alerts: List[AlertRecord] = []

    def create_alert(
        self,
        title: str,
        description: str,
        component: str = "general",
        severity: AlertSeverity = AlertSeverity.WARNING,
    ) -> AlertRecord:
        """Generates and logs an operational alert."""
        record = AlertRecord(
            title=title,
            description=description,
            component=component,
            severity=severity,
        )

        with self._lock:
            self._alerts.append(record)
            if len(self._alerts) > 1000:
                self._alerts = self._alerts[-1000:]
            logger.warning(f"ALERT [{severity.value.upper()}] ({component}): {title} - {description}")

        return record

    def list_alerts(self, limit: int = 50) -> List[AlertRecord]:
        """Lists active alerts."""
        with self._lock:
            return self._alerts[-limit:]


# Global AlertEngine instance
alert_engine = AlertEngine()
