"""
Decision Engine for Enterprise Planning & Reasoning Engine.

Multi-strategy scoring (Fastest, Cheapest, Highest Quality, Balanced)
estimating success probability, cost, latency, risk, and resource usage.
"""

from typing import Dict, Any, List
from app.core.planning.planning_models import Plan, DecisionNode, Goal


class DecisionEngine:
    """Evaluates and scores execution strategies to select optimal plan decision."""

    @staticmethod
    def evaluate_and_select_decision(
        plan: Plan,
        policy: str = "balanced",
    ) -> DecisionNode:
        """
        Scores multiple execution strategies and returns the selected decision node.
        Policies: fastest, cheapest, highest_quality, balanced.
        """
        goal = plan.goal

        # Baseline Strategy Scores
        strategies = {
            "fastest": DecisionNode(
                strategy_name="fastest",
                score=0.85 if policy == "fastest" else 0.70,
                success_probability=0.88,
                estimated_cost=goal.estimated_cost,
                estimated_latency_s=1.5,
                risk_score=0.20,
            ),
            "cheapest": DecisionNode(
                strategy_name="cheapest",
                score=0.90 if policy == "cheapest" else 0.75,
                success_probability=0.85,
                estimated_cost=goal.estimated_cost * 0.5,
                estimated_latency_s=2.5,
                risk_score=0.15,
            ),
            "highest_quality": DecisionNode(
                strategy_name="highest_quality",
                score=0.95 if policy == "highest_quality" else 0.85,
                success_probability=0.96,
                estimated_cost=goal.estimated_cost * 1.5,
                estimated_latency_s=4.0,
                risk_score=0.10,
            ),
            "balanced": DecisionNode(
                strategy_name="balanced",
                score=0.92 if policy == "balanced" else 0.80,
                success_probability=0.92,
                estimated_cost=goal.estimated_cost,
                estimated_latency_s=2.0,
                risk_score=0.12,
            ),
        }

        selected_key = policy if policy in strategies else "balanced"
        selected_decision = strategies[selected_key]
        selected_decision.selected = True

        plan.decision = selected_decision
        return selected_decision


# Global DecisionEngine instance
decision_engine = DecisionEngine()
