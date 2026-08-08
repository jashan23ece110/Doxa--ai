"""
Enterprise Self-Learning & Adaptive Intelligence Engine Orchestrator.

Main entry point unifying intent analysis, strategy selection, dynamic parameter optimization,
model routing, feedback signals, learning updates, A/B testing, and explainable recommendations.
"""

from typing import Dict, Any, List, Optional
from app.core.adaptive.experiment_manager import experiment_manager
from app.core.adaptive.feedback_engine import feedback_engine
from app.core.adaptive.learning_engine import learning_engine
from app.core.adaptive.optimization_engine import optimization_engine
from app.core.adaptive.policy_manager import policy_manager
from app.core.adaptive.recommendation_engine import recommendation_engine
from app.core.adaptive.routing_optimizer import routing_optimizer
from app.core.adaptive.strategy_manager import strategy_manager
from app.core.diagnostics import DiagnosticSpan
from app.core.logging import logger


class AdaptiveEngine:
    """Main orchestrator for self-learning adaptive intelligence."""

    @staticmethod
    def analyze_and_adapt_request(prompt: str) -> Dict[str, Any]:
        """
        Analyzes prompt and returns adaptive parameters for execution:
        - Active Policy
        - Selected Strategy
        - Optimized Retrieval Weights
        - Selected Model
        - A/B Variant Config
        """
        with DiagnosticSpan(span_name="adaptive_request_analysis", slow_threshold_ms=20.0, category="general"):
            policy = policy_manager.get_active_policy()
            strategy_name, strategy_config = strategy_manager.select_strategy(prompt)
            retrieval_params = optimization_engine.get_optimized_retrieval_params()
            selected_model = routing_optimizer.select_model(
                query_type=strategy_name,
                complexity=strategy_config.get("max_reasoning_depth", "balanced"),
            )
            variant_name, variant_config = experiment_manager.select_variant()

            logger.info(
                f"Adaptive Engine Analysis: Policy='{policy.name}', Strategy='{strategy_name}', "
                f"Model='{selected_model}', DenseWeight={retrieval_params.get('dense_weight')}"
            )

            return {
                "active_policy": policy.name,
                "strategy": strategy_name,
                "strategy_config": strategy_config,
                "retrieval_params": retrieval_params,
                "selected_model": selected_model,
                "ab_experiment": {"variant": variant_name, "config": variant_config},
            }

    @staticmethod
    def record_feedback(
        query_type: str = "general",
        strategy_used: str = "balanced",
        model_used: str = "llama-3.3-70b-versatile",
        retrieval_similarity: float = 0.80,
        verification_passed: bool = True,
        user_rating: Optional[float] = None,
        latency_ms: float = 0.0,
    ) -> None:
        """Records feedback signal and triggers statistical learning update."""
        feedback_engine.record_signal(
            query_type=query_type,
            strategy_used=strategy_used,
            model_used=model_used,
            retrieval_similarity=retrieval_similarity,
            verification_passed=verification_passed,
            user_rating=user_rating,
            latency_ms=latency_ms,
        )

        # Trigger background statistical learning update
        learning_engine.process_feedback_batch()

    @staticmethod
    def get_system_recommendations() -> List[Dict[str, Any]]:
        """Generates explainable internal optimization recommendations."""
        return recommendation_engine.generate_recommendations()


# Global AdaptiveEngine instance
adaptive_engine = AdaptiveEngine()
