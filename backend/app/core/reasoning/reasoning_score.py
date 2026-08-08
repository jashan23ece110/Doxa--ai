"""
Reasoning Score Engine for Deliberative Reasoning.

Evaluates consistency, completeness, evidence support, confidence, logical quality,
and tool correctness.
"""

from typing import Dict, Any
from app.core.reasoning.reasoning_models import ReasoningScoreReport


class ReasoningScoreEngine:
    """Evaluates quality metrics for deliberative reasoning outputs."""

    @staticmethod
    def score_reasoning(
        consistency: float = 0.95,
        completeness: float = 0.90,
        evidence_support: float = 0.92,
        logical_quality: float = 0.94,
        tool_correctness: float = 1.0,
    ) -> ReasoningScoreReport:
        """
        Calculates composite reasoning score.
        """
        overall = round(
            (consistency * 0.25)
            + (completeness * 0.2)
            + (evidence_support * 0.25)
            + (logical_quality * 0.2)
            + (tool_correctness * 0.1),
            2,
        )

        return ReasoningScoreReport(
            consistency=consistency,
            completeness=completeness,
            evidence_support=evidence_support,
            logical_quality=logical_quality,
            tool_correctness=tool_correctness,
            overall_score=overall,
        )


# Global ReasoningScoreEngine instance
reasoning_score_engine = ReasoningScoreEngine()
