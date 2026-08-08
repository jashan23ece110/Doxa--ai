"""
Enterprise AI Safety Audit Logger.

Creates immutable audit events with timestamps, actor, user, agent, tool,
request IDs, decisions, risk/trust scores, latency, and outcomes.

Stores asynchronously to disk at `./safety_data/safety_audit.json`.
"""

import asyncio
import json
import os
import threading
import time
from typing import Dict, Any, List, Optional
from app.core.logging import logger
from app.core.config import settings
from app.core.safety.safety_types import SafetyAuditRecord


class SafetyAuditLogger:
    """Thread-safe immutable audit logger for the AI Safety layer."""

    def __init__(self, file_path: str = "./safety_data/safety_audit.json"):
        self.file_path = file_path
        self._lock = threading.Lock()
        self._records: List[SafetyAuditRecord] = []
        self._pending_writes: List[SafetyAuditRecord] = []
        self._ensure_storage()
        self._load_from_disk()

    def _ensure_storage(self) -> None:
        """Ensures storage directory exists."""
        dir_path = os.path.dirname(self.file_path)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)

    def _load_from_disk(self) -> None:
        """Loads existing audit records from disk."""
        if not os.path.exists(self.file_path):
            return
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            for item in data:
                self._records.append(SafetyAuditRecord.model_validate(item))
            logger.info(f"SafetyAuditLogger loaded {len(self._records)} records from disk.")
        except Exception as e:
            logger.error(f"Failed to load safety audit logs: {e}")

    def _flush_to_disk(self) -> None:
        """Writes current records to disk (keeps last MAX_AUDIT_HISTORY)."""
        try:
            max_history = settings.MAX_AUDIT_HISTORY
            trimmed = self._records[-max_history:] if len(self._records) > max_history else self._records
            data = [r.model_dump() for r in trimmed]
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Failed to flush safety audit logs to disk: {e}")

    async def log_event(
        self,
        event_type: str,
        actor: str = "system",
        user_id: str = "anonymous",
        agent_id: Optional[str] = None,
        tool_id: Optional[str] = None,
        request_id: Optional[str] = None,
        decision: str = "approved",
        risk_score: float = 0.0,
        trust_score: float = 1.0,
        latency_ms: float = 0.0,
        outcome: str = "success",
        details: Optional[Dict[str, Any]] = None,
    ) -> SafetyAuditRecord:
        """
        Logs an immutable safety audit event.

        All parameters are optional except event_type.
        Recording is thread-safe and persists to disk asynchronously.

        Returns:
            The created SafetyAuditRecord.
        """
        if not settings.AUDIT_ENABLED:
            return SafetyAuditRecord(event_type=event_type)

        record = SafetyAuditRecord(
            actor=actor,
            user_id=user_id,
            agent_id=agent_id,
            tool_id=tool_id,
            request_id=request_id,
            decision=decision,
            risk_score=risk_score,
            trust_score=trust_score,
            latency_ms=latency_ms,
            outcome=outcome,
            event_type=event_type,
            details=details or {},
        )

        with self._lock:
            self._records.append(record)
            self._pending_writes.append(record)

            # Batch flush every 50 pending writes for performance
            if len(self._pending_writes) >= 50:
                self._flush_to_disk()
                self._pending_writes.clear()

        logger.debug(
            f"SafetyAudit '{record.audit_id}': type={event_type}, "
            f"actor={actor}, decision={decision}, risk={risk_score:.4f}, "
            f"trust={trust_score:.4f}, outcome={outcome}"
        )
        return record

    async def flush(self) -> None:
        """Forces a flush of all pending records to disk."""
        with self._lock:
            self._flush_to_disk()
            self._pending_writes.clear()

    def list_records(
        self,
        limit: int = 100,
        event_type: Optional[str] = None,
        user_id: Optional[str] = None,
        decision: Optional[str] = None,
    ) -> List[SafetyAuditRecord]:
        """Lists audit records with optional filtering."""
        with self._lock:
            records = list(self._records)

        if event_type:
            records = [r for r in records if r.event_type == event_type]
        if user_id:
            records = [r for r in records if r.user_id == user_id]
        if decision:
            records = [r for r in records if r.decision == decision]

        return records[-limit:]

    def get_statistics(self) -> Dict[str, Any]:
        """Returns audit statistics summary."""
        with self._lock:
            total = len(self._records)
            if total == 0:
                return {"total": 0}

            approved = sum(1 for r in self._records if r.decision == "approved")
            denied = sum(1 for r in self._records if r.decision == "denied")
            escalated = sum(1 for r in self._records if r.decision == "escalated")
            blocked = sum(1 for r in self._records if r.decision == "blocked")
            avg_risk = sum(r.risk_score for r in self._records) / total
            avg_trust = sum(r.trust_score for r in self._records) / total

            return {
                "total": total,
                "approved": approved,
                "denied": denied,
                "escalated": escalated,
                "blocked": blocked,
                "approval_rate": round(approved / total, 4),
                "avg_risk_score": round(avg_risk, 4),
                "avg_trust_score": round(avg_trust, 4),
                "pending_writes": len(self._pending_writes),
            }


# Global SafetyAuditLogger instance
safety_audit_logger = SafetyAuditLogger()
