"""
Data Connector Registry.

Dynamic registry for database, file, API, streaming, message queue, and cloud storage connectors.
Supports auto-registration, dependency resolution, versioning, and capability discovery.
"""

import threading
from typing import Dict, Any, List, Optional
from app.core.logging import security_logger
from app.core.data_intelligence.data_intelligence_types import DataConnector, DataSourceType


class ConnectorRegistry:
    """Thread-safe Data Connector Registry."""

    def __init__(self):
        self._lock = threading.Lock()
        self._connectors: Dict[str, DataConnector] = {}

    def register_connector(self, name: str, connector_type: DataSourceType, version: str = "1.0.0", capabilities: Optional[List[str]] = None) -> DataConnector:
        """Registers a new data connector in the platform registry."""
        caps = capabilities or ["ingest", "validate", "stream"]
        conn = DataConnector(
            name=name,
            connector_type=connector_type,
            version=version,
            capabilities=caps,
        )
        with self._lock:
            self._connectors[conn.connector_id] = conn
            security_logger.info(f"ConnectorRegistry: Registered connector '{name}' ({conn.connector_id}, type={connector_type.value}).")
        return conn

    def get_connector(self, connector_id: str) -> Optional[DataConnector]:
        """Retrieves connector details by ID."""
        with self._lock:
            return self._connectors.get(connector_id)

    def list_connectors_by_type(self, connector_type: DataSourceType) -> List[DataConnector]:
        """Lists registered connectors matching a source type."""
        with self._lock:
            return [c for c in self._connectors.values() if c.connector_type == connector_type]


# Global ConnectorRegistry instance
connector_registry = ConnectorRegistry()
