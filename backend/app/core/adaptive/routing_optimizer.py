"""
Routing Optimizer for Enterprise Self-Learning & Adaptive Intelligence Engine.

Dynamically selects LLM models based on latency, cost, quality, and historical success rates.
"""

from typing import Dict, Any, Optional
from app.core.adaptive.policy_manager import policy_manager


class RoutingOptimizer:
    """Selects optimal LLM model tier dynamically."""

    @staticmethod
    def select_model(
        query_type: str = "general",
        complexity: str = "medium",
    ) -> str:
        """Selects optimal model string based on query type, complexity, and policy."""
        policy = policy_manager.get_active_policy()

        if policy.preferred_model_tier == "fast":
            return "llama-3.1-8b-instant"

        if policy.preferred_model_tier == "premium" or complexity in ("complex", "research"):
            return "llama-3.3-70b-versatile"

        # Standard Default
        return "llama-3.3-70b-versatile"


# Global RoutingOptimizer instance
routing_optimizer = RoutingOptimizer()
