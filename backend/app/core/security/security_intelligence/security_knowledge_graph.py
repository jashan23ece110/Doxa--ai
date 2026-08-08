"""
Enterprise Security Knowledge Graph.

Stores relationships between malware families, threat actors, vulnerabilities, CVEs,
IOCs, attack techniques, forensic artifacts, investigations, affected assets, and mitigation strategies.
Supports graph traversal and semantic relationship discovery.
"""

import threading
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from app.core.logging import security_logger


class GraphNode(BaseModel):
    node_id: str
    node_type: str  # malware, threat_actor, cve, ioc, asset, technique
    label: str
    properties: Dict[str, Any] = Field(default_factory=dict)


class GraphEdge(BaseModel):
    source_id: str
    target_id: str
    relationship: str  # uses, targets, manifests, mitigates, contains


class SecurityKnowledgeGraph:
    """Thread-safe Enterprise Security Knowledge Graph."""

    def __init__(self):
        self._lock = threading.Lock()
        self._nodes: Dict[str, GraphNode] = {}
        self._edges: List[GraphEdge] = []

    def add_node(self, node_id: str, node_type: str, label: str, properties: Optional[Dict[str, Any]] = None) -> GraphNode:
        """Adds a entity node to the security knowledge graph."""
        node = GraphNode(node_id=node_id, node_type=node_type, label=label, properties=properties or {})
        with self._lock:
            self._nodes[node_id] = node
            security_logger.debug(f"SecurityKnowledgeGraph: Added node '{label}' ({node_id}).")
        return node

    def add_edge(self, source_id: str, target_id: str, relationship: str) -> GraphEdge:
        """Adds a relationship edge between two nodes."""
        edge = GraphEdge(source_id=source_id, target_id=target_id, relationship=relationship)
        with self._lock:
            self._edges.append(edge)
            security_logger.debug(f"SecurityKnowledgeGraph: Connected '{source_id}' -[{relationship}]-> '{target_id}'.")
        return edge

    def get_neighbors(self, node_id: str) -> List[Dict[str, Any]]:
        """Retrieves neighboring connected nodes and relationships."""
        with self._lock:
            connected = []
            for edge in self._edges:
                if edge.source_id == node_id and edge.target_id in self._nodes:
                    connected.append({
                        "relationship": edge.relationship,
                        "node": self._nodes[edge.target_id],
                    })
            return connected


# Global SecurityKnowledgeGraph instance
security_knowledge_graph = SecurityKnowledgeGraph()
