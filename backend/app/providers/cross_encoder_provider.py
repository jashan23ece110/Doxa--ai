"""
Cross-Encoder Concrete Reranker Provider Implementation.

Implements IRerankerProvider using sentence_transformers CrossEncoder model.
Executes non-blocking batch inference with automatic graceful fallback.
"""

import asyncio
import time
from typing import List, Dict, Any, Optional
from sentence_transformers import CrossEncoder
from app.core.config import settings
from app.core.diagnostics import DiagnosticSpan
from app.core.interfaces.reranker_provider import IRerankerProvider
from app.core.logging import logger


class CrossEncoderRerankerProvider(IRerankerProvider):
    """Concrete implementation of IRerankerProvider using CrossEncoder models."""

    def __init__(self, model_name: Optional[str] = None):
        self._model_name = model_name or settings.RERANK_MODEL
        self._model: Optional[CrossEncoder] = None

    def _get_model(self) -> CrossEncoder:
        """Lazy-loads the CrossEncoder model instance."""
        if self._model is None:
            logger.info(f"Loading CrossEncoder reranker model '{self._model_name}'")
            start_time = time.time()
            self._model = CrossEncoder(self._model_name)
            load_time = (time.time() - start_time) * 1000
            logger.info(f"Loaded CrossEncoder model '{self._model_name}' in {load_time:.2f}ms")
        return self._model

    def _sync_predict(self, query: str, candidates: List[Dict[str, Any]]) -> List[float]:
        """Synchronous batch inference call for CrossEncoder."""
        model = self._get_model()
        pairs = [[query, item["text"]] for item in candidates]
        scores = model.predict(pairs, batch_size=settings.RERANK_BATCH_SIZE)
        return [float(s) for s in scores]

    async def rerank(
        self,
        query: str,
        candidates: List[Dict[str, Any]],
        top_k: int = settings.RERANK_TOP_K,
    ) -> List[Dict[str, Any]]:
        """Reranks candidate chunks based on CrossEncoder query-document relevance scores."""
        if not candidates or not query.strip():
            return candidates[:top_k]

        try:
            with DiagnosticSpan(span_name="cross_encoder_rerank", slow_threshold_ms=400.0, category="vector"):
                logger.debug(f"Cross-Encoder reranking {len(candidates)} candidates for query '{query[:30]}...'")

                # Execute batch prediction off event loop thread
                scores = await asyncio.to_thread(self._sync_predict, query, candidates)

                # Enrich candidates with cross-encoder scores
                enriched = []
                for item, score in zip(candidates, scores):
                    item_copy = dict(item)
                    item_copy["cross_encoder_score"] = round(score, 4)
                    enriched.append(item_copy)

                # Filter by threshold if applicable and sort descending
                filtered = [c for c in enriched if c["cross_encoder_score"] >= settings.RERANK_THRESHOLD]
                if not filtered:
                    filtered = enriched

                sorted_candidates = sorted(filtered, key=lambda x: x["cross_encoder_score"], reverse=True)

                # Assign final ranks
                final_results = []
                for rank, c in enumerate(sorted_candidates[:top_k], start=1):
                    c["final_rank"] = rank
                    final_results.append(c)

                logger.debug(f"Cross-Encoder reranked top {len(final_results)} chunks (Top score: {final_results[0].get('cross_encoder_score', 0.0)})")
                return final_results

        except Exception as e:
            logger.warning(f"Cross-Encoder reranking failed ({e}). Falling back cleanly to RRF candidate ranking.")
            # Graceful Fallback: Return original candidates truncated to top_k
            return candidates[:top_k]
