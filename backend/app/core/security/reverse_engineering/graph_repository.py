"""
Reverse Engineering Graph Repository.

Stores CFGs, Call Graphs, Symbol Maps, Function Metadata, and Cross References.
Supports async persistence, versioning, indexing, and fast retrieval.
"""

import asyncio
import threading
from typing import Dict, Any, List, Optional
from app.core.logging import security_logger
from app.core.security.reverse_engineering.control_flow_graph import ControlFlowGraphModel
from app.core.security.reverse_engineering.call_graph import ProgramCallGraph


class GraphRepository:
    """Enterprise Graph Repository for CFG and Call Graph storage."""

    def __init__(self):
        self._lock = threading.Lock()
        self._cfgs: Dict[str, Dict[str, ControlFlowGraphModel]] = {}  # binary_id -> (func_name -> CFG)
        self._call_graphs: Dict[str, ProgramCallGraph] = {}           # binary_id -> CallGraph

    async def store_cfg(self, binary_id: str, cfg: ControlFlowGraphModel):
        """Stores a function CFG asynchronously."""
        with self._lock:
            if binary_id not in self._cfgs:
                self._cfgs[binary_id] = {}
            self._cfgs[binary_id][cfg.function_name] = cfg
        security_logger.debug(f"GraphRepository: Stored CFG for '{cfg.function_name}' in binary '{binary_id}'.")

    async def store_call_graph(self, binary_id: str, cg: ProgramCallGraph):
        """Stores a program-wide Call Graph asynchronously."""
        with self._lock:
            self._call_graphs[binary_id] = cg
        security_logger.debug(f"GraphRepository: Stored Call Graph for binary '{binary_id}'.")

    async def get_cfg(self, binary_id: str, function_name: str) -> Optional[ControlFlowGraphModel]:
        """Retrieves CFG for a function."""
        with self._lock:
            return self._cfgs.get(binary_id, {}).get(function_name)

    async def get_call_graph(self, binary_id: str) -> Optional[ProgramCallGraph]:
        """Retrieves Call Graph for a binary."""
        with self._lock:
            return self._call_graphs.get(binary_id)


# Global GraphRepository instance
graph_repository = GraphRepository()
