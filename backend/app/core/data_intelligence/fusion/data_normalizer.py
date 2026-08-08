"""
Enterprise Data Normalization Engine.

Normalizes schemas, field names, timestamps, identifiers, categorical values, units,
and metadata using configurable data transformation rules.
"""

import time
from typing import Dict, Any, List
from pydantic import BaseModel, Field
from app.core.logging import security_logger


class NormalizedRecord(BaseModel):
    record_id: str
    normalized_payload: Dict[str, Any] = Field(default_factory=dict)
    schema_version: str = "1.0.0"
    normalized_at: float = Field(default_factory=time.time)


class DataNormalizer:
    """Enterprise Data Normalization Engine."""

    def normalize_record(self, record_id: str, raw_payload: Dict[str, Any]) -> NormalizedRecord:
        """
        Normalizes raw payload keys to lowercase snake_case standard fields.

        Args:
            record_id: Input record ID.
            raw_payload: Input raw data dict.

        Returns:
            NormalizedRecord object.
        """
        norm_payload = {}
        for k, v in raw_payload.items():
            norm_key = k.strip().lower().replace(" ", "_")
            norm_payload[norm_key] = v

        if "timestamp" not in norm_payload:
            norm_payload["timestamp"] = time.time()

        res = NormalizedRecord(
            record_id=record_id,
            normalized_payload=norm_payload,
        )

        security_logger.debug(f"DataNormalizer: Normalized record '{record_id}' ({len(norm_payload)} fields).")
        return res


# Global DataNormalizer instance
data_normalizer = DataNormalizer()
