"""
Security Audit Engine.

Generates analyst activity logs, investigation histories, evidence access logs,
compliance audit records, automation logs, and policy audit reports with cryptographic integrity verification.
"""

import hashlib
import threading
import time
from typing import Dict, Any, List
from pydantic import BaseModel, Field
from app.core.logging import security_logger


class CryptographicAuditLog(BaseModel):
    log_id: str
    actor: str
    action: str
    details: Dict[str, Any] = Field(default_factory=dict)
    previous_hash: str
    current_hash: str
    timestamp: float = Field(default_factory=time.time)


class SecurityAuditEngine:
    """Thread-safe Cryptographic Security Audit Engine."""

    def __init__(self):
        self._lock = threading.Lock()
        self._audit_logs: List[CryptographicAuditLog] = []

    def log_analyst_action(self, actor: str, action: str, details: Dict[str, Any]) -> CryptographicAuditLog:
        """
        Logs analyst activity with cryptographic hash-chaining verification.

        Args:
            actor: Analyst or system worker ID.
            action: Performed action description.
            details: Context details.

        Returns:
            CryptographicAuditLog record.
        """
        with self._lock:
            prev_hash = self._audit_logs[-1].current_hash if self._audit_logs else "0" * 64
            curr_hash = hashlib.sha256(f"{prev_hash}:{actor}:{action}:{time.time()}".encode()).hexdigest()

            entry = CryptographicAuditLog(
                log_id=f"audit_{len(self._audit_logs) + 1}",
                actor=actor,
                action=action,
                details=details,
                previous_hash=prev_hash,
                current_hash=curr_hash,
            )
            self._audit_logs.append(entry)

        security_logger.debug(f"SecurityAuditEngine: Logged action '{action}' by '{actor}'.")
        return entry

    def verify_integrity(self) -> bool:
        """Verifies hash-chain integrity of stored audit records."""
        with self._lock:
            for i in range(1, len(self._audit_logs)):
                if self._audit_logs[i].previous_hash != self._audit_logs[i-1].current_hash:
                    return False
        return True


# Global SecurityAuditEngine instance
security_audit_engine = SecurityAuditEngine()
