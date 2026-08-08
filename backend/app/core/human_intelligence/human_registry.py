"""
Human Intelligence Dynamic Plugin Registry.

Provides dynamic registry for behavior analyzers, awareness providers, training providers,
assessment engines, organizational intelligence providers, and analytics plugins.
"""

import threading
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from app.core.logging import security_logger


class HumanIntelligencePluginMetadata(BaseModel):
    plugin_id: str
    name: str
    version: str = "1.0.0"
    capability: str  # behavior_analysis, awareness, training, assessment, org_intelligence
    description: str


class HumanRegistry:
    """Thread-safe Dynamic Human Intelligence Plugin Registry."""

    def __init__(self):
        self._lock = threading.Lock()
        self._plugins: Dict[str, HumanIntelligencePluginMetadata] = {}

    def register_plugin(self, plugin: HumanIntelligencePluginMetadata):
        """Registers a new plugin metadata entry."""
        with self._lock:
            self._plugins[plugin.plugin_id] = plugin
            security_logger.info(f"HumanRegistry: Registered plugin '{plugin.name}' ({plugin.capability}) version {plugin.version}.")

    def discover_plugins(self, capability: Optional[str] = None) -> List[HumanIntelligencePluginMetadata]:
        """Discovers registered plugins filtered by capability."""
        with self._lock:
            if capability:
                return [p for p in self._plugins.values() if p.capability == capability]
            return list(self._plugins.values())


# Global HumanRegistry instance
human_registry = HumanRegistry()
