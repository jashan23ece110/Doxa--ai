"""
Connector Registry for Universal Integration Platform.

Dynamic registration, capability tracking, enable/disable toggles, and metadata lookup
across 11 connector protocol types.
"""

import threading
from typing import Dict, Any, List, Optional
from app.core.logging import logger
from app.core.integrations.integration_models import ConnectorConfig, ConnectorMetadata, ConnectorType


class ConnectorRegistry:
    """Thread-safe registry for integration connectors."""

    def __init__(self):
        self._lock = threading.Lock()
        self._configs: Dict[str, ConnectorConfig] = {}
        self._metadata: Dict[str, ConnectorMetadata] = {}

    def register_connector(self, config: ConnectorConfig, metadata: Optional[ConnectorMetadata] = None) -> ConnectorConfig:
        """Registers a connector config and metadata."""
        with self._lock:
            self._configs[config.connector_id] = config
            if metadata:
                self._metadata[config.connector_id] = metadata
            else:
                self._metadata[config.connector_id] = ConnectorMetadata(
                    connector_id=config.connector_id,
                    name=config.name,
                    connector_type=config.connector_type,
                )
            logger.info(f"Registered connector '{config.name}' (ID: {config.connector_id}, Type: {config.connector_type.value}).")
            return config

    def unregister_connector(self, connector_id: str) -> bool:
        """Unregisters a connector."""
        with self._lock:
            if connector_id in self._configs:
                del self._configs[connector_id]
                self._metadata.pop(connector_id, None)
                logger.info(f"Unregistered connector '{connector_id}'.")
                return True
            return False

    def get_config(self, connector_id: str) -> Optional[ConnectorConfig]:
        """Retrieves connector config by ID."""
        with self._lock:
            return self._configs.get(connector_id)

    def get_metadata(self, connector_id: str) -> Optional[ConnectorMetadata]:
        """Retrieves connector metadata by ID."""
        with self._lock:
            return self._metadata.get(connector_id)

    def list_connectors(self, connector_type: Optional[ConnectorType] = None) -> List[ConnectorConfig]:
        """Lists registered connectors."""
        with self._lock:
            configs = list(self._configs.values())
            if connector_type:
                return [c for c in configs if c.connector_type == connector_type]
            return configs


# Global ConnectorRegistry instance
connector_registry = ConnectorRegistry()
