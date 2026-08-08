"""
Reciprocal Rank Fusion (RRF) and Chunk Deduplication Engine.

Fuses dense vector search rankings and BM25 sparse search rankings using Reciprocal Rank Fusion:
RRF_Score(d) = sum(1 / (k + rank_m(d))) for m in {dense, bm25}
Deduplicates chunks by (doc_id, chunk_index) and normalizes relevance scores.
"""

from typing import List, Dict, Any
from app.core.config import settings


class ReciprocalRankFusion:
    """Executes RRF rank merging, score normalization, and chunk deduplication."""

    @staticmethod
    def fuse_and_deduplicate(
        dense_results: List[Dict[str, Any]],
        bm25_results: List[Dict[str, Any]],
        top_k: int = settings.RAG_DEFAULT_TOP_K,
        rrf_k: int = settings.RAG_RRF_K,
    ) -> List[Dict[str, Any]]:
        """
        Fuses dense and sparse result lists using Reciprocal Rank Fusion (RRF).
        Deduplicates chunks by (filename, chunk_index) or doc_id.
        """
        fused_scores: Dict[str, float] = {}
        merged_chunks: Dict[str, Dict[str, Any]] = {}

        # 1. Process Dense Results
        for rank, item in enumerate(dense_results, start=1):
            key = f"{item.get('filename', '')}_chunk_{item.get('chunk_index', 0)}"
            rrf_score = 1.0 / (rrf_k + rank)
            fused_scores[key] = fused_scores.get(key, 0.0) + rrf_score

            if key not in merged_chunks:
                merged_chunks[key] = {
                    "text": item["text"],
                    "filename": item.get("filename", ""),
                    "chunk_index": item.get("chunk_index", 0),
                    "similarity": item.get("similarity", 0.0),
                    "dense_score": item.get("similarity", 0.0),
                    "bm25_score": 0.0,
                    "retrieval_source": "dense",
                }
            else:
                merged_chunks[key]["dense_score"] = item.get("similarity", 0.0)

        # 2. Process BM25 Results
        for rank, item in enumerate(bm25_results, start=1):
            key = f"{item.get('filename', '')}_chunk_{item.get('chunk_index', 0)}"
            rrf_score = 1.0 / (rrf_k + rank)
            fused_scores[key] = fused_scores.get(key, 0.0) + rrf_score

            if key not in merged_chunks:
                merged_chunks[key] = {
                    "text": item["text"],
                    "filename": item.get("filename", ""),
                    "chunk_index": item.get("chunk_index", 0),
                    "similarity": round(rrf_score * 10, 4),  # Scaled fallback similarity
                    "dense_score": 0.0,
                    "bm25_score": item.get("bm25_score", 0.0),
                    "retrieval_source": "bm25",
                }
            else:
                merged_chunks[key]["bm25_score"] = item.get("bm25_score", 0.0)
                merged_chunks[key]["retrieval_source"] = "hybrid"

        if not fused_scores:
            return []

        # 3. Sort by RRF Score Descending
        sorted_keys = sorted(fused_scores.keys(), key=lambda k: fused_scores[k], reverse=True)[:top_k]

        final_results = []
        for key in sorted_keys:
            chunk_data = merged_chunks[key]
            chunk_data["rrf_score"] = round(fused_scores[key], 6)
            # Ensure similarity score is populated for backward compatibility
            if chunk_data["similarity"] == 0.0 and chunk_data.get("dense_score", 0.0) > 0:
                chunk_data["similarity"] = chunk_data["dense_score"]
            final_results.append(chunk_data)

        return final_results
