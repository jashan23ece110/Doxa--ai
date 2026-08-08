"""
Enterprise Data Lineage Engine.

Tracks data origin lineage graphs across source -> pipeline, pipeline -> dataset,
dataset -> analytics, dataset -> knowledge graph, and dataset -> enterprise memory.
Provides lineage graph traversal APIs.
"""

import threading
import time
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from app.core.logging import security_logger
from app.core.data_intelligence.data_intelligence_types import DataLineage


class DataLineageNode(BaseModel):
    node_id: str
    node_type: str  # source, pipeline, dataset, analytics, memory
    label: str
    parents: List[str] = Field(default_factory=list)
    created_at: float = Field(default_factory=time.time)


class DataLineageEngine:
    """Thread-safe Enterprise Data Lineage Engine."""

    def __init__(self):
        self._lock = threading.Lock()
        self._lineage_nodes: Dict[str, DataLineageNode] = {}

    def record_lineage(self, node_id: str, node_type: str, label: str, parents: Optional[List[str]] = None) -> DataLineageNode:
        """Records a data transformation lineage step."""
        node = DataLineageNode(
            node_id=node_id,
            node_type=node_type,
            label=label,
            parents=parents or [],
        )
        with self._lock:
            self._lineage_nodes[node_id] = node
            security_logger.debug(f"DataLineageEngine: Recorded lineage node '{node_id}' ({node_type}: '{label}').")
        return node

    def trace_lineage(self, destination_id: str) -> List[DataLineageNode]:
        """Traces upstream lineage path for a destination dataset or artifact."""
        with self._lock:
            visited = []
            queue = [destination_id]
            while queue:
                curr = queue.pop(0)
                node = self._lineage_nodes.get(curr)
                if node and node not in visited:
                    visited.append(node)
                    queue.extend(node.parents)
            return visited


# Global DataLineageEngine instance
data_lineage_engine = DataLineageEngine()
