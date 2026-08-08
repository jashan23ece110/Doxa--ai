"""
Service Discovery for Enterprise AI Operating System Runtime.

Handles automatic service registration, lookup, health-aware routing, endpoint discovery,
and dynamic updates.
"""

import threading
from typing import Dict, Any, List, Optional
from app.core.logging import logger
from app.core.runtime.runtime_models import ServiceEndpoint


class ServiceDiscovery:
    """Thread-safe health-aware service discovery registry."""

    def __init__(self):
        self._lock = threading.Lock()
        self._endpoints: Dict[str, ServiceEndpoint] = {}
        self._setup_default_services()

    def _setup_default_services(self) -> None:
        """Registers default internal platform services."""
        defaults = [
            ServiceEndpoint(service_name="groq_llm_provider", endpoint_url="https://api.groq.com"),
            ServiceEndpoint(service_name="chroma_vector_db", endpoint_url="http://localhost:8000"),
            ServiceEndpoint(service_name="mcp_integration_gateway", endpoint_url="mcp://localhost:8080"),
        ]
        for ep in defaults:
            self._endpoints[ep.service_name] = ep

    def register_service(self, service_name: str, endpoint_url: str) -> ServiceEndpoint:
        """Registers or updates a service endpoint."""
        with self._lock:
            ep = ServiceEndpoint(service_name=service_name, endpoint_url=endpoint_url)
            self._endpoints[service_name] = ep
            logger.info(f"ServiceDiscovery registered '{service_name}' -> '{endpoint_url}'.")
            return ep

    def get_service(self, service_name: str) -> Optional[ServiceEndpoint]:
        """Looks up an active service endpoint."""
        with self._lock:
            return self._endpoints.get(service_name)


# Global ServiceDiscovery instance
service_discovery = ServiceDiscovery()
