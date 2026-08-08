"""
LLM Service for TokenRouter and Multi-Model API Management.

Encapsulates LLM provider calls, model name mapping, streaming completions,
and retry handling using the LLMProviderFactory and ILLMProvider abstraction.
"""

from typing import List, Dict, Any, Optional, AsyncGenerator
from app.core.config import settings
from app.core.factories.llm_factory import LLMProviderFactory
from app.core.interfaces.llm_provider import ILLMProvider
from app.core.logging import logger


class LLMService:
    """Service managing LLM provider selection and completion delegation."""

    def __init__(self, provider_name: str = "tokenrouter"):
        self._provider_name = provider_name
        self._provider: Optional[ILLMProvider] = None

    def get_provider(self) -> ILLMProvider:
        """Lazily obtains the configured ILLMProvider strategy instance."""
        if self._provider is None:
            self._provider = LLMProviderFactory.get_provider(self._provider_name)
        return self._provider

    @staticmethod
    def map_model_name(requested_name: Optional[str]) -> str:
        """
        Maps requested model names to standard supported model strings.
        Legacy or unrecognized model names default to settings.DEFAULT_MODEL.
        """
        if not requested_name or not isinstance(requested_name, str):
            return settings.DEFAULT_MODEL

        name = requested_name.strip().lower()
        if "kimi" in name:
            return "moonshotai/kimi-k3-free"
        elif "llama" in name:
            return "llama-3.3-70b-versatile"
        elif "gemini" in name:
            return "google/gemini-2.0-flash-lite-001"
        elif "claude" in name:
            return "anthropic/claude-3-5-haiku-20241022"
        return settings.DEFAULT_MODEL

    async def call_tokenrouter(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        temperature: Optional[float] = None,
    ) -> Any:
        """Executes LLM completion via configured LLM provider strategy."""
        provider = self.get_provider()
        target_model = self.map_model_name(model)
        return await provider.call(
            messages=messages,
            model=target_model,
            tools=tools,
            temperature=temperature,
        )

    async def stream_tokenrouter(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: Optional[float] = None,
    ) -> AsyncGenerator[Any, None]:
        """Streams completion chunks via configured LLM provider strategy."""
        provider = self.get_provider()
        target_model = self.map_model_name(model)
        async for chunk in provider.stream(
            messages=messages,
            model=target_model,
            temperature=temperature,
        ):
            yield chunk


llm_service = LLMService()
