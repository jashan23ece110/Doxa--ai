"""
Abstract Embedding Provider Interface.

Defines the contract for vector embedding models (SentenceTransformers, OpenAI, Voyage AI, Jina, Nomic).
"""

from abc import ABC, abstractmethod
from typing import List


class IEmbeddingProvider(ABC):
    """Abstract interface for text embedding generation providers."""

    @abstractmethod
    def encode(self, texts: List[str]) -> List[List[float]]:
        """Generates vector embeddings for a list of text strings."""
        pass
