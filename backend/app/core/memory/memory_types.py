"""
Memory Data Models for Enterprise Memory Intelligence Platform.

Defines 9 specialized memory models:
- ShortTermMemory
- LongTermMemory
- SemanticMemory
- EpisodicMemory
- ProceduralMemory
- PreferenceMemory
- RelationshipMemory
- TaskMemory
- KnowledgeMemory
"""

import time
import uuid
from enum import Enum
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class MemoryCategory(str, Enum):
    """Memory type categorization enum."""

    SHORT_TERM = "short_term"
    LONG_TERM = "long_term"
    SEMANTIC = "semantic"
    EPISODIC = "episodic"
    PROCEDURAL = "procedural"
    PREFERENCE = "preference"
    RELATIONSHIP = "relationship"
    TASK = "task"
    KNOWLEDGE = "knowledge"
    FACT = "fact"
    PROJECT = "project"
    IDENTITY = "identity"
    SKILL = "skill"
    GOAL = "goal"


class BaseMemoryItem(BaseModel):
    """Base schema for all memory types."""

    id: str = Field(default_factory=lambda: f"mem_{uuid.uuid4().hex[:10]}")
    user_id: str = "default_user"
    content: str
    category: MemoryCategory = MemoryCategory.LONG_TERM
    importance_score: float = Field(default=0.50, ge=0.0, le=1.0)
    confidence_score: float = Field(default=0.90, ge=0.0, le=1.0)
    created_at: float = Field(default_factory=time.time)
    updated_at: float = Field(default_factory=time.time)
    last_accessed: float = Field(default_factory=time.time)
    access_count: int = 1
    tags: List[str] = Field(default_factory=list)
    embedding_reference: Optional[str] = None
    source: str = "user_interaction"
    metadata: Dict[str, Any] = Field(default_factory=dict)


# Backward compatibility aliases
MemoryItem = BaseMemoryItem
MemoryType = MemoryCategory


class ShortTermMemory(BaseMemoryItem):
    category: MemoryCategory = MemoryCategory.SHORT_TERM


class LongTermMemory(BaseMemoryItem):
    category: MemoryCategory = MemoryCategory.LONG_TERM


class SemanticMemory(BaseMemoryItem):
    category: MemoryCategory = MemoryCategory.SEMANTIC


class EpisodicMemory(BaseMemoryItem):
    category: MemoryCategory = MemoryCategory.EPISODIC


class ProceduralMemory(BaseMemoryItem):
    category: MemoryCategory = MemoryCategory.PROCEDURAL


class PreferenceMemory(BaseMemoryItem):
    category: MemoryCategory = MemoryCategory.PREFERENCE


class RelationshipMemory(BaseMemoryItem):
    category: MemoryCategory = MemoryCategory.RELATIONSHIP


class TaskMemory(BaseMemoryItem):
    category: MemoryCategory = MemoryCategory.TASK


class KnowledgeMemory(BaseMemoryItem):
    category: MemoryCategory = MemoryCategory.KNOWLEDGE
