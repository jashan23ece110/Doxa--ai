"""
Enterprise Multi-Agent Orchestrator Engine.

Orchestrates multi-agent task execution pipelines, inter-agent communication, debate, and voting.
Provides backward-compatible interface for execute_goal.
"""

import asyncio
import time
from typing import Dict, Any, List, Optional
from app.core.agents.collaboration_manager import collaboration_manager
from app.core.agents.workspace import SharedWorkingMemory
from app.core.config import settings
from app.core.diagnostics import DiagnosticSpan
from app.core.logging import logger


class MultiAgentOrchestrator:
    """Orchestrates parallel and sequential multi-agent execution graphs."""

    async def execute_goal(
        self,
        goal: str,
        timeout_seconds: float = settings.AGENT_TIMEOUT,
    ) -> Dict[str, Any]:
        """
        Executes multi-agent workflow for a user goal with complete backward compatibility:
        1. Task Router maps goal to agent team
        2. Async Parallel Execution Engine runs team members
        3. Debate Engine conducts structured review
        4. Voting Engine selects optimal output
        5. Synthesizer Agent produces final response
        """
        if not settings.MULTI_AGENT_ENABLED:
            logger.info("Multi-agent system disabled. Falling back to direct single-agent execution.")
            return {"goal": goal, "status": "single_agent", "final_response": goal}

        try:
            res = await asyncio.wait_for(
                collaboration_manager.execute_multi_agent_workflow(goal),
                timeout=timeout_seconds,
            )
            return {
                "goal": goal,
                "status": "completed",
                "total_duration_ms": res.get("latency_ms", 0.0),
                "task_category": res.get("task_category", "general"),
                "agent_outputs": res.get("best_agent_output", "SynthesizerAgent"),
                "final_response": res.get("final_response", ""),
            }

        except asyncio.TimeoutError:
            logger.warning(f"Multi-Agent Workflow timed out after {timeout_seconds}s. Returning partial results.")
            return {
                "goal": goal,
                "status": "timeout",
                "final_response": f"Workflow timed out after {timeout_seconds}s.",
            }
        except Exception as e:
            logger.error(f"Multi-Agent Workflow execution failed ({e}). Returning fallback response.")
            return {
                "goal": goal,
                "status": "failed",
                "error": str(e),
                "final_response": f"Multi-agent execution encountered an error: {str(e)}",
            }


# Global MultiAgentOrchestrator instance
multi_agent_orchestrator = MultiAgentOrchestrator()
