"""
Enterprise Trust Graph.

Maintains organizational trust and collaboration relationships between employees,
departments, teams, projects, managers, and organizational units.
Supports graph traversal and relationship scoring.
"""

import threading
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from app.core.logging import security_logger
from app.core.human_intelligence.human_intelligence_types import TrustRelationship


class EnterpriseTrustGraph:
    """Thread-safe Enterprise Organizational Trust Graph."""

    def __init__(self):
        self._lock = threading.Lock()
        self._relationships: List[TrustRelationship] = []

    def add_relationship(self, source_id: str, target_id: str, relationship_type: str = "peer", trust_score: float = 0.9) -> TrustRelationship:
        """Adds a trust relationship edge to the graph."""
        rel = TrustRelationship(
            source_employee_id=source_id,
            target_employee_id=target_id,
            relationship_type=relationship_type,
            trust_score=trust_score,
        )
        with self._lock:
            self._relationships.append(rel)
            security_logger.debug(f"EnterpriseTrustGraph: Added relationship '{source_id}' -[{relationship_type}]-> '{target_id}'.")
        return rel

    def get_trusted_connections(self, employee_id: str) -> List[TrustRelationship]:
        """Retrieves connected trust relationships for an employee."""
        with self._lock:
            return [r for r in self._relationships if r.source_employee_id == employee_id or r.target_employee_id == employee_id]


# Global EnterpriseTrustGraph instance
enterprise_trust_graph = EnterpriseTrustGraph()
