"""
Citation Manager for Enterprise Knowledge Platform.

Generates evidence references, source attribution, citation formatting,
and citation confidence metrics.
"""

from typing import List, Dict, Any
from app.core.logging import logger
from app.core.knowledge.knowledge_models import CitationReference


class CitationManager:
    """Formats and tracks evidence citations."""

    @staticmethod
    def generate_citation(
        source_title: str,
        source_url_or_path: str,
        snippet: str,
        confidence: float = 0.95,
    ) -> CitationReference:
        """
        Formats a citation reference for evidence attribution.
        """
        fmt = f"[{source_title}] ({source_url_or_path}) - \"{snippet[:60]}...\" (Confidence: {confidence})"

        ref = CitationReference(
            source_title=source_title,
            source_url_or_path=source_url_or_path,
            snippet=snippet,
            confidence=confidence,
            formatted_citation=fmt,
        )

        logger.info(f"CitationManager created citation '{ref.citation_id}' for '{source_title}'.")
        return ref


# Global CitationManager instance
citation_manager = CitationManager()
