"""
Enterprise Evaluation Platform Orchestrator.

Orchestrates non-blocking asynchronous evaluation of RAG and Memory pipeline executions,
calculates IR metrics (Hit Rate, Recall@K, Precision@K, MRR, nDCG@K), computes stage quality scores,
and monitors regression alerts without adding latency to production inference requests.
"""

import asyncio
import time
from typing import List, Dict, Any, Optional, Set
from app.core.config import settings
from app.core.eval.eval_storage import eval_storage
from app.core.eval.ir_metrics import ir_metrics_calculator
from app.core.eval.quality_engine import quality_engine
from app.core.logging import logger


class EvalPlatform:
    """Orchestrates non-blocking background pipeline evaluation and metrics logging."""

    @staticmethod
    def _evaluate_sync_task(
        query: str,
        retrieved_contexts: List[Dict[str, Any]],
        memory_count: int,
        context_confidence: float,
        reasoning_confidence: float,
        duration_ms: float,
        ground_truth_ids: Optional[Set[str]] = None,
    ) -> Dict[str, Any]:
        """Synchronous calculation of IR metrics, stage scores, and regression alerts."""
        retrieved_ids = [c.get("doc_id", c.get("filename", "")) for c in retrieved_contexts]

        ir_scores = {}
        if ground_truth_ids:
            ir_scores = {
                "hit_rate": ir_metrics_calculator.calculate_hit_rate(retrieved_ids, ground_truth_ids),
                "precision_at_5": ir_metrics_calculator.calculate_precision_at_k(retrieved_ids, ground_truth_ids, k=5),
                "recall_at_5": ir_metrics_calculator.calculate_recall_at_k(retrieved_ids, ground_truth_ids, k=5),
                "mrr": ir_metrics_calculator.calculate_mrr(retrieved_ids, ground_truth_ids),
                "ndcg_at_5": ir_metrics_calculator.calculate_ndcg_at_k(retrieved_ids, ground_truth_ids, k=5),
            }

        # Calculate Stage Quality Scores
        scores = quality_engine.calculate_pipeline_scores(
            retrieval_count=len(retrieved_contexts),
            memory_count=memory_count,
            context_confidence=context_confidence,
            reasoning_confidence=reasoning_confidence,
        )

        record = {
            "query": query[:50],
            "total_latency_ms": round(duration_ms, 2),
            "retrieval_count": len(retrieved_contexts),
            "memory_count": memory_count,
            "ir_metrics": ir_scores,
            **scores,
        }

        # Check for Regressions against historic summary baseline
        summary_base = eval_storage.get_summary_statistics()
        baseline_record = {
            "overall_pipeline_score": summary_base.get("avg_overall_score", 0.0),
            "total_latency_ms": summary_base.get("avg_latency_ms", 0.0),
        }
        regressions = quality_engine.detect_regressions(record, baseline_record)
        record["regressions_count"] = len(regressions)

        eval_storage.add_evaluation_record(record)
        logger.debug(f"Recorded evaluation record: Overall Score={scores['overall_pipeline_score']}, Latency={duration_ms:.2f}ms")
        return record

    @classmethod
    async def record_pipeline_execution_async(
        cls,
        query: str,
        retrieved_contexts: List[Dict[str, Any]],
        memory_count: int = 0,
        context_confidence: float = 0.85,
        reasoning_confidence: float = 0.85,
        duration_ms: float = 0.0,
        ground_truth_ids: Optional[Set[str]] = None,
    ) -> None:
        """Schedules evaluation task asynchronously in background without delaying user response."""
        if not settings.EVALUATION_ENABLED:
            return

        try:
            asyncio.create_task(
                asyncio.to_thread(
                    cls._evaluate_sync_task,
                    query,
                    retrieved_contexts,
                    memory_count,
                    context_confidence,
                    reasoning_confidence,
                    duration_ms,
                    ground_truth_ids,
                )
            )
        except Exception as e:
            logger.warning(f"Failed to launch non-blocking evaluation task: {e}")


# Global EvalPlatform instance
eval_platform = EvalPlatform()
