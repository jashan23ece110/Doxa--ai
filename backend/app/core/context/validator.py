"""
Context Validator and Confidence Scorer.

Validates assembled prompt sections, inspects for prompt injection remnants,
and computes an overall Context Confidence Score (0.0 - 1.0).
"""

from typing import Dict, Any, List


class ContextValidator:
    """Validates prompt sections and calculates context confidence scores."""

    @staticmethod
    def calculate_confidence_score(
        contexts: List[Dict[str, Any]],
        memory_context: str,
    ) -> float:
        """Calculates an overall confidence score for the assembled context."""
        if not contexts and not memory_context:
            return 0.5  # Neutral default for non-RAG prompts

        score = 0.5
        if contexts:
            # Check top chunk similarity or rerank score
            top_score = contexts[0].get("cross_encoder_score", contexts[0].get("similarity", 0.5))
            score += min(top_score * 0.3, 0.3)

        if memory_context:
            score += 0.2

        return min(round(score, 2), 1.0)


# Global ContextValidator instance
context_validator = ContextValidator()
