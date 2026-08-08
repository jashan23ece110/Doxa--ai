"""
Layer 4: Episodic Memory Manager.

Stores completed task outcomes, key decisions, and historical session summaries.
"""

import time
from typing import List, Dict, Any


class EpisodicMemory:
    """Manages historical task episodes and completed workflow summaries."""

    def __init__(self):
        self.episodes: List[Dict[str, Any]] = []

    def record_episode(self, task_goal: str, outcome_summary: str, tools_used: List[str]) -> Dict[str, Any]:
        """Records a completed task episode."""
        episode = {
            "timestamp": time.time(),
            "task_goal": task_goal,
            "outcome_summary": outcome_summary,
            "tools_used": tools_used,
        }
        self.episodes.append(episode)
        if len(self.episodes) > 50:
            self.episodes = self.episodes[-50:]
        return episode

    def get_recent_episodes(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Returns the most recent completed episodes."""
        return self.episodes[-limit:]


# Global EpisodicMemory instance
episodic_memory = EpisodicMemory()
