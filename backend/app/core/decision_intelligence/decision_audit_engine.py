"""
Enterprise Decision Audit Engine.

Maintains complete decision lineage: Request -> Context -> Evidence -> Alternatives -> Models -> Evaluation -> Recommendation -> Approval -> Outcome.
"""

import threading
import time
from typing import Dict, Any, List
from app.core.logging import security_logger
from app.core.decision_intelligence.decision_types import DecisionAudit


class DecisionAuditEngine:
    """Thread-safe Enterprise Decision Audit Engine."""

    def __init__(self):
        self._lock = threading.Lock()
        self._audits: List[DecisionAudit] = []

    def record_decision_lineage(self, request_id: str, steps: List[str]) -> DecisionAudit:
        """
        Records reproducible decision lineage entry.

        Args:
            request_id: Request ID string.
            steps: Lineage step names list.

        Returns:
            DecisionAudit object.
        """
        audit = DecisionAudit(request_id=request_id, lineage_steps=steps, model_version="1.0.0", is_reproducible=True)
        with self._lock:
            self._audits.append(audit)
            security_logger.info(f"DecisionAuditEngine: Recorded decision audit '{audit.audit_id}' for request '{request_id}' ({len(steps)} steps).")
        return audit


# Global DecisionAuditEngine instance
decision_audit_engine = DecisionAuditEngine()
