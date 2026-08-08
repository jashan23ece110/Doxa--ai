"""
Enterprise Decision Audit Engine.

Maintains immutable decision audit logs to support complete decision reconstruction.
"""

import threading
import time
from typing import Dict, Any, List
from app.core.logging import security_logger
from app.core.decision_intelligence.governance.explainability_types import AuditRecord


class DecisionAuditEngine:
    """Thread-safe Enterprise Decision Audit Engine."""

    def __init__(self):
        self._lock = threading.Lock()
        self._audit_records: List[AuditRecord] = []

    def record_audit(self, event_type: str, entity_id: str, details: Dict[str, Any]) -> AuditRecord:
        """
        Records an immutable decision audit entry.

        Args:
            event_type: Event category string.
            entity_id: Target entity ID string.
            details: Context details dictionary.

        Returns:
            AuditRecord object.
        """
        record = AuditRecord(event_type=event_type, entity_id=entity_id, actor="System", details=details)
        with self._lock:
            self._audit_records.append(record)
            security_logger.info(f"DecisionAuditEngine: Recorded audit entry '{record.record_id}' ({event_type} on {entity_id}).")
        return record


# Global DecisionAuditEngine instance
decision_audit_engine = DecisionAuditEngine()
