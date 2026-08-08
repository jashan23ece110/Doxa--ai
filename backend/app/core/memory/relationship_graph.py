"""
Relationship Graph for Enterprise Memory Intelligence Platform.

Builds a graph connecting entities (people, projects, documents, goals, companies, tasks, events).
Enables graph traversal during memory retrieval.
"""

import threading
from typing import Dict, Any, List, Set, Optional
from pydantic import BaseModel, Field


class GraphNode(BaseModel):
    """Entity node in relationship graph."""

    node_id: str
    label: str
    entity_type: str  # person, project, document, goal, company, task, event
    properties: Dict[str, Any] = Field(default_factory=dict)


class GraphEdge(BaseModel):
    """Directed relationship edge between entity nodes."""

    edge_id: str
    source_id: str
    target_id: str
    relationship: str  # works_on, authored, related_to, belongs_to, depends_on
    weight: float = 1.0


class RelationshipGraph:
    """Thread-safe relationship graph engine."""

    def __init__(self):
        self._lock = threading.Lock()
        self.nodes: Dict[str, GraphNode] = {}
        self.edges: List[GraphEdge] = []
        self._adjacency: Dict[str, Set[str]] = {}

    def add_node(self, node_id: str, label: str, entity_type: str, properties: Optional[Dict[str, Any]] = None) -> GraphNode:
        """Adds or updates a node in the graph."""
        with self._lock:
            node = GraphNode(node_id=node_id, label=label, entity_type=entity_type, properties=properties or {})
            self.nodes[node_id] = node
            if node_id not in self._adjacency:
                self._adjacency[node_id] = set()
            return node

    def add_edge(self, source_id: str, target_id: str, relationship: str = "related_to", weight: float = 1.0) -> GraphEdge:
        """Adds a relationship edge between two nodes."""
        with self._lock:
            edge_id = f"{source_id}->{target_id}:{relationship}"
            edge = GraphEdge(edge_id=edge_id, source_id=source_id, target_id=target_id, relationship=relationship, weight=weight)
            self.edges.append(edge)
            if source_id in self._adjacency:
                self._adjacency[source_id].add(target_id)
            if target_id in self._adjacency:
                self._adjacency[target_id].add(source_id)
            return edge

    def traverse(self, start_node_id: str, max_depth: int = 2) -> List[GraphNode]:
        """Traverses graph starting from node_id up to max_depth."""
        with self._lock:
            if start_node_id not in self.nodes:
                return []

            visited: Set[str] = {start_node_id}
            queue = [(start_node_id, 0)]
            result = []

            while queue:
                curr_id, depth = queue.pop(0)
                if curr_id in self.nodes:
                    result.append(self.nodes[curr_id])

                if depth < max_depth:
                    neighbors = self._adjacency.get(curr_id, set())
                    for nbr in neighbors:
                        if nbr not in visited:
                            visited.add(nbr)
                            queue.append((nbr, depth + 1))

            return result

    def get_stats(self) -> Dict[str, int]:
        """Returns node and edge counts."""
        with self._lock:
            return {"nodes_count": len(self.nodes), "edges_count": len(self.edges)}


# Global RelationshipGraph instance
relationship_graph = RelationshipGraph()
