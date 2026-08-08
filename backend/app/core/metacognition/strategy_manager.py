"""
Reasoning Strategy Manager for Meta-Cognitive Layer.

Dynamically selects optimal reasoning paths (Direct QA, RAG, Tool Calling, Python Reasoning,
Workflow Engine, Multi-Agent, Tree of Thoughts, Graph Reasoning, Reflection, Self Critique)
based on query complexity, context size, uncertainty, memory availability, and tool availability.
"""

from typing import Dict, Any, Optional
from app.core.logging import logger
from app.core.metacognition.metacognition_models import CognitiveStrategy


class ReasoningStrategyManager:
    """Dynamic reasoning strategy selector."""

    @staticmethod
    def select_strategy(
        query: str,
        context_size: int = 0,
        uncertainty: float = 0.0,
        has_tools: bool = True,
        has_memory: bool = True,
    ) -> CognitiveStrategy:
        """
        Evaluates query complexity and operational state to pick the optimal cognitive strategy.
        """
        query_len = len(query)

        if "workflow" in query.lower() or "pipeline" in query.lower():
            strat = CognitiveStrategy.WORKFLOW_ENGINE
        elif "calculate" in query.lower() or "python" in query.lower() or "code" in query.lower():
            strat = CognitiveStrategy.PYTHON_REASONING
        elif "analyze multi" in query.lower() or "collaborate" in query.lower():
            strat = CognitiveStrategy.MULTI_AGENT
        elif context_size > 1000 or "document" in query.lower():
            strat = CognitiveStrategy.RAG
        elif has_tools and ("search" in query.lower() or "tool" in query.lower()):
            strat = CognitiveStrategy.TOOL_CALLING
        elif query_len > 200 or uncertainty > 0.5:
            strat = CognitiveStrategy.TREE_OF_THOUGHTS
        else:
            strat = CognitiveStrategy.DIRECT_QA

        logger.info(f"ReasoningStrategyManager selected strategy '{strat.value}' for query (Len: {query_len}).")
        return strat


# Global ReasoningStrategyManager instance
strategy_manager = ReasoningStrategyManager()
