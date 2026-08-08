"""
Enterprise Knowledge Graph Builder.

Constructs graph nodes and edges for entities, events, documents, organizations,
relationships, observations, and datasets. Supports incremental updates and graph versioning.
"""

import threading
import time
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from app.core.logging import security_logger


class KnowledgeGraphNode(BaseModel):
    node_id: str
    label: str
    node_type: str  # entity, event, document, organization, dataset
    properties: Dict[str, Any] = Field(default_factory=dict)


class KnowledgeGraphEdge(BaseModel):
    edge_id: str
    source_node_id: str
    target_node_id: str
    relationship_type: str
    confidence_score: float = 0.95


class KnowledgeGraphBuilder:
    """Thread-safe Enterprise Knowledge Graph Builder."""

    def __init__(self):
        self._lock = threading.Lock()
        self._nodes: Dict[str, KnowledgeGraphNode] = {}
        self._edges: Dict[str, KnowledgeGraphEdge] = {}

    def add_node(self, node_id: str, label: str, node_type: str, properties: Optional[Dict[str, Any]] = None) -> KnowledgeGraphNode:
        """Adds or updates a node in the knowledge graph."""
        node = KnowledgeGraphNode(node_id=node_id, label=label, node_type=node_type, properties=properties or {})
        with self._lock:
            self._nodes[node_id] = node
            security_logger.debug(f"KnowledgeGraphBuilder: Added node '{node_id}' ({node_type}: '{label}').")
        return node

    def add_edge(self, source_id: str, target_id: str, relationship_type: str, confidence: float = 0.95) -> KnowledgeGraphEdge:
        """Adds a directional edge between two nodes."""
        edge_id = f"edge_{source_id[:4]}_{target_id[:4]}_{relationship_type}"
        edge = KnowledgeGraphEdge(
            edge_id=edge_id,
            source_node_id=source_id,
            target_node_id=target_id,
            relationship_type=relationship_type,
            confidence_score=confidence,
        )
        with self._lock:
            self._edges[edge_id] = edge
            security_logger.debug(f"KnowledgeGraphBuilder: Added edge '{edge_id}' ({source_id} -[{relationship_type}]-> {target_id}).")
        return edge


# Global KnowledgeGraphBuilder instance
knowledge_graph_builder = KnowledgeGraphBuilder()
