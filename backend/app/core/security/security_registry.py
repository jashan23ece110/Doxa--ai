"""
Security Subsystem Dynamic Registry.

Manages dynamic auto-registration, dependency resolution, versioning,
and capability discovery for analyzers, scanners, sandbox providers,
forensic engines, RE plugins, and threat intelligence providers.
"""

import threading
from typing import Dict, Any, List, Optional, Type
from app.core.logging import security_logger


class SecurityRegistry:
    """Thread-safe dynamic registry for security research modules."""

    def __init__(self):
        self._lock = threading.Lock()
        self._analyzers: Dict[str, Dict[str, Any]] = {}
        self._scanners: Dict[str, Dict[str, Any]] = {}
        self._sandbox_providers: Dict[str, Dict[str, Any]] = {}
        self._forensic_engines: Dict[str, Dict[str, Any]] = {}
        self._re_plugins: Dict[str, Dict[str, Any]] = {}
        self._intel_providers: Dict[str, Dict[str, Any]] = {}

    def register(
        self,
        category: str,
        name: str,
        provider_class: Type,
        version: str = "1.0.0",
        capabilities: Optional[List[str]] = None,
        dependencies: Optional[List[str]] = None,
    ) -> bool:
        """
        Registers a new security research module.

        Args:
            category: Module category ('analyzer', 'scanner', 'sandbox', 'forensics', 're_plugin', 'intel').
            name: Unique name of the module.
            provider_class: The class implementation.
            version: Semantic version string.
            capabilities: List of capabilities provided.
            dependencies: Required dependency module names.

        Returns:
            True if registered successfully.
        """
        target_dict = self._get_target_dict(category)
        if target_dict is None:
            security_logger.error(f"SecurityRegistry: Unknown category '{category}'")
            return False

        with self._lock:
            target_dict[name] = {
                "name": name,
                "class": provider_class,
                "version": version,
                "capabilities": capabilities or [],
                "dependencies": dependencies or [],
                "instance": None,
            }
            security_logger.info(f"SecurityRegistry: Registered {category} '{name}' v{version}")
        return True

    def get_provider(self, category: str, name: str) -> Optional[Any]:
        """Instantiates or retrieves a registered provider instance."""
        target_dict = self._get_target_dict(category)
        if not target_dict:
            return None

        with self._lock:
            info = target_dict.get(name)
            if not info:
                return None
            if info["instance"] is None:
                try:
                    info["instance"] = info["class"]()
                except Exception as e:
                    security_logger.error(f"SecurityRegistry: Failed to instantiate {category} '{name}': {e}")
                    return None
            return info["instance"]

    def discover_capabilities(self, category: Optional[str] = None) -> Dict[str, List[str]]:
        """Returns map of registered modules and their capabilities."""
        with self._lock:
            results = {}
            categories = [category] if category else ["analyzer", "scanner", "sandbox", "forensics", "re_plugin", "intel"]
            for cat in categories:
                target_dict = self._get_target_dict(cat)
                if target_dict:
                    results[cat] = [
                        f"{name} (v{info['version']}) -> [{', '.join(info['capabilities'])}]"
                        for name, info in target_dict.items()
                    ]
            return results

    def _get_target_dict(self, category: str) -> Optional[Dict[str, Dict[str, Any]]]:
        mapping = {
            "analyzer": self._analyzers,
            "scanner": self._scanners,
            "sandbox": self._sandbox_providers,
            "forensics": self._forensic_engines,
            "re_plugin": self._re_plugins,
            "intel": self._intel_providers,
        }
        return mapping.get(category)


# Global SecurityRegistry instance
security_registry = SecurityRegistry()
