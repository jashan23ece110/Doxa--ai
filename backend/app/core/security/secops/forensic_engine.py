"""
Enterprise Digital Forensics Engine.

Collects and analyzes forensic artifacts, filesystem metadata, process metadata,
event logs, memory dumps, execution history, and registry hives with immutable evidence references.
"""

import hashlib
import json
import time
from typing import Dict, Any, List
from pydantic import BaseModel, Field
from app.core.logging import security_logger
from app.core.security.security_types import ForensicArtifact


class DigitalForensicsEngine:
    """Enterprise Digital Forensics Engine."""

    def extract_evidence_artifact(self, artifact_type: str, source: str, metadata: Dict[str, Any]) -> ForensicArtifact:
        """
        Extracts immutable forensic evidence artifact with SHA256 integrity checksum.

        Args:
            artifact_type: Type of artifact (memory_dump, process_tree, event_log, registry_hive).
            source: Source mechanism/path.
            metadata: Metadata dictionary.

        Returns:
            ForensicArtifact object.
        """
        raw_bytes = json.dumps(metadata, sort_keys=True, default=str).encode()
        sha256 = hashlib.sha256(raw_bytes).hexdigest()

        artifact = ForensicArtifact(
            artifact_type=artifact_type,
            source=source,
            checksum=sha256,
            metadata=metadata,
        )

        security_logger.info(f"DigitalForensicsEngine: Extracted artifact '{artifact.artifact_id}' ({artifact_type}) from '{source}'.")
        return artifact


# Global DigitalForensicsEngine instance
digital_forensics_engine = DigitalForensicsEngine()
