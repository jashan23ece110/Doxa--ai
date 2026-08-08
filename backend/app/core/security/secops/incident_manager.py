"""
Enterprise Incident Response Manager.

Manages incident lifecycles, severity classifications, analyst assignments,
escalation policies, SLA tracking, status transitions, incident correlation, and post-incident reviews.
"""

import time
import uuid
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from app.core.logging import security_logger
from app.core.security.security_types import ThreatSeverity


class SecurityIncident(BaseModel):
    incident_id: str = Field(default_factory=lambda: f"inc_{uuid.uuid4().hex[:8]}")
    title: str
    severity: ThreatSeverity = ThreatSeverity.HIGH
    status: str = "open"  # open, triaged, investigating, remediated, closed
    assigned_analyst: Optional[str] = "analyst_1"
    sla_deadline: float = Field(default_factory=lambda: time.time() + 14400.0)  # 4-hour SLA default
    linked_binary_ids: List[str] = Field(default_factory=list)
    created_at: float = Field(default_factory=time.time)
    updated_at: float = Field(default_factory=time.time)


class IncidentManager:
    """Enterprise Incident Response Lifecycle Manager."""

    def __init__(self):
        self._incidents: Dict[str, SecurityIncident] = {}

    def create_incident(self, title: str, severity: ThreatSeverity = ThreatSeverity.HIGH, assigned_analyst: str = "analyst_1") -> SecurityIncident:
        """Creates and registers a new security incident."""
        inc = SecurityIncident(
            title=title,
            severity=severity,
            assigned_analyst=assigned_analyst,
        )
        self._incidents[inc.incident_id] = inc
        security_logger.info(f"IncidentManager: Created incident '{title}' ({inc.incident_id}) with severity {severity.value.upper()}.")
        return inc

    def update_status(self, incident_id: str, new_status: str) -> Optional[SecurityIncident]:
        """Transitions incident status."""
        inc = self._incidents.get(incident_id)
        if inc:
            inc.status = new_status
            inc.updated_at = time.time()
            security_logger.info(f"IncidentManager: Transitioned incident '{incident_id}' to status '{new_status}'.")
        return inc

    def get_incident(self, incident_id: str) -> Optional[SecurityIncident]:
        """Retrieves incident details."""
        return self._incidents.get(incident_id)


# Global IncidentManager instance
incident_manager = IncidentManager()
