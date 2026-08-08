"""
Importance Engine for Enterprise Memory Intelligence Platform.

Calculates normalized importance score (0.0 to 1.0) using frequency, recency,
explicit feedback, conversation length, goal completion, user corrections, and task criticality.
"""

from typing import Dict, Any, Optional
from app.core.memory.memory_types import BaseMemoryItem, MemoryCategory


class ImportanceEngine:
    """Calculates importance scores for memory items."""

    @staticmethod
    def calculate_importance(
        content: str,
        category: MemoryCategory = MemoryCategory.LONG_TERM,
        access_count: int = 1,
        user_rating: Optional[float] = None,
        is_user_correction: bool = False,
        is_task_critical: bool = False,
    ) -> float:
        """
        Calculates a calibrated importance score (0.0 to 1.0).
        """
        # Baseline score by category
        category_weights = {
            MemoryCategory.PREFERENCE: 0.85,
            MemoryCategory.PROCEDURAL: 0.80,
            MemoryCategory.RELATIONSHIP: 0.75,
            MemoryCategory.TASK: 0.70,
            MemoryCategory.SEMANTIC: 0.65,
            MemoryCategory.KNOWLEDGE: 0.60,
            MemoryCategory.EPISODIC: 0.50,
            MemoryCategory.LONG_TERM: 0.50,
            MemoryCategory.SHORT_TERM: 0.30,
        }
        score = category_weights.get(category, 0.50)

        # Access count frequency boost (+0.05 per access up to +0.20)
        freq_boost = min((access_count - 1) * 0.05, 0.20)
        score += freq_boost

        # User feedback rating adjustment
        if user_rating is not None:
            rating_delta = (user_rating - 3.0) * 0.10  # -0.2 to +0.2
            score += rating_delta

        # User correction boost (+0.25)
        if is_user_correction:
            score += 0.25

        # Task criticality boost (+0.20)
        if is_task_critical:
            score += 0.20

        # Clamp between 0.0 and 1.0
        return round(min(max(score, 0.0), 1.0), 2)


# Global ImportanceEngine instance
importance_engine = ImportanceEngine()
