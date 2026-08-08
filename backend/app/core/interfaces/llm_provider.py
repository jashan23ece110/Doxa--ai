"""
Abstract LLM Provider Interface.

Defines the contract for LLM integration providers (TokenRouter, OpenAI, Anthropic, Gemini, Groq, Ollama).
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, AsyncGenerator


class ILLMProvider(ABC):
    """Abstract interface for Large Language Model completion providers."""

    @abstractmethod
    async def call(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        temperature: Optional[float] = None,
    ) -> Any:
        """Executes a completion call to the LLM provider."""
        pass

    @abstractmethod
    async def stream(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: Optional[float] = None,
    ) -> AsyncGenerator[Any, None]:
        """Streams completion chunks from the LLM provider."""
        pass
