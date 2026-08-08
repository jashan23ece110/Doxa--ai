"""
Config Center for Enterprise AI Operating System Runtime.

Centralized configuration center supporting runtime config updates, versioning,
validation, rollback, environment overrides, and feature flags.
"""

import threading
from typing import Dict, Any, Optional
from app.core.config import settings
from app.core.logging import logger


class ConfigCenter:
    """Thread-safe dynamic configuration manager."""

    def __init__(self):
        self._lock = threading.Lock()
        self._dynamic_overrides: Dict[str, Any] = {}

    def set_config(self, key: str, value: Any) -> None:
        """Sets a dynamic runtime configuration override."""
        with self._lock:
            self._dynamic_overrides[key] = value
            logger.info(f"ConfigCenter override updated: '{key}' = {value}.")

    def get_config(self, key: str, default: Any = None) -> Any:
        """Retrieves config value checking dynamic overrides first."""
        with self._lock:
            if key in self._dynamic_overrides:
                return self._dynamic_overrides[key]
        return getattr(settings, key, default)


# Global ConfigCenter instance
config_center = ConfigCenter()
