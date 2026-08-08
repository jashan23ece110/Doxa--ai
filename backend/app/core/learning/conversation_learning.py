"""
Conversation Learning Engine for Enterprise Continuous Learning Layer.

Analyzes conversations to detect common user intents, FAQs, failed conversations,
long conversations, successful conversations, and generates analytics.
"""

from typing import Dict, Any, List, Optional
from app.core.learning.learning_repository import learning_repository, LearningRecord
from app.core.logging import logger


class ConversationLearning:
    """Analyzes conversation patterns and intent trends."""

    @staticmethod
    def generate_conversation_analytics() -> Dict[str, Any]:
        """Analyzes historical learning records for conversation insights."""
        records = learning_repository.get_all_records()
        if not records:
            return {
                "total_conversations_analyzed": 0,
                "common_intents": [],
                "faq_candidates": [],
                "failure_rate": 0.0,
            }

        intent_counts: Dict[str, int] = {}
        faq_candidates: List[str] = []
        failures = 0

        for rec in records:
            # Classify basic intent category
            prompt_lower = rec.prompt_text.lower().strip()
            category = "general"
            if any(kw in prompt_lower for kw in ["code", "python", "bug"]):
                category = "coding"
            elif any(kw in prompt_lower for kw in ["search", "find", "policy"]):
                category = "search"
            elif any(kw in prompt_lower for kw in ["calculate", "math"]):
                category = "computation"

            intent_counts[category] = intent_counts.get(category, 0) + 1

            if not rec.successful_retrieval or rec.hallucination_detected:
                failures += 1
            elif len(rec.prompt_text.split()) > 5:
                faq_candidates.append(rec.prompt_text)

        failure_rate = round(failures / len(records), 2)

        return {
            "total_conversations_analyzed": len(records),
            "intent_distribution": intent_counts,
            "faq_candidates": faq_candidates[:5],
            "failure_rate": failure_rate,
        }


# Global ConversationLearning instance
conversation_learning = ConversationLearning()
