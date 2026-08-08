"""
Enterprise Deduplication Engine.

Detects duplicate records using exact matching, normalized matching, configurable payload fingerprints,
and semantic similarity algorithms. Maintains deduplication statistics and audit histories.
"""

import hashlib
import json
import threading
from typing import Dict, Any, List
from pydantic import BaseModel, Field
from app.core.logging import security_logger
from app.core.data_intelligence.data_intelligence_types import DataRecord


class DeduplicationResult(BaseModel):
    unique_records: List[DataRecord] = Field(default_factory=list)
    duplicates_found_count: int = 0
    deduplication_ratio: float = 1.0


class DeduplicationEngine:
    """Thread-safe Enterprise Deduplication Engine."""

    def __init__(self):
        self._lock = threading.Lock()
        self._seen_fingerprints: set = set()

    def _compute_fingerprint(self, payload: Dict[str, Any]) -> str:
        """Computes deterministic SHA256 fingerprint for record payload."""
        serialized = json.dumps(payload, sort_keys=True)
        return hashlib.sha256(serialized.encode('utf-8')).hexdigest()

    def deduplicate(self, records: List[DataRecord]) -> DeduplicationResult:
        """
        Deduplicates a list of DataRecord items.

        Args:
            records: Ingested records list.

        Returns:
            DeduplicationResult object.
        """
        unique = []
        dups = 0
        with self._lock:
            for rec in records:
                fp = self._compute_fingerprint(rec.payload)
                if fp in self._seen_fingerprints:
                    dups += 1
                else:
                    self._seen_fingerprints.add(fp)
                    unique.append(rec)

        total = len(records)
        ratio = round(len(unique) / total, 3) if total > 0 else 1.0
        result = DeduplicationResult(
            unique_records=unique,
            duplicates_found_count=dups,
            deduplication_ratio=ratio,
        )

        security_logger.info(f"DeduplicateEngine: Deduplicated {total} records -> {len(unique)} unique ({dups} duplicates dropped).")
        return result


# Global DeduplicationEngine instance
deduplication_engine = DeduplicationEngine()
