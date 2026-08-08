"""
Abstract Reranker Provider Interface.

Defines the contract for RAG reranking models (SentenceTransformers CrossEncoder,
bge-reranker, Cohere Rerank API, Jina, Voyage AI, ONNX).
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any


class IRerankerProvider(ABC):
    """Abstract interface for candidate chunk reranking providers."""

    @abstractmethod
    async def rerank(
        self,
        query: str,
        candidates: List[Dict[str, Any]],
        top_k: int = 3,
    ) -> List[Dict[str, Any]]:
        """Reranks candidate chunks based on query relevance scores."""
        pass
