"""
Quality & Regression Detection Engine.

Computes stage quality scores (Retrieval, Memory, Context, Reasoning, Overall)
and detects quality drops or latency regressions against historic baselines.
"""

from typing import List, Dict, Any, Optional
from app.core.config import settings
from app.core.logging import logger


class QualityEngine:
    """Computes stage quality scores and checks for quality/latency regressions."""

    @staticmethod
    def calculate_pipeline_scores(
        retrieval_count: int,
        memory_count: int,
        context_confidence: float,
        reasoning_confidence: float,
    ) -> Dict[str, float]:
        """Calculates unified stage quality scores (0.0 - 1.0)."""
        retrieval_score = min(retrieval_count / 3.0, 1.0) if retrieval_count > 0 else 0.5
        memory_score = min(memory_count / 2.0, 1.0) if memory_count > 0 else 0.5
        context_score = min(max(context_confidence, 0.0), 1.0)
        reasoning_score = min(max(reasoning_confidence, 0.0), 1.0)

        overall_score = round(
            (retrieval_score * 0.3) + (memory_score * 0.2) + (context_score * 0.25) + (reasoning_score * 0.25),
            2,
        )

        return {
            "retrieval_score": round(retrieval_score, 2),
            "memory_score": round(memory_score, 2),
            "context_score": round(context_score, 2),
            "reasoning_score": round(reasoning_score, 2),
            "overall_pipeline_score": overall_score,
        }

    @staticmethod
    def detect_regressions(
        current_metrics: Dict[str, Any],
        baseline_metrics: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """Detects quality or latency regressions compared to a historic baseline."""
        regressions = []
        if not settings.REGRESSION_DETECTION_ENABLED or not baseline_metrics:
            return regressions

        # Check Overall Score Drop (> 15% drop)
        curr_score = current_metrics.get("overall_pipeline_score", 0.0)
        base_score = baseline_metrics.get("overall_pipeline_score", 0.0)
        if base_score > 0 and curr_score < base_score * 0.85:
            regressions.append({
                "type": "quality_regression",
                "message": f"Overall pipeline score dropped from {base_score} to {curr_score} (>15% drop)",
            })

        # Check Latency Regression (> 50% increase)
        curr_lat = current_metrics.get("total_latency_ms", 0.0)
        base_lat = baseline_metrics.get("total_latency_ms", 0.0)
        if base_lat > 0 and curr_lat > base_lat * 1.5:
            regressions.append({
                "type": "latency_regression",
                "message": f"Total latency increased from {base_lat:.2f}ms to {curr_lat:.2f}ms (>50% increase)",
            })

        if regressions:
            logger.warning(f"REGRESSION DETECTED: {len(regressions)} alerts generated!")

        return regressions


# Global QualityEngine instance
quality_engine = QualityEngine()
