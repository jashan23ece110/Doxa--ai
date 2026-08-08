"""
Meta-Cognitive Controller for Meta-Cognitive Layer.

Central controller responsible for planning reasoning, selecting reasoning strategy,
monitoring execution, evaluating confidence, stopping poor reasoning, and selecting better paths.
"""

from typing import Dict, Any, Optional
from app.core.logging import logger
from app.core.metacognition.cognitive_state import cognitive_state_manager
from app.core.metacognition.confidence_engine import meta_confidence_engine
from app.core.metacognition.metacognition_models import (
    CognitiveStateSnapshot,
    CognitiveStrategy,
    ConfidenceAssessment,
    CritiqueResult,
    ReflectionPlan,
    UncertaintyDetection,
)
from app.core.metacognition.reflection import reflection_engine
from app.core.metacognition.self_critic import self_critic
from app.core.metacognition.strategy_manager import strategy_manager
from app.core.metacognition.uncertainty import uncertainty_engine


class MetaCognitiveController:
    """Central Orchestrator for higher-order Meta-Cognitive reasoning."""

    @staticmethod
    def process_query_cognitively(
        query: str,
        initial_reasoning: str,
        context_size: int = 0,
    ) -> Dict[str, Any]:
        """
        Executes full meta-cognitive evaluation pass over a reasoning candidate.
        """
        logger.info(f"MetaCognitiveController analyzing query: '{query[:60]}...'")

        # 1. Strategy Selection
        strategy = strategy_manager.select_strategy(query, context_size=context_size)

        # 2. Confidence & Uncertainty Assessment
        conf = meta_confidence_engine.estimate_confidence()
        uncert = uncertainty_engine.detect_uncertainty(query, confidence_score=conf.overall_confidence)

        # 3. Self-Critique & Reflection
        critique = self_critic.critique_reasoning(initial_reasoning)
        reflection = reflection_engine.reflect_and_improve(initial_reasoning)

        # 4. Update Cognitive State
        state = cognitive_state_manager.update_state(
            strategy=strategy,
            uncertainty=uncert.uncertainty_level,
            confidence=conf.overall_confidence,
        )

        return {
            "strategy": strategy.value,
            "confidence": conf.model_dump(),
            "uncertainty": uncert.model_dump(),
            "critique": critique.model_dump(),
            "reflection": reflection.model_dump(),
            "cognitive_state": state.model_dump(),
            "final_optimized_reasoning": reflection.improved_reasoning_path,
        }


# Global MetaCognitiveController instance
meta_cognitive_controller = MetaCognitiveController()
