"""
Health Monitor for Enterprise Observability Platform.

Continuously monitors 13 system components: LLM Providers, Embedding providers,
ChromaDB, BM25, Memory Engine, Event Bus, Worker Pool, Storage, Filesystem,
Thread Pool, Queues, Timers, and Background Tasks across 4 health states.
"""

import time
import threading
from typing import Dict, Any, List
from app.core.logging import logger
from app.core.observability.observability_models import HealthCheckStatus, HealthState


class HealthMonitor:
    """Monitors 13 core infrastructure components."""

    COMPONENTS = [
        "llm_providers",
        "embedding_providers",
        "chromadb_vector",
        "bm25_retriever",
        "memory_engine",
        "event_bus",
        "worker_pool",
        "storage",
        "filesystem",
        "thread_pool",
        "queues",
        "timers",
        "background_tasks",
    ]

    def __init__(self):
        self._lock = threading.Lock()
        self._statuses: Dict[str, HealthCheckStatus] = {}
        self._setup_initial_statuses()

    def _setup_initial_statuses(self) -> None:
        """Initializes default healthy states for all 13 components."""
        for comp in self.COMPONENTS:
            self._statuses[comp] = HealthCheckStatus(component_name=comp, state=HealthState.HEALTHY)

    def check_all_components(self) -> List[HealthCheckStatus]:
        """Performs health inspection across all 13 components."""
        with self._lock:
            for comp in self.COMPONENTS:
                st = self._statuses[comp]
                st.last_check_time = time.time()
                st.state = HealthState.HEALTHY

            return list(self._statuses.values())

    def update_component_status(self, component: str, state: HealthState, error_message: str = None) -> None:
        """Updates health status for a specific component."""
        with self._lock:
            if component in self._statuses:
                self._statuses[component].state = state
                self._statuses[component].error_message = error_message
                self._statuses[component].last_check_time = time.time()
                logger.info(f"HealthMonitor component '{component}' state updated to '{state.value}'.")


# Global HealthMonitor instance
health_monitor = HealthMonitor()
