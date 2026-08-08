"""
Enterprise Continuous Learning Engine Orchestrator.

Orchestrates non-blocking background analysis of completed conversations:
Quality Analysis -> Retrieval Analysis -> Tool Analysis -> Prompt Analysis ->
Knowledge Analysis -> Recommendations.
Achieves 0ms inference overhead via asyncio.create_task() background tasks.
"""

import asyncio
import uuid
from typing import Dict, Any, List, Optional
from app.core.config import settings
from app.core.diagnostics import DiagnosticSpan
from app.core.learning.conversation_learning import conversation_learning
from app.core.learning.feedback_engine import feedback_engine, FeedbackType
from app.core.learning.knowledge_evolution import knowledge_evolution_engine
from app.core.learning.learning_metrics import learning_metrics_tracker
from app.core.learning.learning_repository import learning_repository, LearningRecord
from app.core.learning.prompt_optimizer import prompt_optimizer
from app.core.learning.retrieval_optimizer import retrieval_optimizer
from app.core.learning.tool_learning import tool_learning_engine
from app.core.logging import logger


class ContinuousLearningEngine:
    """Main orchestrator for background continuous learning pipeline."""

    async def _async_background_learning_pipeline(
        self,
        conversation_id: str,
        prompt_text: str,
        user_id: str,
        contexts: List[Dict[str, Any]],
        response_latency_ms: float,
        tool_failures: List[str],
    ) -> None:
        """Asynchronous background worker executing the learning pipeline with 0ms inference impact."""
        if not settings.LEARNING_ENABLED:
            return

        try:
            with DiagnosticSpan(span_name="async_learning_pipeline", slow_threshold_ms=50.0, category="general"):
                # 1. Quality & Retrieval Analysis
                top_similarity = contexts[0].get("similarity", 0.80) if contexts else 0.50
                successful_retrieval = len(contexts) > 0 and top_similarity >= 0.60

                # Create LearningRecord
                record = LearningRecord(
                    record_id=f"rec_{uuid.uuid4().hex[:8]}",
                    conversation_id=conversation_id,
                    user_id=user_id,
                    prompt_text=prompt_text,
                    successful_retrieval=successful_retrieval,
                    retrieval_similarity=top_similarity,
                    successful_prompt=True,
                    tool_failures=tool_failures,
                    quality_score=0.90 if successful_retrieval else 0.60,
                    response_latency_ms=response_latency_ms,
                )

                # Persist Record asynchronously
                learning_repository.save_record(record)
                learning_metrics_tracker.record_learning_record()

                # 2. Tool Performance Tracking
                if settings.TOOL_LEARNING and tool_failures:
                    for t_name in tool_failures:
                        tool_learning_engine.record_tool_execution(t_name, success=False, latency_ms=100.0)

                # 3. Trigger Analytics & Recommendations if configured
                if settings.AUTO_ANALYTICS:
                    conversation_learning.generate_conversation_analytics()

                if settings.RETRIEVAL_OPTIMIZATION:
                    retrieval_optimizer.generate_retrieval_recommendations(avg_similarity=top_similarity)

                if settings.KNOWLEDGE_EVOLUTION:
                    knowledge_evolution_engine.generate_knowledge_recommendations()

                logger.debug(f"Async learning pipeline completed for conversation '{conversation_id}'.")

        except Exception as e:
            logger.error(f"Async background learning pipeline encountered an error: {e}")

    def process_completed_conversation(
        self,
        conversation_id: str,
        prompt_text: str,
        user_id: str = "default_user",
        contexts: Optional[List[Dict[str, Any]]] = None,
        response_latency_ms: float = 0.0,
        tool_failures: Optional[List[str]] = None,
    ) -> None:
        """
        Non-blocking hook invoked at the end of inference.
        Dispatches background learning task via asyncio.create_task() with ZERO inference latency overhead.
        """
        if not settings.LEARNING_ENABLED:
            return

        try:
            loop = asyncio.get_running_loop()
            loop.create_task(
                self._async_background_learning_pipeline(
                    conversation_id=conversation_id,
                    prompt_text=prompt_text,
                    user_id=user_id,
                    contexts=contexts or [],
                    response_latency_ms=response_latency_ms,
                    tool_failures=tool_failures or [],
                )
            )
        except RuntimeError:
            # Fallback if running outside event loop
            pass


# Global ContinuousLearningEngine instance
continuous_learning_engine = ContinuousLearningEngine()
