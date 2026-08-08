"""
JSON Integration Repository for Universal Integration Platform.

Persists registered connectors, configs, credential metadata, and health history to disk
(./integration_data/connectors.json) across application restarts.
"""

import json
import os
import threading
from typing import Dict, Any, List, Optional
from app.core.config import settings
from app.core.logging import logger
from app.core.integrations.integration_models import ConnectorConfig


class JSONIntegrationRepository:
    """Thread-safe JSON repository for integration connector persistence."""

    def __init__(self, file_path: str = "./integration_data/connectors.json"):
        self.file_path = file_path
        self._lock = threading.Lock()
        self._configs: Dict[str, ConnectorConfig] = {}
        self._ensure_storage_dir()
        self._load_from_disk()

    def _ensure_storage_dir(self) -> None:
        """Ensures storage directory exists."""
        dir_path = os.path.dirname(self.file_path)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)

    def _load_from_disk(self) -> None:
        """Loads connector configs from disk."""
        if not os.path.exists(self.file_path):
            return

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            for item in data:
                c = ConnectorConfig.model_validate(item)
                self._configs[c.connector_id] = c

            logger.info(f"Loaded {len(self._configs)} connectors from disk ({self.file_path}).")
        except Exception as e:
            logger.error(f"Failed to load connectors from disk: {e}")

    def _save_to_disk(self) -> None:
        """Saves connector configs to disk."""
        try:
            data = [c.model_dump() for c in self._configs.values()]
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Failed to save connectors to disk: {e}")

    def save_connector(self, config: ConnectorConfig) -> None:
        """Saves or updates a connector config in repository."""
        with self._lock:
            self._configs[config.connector_id] = config
            limit = getattr(settings, "MAX_CONNECTORS", 500)
            if len(self._configs) > limit:
                oldest = min(self._configs.keys(), key=lambda k: self._configs[k].created_at)
                del self._configs[oldest]
            self._save_to_disk()

    def get_connector(self, connector_id: str) -> Optional[ConnectorConfig]:
        """Retrieves connector config by ID."""
        with self._lock:
            return self._configs.get(connector_id)

    def list_connectors(self) -> List[ConnectorConfig]:
        """Lists registered connectors."""
        with self._lock:
            return list(self._configs.values())


# Global JSONIntegrationRepository instance
integration_repository = JSONIntegrationRepository()
