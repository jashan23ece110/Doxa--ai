"""
TokenRouter Concrete LLM Provider Implementation.
"""

from typing import List, Dict, Any, Optional, AsyncGenerator
from openai import AsyncOpenAI
from app.core.config import settings
from app.core.interfaces.llm_provider import ILLMProvider
from app.core.logging import logger


class TokenRouterLLMProvider(ILLMProvider):
    """Concrete implementation of ILLMProvider interfacing with TokenRouter via AsyncOpenAI SDK."""

    def __init__(self):
        self._client: Optional[AsyncOpenAI] = None

    def _get_client(self) -> AsyncOpenAI:
        """Returns or initializes the AsyncOpenAI client."""
        if self._client is None:
            api_key = settings.TOKENROUTER_API_KEY or "dummy_key"
            base_url = settings.TOKENROUTER_BASE_URL
            logger.info(f"Initializing AsyncOpenAI LLM provider client (Base URL: {base_url})")
            self._client = AsyncOpenAI(api_key=api_key, base_url=base_url)
        return self._client

    async def call(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        temperature: Optional[float] = None,
    ) -> Any:
        """Executes non-streaming completion call with exponential retries."""
        client = self._get_client()
        target_model = model or settings.DEFAULT_MODEL
        temp = temperature if temperature is not None else settings.LLM_TEMPERATURE

        kwargs: Dict[str, Any] = {
            "model": target_model,
            "messages": messages,
            "temperature": temp,
            "timeout": settings.LLM_TIMEOUT_SECONDS,
        }
        if tools:
            kwargs["tools"] = tools
            kwargs["tool_choice"] = "auto"

        for attempt in range(1, settings.LLM_MAX_RETRIES + 1):
            try:
                response = await client.chat.completions.create(**kwargs)
                return response.choices[0].message
            except Exception as e:
                logger.warning(f"TokenRouter call attempt {attempt}/{settings.LLM_MAX_RETRIES} failed: {e}")
                if attempt == settings.LLM_MAX_RETRIES:
                    raise e
                import asyncio
                await asyncio.sleep(settings.LLM_RETRY_DELAY * attempt)

    async def stream(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: Optional[float] = None,
    ) -> AsyncGenerator[Any, None]:
        """Streams completion chunks from TokenRouter."""
        client = self._get_client()
        target_model = model or settings.DEFAULT_MODEL
        temp = temperature if temperature is not None else settings.LLM_TEMPERATURE

        stream_resp = await client.chat.completions.create(
            model=target_model,
            messages=messages,
            temperature=temp,
            stream=True,
            timeout=settings.LLM_TIMEOUT_SECONDS,
        )
        async for chunk in stream_resp:
            yield chunk
