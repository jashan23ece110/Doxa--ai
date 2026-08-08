"""
Dynamic User Profile Builder Engine.

Synthesizes user identity, skills, preferences, and goals into a unified user profile snapshot.
"""

from typing import Dict, Any, List
from app.core.memory.memory_store import memory_store
from app.core.memory.memory_types import MemoryType


class ProfileBuilder:
    """Builds and maintains a dynamic user profile from stored memories."""

    @staticmethod
    def build_user_profile(user_id: str = "default_user") -> Dict[str, Any]:
        """Synthesizes structured user profile from active long-term memories."""
        memories = memory_store.list_memories(user_id=user_id)

        profile = {
            "user_id": user_id,
            "identity": [],
            "projects": [],
            "skills": [],
            "goals": [],
            "preferences": [],
            "location": "Not specified",
            "preferred_language": "Python",
            "communication_style": "Concise, technical, precise",
        }

        for item in memories:
            if item.type == MemoryType.IDENTITY:
                profile["identity"].append(item.content)
                if "location" in item.title.lower():
                    profile["location"] = item.content
            elif item.type == MemoryType.PROJECT:
                profile["projects"].append(item.content)
            elif item.type == MemoryType.SKILL:
                profile["skills"].append(item.content)
            elif item.type == MemoryType.GOAL:
                profile["goals"].append(item.content)
            elif item.type == MemoryType.PREFERENCE:
                profile["preferences"].append(item.content)
                if "language" in item.title.lower():
                    profile["preferred_language"] = item.content

        return profile


# Global ProfileBuilder instance
profile_builder = ProfileBuilder()
