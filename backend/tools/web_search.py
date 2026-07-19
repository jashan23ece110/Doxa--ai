import os
from typing import Dict
from tavily import TavilyClient

# Global in-memory cache for search queries
# Format: { query: "formatted results" }
_search_cache: Dict[str, str] = {}

def get_tavily_client():
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return None
    try:
        return TavilyClient(api_key=api_key)
    except Exception:
        return None

def web_search(query: str) -> str:
    """
    Searches the web using Tavily API.
    Implements a simple in-memory cache to avoid rate limiting for repeated queries.
    """
    if not query:
        return "Search query cannot be empty."

    query_lower = query.lower().strip()
    
    # Check cache first
    if query_lower in _search_cache:
        return _search_cache[query_lower]

    client = get_tavily_client()
    if not client:
        return "Tavily API key is not configured or client failed to initialize. Maine search try kiya lekin issue aaya, apne existing knowledge se jawab de raha hoon."

    try:
        # Perform the search
        response = client.search(query, search_depth="basic", max_results=3)
        
        results = response.get("results", [])
        if not results:
            return f"No web search results found for: {query}"

        # Format results
        formatted_results = []
        for res in results:
            title = res.get("title", "No Title")
            url = res.get("url", "No URL")
            content = res.get("content", "No content available")
            formatted_results.append(f"Title: {title}\nURL: {url}\nSnippet: {content}")

        final_output = "\n\n---\n\n".join(formatted_results)
        
        # Save to cache
        _search_cache[query_lower] = final_output
        return final_output

    except Exception as e:
        # Graceful fallback on API error/rate limits
        return f"Tavily search failed (Error: {str(e)}). Maine search try kiya lekin issue aaya, apne existing knowledge se jawab de raha hoon."
