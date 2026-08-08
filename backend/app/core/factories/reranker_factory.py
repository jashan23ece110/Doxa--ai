"""
Reranker Provider Factory.

Instantiates and returns IRerankerProvider strategy instances.
"""

from typing import Dict, Type
from app.core.interfaces.reranker_provider import IRerankerProvider
from app.providers.cross_encoder_provider import CrossEncoderRerankerProvider


class RerankerFactory:
    """Factory for creating reranker provider strategy implementations."""

    _registry: Dict[str, Type[IRerankerProvider]] = {
        "cross_encoder": CrossEncoderRerankerProvider,
    }

    @classmethod
    def register_provider(cls, name: str, provider_cls: Type[IRerankerProvider]) -> None:
        """Registers a new reranker provider strategy."""
        cls._registry[name.lower()] = provider_cls

    @classmethod
    def get_reranker(cls, name: str = "cross_encoder") -> IRerankerProvider:
        """Returns an instance of the requested reranker provider strategy."""
        key = name.lower()
        if key not in cls._registry:
            raise ValueError(f"Unknown reranker provider '{name}'. Registered providers: {list(cls._registry.keys())}")
        return cls._registry[key]()
