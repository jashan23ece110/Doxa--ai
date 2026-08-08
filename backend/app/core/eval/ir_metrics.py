"""
Information Retrieval (IR) Metrics Calculator.

Computes Hit Rate, Recall@K, Precision@K, Mean Reciprocal Rank (MRR),
and Normalized Discounted Cumulative Gain (nDCG@K) for RAG benchmarks.
"""

import math
from typing import List, Dict, Any, Set


class IRMetricsCalculator:
    """Calculates information retrieval precision, recall, MRR, and nDCG metrics."""

    @staticmethod
    def calculate_hit_rate(retrieved_ids: List[str], ground_truth_ids: Set[str]) -> float:
        """Calculates Hit Rate (1.0 if at least one ground truth ID is retrieved, else 0.0)."""
        if not ground_truth_ids or not retrieved_ids:
            return 0.0
        return 1.0 if any(r_id in ground_truth_ids for r_id in retrieved_ids) else 0.0

    @staticmethod
    def calculate_precision_at_k(retrieved_ids: List[str], ground_truth_ids: Set[str], k: int = 5) -> float:
        """Calculates Precision@K (relevant retrieved items / K)."""
        if not retrieved_ids or k <= 0:
            return 0.0
        sub_list = retrieved_ids[:k]
        hits = sum(1 for r_id in sub_list if r_id in ground_truth_ids)
        return round(hits / len(sub_list), 4)

    @staticmethod
    def calculate_recall_at_k(retrieved_ids: List[str], ground_truth_ids: Set[str], k: int = 5) -> float:
        """Calculates Recall@K (relevant retrieved items / total ground truth items)."""
        if not ground_truth_ids or not retrieved_ids or k <= 0:
            return 0.0
        sub_list = retrieved_ids[:k]
        hits = sum(1 for r_id in sub_list if r_id in ground_truth_ids)
        return round(hits / len(ground_truth_ids), 4)

    @staticmethod
    def calculate_mrr(retrieved_ids: List[str], ground_truth_ids: Set[str]) -> float:
        """Calculates Mean Reciprocal Rank (MRR = 1 / rank of first relevant item)."""
        if not ground_truth_ids or not retrieved_ids:
            return 0.0
        for rank, r_id in enumerate(retrieved_ids, start=1):
            if r_id in ground_truth_ids:
                return round(1.0 / rank, 4)
        return 0.0

    @staticmethod
    def calculate_ndcg_at_k(retrieved_ids: List[str], ground_truth_ids: Set[str], k: int = 5) -> float:
        """Calculates Normalized Discounted Cumulative Gain (nDCG@K)."""
        if not ground_truth_ids or not retrieved_ids or k <= 0:
            return 0.0

        sub_list = retrieved_ids[:k]
        dcg = 0.0
        for rank, r_id in enumerate(sub_list, start=1):
            if r_id in ground_truth_ids:
                dcg += 1.0 / math.log2(rank + 1)

        # Ideal DCG
        idcg = sum(1.0 / math.log2(rank + 1) for rank in range(1, min(len(ground_truth_ids), k) + 1))
        if idcg == 0.0:
            return 0.0
        return round(dcg / idcg, 4)


# Global IRMetricsCalculator instance
ir_metrics_calculator = IRMetricsCalculator()
