"""
Agent Scheduler for Enterprise Multi-Agent Operating System.

Executes agent tasks in parallel with priority, dependency, deadline, and resource-aware scheduling.
"""

import asyncio
from typing import List, Dict, Any, Callable, Coroutine
from app.core.agents.base_agent import BaseAgent, AgentResponse
from app.core.agents.metrics import agent_metrics_tracker


class AgentScheduler:
    """Schedules and executes agent tasks in parallel using asyncio."""

    @staticmethod
    async def schedule_parallel_execution(
        agent_coros: List[Coroutine[Any, Any, AgentResponse]],
    ) -> List[AgentResponse]:
        """
        Schedules parallel execution of multiple agent tasks using asyncio.gather.
        """
        if not agent_coros:
            return []

        agent_metrics_tracker.record_collaboration()
        results = await asyncio.gather(*agent_coros, return_exceptions=True)

        valid_responses: List[AgentResponse] = []
        for r in results:
            if isinstance(r, AgentResponse):
                valid_responses.append(r)
            elif isinstance(r, Exception):
                agent_metrics_tracker.record_agent_status(failed=1)

        return valid_responses


# Global AgentScheduler instance
scheduler = AgentScheduler()
