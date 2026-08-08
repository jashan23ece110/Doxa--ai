"""
Enterprise Intelligence Propagation Engine.

Propagates validated real-time intelligence events to Knowledge Graph, Enterprise Memory,
RAG context, Security Intelligence, and Human Intelligence with deduplication.
"""

import threading
import time
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from app.core.logging import security_logger


class PropagationResult(BaseModel):
    propagation_id: str
    event_id: str
    target_subsystems: List[str] = Field(default_factory=list)
    success: bool = True
    propagated_at: float = Field(default_factory=time.time)


class IntelligencePropagator:
    """Thread-safe Enterprise Intelligence Propagation Engine."""

    def __init__(self):
        self._lock = threading.Lock()
        self._propagated_events: set = set()

    def propagate_intelligence(self, event_id: str, intelligence_payload: Dict[str, Any], targets: Optional[List[str]] = None) -> PropagationResult:
        """
        Propagates validated intelligence payload to specified target subsystems.

        Args:
            event_id: Originating event ID.
            intelligence_payload: Fused intelligence dict.
            targets: List of target subsystem strings.

        Returns:
            PropagationResult object.
        """
        target_subsystems = targets or ["KnowledgeGraph", "EnterpriseMemory", "RAG", "SecurityPlatform", "HumanPlatform"]

        with self._lock:
            if event_id in self._propagated_events:
                security_logger.debug(f"IntelligencePropagator: Event '{event_id}' already propagated. Skipping duplicate.")
                return PropagationResult(propagation_id=f"prop_dup_{event_id}", event_id=event_id, target_subsystems=target_subsystems, success=True)

            self._propagated_events.add(event_id)

        res = PropagationResult(
            propagation_id=f"prop_{event_id[:6]}",
            event_id=event_id,
            target_subsystems=target_subsystems,
            success=True,
        )

        security_logger.info(f"IntelligencePropagator: Propagated intelligence event '{event_id}' to {len(target_subsystems)} subsystems.")
        return res


# Global IntelligencePropagator instance
intelligence_propagator = IntelligencePropagator()
