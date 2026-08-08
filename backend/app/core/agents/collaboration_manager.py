"""
Collaboration Manager Orchestrator for Enterprise Multi-Agent Framework.

Orchestrates dynamic agent spawning, execution, multi-round debates, weighted voting,
and unified answer synthesis with complete backward compatibility.
"""

import time
from typing import List, Dict, Any, Optional
from app.core.agents.agent_metrics import agent_metrics_tracker
from app.core.agents.agent_registry import agent_registry
from app.core.agents.base_agent import BaseAgent, AgentResponse
from app.core.agents.critic_agent import CriticAgent
from app.core.agents.debate_engine import debate_engine
from app.core.agents.execution_engine import execution_engine
from app.core.agents.planner_agent import PlannerAgent
from app.core.agents.reasoning_agent import ReasoningAgent
from app.core.agents.researcher_agent import ResearcherAgent
from app.core.agents.retriever_agent import RetrieverAgent
from app.core.agents.synthesizer_agent import SynthesizerAgent
from app.core.agents.task_router import task_router
from app.core.agents.verifier_agent import VerifierAgent
from app.core.agents.voting_engine import voting_engine
from app.core.agents.workspace import SharedWorkingMemory
from app.core.agents.writer_agent import WriterAgent
from app.core.diagnostics import DiagnosticSpan
from app.core.logging import logger


class CollaborationManager:
    """Orchestrates multi-agent collaboration workflows."""

    def __init__(self):
        self._register_default_agents()

    def _register_default_agents(self) -> None:
        """Registers default specialized agents into AgentRegistry."""
        agent_registry.register_agent(PlannerAgent())
        agent_registry.register_agent(ResearcherAgent())
        agent_registry.register_agent(RetrieverAgent())
        agent_registry.register_agent(ReasoningAgent())
        agent_registry.register_agent(CriticAgent())
        agent_registry.register_agent(VerifierAgent())
        agent_registry.register_agent(WriterAgent())
        agent_registry.register_agent(SynthesizerAgent())

    async def execute_multi_agent_workflow(
        self,
        prompt: str,
        user_id: str = "default_user",
    ) -> Dict[str, Any]:
        """
        Executes complete multi-agent collaboration pipeline:
        1. Task Routing & Agent Team Selection
        2. Async Parallel Agent Execution
        3. Multi-Round Debate (Reasoning vs Critic)
        4. Calibrated Weighted Voting
        5. Answer Synthesis
        """
        start_time = time.time()
        workspace = SharedWorkingMemory()

        task_category, team_names = task_router.route_task(prompt)
        logger.info(f"Multi-Agent Task Routing: Category='{task_category}', Team={team_names}")

        try:
            with DiagnosticSpan(span_name="multi_agent_collaboration", slow_threshold_ms=1000.0, category="general"):
                # 1. Parallel Team Execution
                agent_responses = await execution_engine.execute_team(team_names, prompt, workspace)

                # 2. Debate Engine (if both Reasoning & Critic agents present)
                reasoning_res = next((r for r in agent_responses if r.agent_name == "ReasoningAgent"), None)
                critic_res = next((r for r in agent_responses if r.agent_name == "CriticAgent"), None)
                debate_summary = None

                if reasoning_res and critic_res:
                    debate_summary = await debate_engine.conduct_debate(
                        prompt=prompt,
                        reasoning_response=reasoning_res,
                        critic_response=critic_res,
                        workspace=workspace,
                        rounds=1,
                    )

                # 3. Weighted Voting Selection
                best_response = voting_engine.select_best_response(agent_responses, strategy="weighted_confidence")

                # 4. Synthesizer Execution
                synthesizer = SynthesizerAgent()
                await synthesizer.initialize()
                synthesis_res = await synthesizer.execute(prompt, workspace)

                duration_ms = (time.time() - start_time) * 1000
                agent_metrics_tracker.record_collaboration(
                    success=True,
                    debate_rounds=1 if debate_summary else 0,
                    votes_conducted=1,
                )

                logger.info(
                    f"Multi-Agent Collaboration complete: Task='{task_category}', TeamSize={len(team_names)}, "
                    f"Final Confidence={synthesis_res.confidence:.2f}, Latency={duration_ms:.2f}ms"
                )

                return {
                    "prompt": prompt,
                    "task_category": task_category,
                    "team_executed": team_names,
                    "agent_count": len(team_names),
                    "best_agent_output": best_response.agent_name,
                    "debate_conducted": debate_summary is not None,
                    "final_response": synthesis_res.result,
                    "confidence_score": synthesis_res.confidence,
                    "latency_ms": round(duration_ms, 2),
                }

        except Exception as e:
            logger.error(f"Multi-Agent Collaboration workflow failed ({e}). Returning fallback.")
            duration_ms = (time.time() - start_time) * 1000
            agent_metrics_tracker.record_collaboration(success=False)
            return {
                "prompt": prompt,
                "task_category": task_category,
                "final_response": f"Multi-Agent fallback response for query: '{prompt}'.",
                "confidence_score": 0.60,
                "latency_ms": round(duration_ms, 2),
            }


# Global CollaborationManager instance
collaboration_manager = CollaborationManager()
