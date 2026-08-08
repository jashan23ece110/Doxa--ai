"""
Hybrid Retrieval Pipeline combining Intelligent Query Processing, Dense ChromaDB,
Sparse BM25 via RRF, and Cross-Encoder Reranking.

Processes queries through language/intent/acronym/HyDE/multi-query pipeline,
executes parallel dense + sparse searches across query variations, fuses rank scores via RRF,
passes candidate pool through Cross-Encoder reranker, and returns top deduplicated context chunks.
"""

import asyncio
from typing import List, Dict, Any, Optional
from app.core.config import settings
from app.core.diagnostics import DiagnosticSpan
from app.core.factories.reranker_factory import RerankerFactory
from app.core.interfaces.reranker_provider import IRerankerProvider
from app.core.logging import logger
from app.core.retrieval.bm25 import bm25_index
from app.core.retrieval.fusion import ReciprocalRankFusion
from app.core.retrieval.query_processor import query_processor
from app.repositories.vector_repository import vector_repository


class HybridRetriever:
    """Orchestrates intelligent query processing, hybrid search, RRF fusion, and Cross-Encoder reranking."""

    def __init__(self, reranker_provider_name: str = "cross_encoder"):
        self._reranker_provider_name = reranker_provider_name
        self._reranker: Optional[IRerankerProvider] = None

    def get_reranker(self) -> IRerankerProvider:
        """Lazy-obtains configured IRerankerProvider strategy instance."""
        if self._reranker is None:
            self._reranker = RerankerFactory.get_reranker(self._reranker_provider_name)
        return self._reranker

    async def _execute_single_query_search(
        self,
        search_query: str,
    ) -> List[Dict[str, Any]]:
        """Executes concurrent dense vector search and sparse BM25 search for a single query variation."""
        dense_task = vector_repository.query_similar(search_query, n_results=settings.RAG_DENSE_TOP_K)
        sparse_task = asyncio.to_thread(bm25_index.search, search_query, top_k=settings.RAG_BM25_TOP_K)

        dense_results, sparse_results = await asyncio.gather(dense_task, sparse_task)
        return dense_results + sparse_results

    async def retrieve_context(
        self,
        query: str,
        n_results: int = settings.RAG_DEFAULT_TOP_K,
    ) -> List[Dict[str, Any]]:
        """
        Executes intelligent query processing, multi-query expansion, HyDE generation,
        parallel dense + sparse searches, RRF fusion, and Cross-Encoder reranking.
        """
        if not query or not query.strip():
            return []

        with DiagnosticSpan(span_name="hybrid_retrieval_pipeline", slow_threshold_ms=450.0, category="vector"):
            # 1. Intelligent Query Processing Stage
            processed_query = query_processor.process_query(query) if settings.QUERY_PROCESSING_ENABLED else {"intent": "search", "multi_queries": [query], "hyde_query": None}

            # Adaptive Strategy: Skip retrieval for greetings
            if processed_query.get("intent") == "greeting":
                logger.debug(f"Adaptive Query Strategy: Skipping retrieval for greeting query '{query}'")
                return []

            search_queries = list(processed_query.get("multi_queries", [query]))
            if processed_query.get("hyde_query"):
                search_queries.append(processed_query["hyde_query"])

            # 2. Execute Parallel Hybrid Searches across Query Variations
            if not settings.HYBRID_RETRIEVAL_ENABLED:
                return await vector_repository.query_similar(query, n_results=n_results)

            logger.debug(f"Executing parallel retrieval for {len(search_queries)} query variations")
            search_tasks = [self._execute_single_query_search(q) for q in search_queries]
            search_results_lists = await asyncio.gather(*search_tasks, return_exceptions=True)

            # Separate dense and sparse results across all variations
            all_dense_results: List[Dict[str, Any]] = []
            all_bm25_results: List[Dict[str, Any]] = []

            for res in search_results_lists:
                if isinstance(res, list):
                    for item in res:
                        if item.get("retrieval_source") == "bm25":
                            all_bm25_results.append(item)
                        else:
                            all_dense_results.append(item)

            # 3. Fuse & Deduplicate Candidate Pool using RRF
            max_candidates = max(n_results, settings.RERANK_MAX_CANDIDATES)
            candidate_pool = ReciprocalRankFusion.fuse_and_deduplicate(
                dense_results=all_dense_results,
                bm25_results=all_bm25_results,
                top_k=max_candidates,
                rrf_k=settings.RAG_RRF_K,
            )

            if not candidate_pool:
                return []

            # 4. Cross-Encoder Reranking Pass (with Graceful Fallback)
            if settings.RERANK_ENABLED:
                try:
                    reranker = self.get_reranker()
                    final_chunks = await reranker.rerank(query, candidate_pool, top_k=n_results)
                    return final_chunks
                except Exception as e:
                    logger.warning(f"Cross-Encoder reranking stage failed ({e}). Returning RRF candidate pool.")
                    return candidate_pool[:n_results]

            return candidate_pool[:n_results]


# Global hybrid retriever instance
hybrid_retriever = HybridRetriever()
