"""
Confidence Engine for Enterprise Cognitive Reasoning.

Computes unified 5-factor confidence scores (0.0 to 1.0) calibrated across evidence support,
retrieval top-1 score, graph execution confidence, absence of contradictions, and reflection pass status.
"""

from typing import List, Dict, Any, Optional


class ConfidenceEngine:
    """Computes unified calibrated confidence scores."""

    @staticmethod
    def calculate_confidence(
        contexts: List[Dict[str, Any]],
        verification_result: Dict[str, Any],
        reflection_passed: bool = True,
        graph_confidence: float = 0.95,
    ) -> float:
        """Calculates unified 5-factor confidence score (0.0 to 1.0)."""
        # Factor 1: Retrieval Top-1 Score (30%)
        top_similarity = (
            contexts[0].get("similarity", 0.70) if contexts else 0.50
        )
        retrieval_factor = min(max(top_similarity, 0.0), 1.0) * 0.30

        # Factor 2: Grounded Ratio (25%)
        grounded_ratio = verification_result.get("grounded_ratio", 1.0)
        grounding_factor = min(max(grounded_ratio, 0.0), 1.0) * 0.25

        # Factor 3: Graph Execution Confidence (20%)
        graph_factor = min(max(graph_confidence, 0.0), 1.0) * 0.20

        # Factor 4: Absence of Contradictions (15%)
        contradiction_count = len(verification_result.get("contradictions", []))
        contradiction_factor = (1.0 if contradiction_count == 0 else 0.2) * 0.15

        # Factor 5: Reflection Status (10%)
        reflection_factor = (1.0 if reflection_passed else 0.5) * 0.10

        total_confidence = round(
            retrieval_factor + grounding_factor + graph_factor + contradiction_factor + reflection_factor,
            2,
        )

        return min(max(total_confidence, 0.0), 1.0)


# Global ConfidenceEngine instance
confidence_engine = ConfidenceEngine()
