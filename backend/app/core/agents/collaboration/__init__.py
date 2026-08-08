"""
Enterprise Multi-Agent Collaboration & Autonomous Workflow Package Initialization.
"""

from app.core.agents.collaboration.collaboration_types import (
    CollaborationSession,
    AgentTeam,
    AgentRole,
    CollaborationGoal,
    DelegatedTask,
    TaskAssignment,
    AgentMessage,
    AgentObservation,
    SharedContext,
    AgentVote,
    Conflict,
    Resolution,
    ConsensusResult,
    WorkflowState,
    WorkflowCheckpoint,
    CollaborationMetrics,
)
from app.core.agents.collaboration.agent_team_manager import agent_team_manager, AgentTeamManager
from app.core.agents.collaboration.task_delegation_engine import task_delegation_engine, TaskDelegationEngine
from app.core.agents.collaboration.collaboration_bus import collaboration_bus, CollaborationBus
from app.core.agents.collaboration.shared_context_manager import shared_context_manager, SharedContextManager
from app.core.agents.collaboration.consensus_engine import consensus_engine, ConsensusEngine
from app.core.agents.collaboration.conflict_resolution_engine import conflict_resolution_engine, ConflictResolutionEngine
from app.core.agents.collaboration.workflow_state_manager import workflow_state_manager, WorkflowStateManager
from app.core.agents.collaboration.workflow_coordinator import workflow_coordinator, WorkflowCoordinator
from app.core.agents.collaboration.collaboration_orchestrator import collaboration_orchestrator, CollaborationOrchestrator, MultiAgentCollaborationResult

__all__ = [
    "CollaborationSession",
    "AgentTeam",
    "AgentRole",
    "CollaborationGoal",
    "DelegatedTask",
    "TaskAssignment",
    "AgentMessage",
    "AgentObservation",
    "SharedContext",
    "AgentVote",
    "Conflict",
    "Resolution",
    "ConsensusResult",
    "WorkflowState",
    "WorkflowCheckpoint",
    "CollaborationMetrics",
    "agent_team_manager",
    "AgentTeamManager",
    "task_delegation_engine",
    "TaskDelegationEngine",
    "collaboration_bus",
    "CollaborationBus",
    "shared_context_manager",
    "SharedContextManager",
    "consensus_engine",
    "ConsensusEngine",
    "conflict_resolution_engine",
    "ConflictResolutionEngine",
    "workflow_state_manager",
    "WorkflowStateManager",
    "workflow_coordinator",
    "WorkflowCoordinator",
    "collaboration_orchestrator",
    "CollaborationOrchestrator",
    "MultiAgentCollaborationResult",
]
