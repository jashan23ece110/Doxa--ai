"""
Planning Engine for Enterprise Cognitive Reasoning.

Analyzes complexity, determines adaptive reasoning depth (Fast, Balanced, Deep, Research),
and builds structured DAG execution graphs.
"""

from typing import Tuple, List, Dict, Any
from app.core.config import settings
from app.core.logging import logger
from app.core.reasoning.reasoning_graph import ReasoningGraph
from app.core.reasoning.task_decomposer import task_decomposer, SubTask


class PlanningEngine:
    """Classifies complexity and constructs reasoning execution graphs."""

    @staticmethod
    def detect_complexity_and_mode(query: str) -> Tuple[str, str]:
        """
        Classifies query request into complexity level and adaptive reasoning mode.
        Returns: (complexity_level, reasoning_mode)
        """
        if not query or not query.strip():
            return "simple", "fast"

        clean_query = query.strip().lower()
        word_count = len(clean_query.split())

        # Research / Multi-Step Detection
        if any(kw in clean_query for kw in ["compare", "analyze", "benchmark", "tradeoffs", "architecture", "research", "deep dive"]):
            return "research", "research"
        
        # Complex Multi-Step Detection
        if word_count > 15 or any(kw in clean_query for kw in ["calculate", "compute", "build", "plan", "roadmap", "steps"]):
            return "complex", "deep"

        # Medium Detection
        if word_count > 6:
            return "medium", "balanced"

        # Simple Query
        return "simple", "fast"

    @classmethod
    def create_reasoning_plan(cls, query: str) -> Tuple[str, str, ReasoningGraph]:
        """Generates DAG execution graph for a user prompt."""
        complexity_level, reasoning_mode = cls.detect_complexity_and_mode(query)
        logger.info(f"Query complexity detected: '{complexity_level}', Mode: '{reasoning_mode}'")

        subtasks = task_decomposer.decompose_goal(query, complexity_level=complexity_level)

        graph = ReasoningGraph()
        for task in subtasks:
            graph.add_node(task)

        return complexity_level, reasoning_mode, graph


# Global PlanningEngine instance
planning_engine = PlanningEngine()
