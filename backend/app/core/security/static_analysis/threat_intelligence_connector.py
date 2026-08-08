"""
Threat Intelligence Connector.

Enterprise threat intelligence abstraction supporting future integrations with:
VirusTotal, MalwareBazaar, MISP, OpenCTI, and internal IOC databases.
Includes async provider registry, caching, provider priority, and graceful fallback.
"""

import asyncio
import threading
import time
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from app.core.logging import security_logger
from app.core.security.security_types import IOC, ThreatSeverity, ThreatActorProfile


class BaseThreatIntelProvider(ABC):
    """Abstract Strategy interface for threat intelligence providers."""

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def priority(self) -> int:
        pass

    @abstractmethod
    async def lookup_hash(self, sha256_hash: str) -> Optional[Dict[str, Any]]:
        pass


class InternalIOCDatabaseProvider(BaseThreatIntelProvider):
    """Local / internal IOC database provider."""

    @property
    def name(self) -> str:
        return "Internal_IOC_Database"

    @property
    def priority(self) -> int:
        return 100  # Highest priority

    async def lookup_hash(self, sha256_hash: str) -> Optional[Dict[str, Any]]:
        # Mock internal database lookup fallback
        return {
            "source": self.name,
            "found": False,
            "reputation_score": 0.0,
            "threat_family": None,
        }


class ThreatIntelligenceConnector:
    """Enterprise Threat Intelligence Connector with Provider Registry and Caching."""

    def __init__(self):
        self._lock = threading.Lock()
        self._providers: List[BaseThreatIntelProvider] = [InternalIOCDatabaseProvider()]
        self._cache: Dict[str, Dict[str, Any]] = {}

    def register_provider(self, provider: BaseThreatIntelProvider):
        """Registers a new threat intelligence provider."""
        with self._lock:
            self._providers.append(provider)
            self._providers.sort(key=lambda p: p.priority, reverse=True)
            security_logger.info(f"ThreatIntelligenceConnector: Registered provider '{provider.name}' (priority={provider.priority}).")

    async def query_hash(self, sha256_hash: str) -> Dict[str, Any]:
        """
        Queries threat intelligence providers sequentially by priority with caching and graceful fallback.

        Args:
            sha256_hash: SHA256 file hash to query.

        Returns:
            Aggregated threat intelligence result dict.
        """
        with self._lock:
            if sha256_hash in self._cache:
                security_logger.debug(f"ThreatIntelligenceConnector: Cache hit for SHA256 {sha256_hash[:8]}")
                return self._cache[sha256_hash]

        with self._lock:
            providers = list(self._providers)

        for provider in providers:
            try:
                result = await provider.lookup_hash(sha256_hash)
                if result and result.get("found", False):
                    with self._lock:
                        self._cache[sha256_hash] = result
                    return result
            except Exception as e:
                security_logger.error(f"ThreatIntelligenceConnector: Provider '{provider.name}' failed: {e}")

        # Fallback response
        fallback_res = {
            "sha256": sha256_hash,
            "found": False,
            "reputation_score": 0.0,
            "threat_family": "unknown",
            "queried_providers_count": len(providers),
            "queried_at": time.time(),
        }

        with self._lock:
            self._cache[sha256_hash] = fallback_res
        return fallback_res


# Global ThreatIntelligenceConnector instance
threat_intel_connector = ThreatIntelligenceConnector()
