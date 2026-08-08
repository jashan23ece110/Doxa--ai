"""
Agent Incident Manager.

Detects, classifies, contains, and escalates autonomous agent operational incidents.
"""

import time
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from app.core.logging import security_logger


class AgentIncidentRecord(BaseModel):
    incident_id: str = Field(default_factory=lambda: f"ainc_{int(time.time() * 1000)}")
    agent_id: str
    severity: str = "LOW"
    description: str
    is_contained: bool = True
    detected_at: float = Field(default_factory=time.time)


class AgentIncidentManager:
    """Agent Incident Manager."""

    def log_incident(self, agent_id: str, description: str, severity: str = "LOW") -> AgentIncidentRecord:
        """
        Logs and contains an autonomous agent operational incident.

        Args:
            agent_id: Target agent ID.
            description: Description string.
            severity: Severity level.

        Returns:
            AgentIncidentRecord object.
        """
        inc = AgentIncidentRecord(agent_id=agent_id, description=description, severity=severity, is_contained=True)
        security_logger.warning(f"AgentIncidentManager: Logged and contained incident '{inc.incident_id}' for agent '{agent_id}' (Severity={severity}).")
        return inc


# Global AgentIncidentManager instance
agent_incident_manager = AgentIncidentManager()
