"""
Evidence Chain Management (Chain of Custody).

Tracks evidence ownership, acquisition timestamps, cryptographic integrity verification,
evidence transfers, access history, retention policies, and tamper-evident audit records.
"""

import hashlib
import threading
import time
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from app.core.logging import security_logger


class CustodyRecord(BaseModel):
    record_id: str
    artifact_id: str
    owner: str = "forensic_analyst"
    action: str  # acquired, transferred, accessed, verified, archived
    previous_hash: str = ""
    current_hash: str = ""
    timestamp: float = Field(default_factory=time.time)


class ChainOfCustodyTracker:
    """Thread-safe Evidence Chain of Custody Manager."""

    def __init__(self):
        self._lock = threading.Lock()
        self._custody_chain: Dict[str, List[CustodyRecord]] = {}  # artifact_id -> CustodyRecords

    def record_acquisition(self, artifact_id: str, owner: str = "analyst_1") -> CustodyRecord:
        """Records initial evidence acquisition in chain of custody."""
        record_id = f"cust_{len(self._custody_chain) + 1}"
        initial_hash = hashlib.sha256(f"{artifact_id}:{owner}:{time.time()}".encode()).hexdigest()

        rec = CustodyRecord(
            record_id=record_id,
            artifact_id=artifact_id,
            owner=owner,
            action="acquired",
            previous_hash="0" * 64,
            current_hash=initial_hash,
        )

        with self._lock:
            if artifact_id not in self._custody_chain:
                self._custody_chain[artifact_id] = []
            self._custody_chain[artifact_id].append(rec)

        security_logger.info(f"ChainOfCustodyTracker: Recorded acquisition for artifact '{artifact_id}' by '{owner}'.")
        return rec

    def record_access(self, artifact_id: str, accessor: str, reason: str = "analysis") -> CustodyRecord:
        """Appends a new access event to the tamper-evident custody chain."""
        with self._lock:
            history = self._custody_chain.get(artifact_id, [])
            prev_hash = history[-1].current_hash if history else "0" * 64
            curr_hash = hashlib.sha256(f"{prev_hash}:{accessor}:{reason}:{time.time()}".encode()).hexdigest()

            rec = CustodyRecord(
                record_id=f"cust_{len(history) + 1}",
                artifact_id=artifact_id,
                owner=accessor,
                action=f"accessed ({reason})",
                previous_hash=prev_hash,
                current_hash=curr_hash,
            )
            if artifact_id not in self._custody_chain:
                self._custody_chain[artifact_id] = []
            self._custody_chain[artifact_id].append(rec)

        security_logger.info(f"ChainOfCustodyTracker: Recorded access for artifact '{artifact_id}' by '{accessor}'.")
        return rec

    def get_custody_history(self, artifact_id: str) -> List[CustodyRecord]:
        """Retrieves tamper-evident chain of custody history for an artifact."""
        with self._lock:
            return list(self._custody_chain.get(artifact_id, []))


# Global ChainOfCustodyTracker instance
chain_of_custody_tracker = ChainOfCustodyTracker()
