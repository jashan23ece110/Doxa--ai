"""
Security Memory Engine.

Maintains previous investigations, historical threats, IOC history, analyst decisions,
recurring attack patterns, and remediation history.
Integrates with the Enterprise Memory Platform.
"""

import threading
import time
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from app.core.logging import security_logger


class SecurityMemoryRecord(BaseModel):
    record_id: str
    category: str  # investigation, threat_history, ioc_history, analyst_decision
    summary: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    timestamp: float = Field(default_factory=time.time)


class SecurityMemoryEngine:
    """Thread-safe Security Memory Engine."""

    def __init__(self):
        self._lock = threading.Lock()
        self._memory_store: Dict[str, SecurityMemoryRecord] = {}

    def remember_investigation(self, binary_id: str, summary: str, metadata: Optional[Dict[str, Any]] = None) -> SecurityMemoryRecord:
        """Stores investigation outcome in security memory."""
        rec_id = f"mem_sec_{binary_id[:8]}"
        rec = SecurityMemoryRecord(
            record_id=rec_id,
            category="investigation",
            summary=summary,
            metadata=metadata or {},
        )

        with self._lock:
            self._memory_store[rec_id] = rec

        security_logger.info(f"SecurityMemoryEngine: Remembered investigation '{rec_id}' for binary '{binary_id}'.")
        return rec

    def recall_history(self, category: str = "investigation", limit: int = 50) -> List[SecurityMemoryRecord]:
        """Retrieves historical security memory records."""
        with self._lock:
            records = [r for r in self._memory_store.values() if r.category == category]
            return sorted(records, key=lambda r: r.timestamp, reverse=True)[:limit]


# Global SecurityMemoryEngine instance
security_memory_engine = SecurityMemoryEngine()
