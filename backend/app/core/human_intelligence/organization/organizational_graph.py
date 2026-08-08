"""
Enterprise Organizational Knowledge Graph.

Represents employees, teams, departments, projects, reporting hierarchies, trust relationships,
collaboration links, and organizational dependencies.
Supports semantic traversal and relationship analytics.
"""

import threading
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from app.core.logging import security_logger


class OrganizationalGraphNode(BaseModel):
    node_id: str
    node_type: str  # employee, team, department, project
    label: str
    attributes: Dict[str, Any] = Field(default_factory=dict)


class EnterpriseOrganizationalGraph:
    """Thread-safe Enterprise Organizational Knowledge Graph."""

    def __init__(self):
        self._lock = threading.Lock()
        self._nodes: Dict[str, OrganizationalGraphNode] = {}

    def add_node(self, node_id: str, node_type: str, label: str, attributes: Optional[Dict[str, Any]] = None) -> OrganizationalGraphNode:
        """Adds an organizational node to the knowledge graph."""
        node = OrganizationalGraphNode(node_id=node_id, node_type=node_type, label=label, attributes=attributes or {})
        with self._lock:
            self._nodes[node_id] = node
            security_logger.debug(f"EnterpriseOrganizationalGraph: Added node '{node_id}' ({node_type}: '{label}').")
        return node

    def get_nodes_by_type(self, node_type: str) -> List[OrganizationalGraphNode]:
        """Retrieves nodes of a specific type."""
        with self._lock:
            return [n for n in self._nodes.values() if n.node_type == node_type]


# Global EnterpriseOrganizationalGraph instance
enterprise_organizational_graph = EnterpriseOrganizationalGraph()
