"""
Feedback Engine for Enterprise Continuous Learning Layer.

Captures thumbs_up, thumbs_down, edited_response, retry, regenerate, ignored_answer,
accepted_answer, response_time, conversation_abandonment, and computes quality scores.
"""

import time
import uuid
from enum import Enum
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from app.core.learning.learning_metrics import learning_metrics_tracker


class FeedbackType(str, Enum):
    """Supported feedback interaction types."""

    THUMBS_UP = "thumbs_up"
    THUMBS_DOWN = "thumbs_down"
    EDITED_RESPONSE = "edited_response"
    RETRY = "retry"
    REGENERATE = "regenerate"
    IGNORED_ANSWER = "ignored_answer"
    ACCEPTED_ANSWER = "accepted_answer"
    CONVERSATION_ABANDONMENT = "conversation_abandonment"


class UserFeedbackItem(BaseModel):
    """Captured feedback interaction record."""

    feedback_id: str = Field(default_factory=lambda: f"fb_{uuid.uuid4().hex[:8]}")
    conversation_id: str = "default_session"
    feedback_type: FeedbackType
    quality_score: float = Field(default=0.85, ge=0.0, le=1.0)
    user_edited_text: Optional[str] = None
    response_time_ms: float = 0.0
    timestamp: float = Field(default_factory=time.time)


class FeedbackEngine:
    """Processes user feedback and calculates quality scores."""

    @staticmethod
    def calculate_quality_score(feedback_type: FeedbackType, response_time_ms: float = 0.0) -> float:
        """Calculates a normalized quality score (0.0 to 1.0) for a feedback signal."""
        scores = {
            FeedbackType.THUMBS_UP: 1.0,
            FeedbackType.ACCEPTED_ANSWER: 0.95,
            FeedbackType.EDITED_RESPONSE: 0.70,
            FeedbackType.REGENERATE: 0.40,
            FeedbackType.RETRY: 0.35,
            FeedbackType.IGNORED_ANSWER: 0.30,
            FeedbackType.THUMBS_DOWN: 0.10,
            FeedbackType.CONVERSATION_ABANDONMENT: 0.05,
        }
        base_score = scores.get(feedback_type, 0.80)

        # Minor latency penalty if response took > 5000ms
        if response_time_ms > 5000:
            base_score = max(base_score - 0.05, 0.0)

        return round(base_score, 2)

    def record_feedback(
        self,
        feedback_type: FeedbackType,
        conversation_id: str = "default_session",
        user_edited_text: Optional[str] = None,
        response_time_ms: float = 0.0,
    ) -> UserFeedbackItem:
        """Records a user feedback signal and updates metrics."""
        score = self.calculate_quality_score(feedback_type, response_time_ms)
        is_pos = score >= 0.70
        learning_metrics_tracker.record_feedback_signal(is_positive=is_pos)

        return UserFeedbackItem(
            conversation_id=conversation_id,
            feedback_type=feedback_type,
            quality_score=score,
            user_edited_text=user_edited_text,
            response_time_ms=response_time_ms,
        )


# Global FeedbackEngine instance
feedback_engine = FeedbackEngine()
