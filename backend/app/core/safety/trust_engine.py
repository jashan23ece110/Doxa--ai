"""
Enterprise AI Trust Engine.

Computes composite trust scores for every execution by evaluating tool usage
reliability, memory integrity, retrieval confidence, hallucination likelihood,
citation availability, reasoning consistency, and execution history.
"""

import asyncio
import time
from typing import Dict, Any, List
from app.core.logging import logger
from app.core.config import settings
from app.core.safety.safety_types import TrustScore


class TrustEngine:
    """Computes multi-dimensional trust scores for AI executions."""

    # Weights for composite score calculation
    _WEIGHTS: Dict[str, float] = {
        "tool_trust": 0.15,
        "memory_trust": 0.12,
        "retrieval_trust": 0.18,
        "hallucination_risk": 0.20,
        "citation_score": 0.10,
        "reasoning_consistency": 0.15,
        "execution_history_score": 0.10,
    }

    async def compute_trust(
        self,
        context: Dict[str, Any] = None,
    ) -> TrustScore:
        """
        Computes trust score for an execution based on multi-dimensional signals.

        Args:
            context: Dict containing signal values. Supported keys:
                - tool_invocations (int): Number of tool calls in this execution.
                - tool_success_rate (float): Historical tool success rate.
                - memory_operations (int): Number of memory reads/writes.
                - memory_consistency (float): Memory data consistency score.
                - retrieval_count (int): Number of RAG retrievals.
                - retrieval_confidence (float): Average retrieval similarity score.
                - has_citations (bool): Whether the response includes citations.
                - citation_count (int): Number of verifiable citations.
                - reasoning_steps (int): Number of reasoning steps taken.
                - reasoning_coherence (float): Coherence score of reasoning chain.
                - response_length (int): Token length of the response.
                - source_count (int): Number of distinct sources used.
                - execution_history_success_rate (float): Rolling success rate.

        Returns:
            TrustScore with per-dimension and composite scores.
        """
        if not settings.TRUST_SCORING_ENABLED:
            return TrustScore(overall_score=1.0, is_trustworthy=True)

        start = time.time()
        ctx = context or {}

        # ── Dimension: Tool Trust ──
        tool_success = ctx.get("tool_success_rate", 0.95)
        tool_count = ctx.get("tool_invocations", 0)
        # Trust decreases slightly with more tools, increases with success rate
        tool_trust = min(1.0, tool_success * (1.0 - (min(tool_count, 10) * 0.01)))

        # ── Dimension: Memory Trust ──
        memory_consistency = ctx.get("memory_consistency", 0.92)
        memory_ops = ctx.get("memory_operations", 0)
        memory_trust = min(1.0, memory_consistency * (1.0 - (min(memory_ops, 20) * 0.005)))

        # ── Dimension: Retrieval Trust ──
        retrieval_confidence = ctx.get("retrieval_confidence", 0.85)
        retrieval_count = ctx.get("retrieval_count", 0)
        if retrieval_count == 0:
            retrieval_trust = 0.5  # No retrieval = neutral trust
        else:
            retrieval_trust = min(1.0, retrieval_confidence * 1.1)

        # ── Dimension: Hallucination Risk ──
        source_count = ctx.get("source_count", 0)
        response_length = ctx.get("response_length", 100)
        has_citations = ctx.get("has_citations", False)
        # Longer responses with fewer sources are riskier
        if source_count > 0:
            source_density = source_count / max(response_length / 200, 1)
            hallucination_raw = max(0.0, 1.0 - min(source_density, 1.0))
        else:
            hallucination_raw = 0.6 if not has_citations else 0.3
        hallucination_risk = round(hallucination_raw, 4)

        # ── Dimension: Citation Score ──
        citation_count = ctx.get("citation_count", 0)
        if has_citations and citation_count > 0:
            citation_score = min(1.0, 0.5 + (citation_count * 0.1))
        elif has_citations:
            citation_score = 0.5
        else:
            citation_score = 0.2

        # ── Dimension: Reasoning Consistency ──
        reasoning_coherence = ctx.get("reasoning_coherence", 0.90)
        reasoning_steps = ctx.get("reasoning_steps", 1)
        # More steps with high coherence = higher trust
        step_bonus = min(0.1, reasoning_steps * 0.02)
        reasoning_consistency = min(1.0, reasoning_coherence + step_bonus)

        # ── Dimension: Execution History ──
        execution_history_score = ctx.get("execution_history_success_rate", 0.95)

        # ── Composite Score ──
        # Hallucination risk is inverted (high risk = low trust contribution)
        dimension_scores = {
            "tool_trust": round(tool_trust, 4),
            "memory_trust": round(memory_trust, 4),
            "retrieval_trust": round(retrieval_trust, 4),
            "hallucination_risk": round(1.0 - hallucination_risk, 4),
            "citation_score": round(citation_score, 4),
            "reasoning_consistency": round(reasoning_consistency, 4),
            "execution_history_score": round(execution_history_score, 4),
        }

        weighted_sum = sum(
            dimension_scores[dim] * self._WEIGHTS[dim] for dim in self._WEIGHTS
        )
        total_weight = sum(self._WEIGHTS.values())
        overall = round(weighted_sum / total_weight, 4) if total_weight > 0 else 0.0

        is_trustworthy = overall >= settings.TRUST_THRESHOLD

        elapsed_ms = (time.time() - start) * 1000

        trust = TrustScore(
            overall_score=overall,
            tool_trust=dimension_scores["tool_trust"],
            memory_trust=dimension_scores["memory_trust"],
            retrieval_trust=dimension_scores["retrieval_trust"],
            hallucination_risk=hallucination_risk,
            citation_score=dimension_scores["citation_score"],
            reasoning_consistency=dimension_scores["reasoning_consistency"],
            execution_history_score=dimension_scores["execution_history_score"],
            is_trustworthy=is_trustworthy,
            factors=dimension_scores,
        )

        logger.debug(
            f"TrustEngine computed '{trust.trust_id}': "
            f"Overall={overall}, Hallucination={hallucination_risk}, "
            f"Trustworthy={is_trustworthy}, Duration={elapsed_ms:.2f}ms"
        )
        return trust


# Global TrustEngine instance
trust_engine = TrustEngine()
