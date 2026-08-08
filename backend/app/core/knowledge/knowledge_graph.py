"""
Knowledge Graph Engine for Enterprise Knowledge Platform.

Constructs, traverses, and persists Knowledge Graphs (`./knowledge_data/graph.json`).
"""

import json
import os
import threading
from typing import Dict, Any, List, Optional
from app.core.logging import logger
from app.core.knowledge.knowledge_models import KnowledgeGraph, KnowledgeGraphEdge, KnowledgeGraphNode


class KnowledgeGraphEngine:
    """Thread-safe Knowledge Graph management engine with disk persistence."""

    def __init__(self, storage_dir: str = "./knowledge_data"):
        self.storage_dir = storage_dir
        self.file_path = os.path.join(storage_dir, "graph.json")
        self._lock = threading.Lock()
        self._graph = KnowledgeGraph()
        self._ensure_storage()

    def _ensure_storage(self) -> None:
        """Ensures storage directory exists."""
        if not os.path.exists(self.storage_dir):
            os.makedirs(self.storage_dir, exist_ok=True)
        self._load_from_disk()

    def _load_from_disk(self) -> None:
        """Loads Knowledge Graph state from disk."""
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self._graph = KnowledgeGraph.model_validate(data)
                logger.info(f"KnowledgeGraphEngine loaded graph with {len(self._graph.nodes)} nodes from disk.")
            except Exception as e:
                logger.error(f"Failed to load knowledge graph from disk: {e}")

    def _save_to_disk(self) -> None:
        """Saves Knowledge Graph state to disk."""
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(self._graph.model_dump(), f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Failed to save knowledge graph to disk: {e}")

    def add_concept(self, label: str, entity_type: str = "concept") -> KnowledgeGraphNode:
        """Adds a concept node to the Knowledge Graph."""
        with self._lock:
            node = KnowledgeGraphNode(label=label, entity_type=entity_type)
            self._graph.nodes[node.node_id] = node
            self._save_to_disk()
            logger.info(f"KnowledgeGraphEngine added node '{label}' ({node.node_id}).")
            return node

    def get_graph(self) -> KnowledgeGraph:
        """Returns active Knowledge Graph."""
        with self._lock:
            return self._graph


# Global KnowledgeGraphEngine instance
knowledge_graph_engine = KnowledgeGraphEngine()
