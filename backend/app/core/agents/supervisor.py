"""
Agent Supervisor for Enterprise Multi-Agent Operating System.

Continuously monitors agent latency, failure rate, health, and memory usage,
automatically restarting failed agents.
"""

from typing import Dict, Any, List
from app.core.agents.agent_registry import agent_registry
from app.core.agents.metrics import agent_metrics_tracker
from app.core.logging import logger


class AgentSupervisor:
    """Monitors agent health and executes automated recovery restarts."""

    @staticmethod
    async def inspect_and_recover_agents() -> int:
        """
        Inspects registered agents for failures and triggers auto-recovery restarts.
        Returns: number of recovered agents.
        """
        restarts = 0
        agents_meta = agent_registry.list_agents()

        for meta in agents_meta:
            if meta.health_status == "failed":
                agent = agent_registry.get_agent(meta.name)
                if agent:
                    logger.info(f"AgentSupervisor restarting failed agent '{meta.name}'.")
                    await agent.recover()
                    agent_registry.set_agent_health(meta.name, "healthy")
                    agent_metrics_tracker.record_restart()
                    restarts += 1

        return restarts


# Global AgentSupervisor instance
supervisor = AgentSupervisor()
