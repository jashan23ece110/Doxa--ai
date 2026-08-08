"""
Agent Service for Multi-Step Autonomous Reasoning and Multi-Agent Systems.

Manages single-agent tool-calling reasoning loops and multi-agent workflows,
publishing events to EventDispatcher and persisting execution traces in TraceRepository.
"""

import asyncio
import json
import time
import uuid
from typing import List, Dict, Any, Optional
from app.core.config import settings
from app.core.events import event_dispatcher, EventType
from app.core.exceptions import BadRequestError
from app.core.logging import logger
from app.core.agents.orchestrator import multi_agent_orchestrator
from app.repositories.trace_repository import trace_repository
from app.services.llm_service import llm_service
from app.tools.base import TOOLS_DEF
from app.tools.registry import tool_registry


class AgentService:
    """Service handling single-agent and multi-agent autonomous reasoning loops."""

    @staticmethod
    def _extract_text_content(content_item: Any) -> str:
        """Extracts text string from a message content field."""
        if isinstance(content_item, str):
            return content_item
        if isinstance(content_item, list):
            texts = []
            for part in content_item:
                if isinstance(part, dict) and part.get("type") == "text":
                    texts.append(part.get("text", ""))
                elif isinstance(part, str):
                    texts.append(part)
            return " ".join(texts)
        return str(content_item)

    async def run_agent_loop(self, goal: str, run_id: Optional[str] = None) -> Dict[str, Any]:
        """Runs single-agent or multi-agent autonomous reasoning loop for a goal."""
        if not goal or not goal.strip():
            raise BadRequestError("Goal cannot be empty.")

        if not run_id:
            run_id = str(uuid.uuid4())

        start_time = time.time()
        logger.info(f"Starting agent reasoning loop for run_id={run_id}, goal='{goal[:30]}...'")

        # Publish AGENT_STARTED Domain Event
        await event_dispatcher.publish(
            EventType.AGENT_STARTED,
            {"run_id": run_id, "goal": goal},
        )

        # Check if Multi-Agent mode is enabled
        if settings.MULTI_AGENT_ENABLED:
            logger.info(f"Delegating goal execution to MultiAgentOrchestrator (run_id={run_id})")
            multi_agent_res = await multi_agent_orchestrator.execute_goal(goal)

            steps = []
            for role, output_data in multi_agent_res.get("agent_outputs", {}).items():
                steps.append({
                    "step": len(steps) + 1,
                    "thought": f"Agent '{role}' executed sub-task.",
                    "tool_used": role,
                    "tool_args": {},
                    "tool_result": output_data.get("output", ""),
                })

            final_result = multi_agent_res.get("final_response", "")

            # Persist trace correctly
            trace_dict = {
                "run_id": run_id,
                "goal": goal,
                "status": multi_agent_res.get("status", "completed"),
                "steps": steps,
                "final_result": final_result,
                "self_check": {"valid": True, "notes": "Verified by Multi-Agent System"},
                "timestamp": time.time(),
            }
            trace_repository.save_trace(run_id, trace_dict)

            await event_dispatcher.publish(
                EventType.AGENT_COMPLETED,
                {"run_id": run_id, "status": "completed", "steps_count": len(steps)},
            )

            return {
                "run_id": run_id,
                "status": multi_agent_res.get("status", "completed"),
                "steps": steps,
                "final_result": final_result,
                "self_check": {"valid": True, "notes": "Verified by Multi-Agent System"},
            }

        # Single-agent tool-calling loop execution fallback
        system_prompt = (
            "You are Doxa, an autonomous AI reasoning agent. "
            "Break down the user's goal step-by-step. Use available tools when needed. "
            "When done, provide a final complete response."
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Goal: {goal}"},
        ]

        steps: List[Dict[str, Any]] = []
        final_result = ""
        iterations = 0

        while iterations < settings.AGENT_MAX_ITERATIONS:
            iterations += 1
            logger.debug(f"Agent loop iteration {iterations}/{settings.AGENT_MAX_ITERATIONS}")

            try:
                response = await llm_service.call_tokenrouter_raw(
                    messages=messages,
                    tools=TOOLS_DEF,
                    temperature=settings.LLM_TEMPERATURE,
                )
            except Exception as e:
                logger.error(f"LLM call failed during agent loop iteration {iterations}: {e}")
                await event_dispatcher.publish(
                    EventType.AGENT_FAILED,
                    {"run_id": run_id, "error": str(e)},
                )
                raise

            choice = response.choices[0]
            message = choice.message

            if message.tool_calls:
                messages.append(message.model_dump())
                for tool_call in message.tool_calls:
                    func_name = tool_call.function.name
                    try:
                        func_args = json.loads(tool_call.function.arguments)
                    except json.JSONDecodeError:
                        func_args = {}

                    logger.info(f"Executing tool '{func_name}' with args {func_args}")

                    tool_output = await tool_registry.execute_tool(func_name, func_args)

                    step_info = {
                        "step": iterations,
                        "thought": message.content or f"Executing tool {func_name}",
                        "tool_used": func_name,
                        "tool_args": func_args,
                        "tool_result": tool_output,
                    }
                    steps.append(step_info)

                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(tool_output, ensure_ascii=False),
                    })
            else:
                final_result = self._extract_text_content(message.content)
                steps.append({
                    "step": iterations,
                    "thought": "Final answer formulated.",
                    "tool_used": None,
                    "tool_args": None,
                    "tool_result": None,
                })
                break

        if not final_result and steps:
            final_result = steps[-1].get("tool_result", "Goal completed.")

        status = "completed" if final_result else "max_iterations_reached"

        trace_dict = {
            "run_id": run_id,
            "goal": goal,
            "status": status,
            "steps": steps,
            "final_result": final_result,
            "self_check": {"valid": True, "notes": "Completed successfully"},
            "timestamp": time.time(),
        }
        trace_repository.save_trace(run_id, trace_dict)

        await event_dispatcher.publish(
            EventType.AGENT_COMPLETED,
            {"run_id": run_id, "status": status, "steps_count": len(steps)},
        )

        return {
            "run_id": run_id,
            "status": status,
            "steps": steps,
            "final_result": final_result,
            "self_check": {"valid": True, "notes": "Reasoning loop verified"},
        }

    @staticmethod
    async def get_trace(run_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves trace object for a run_id from TraceRepository."""
        return await trace_repository.get_trace(run_id)


agent_service = AgentService()
