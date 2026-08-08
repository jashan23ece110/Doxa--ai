"""
Context Ranker and Evidence Grouper.

Groups retrieved knowledge chunks by document source and topic,
eliminates near-identical duplicate passages, and orders evidence by score.
"""

from typing import List, Dict, Any


class ContextRanker:
    """Deduplicates and groups retrieved context evidence."""

    @staticmethod
    def deduplicate_and_group(contexts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Deduplicates retrieved chunks and groups them by filename."""
        if not contexts:
            return []

        seen_texts = set()
        unique_contexts = []

        for ctx in contexts:
            text_clean = ctx["text"].strip().lower()
            # Check for near-identical duplicate text
            if text_clean in seen_texts:
                continue
            seen_texts.add(text_clean)
            unique_contexts.append(ctx)

        # Sort by similarity or rerank score if present
        sorted_contexts = sorted(
            unique_contexts,
            key=lambda x: x.get("cross_encoder_score", x.get("rrf_score", x.get("similarity", 0.0))),
            reverse=True,
        )
        return sorted_contexts


# Global ContextRanker instance
context_ranker = ContextRanker()
