"""
Reasoning Graph DAG Engine.

Represents reasoning execution as a Directed Acyclic Graph (DAG) with dependency tracking,
node state management, and topological level generation.
"""

from typing import List, Dict, Any, Optional, Set
from pydantic import BaseModel, Field
from app.core.reasoning.task_decomposer import SubTask


class ReasoningGraphNode(BaseModel):
    """Node in the reasoning execution DAG."""

    node_id: str
    task: SubTask
    dependencies: Set[str] = Field(default_factory=set)
    status: str = "pending"  # pending, running, completed, failed
    confidence: float = 1.0
    output: Optional[Any] = None
    latency_ms: float = 0.0


class ReasoningGraph:
    """Directed Acyclic Graph (DAG) for cognitive reasoning steps."""

    def __init__(self):
        self.nodes: Dict[str, ReasoningGraphNode] = {}

    def add_node(self, task: SubTask) -> ReasoningGraphNode:
        """Adds a node to the reasoning graph."""
        node = ReasoningGraphNode(
            node_id=task.task_id,
            task=task,
            dependencies=set(task.dependencies),
        )
        self.nodes[task.task_id] = node
        return node

    def get_executable_levels(self) -> List[List[ReasoningGraphNode]]:
        """
        Groups graph nodes into topological execution levels.
        Nodes within the same level can be executed concurrently in parallel.
        """
        completed: Set[str] = set()
        remaining = dict(self.nodes)
        levels: List[List[ReasoningGraphNode]] = []

        while remaining:
            # Find all nodes whose dependencies are satisfied by completed nodes
            ready_level = [
                node for node in remaining.values()
                if node.dependencies.issubset(completed)
            ]

            if not ready_level:
                # Fallback for cyclic or unsatisfied dependencies: force remaining
                ready_level = list(remaining.values())

            levels.append(ready_level)
            for node in ready_level:
                completed.add(node.node_id)
                del remaining[node.node_id]

        return levels

    def update_node_status(
        self,
        node_id: str,
        status: str,
        output: Optional[Any] = None,
        confidence: float = 1.0,
        latency_ms: float = 0.0,
    ) -> None:
        """Updates state, outputs, and confidence for a graph node."""
        if node_id in self.nodes:
            node = self.nodes[node_id]
            node.status = status
            node.output = output
            node.confidence = confidence
            node.latency_ms = latency_ms
            node.task.status = status
            node.task.output = output
