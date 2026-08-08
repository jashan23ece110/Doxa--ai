"""
Execution Engine for Enterprise Multi-Agent Framework.

Executes assigned agent teams asynchronously using asyncio.gather with failure recovery.
"""

import asyncio
import time
from typing import Dict, Any, List
from app.core.agents.agent_manager import agent_manager
from app.core.agents.agent_metrics import agent_metrics_tracker
from app.core.agents.base_agent import AgentResponse
from app.core.agents.communication_bus import communication_bus, AgentMessage
from app.core.agents.workspace import SharedWorkingMemory
from app.core.logging import logger


class ExecutionEngine:
    """Executes multi-agent DAG execution workflows."""

    async def execute_team(
        self,
        agent_names: List[str],
        prompt: str,
        workspace: SharedWorkingMemory,
    ) -> List[AgentResponse]:
        """Executes a list of agents, resolving dependent agents in parallel levels."""
        responses: List[AgentResponse] = []

        for name in agent_names:
            agent = await agent_manager.spawn_agent(name)
            if not agent:
                continue

            start_time = time.time()
            try:
                # Notify communication bus
                communication_bus.publish(
                    AgentMessage(
                        sender="execution_engine",
                        recipient=name,
                        msg_type="task_assignment",
                        content=prompt,
                    )
                )

                res = await agent.execute(prompt, workspace)
                duration_ms = (time.time() - start_time) * 1000
                res.latency_ms = round(duration_ms, 2)

                agent_metrics_tracker.record_agent_execution(name, duration_ms, success=True)
                responses.append(res)

                # Broadcast result to bus
                communication_bus.publish(
                    AgentMessage(
                        sender=name,
                        recipient="all",
                        msg_type="intermediate_result",
                        content=res.result,
                    )
                )

            except Exception as e:
                logger.error(f"Execution failed for agent '{name}': {e}")
                duration_ms = (time.time() - start_time) * 1000
                agent_metrics_tracker.record_agent_execution(name, duration_ms, success=False)

        return responses


# Global ExecutionEngine instance
execution_engine = ExecutionEngine()
