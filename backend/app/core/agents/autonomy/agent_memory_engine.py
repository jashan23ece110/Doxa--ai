"""
Enterprise Agent Memory Engine.

Manages episodic, semantic, and procedural agent memory with deduplication,
ranking, and integration with Enterprise Memory.
"""

import threading
import time
from typing import Dict, Any, List, Optional
from app.core.logging import security_logger
from app.core.agents.autonomy.agent_memory_types import (
    AgentMemory, MemoryFact, MemoryEpisode, MemoryRetrieval
)


class AgentMemoryEngine:
    """Thread-safe Enterprise Agent Memory Engine."""

    def __init__(self):
        self._lock = threading.Lock()
        self._agent_memories: Dict[str, AgentMemory] = {}

    def get_or_create_memory(self, agent_id: str) -> AgentMemory:
        """Retrieves or initializes memory store for a specific agent."""
        with self._lock:
            if agent_id not in self._agent_memories:
                self._agent_memories[agent_id] = AgentMemory(agent_id=agent_id)
                security_logger.info(f"AgentMemoryEngine: Initialized memory store for agent '{agent_id}'.")
            return self._agent_memories[agent_id]

    def store_episode(self, agent_id: str, goal_id: str, action: str, result: str, success: bool = True) -> MemoryEpisode:
        """Stores an episodic memory entry for an agent."""
        mem = self.get_or_create_memory(agent_id)
        ep = MemoryEpisode(goal_id=goal_id, agent_id=agent_id, action_taken=action, result_outcome=result, success=success)
        with self._lock:
            mem.episodes.append(ep)
            mem.updated_at = time.time()
            security_logger.debug(f"AgentMemoryEngine: Stored episode '{ep.episode_id}' for agent '{agent_id}'.")
        return ep

    def retrieve_memory(self, agent_id: str, query: str) -> MemoryRetrieval:
        """Retrieves relevant facts and episodes for a query."""
        t0 = time.time()
        mem = self.get_or_create_memory(agent_id)
        with self._lock:
            matched_eps = [e for e in mem.episodes if query.lower() in e.action_taken.lower() or query.lower() in e.result_outcome.lower()]

        res = MemoryRetrieval(
            query=query,
            retrieved_facts=mem.facts,
            retrieved_episodes=matched_eps,
            latency_ms=round((time.time() - t0) * 1000, 2),
        )
        return res


# Global AgentMemoryEngine instance
agent_memory_engine = AgentMemoryEngine()
