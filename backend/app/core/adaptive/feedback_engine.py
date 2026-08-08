"""
Feedback Engine for Enterprise Self-Learning & Adaptive Intelligence Engine.

Captures, buffers, and processes feedback signals from retrieval, verification, and user interactions.
"""

import time
import uuid
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from app.core.adaptive.adaptive_metrics import adaptive_metrics_tracker


class FeedbackSignal(BaseModel):
    """Structured feedback signal captured from an interaction."""

    signal_id: str = Field(default_factory=lambda: f"sig_{uuid.uuid4().hex[:8]}")
    query_type: str = "general"
    strategy_used: str = "balanced"
    model_used: str = "llama-3.3-70b-versatile"
    retrieval_similarity: float = 0.80
    verification_passed: bool = True
    user_rating: Optional[float] = None  # 1.0 to 5.0 rating if provided
    latency_ms: float = 0.0
    timestamp: float = Field(default_factory=time.time)


class FeedbackEngine:
    """Collects and buffers feedback signals for adaptive learning."""

    def __init__(self):
        self._buffer: List[FeedbackSignal] = []

    def record_signal(
        self,
        query_type: str = "general",
        strategy_used: str = "balanced",
        model_used: str = "llama-3.3-70b-versatile",
        retrieval_similarity: float = 0.80,
        verification_passed: bool = True,
        user_rating: Optional[float] = None,
        latency_ms: float = 0.0,
    ) -> FeedbackSignal:
        """Captures a feedback signal entry."""
        signal = FeedbackSignal(
            query_type=query_type,
            strategy_used=strategy_used,
            model_used=model_used,
            retrieval_similarity=retrieval_similarity,
            verification_passed=verification_passed,
            user_rating=user_rating,
            latency_ms=latency_ms,
        )

        self._buffer.append(signal)
        if len(self._buffer) > 2000:
            self._buffer = self._buffer[-2000:]

        quality_score = 0.90 if verification_passed else 0.50
        if user_rating is not None:
            quality_score = min(max(user_rating / 5.0, 0.0), 1.0)

        adaptive_metrics_tracker.record_feedback(quality_score=quality_score, latency_ms=latency_ms)
        return signal

    def get_recent_signals(self, limit: int = 100) -> List[FeedbackSignal]:
        """Returns recent buffered feedback signals."""
        return self._buffer[-limit:]


# Global FeedbackEngine instance
feedback_engine = FeedbackEngine()
