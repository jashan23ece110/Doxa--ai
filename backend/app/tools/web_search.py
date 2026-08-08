"""
Tavily Web Search Integration Tool with Bounded In-Memory Query Caching.
Validates input parameter limits and prevents parameter abuse.
"""

import asyncio
from typing import Dict, Optional
from tavily import TavilyClient
from app.core.config import settings
from app.core.logging import logger
from app.core.security import ToolValidator

_search_cache: Dict[str, str] = {}
_MAX_CACHE_SIZE = 500


def get_tavily_client() -> Optional[TavilyClient]:
    """Instantiates Tavily API Client using configured API key."""
    api_key = settings.TAVILY_API_KEY
    if not api_key:
        return None
    try:
        return TavilyClient(api_key=api_key)
    except Exception as e:
        logger.error(f"Failed to initialize TavilyClient: {e}")
        return None


def _sync_web_search(query: str) -> str:
    """Synchronous web search using Tavily API with bounded caching."""
    try:
        clean_query = ToolValidator.validate_search_query(query)
    except Exception as err:
        return f"Search Validation Error: {str(err)}"

    query_lower = clean_query.lower()

    if query_lower in _search_cache:
        logger.debug(f"Web search cache hit for query: '{clean_query}'")
        return _search_cache[query_lower]

    client = get_tavily_client()
    if not client:
        return "Tavily API key is not configured or client failed to initialize. Maine search try kiya lekin issue aaya, apne existing knowledge se jawab de raha hoon."

    try:
        response = client.search(clean_query, search_depth="basic", max_results=settings.TAVILY_MAX_RESULTS)
        results = response.get("results", [])
        if not results:
            return f"No web search results found for: {clean_query}"

        formatted_results = []
        for res in results:
            title = res.get("title", "No Title")
            url = res.get("url", "No URL")
            content = res.get("content", "No content available")
            formatted_results.append(f"Title: {title}\nURL: {url}\nSnippet: {content}")

        final_output = "\n\n---\n\n".join(formatted_results)

        # Evict oldest entry if cache exceeds limit
        if len(_search_cache) >= _MAX_CACHE_SIZE:
            oldest_key = next(iter(_search_cache))
            del _search_cache[oldest_key]

        _search_cache[query_lower] = final_output
        return final_output

    except Exception as e:
        logger.error(f"Tavily search failed: {e}")
        return f"Tavily search failed (Error: {str(e)}). Maine search try kiya lekin issue aaya, apne existing knowledge se jawab de raha hoon."


def web_search(query: str) -> str:
    """Searches web synchronously."""
    return _sync_web_search(query)


async def web_search_async(query: str) -> str:
    """Searches web off the main event loop thread."""
    return await asyncio.to_thread(_sync_web_search, query)
