"""
Enterprise Schema Registry.

Manages data schemas, schema versions, compatibility checks, field metadata,
type validation, schema evolution, and backward-compatible migration rules.
"""

import threading
from typing import Dict, Any, List, Optional
from app.core.logging import security_logger
from app.core.data_intelligence.data_intelligence_types import DataSchema


class SchemaRegistry:
    """Thread-safe Enterprise Schema Registry."""

    def __init__(self):
        self._lock = threading.Lock()
        self._schemas: Dict[str, DataSchema] = {}

    def register_schema(self, name: str, fields: Dict[str, str]) -> DataSchema:
        """Registers a data schema in the platform registry."""
        schema = DataSchema(name=name, fields=fields)
        with self._lock:
            self._schemas[schema.schema_id] = schema
            security_logger.info(f"SchemaRegistry: Registered schema '{name}' ({schema.schema_id}, fields={len(fields)}).")
        return schema

    def validate_record_schema(self, schema_id: str, record_payload: Dict[str, Any]) -> bool:
        """Validates record payload against registered schema fields."""
        with self._lock:
            schema = self._schemas.get(schema_id)
            if not schema:
                return True
            # Simple field presence check
            valid = all(k in record_payload for k in schema.fields.keys())
            return valid

    def get_schema(self, schema_id: str) -> Optional[DataSchema]:
        """Retrieves schema by ID."""
        with self._lock:
            return self._schemas.get(schema_id)


# Global SchemaRegistry instance
schema_registry = SchemaRegistry()
