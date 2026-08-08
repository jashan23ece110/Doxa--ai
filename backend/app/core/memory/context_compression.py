"""
Context Compression Engine for Enterprise Memory Intelligence Platform.

Compresses memory context, merges repetitive facts, and summarizes conversation history
to significantly reduce prompt token usage while retaining critical information.
"""

from typing import List, Dict, Any, Tuple
from app.core.memory.memory_types import BaseMemoryItem


class ContextCompressionEngine:
    """Compresses memory items into concise prompt context representation."""

    @staticmethod
    def compress_memories_for_context(
        memories: List[BaseMemoryItem],
        max_items: int = 5,
    ) -> Tuple[str, float]:
        """
        Compresses memories into structured text string.
        Returns: (compressed_text, compression_ratio)
        """
        if not memories:
            return "", 1.0

        raw_length = sum(len(m.content) for m in memories)

        # Filter top memories sorted by importance
        sorted_mems = sorted(memories, key=lambda x: x.importance_score, reverse=True)[:max_items]

        lines = []
        for m in sorted_mems:
            lines.append(f"[{m.category.value.upper()}] {m.content}")

        compressed_text = "\n".join(lines)
        compressed_length = max(len(compressed_text), 1)
        ratio = round(compressed_length / max(raw_length, 1), 2)

        return compressed_text, ratio


# Global ContextCompressionEngine instance
context_compression_engine = ContextCompressionEngine()
