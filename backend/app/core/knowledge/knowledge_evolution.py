"""
Knowledge Evolution Engine for Enterprise Knowledge Platform.

Tracks knowledge updates, fact revisions, version history, evidence aging,
and confidence evolution over time.
"""

import threading
from typing import Dict, Any, List, Optional
from app.core.logging import logger
from app.core.knowledge.knowledge_models import KnowledgeRevision


class KnowledgeEvolutionEngine:
    """Thread-safe knowledge revision and evolution tracker."""

    def __init__(self):
        self._lock = threading.Lock()
        self._revisions: List[KnowledgeRevision] = []

    def record_revision(
        self,
        fact_key: str,
        new_value: str,
        previous_value: Optional[str] = None,
        reason: str = "Updated evidence acquired",
    ) -> KnowledgeRevision:
        """Records a knowledge fact revision."""
        rev = KnowledgeRevision(
            fact_key=fact_key,
            previous_value=previous_value,
            new_value=new_value,
            revision_reason=reason,
        )
        with self._lock:
            self._revisions.append(rev)
            logger.info(f"KnowledgeEvolutionEngine recorded revision for '{fact_key}': '{previous_value}' -> '{new_value}'.")

        return rev

    def list_revisions(self) -> List[KnowledgeRevision]:
        """Lists all fact revisions."""
        with self._lock:
            return list(self._revisions)


# Global KnowledgeEvolutionEngine instance
knowledge_evolution_engine = KnowledgeEvolutionEngine()
