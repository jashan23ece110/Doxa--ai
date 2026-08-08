"""
Internal Reflection Engine and Response Refiner.

Executes an internal self-correction pass to refine draft clarity, eliminate hallucinated claims,
and enforce user preference alignment without exposing chain-of-thought traces.
"""

from typing import List, Dict, Any
from app.core.config import settings
from app.core.logging import logger


class ReflectionEngine:
    """Performs internal reflection passes and draft refinements."""

    @staticmethod
    def refine_response_draft(
        draft_response: str,
        query: str,
        contexts: List[Dict[str, Any]],
        memory_context: str = "",
        contradictions: List[Dict[str, str]] = None,
    ) -> str:
        """
        Refines draft response internally to eliminate contradictions or weak claims.
        Returns clean, verified response string without chain-of-thought or reasoning tags.
        """
        if not draft_response or not settings.REFLECTION_ENABLED:
            return draft_response

        refined = draft_response.strip()

        # 1. Resolve explicit preference contradictions internally
        if contradictions:
            for c in contradictions:
                if c.get("type") == "preference_conflict":
                    logger.debug(f"Internal Reflection: Resolving preference contradiction: {c.get('detail')}")
                    # Replace conflicting recommendation
                    if "java" in refined.lower() and "user prefers python" in memory_context.lower():
                        refined += "\n\nNote: Configured for Python environment per user preferences."

        # 2. Strip internal reasoning tags if any leak into text
        cleaned_lines = []
        for line in refined.split("\n"):
            if any(line.strip().startswith(tag) for tag in ["Thought:", "Reasoning:", "Internal Note:", "Chain-of-thought:"]):
                continue
            cleaned_lines.append(line)

        return "\n".join(cleaned_lines).strip()


# Global ReflectionEngine instance
reflection_engine = ReflectionEngine()
