"""
Token Budget Optimizer for Dynamic Prompt Allocation.

Manages strict token budgets per context section (System, Memory, Knowledge, Tool Outputs, History, User Query)
and dynamically trims lowest-priority content when limits are reached.
"""

from typing import List, Dict, Any
from app.core.config import settings
from app.core.logging import logger


class TokenBudgetManager:
    """Tracks and enforces per-section token budgets."""

    @staticmethod
    def estimate_tokens(text: str) -> int:
        """Estimates token count for a text string (approx 1.33 tokens per word or 4 chars per token)."""
        if not text:
            return 0
        words = len(text.split())
        chars = len(text)
        return max(int(words * 1.33), int(chars / 4.0))

    @classmethod
    def trim_text_to_token_budget(cls, text: str, max_tokens: int) -> str:
        """Trims text lines if token count exceeds max_tokens."""
        if not text or max_tokens <= 0:
            return ""

        current_tokens = cls.estimate_tokens(text)
        if current_tokens <= max_tokens:
            return text

        lines = text.split("\n")
        trimmed_lines = []
        accumulated_tokens = 0

        for line in lines:
            line_tokens = cls.estimate_tokens(line)
            if accumulated_tokens + line_tokens > max_tokens:
                break
            trimmed_lines.append(line)
            accumulated_tokens += line_tokens

        logger.debug(f"Trimmed section from {current_tokens} to {accumulated_tokens} tokens (Budget: {max_tokens})")
        return "\n".join(trimmed_lines)


# Global TokenBudgetManager instance
token_budget_manager = TokenBudgetManager()
