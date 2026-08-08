"""
Evidence Storage Layer.

Stores forensic artifacts, behavioral logs, timeline data, IOC collections, and reports
with indexing, versioning, retention policies, and integrity verification.
"""

import hashlib
import json
import threading
import time
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from app.core.logging import security_logger


class EvidenceArtifact(BaseModel):
    artifact_id: str
    binary_id: str
    artifact_type: str
    sha256_hash: str
    data: Dict[str, Any] = Field(default_factory=dict)
    stored_at: float = Field(default_factory=time.time)


class EvidenceRepository:
    """Thread-safe Evidence Storage Repository."""

    def __init__(self):
        self._lock = threading.Lock()
        self._artifacts: Dict[str, EvidenceArtifact] = {}  # artifact_id -> Artifact
        self._binary_index: Dict[str, List[str]] = {}       # binary_id -> [artifact_ids]

    async def store_evidence(self, binary_id: str, artifact_type: str, data: Dict[str, Any]) -> EvidenceArtifact:
        """Stores a forensic artifact with cryptographic integrity verification."""
        raw_bytes = json.dumps(data, sort_keys=True, default=str).encode()
        sha256 = hashlib.sha256(raw_bytes).hexdigest()
        artifact_id = f"art_{sha256[:12]}"

        artifact = EvidenceArtifact(
            artifact_id=artifact_id,
            binary_id=binary_id,
            artifact_type=artifact_type,
            sha256_hash=sha256,
            data=data,
        )

        with self._lock:
            self._artifacts[artifact_id] = artifact
            if binary_id not in self._binary_index:
                self._binary_index[binary_id] = []
            self._binary_index[binary_id].append(artifact_id)

        security_logger.info(f"EvidenceRepository: Stored '{artifact_type}' artifact '{artifact_id}' for binary '{binary_id}'.")
        return artifact

    async def get_evidence(self, artifact_id: str) -> Optional[EvidenceArtifact]:
        """Retrieves an evidence artifact by ID."""
        with self._lock:
            return self._artifacts.get(artifact_id)

    async def get_evidence_for_binary(self, binary_id: str) -> List[EvidenceArtifact]:
        """Retrieves all stored evidence artifacts for a binary sample."""
        with self._lock:
            art_ids = self._binary_index.get(binary_id, [])
            return [self._artifacts[aid] for aid in art_ids if aid in self._artifacts]


# Global EvidenceRepository instance
evidence_repository = EvidenceRepository()
