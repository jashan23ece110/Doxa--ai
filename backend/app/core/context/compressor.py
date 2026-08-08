"""
Context Compressor for Text Noise Elimination.

Removes boilerplate, repeated sentences, and excessive whitespace from context blocks.
"""

import re


class ContextCompressor:
    """Compresses context blocks by removing redundant whitespace and line noise."""

    @staticmethod
    def compress_text(text: str) -> str:
        """Strips redundant empty lines, repeated spaces, and formatting noise."""
        if not text:
            return ""

        # Normalize multiple newlines to max 2
        text = re.sub(r'\n{3,}', '\n\n', text)
        # Normalize multiple spaces to single space
        lines = [re.sub(r'[ \t]+', ' ', line).strip() for line in text.split('\n')]
        return '\n'.join(lines)


# Global ContextCompressor instance
context_compressor = ContextCompressor()
