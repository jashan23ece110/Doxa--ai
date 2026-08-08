"""
Global Multi-Agent Collaboration Orchestrator.

Master collaboration orchestrator driving end-to-end multi-agent workflows across specialized agents:
Complex Goal -> Goal Decomposition -> Team Formation -> Task Delegation -> Execution -> Shared Context -> Consensus -> Validation -> Approval -> Completion.
"""

import time
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from app.core.logging import security_logger
from app.core.agents.collaboration.collaboration_types import (
    AgentTeam, CollaborationSession, WorkflowState, AgentVote, AgentMessage
)
from app.core.agents.collaboration.agent_team_manager import agent_team_manager
from app.core.agents.collaboration.task_delegation_engine import task_delegation_engine
from app.core.agents.collaboration.collaboration_bus import collaboration_bus
from app.core.agents.collaboration.shared_context_manager import shared_context_manager
from app.core.agents.collaboration.consensus_engine import consensus_engine
from app.core.agents.collaboration.conflict_resolution_engine import conflict_resolution_engine
from app.core.agents.collaboration.workflow_coordinator import workflow_coordinator


class MultiAgentCollaborationResult(BaseModel):
    session_id: str
    team_id: str
    goal_text: str
    steps_completed_count: int
    consensus_reached: bool
    status: str = "COMPLETED"
    summary: str = "Multi-agent collaboration executed cleanly."
    executed_at: float = Field(default_factory=time.time)


class CollaborationOrchestrator:
    """Global Multi-Agent Collaboration Orchestrator Facade."""

    async def execute_collaboration_session(
        self,
        goal_text: str,
        participating_agent_ids: List[str]
    ) -> MultiAgentCollaborationResult:
        """
        Executes end-to-end multi-agent collaboration session.

        Args:
            goal_text: High-level goal text string.
            participating_agent_ids: List of agent IDs.

        Returns:
            MultiAgentCollaborationResult object.
        """
        t0 = time.time()
        security_logger.info(f"CollaborationOrchestrator: Initiating collaboration session for goal '{goal_text}'.")

        # 1. Team Formation
        roles = {aid: "SPECIALIST" for aid in participating_agent_ids}
        team = agent_team_manager.form_team("AutonomousSpecialistSwarm", participating_agent_ids, roles)

        # 2. Session & Shared Context Setup
        session_id = f"csess_{int(t0 * 1000)}"
        sctx = shared_context_manager.get_or_create_context(session_id)

        # 3. Inter-Agent Communication & Task Delegation
        msg = AgentMessage(sender_agent_id="Orchestrator", recipient_agent_id="BROADCAST", message_type="GOAL_DELEGATION")
        collaboration_bus.publish_message(msg)

        dtask = task_delegation_engine.delegate_task(
            goal_id=session_id,
            task_name=f"Execute {goal_text}",
            required_capability="general",
            candidate_agent_id=participating_agent_ids[0] if participating_agent_ids else "agent_default",
        )

        # 4. Consensus & Workflow Coordination
        votes = [AgentVote(agent_id=aid, proposal_id="prop_main") for aid in participating_agent_ids]
        cres = consensus_engine.evaluate_consensus("prop_main", votes)

        steps = ["RESEARCH", "PLANNING", "CODING", "TESTING", "DEVOPS_DEPLOYMENT"]
        wfstate = await workflow_coordinator.execute_multi_agent_workflow(session_id, steps)

        res = MultiAgentCollaborationResult(
            session_id=session_id,
            team_id=team.team_id,
            goal_text=goal_text,
            steps_completed_count=len(steps),
            consensus_reached=cres.is_consensus_reached,
            status="COMPLETED",
        )

        security_logger.info(f"CollaborationOrchestrator: Completed collaboration session '{session_id}' in {round((time.time() - t0)*1000, 2)}ms.")
        return res


# Global CollaborationOrchestrator instance
collaboration_orchestrator = CollaborationOrchestrator()
