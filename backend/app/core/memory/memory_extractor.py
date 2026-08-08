"""
Automatic Memory Extractor.

Extracts candidate long-term memory facts, preferences, skills, and goals from user interactions.
"""

import re
from typing import List, Dict, Any, Optional
from app.core.memory.memory_types import MemoryItem, MemoryType


class MemoryExtractor:
    """Extracts candidate long-term memories using rule-based and confidence heuristics."""

    EXTRACTION_PATTERNS = [
        (re.compile(r"i am building\s+(.+)", re.IGNORECASE), MemoryType.PROJECT, "Building Project"),
        (re.compile(r"my favorite language is\s+(.+)", re.IGNORECASE), MemoryType.PREFERENCE, "Preferred Language"),
        (re.compile(r"i work at\s+(.+)", re.IGNORECASE), MemoryType.IDENTITY, "Employment"),
        (re.compile(r"i use\s+(.+)", re.IGNORECASE), MemoryType.SKILL, "Tool Preference"),
        (re.compile(r"i live in\s+(.+)", re.IGNORECASE), MemoryType.IDENTITY, "Location"),
        (re.compile(r"i am preparing for\s+(.+)", re.IGNORECASE), MemoryType.GOAL, "Goal"),
    ]

    IGNORE_PATTERNS = [
        re.compile(r"^(hello|hi|thanks|thank you|write an email|what is|translate|how to)", re.IGNORECASE),
    ]

    @classmethod
    def extract_memories_from_text(cls, user_text: str, user_id: str = "default_user") -> List[MemoryItem]:
        """Analyzes user text and returns candidate long-term memory items."""
        if not user_text or not user_text.strip():
            return []

        clean_text = user_text.strip()
        for ign_pat in cls.IGNORE_PATTERNS:
            if ign_pat.match(clean_text):
                return []

        extracted = []
        for pattern, mem_type, title_prefix in cls.EXTRACTION_PATTERNS:
            match = pattern.search(clean_text)
            if match:
                value = match.group(1).strip()
                extracted.append(
                    MemoryItem(
                        user_id=user_id,
                        type=mem_type,
                        title=f"{title_prefix}: {value[:30]}",
                        content=f"{title_prefix}: {value}",
                        importance_score=0.85,
                        confidence=0.90,
                        tags=[mem_type.value, "auto_extracted"],
                    )
                )

        return extracted


# Global MemoryExtractor instance
memory_extractor = MemoryExtractor()
