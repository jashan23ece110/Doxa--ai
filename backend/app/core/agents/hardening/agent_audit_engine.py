"""
Agent Audit Engine.

Tracks complete agent activity lineage, tool invocation history, decision provenance,
and workflow execution logs.
"""

import threading
import time
import uuid
from typing import Dict, Any, List
from pydantic import BaseModel, Field
from app.core.logging import security_logger


class AgentAuditLog(BaseModel):
    audit_id: str = Field(default_factory=lambda: f"aaud_{uuid.uuid4().hex[:8]}")
    agent_id: str
    action_type: str
    target_resource: str
    decision_provenance: str = "PolicyApproved"
    timestamp: float = Field(default_factory=time.time)


class AgentAuditEngine:
    """Thread-safe Agent Audit Engine."""

    def __init__(self):
        self._lock = threading.Lock()
        self._logs: List[AgentAuditLog] = []

    def record_activity(self, agent_id: str, action_type: str, target_resource: str) -> AgentAuditLog:
        """
        Records an auditable agent activity entry.

        Args:
            agent_id: Target agent ID.
            action_type: Category of action.
            target_resource: Target resource string.

        Returns:
            AgentAuditLog object.
        """
        log = AgentAuditLog(agent_id=agent_id, action_type=action_type, target_resource=target_resource)
        with self._lock:
            self._logs.append(log)
            security_logger.info(f"AgentAuditEngine: Recorded audit log '{log.audit_id}' for agent '{agent_id}' ({action_type}).")
        return log


# Global AgentAuditEngine instance
agent_audit_engine = AgentAuditEngine()
