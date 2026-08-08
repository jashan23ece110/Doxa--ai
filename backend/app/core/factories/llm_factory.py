"""
LLM Provider Factory.

Instantiates and returns ILLMProvider instances based on provider strategy name.
"""

from typing import Dict, Type
from app.core.interfaces.llm_provider import ILLMProvider
from app.providers.tokenrouter_provider import TokenRouterLLMProvider


class LLMProviderFactory:
    """Factory for creating LLM provider implementations."""

    _registry: Dict[str, Type[ILLMProvider]] = {
        "tokenrouter": TokenRouterLLMProvider,
    }

    @classmethod
    def register_provider(cls, name: str, provider_cls: Type[ILLMProvider]) -> None:
        """Registers a new LLM provider implementation."""
        cls._registry[name.lower()] = provider_cls

    @classmethod
    def get_provider(cls, name: str = "tokenrouter") -> ILLMProvider:
        """Returns an instance of the requested LLM provider strategy."""
        key = name.lower()
        if key not in cls._registry:
            raise ValueError(f"Unknown LLM provider '{name}'. Registered providers: {list(cls._registry.keys())}")
        return cls._registry[key]()
