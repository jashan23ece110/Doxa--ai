"""
Enterprise Multi-Agent Collaboration Types & Data Schemas.

Comprehensive Pydantic models for CollaborationSession, AgentTeam, AgentRole, CollaborationGoal,
DelegatedTask, TaskAssignment, AgentMessage, AgentObservation, SharedContext, AgentVote,
Conflict, Resolution, ConsensusResult, WorkflowState, WorkflowCheckpoint, and CollaborationMetrics.
"""

import time
import uuid
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class AgentRole(BaseModel):
    role_id: str = Field(default_factory=lambda: f"arole_{uuid.uuid4().hex[:8]}")
    role_name: str  # RESEARCHER, PLANNER, CODER, DEVOPS, SECURITY
    required_capabilities: List[str] = Field(default_factory=list)


class AgentTeam(BaseModel):
    team_id: str = Field(default_factory=lambda: f"ateam_{uuid.uuid4().hex[:8]}")
    team_name: str
    member_agent_ids: List[str] = Field(default_factory=list)
    roles_map: Dict[str, str] = Field(default_factory=dict)  # agent_id -> role_name
    created_at: float = Field(default_factory=time.time)


class CollaborationGoal(BaseModel):
    goal_id: str = Field(default_factory=lambda: f"cgoal_{uuid.uuid4().hex[:8]}")
    goal_text: str
    priority: int = 1
    created_at: float = Field(default_factory=time.time)


class DelegatedTask(BaseModel):
    task_id: str = Field(default_factory=lambda: f"dtask_{uuid.uuid4().hex[:8]}")
    goal_id: str
    assigned_agent_id: str
    task_name: str
    required_capability: str
    status: str = "PENDING"  # PENDING, IN_PROGRESS, COMPLETED, FAILED
    created_at: float = Field(default_factory=time.time)


class TaskAssignment(BaseModel):
    assignment_id: str = Field(default_factory=lambda: f"tassign_{uuid.uuid4().hex[:8]}")
    task_id: str
    agent_id: str
    assigned_at: float = Field(default_factory=time.time)


class AgentMessage(BaseModel):
    message_id: str = Field(default_factory=lambda: f"msg_{uuid.uuid4().hex[:8]}")
    sender_agent_id: str
    recipient_agent_id: str  # Specific agent ID or "BROADCAST"
    message_type: str = "TASK_UPDATE"
    content: Dict[str, Any] = Field(default_factory=dict)
    sent_at: float = Field(default_factory=time.time)


class AgentObservation(BaseModel):
    observation_id: str = Field(default_factory=lambda: f"obs_{uuid.uuid4().hex[:8]}")
    agent_id: str
    observation_type: str
    details: Dict[str, Any] = Field(default_factory=dict)
    confidence: float = 0.95
    observed_at: float = Field(default_factory=time.time)


class SharedContext(BaseModel):
    context_id: str = Field(default_factory=lambda: f"sctx_{uuid.uuid4().hex[:8]}")
    session_id: str
    global_variables: Dict[str, Any] = Field(default_factory=dict)
    collected_evidence: List[Dict[str, Any]] = Field(default_factory=list)
    observations: List[AgentObservation] = Field(default_factory=list)
    updated_at: float = Field(default_factory=time.time)


class AgentVote(BaseModel):
    vote_id: str = Field(default_factory=lambda: f"vote_{uuid.uuid4().hex[:8]}")
    agent_id: str
    proposal_id: str
    decision: str = "APPROVE"  # APPROVE, REJECT, ABSTAIN
    confidence: float = 0.90
    reason: str = "Valid proposal matching evidence."


class ConsensusResult(BaseModel):
    consensus_id: str = Field(default_factory=lambda: f"cons_{uuid.uuid4().hex[:8]}")
    proposal_id: str
    strategy_used: str = "MAJORITY"  # MAJORITY, WEIGHTED_CONFIDENCE, AUTHORITY
    is_consensus_reached: bool = True
    approval_ratio: float = 1.0
    evaluated_at: float = Field(default_factory=time.time)


class Conflict(BaseModel):
    conflict_id: str = Field(default_factory=lambda: f"conf_{uuid.uuid4().hex[:8]}")
    agent_ids: List[str] = Field(default_factory=list)
    description: str
    competing_proposals: List[Dict[str, Any]] = Field(default_factory=list)
    detected_at: float = Field(default_factory=time.time)


class Resolution(BaseModel):
    resolution_id: str = Field(default_factory=lambda: f"res_{uuid.uuid4().hex[:8]}")
    conflict_id: str
    winning_proposal_id: str
    resolution_strategy: str = "EVIDENCE_COMPARISON"
    resolved_at: float = Field(default_factory=time.time)


class WorkflowCheckpoint(BaseModel):
    checkpoint_id: str = Field(default_factory=lambda: f"chk_{uuid.uuid4().hex[:8]}")
    workflow_id: str
    step_name: str
    state_snapshot: Dict[str, Any] = Field(default_factory=dict)
    created_at: float = Field(default_factory=time.time)


class WorkflowState(BaseModel):
    workflow_id: str = Field(default_factory=lambda: f"wfstate_{uuid.uuid4().hex[:8]}")
    current_step: str = "RESEARCH"
    status: str = "RUNNING"  # RUNNING, PAUSED, COMPLETED, FAILED
    checkpoints: List[WorkflowCheckpoint] = Field(default_factory=list)
    updated_at: float = Field(default_factory=time.time)


class CollaborationSession(BaseModel):
    session_id: str = Field(default_factory=lambda: f"collab_{uuid.uuid4().hex[:8]}")
    team_id: str
    goal_id: str
    status: str = "ACTIVE"
    created_at: float = Field(default_factory=time.time)


class CollaborationMetrics(BaseModel):
    sessions_active_count: int = 0
    messages_routed_count: int = 0
    conflicts_resolved_count: int = 0
    consensus_evaluations_count: int = 0
    average_workflow_duration_sec: float = 0.0
