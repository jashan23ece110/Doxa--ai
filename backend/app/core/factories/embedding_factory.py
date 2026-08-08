"""
Embedding Provider Factory.

Instantiates and returns IEmbeddingProvider instances based on provider strategy name.
"""

from typing import Dict, Type
from app.core.interfaces.embedding_provider import IEmbeddingProvider
from app.providers.sentence_transformers_provider import SentenceTransformerEmbeddingProvider


class EmbeddingProviderFactory:
    """Factory for creating text embedding provider implementations."""

    _registry: Dict[str, Type[IEmbeddingProvider]] = {
        "sentence_transformers": SentenceTransformerEmbeddingProvider,
    }

    @classmethod
    def register_provider(cls, name: str, provider_cls: Type[IEmbeddingProvider]) -> None:
        """Registers a new embedding provider strategy."""
        cls._registry[name.lower()] = provider_cls

    @classmethod
    def get_provider(cls, name: str = "sentence_transformers") -> IEmbeddingProvider:
        """Returns an instance of the requested embedding provider strategy."""
        key = name.lower()
        if key not in cls._registry:
            raise ValueError(f"Unknown embedding provider '{name}'. Registered providers: {list(cls._registry.keys())}")
        return cls._registry[key]()
