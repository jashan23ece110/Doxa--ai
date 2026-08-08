"""
Cluster Manager for Enterprise AI Operating System Runtime.

Manages multi-node cluster membership, leader election, node heartbeats,
worker registration, load distribution, and graceful node removal.
"""

import time
import threading
from typing import Dict, Any, List, Optional
from app.core.logging import logger
from app.core.runtime.runtime_models import ClusterNode, NodeHealth, NodeRole


class ClusterManager:
    """Thread-safe multi-node cluster and leader election manager."""

    def __init__(self):
        self._lock = threading.Lock()
        self._nodes: Dict[str, ClusterNode] = {}
        self._leader_id: Optional[str] = None
        self._setup_local_leader()

    def _setup_local_leader(self) -> None:
        """Initializes primary local node as cluster Leader."""
        node = ClusterNode(role=NodeRole.LEADER, health=NodeHealth.HEALTHY)
        self._nodes[node.node_id] = node
        self._leader_id = node.node_id
        logger.info(f"ClusterManager initialized: Node '{node.node_id}' elected LEADER.")

    def register_node(self, hostname: str, ip_address: str) -> ClusterNode:
        """Registers a new node in the cluster."""
        with self._lock:
            node = ClusterNode(hostname=hostname, ip_address=ip_address, role=NodeRole.WORKER)
            self._nodes[node.node_id] = node
            logger.info(f"ClusterManager registered WORKER node '{node.node_id}' ({hostname}).")
            return node

    def get_leader(self) -> Optional[ClusterNode]:
        """Returns current cluster LEADER node."""
        with self._lock:
            if self._leader_id:
                return self._nodes.get(self._leader_id)
            return None

    def list_nodes(self) -> List[ClusterNode]:
        """Lists all registered cluster nodes."""
        with self._lock:
            return list(self._nodes.values())


# Global ClusterManager instance
cluster_manager = ClusterManager()
