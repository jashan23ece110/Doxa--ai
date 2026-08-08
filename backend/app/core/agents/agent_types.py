"""
Enterprise Autonomous Agent Types & Data Schemas.

Comprehensive Pydantic models for AgentDefinition, AgentCapability, AgentRole, AgentState,
AgentGoal, AgentTask, AgentPlan, PlanStep, AgentAction, ToolDefinition, ToolInvocation,
ToolResult, AgentMessage, AgentContext, AgentMemoryReference, AgentExecution, AgentObservation,
AgentEvaluation, AgentPermission, ApprovalRequest, AgentError, and AgentMetrics.
"""

import time
import uuid
from enum import Enum
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class AgentRole(str, Enum):
    RESEARCHER = "RESEARCHER"
    ANALYST = "ANALYST"
    SECURITY_AUDITOR = "SECURITY_AUDITOR"
    HUMAN_INTELLIGENCE_COACH = "HUMAN_INTELLIGENCE_COACH"
    DATA_ENGINEER = "DATA_ENGINEER"
    ORCHESTRATOR = "ORCHESTRATOR"
    EXECUTOR = "EXECUTOR"


class AgentState(str, Enum):
    IDLE = "IDLE"
    INITIALIZING = "INITIALIZING"
    PLANNING = "PLANNING"
    EXECUTING = "EXECUTING"
    SUSPENDED = "SUSPENDED"
    WAITING_APPROVAL = "WAITING_APPROVAL"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    TERMINATED = "TERMINATED"


class AgentCapability(BaseModel):
    capability_id: str = Field(default_factory=lambda: f"cap_{uuid.uuid4().hex[:8]}")
    name: str
    description: str
    category: str = "general"
    parameters: Dict[str, Any] = Field(default_factory=dict)


class AgentPermission(BaseModel):
    permission_id: str = Field(default_factory=lambda: f"perm_{uuid.uuid4().hex[:8]}")
    resource: str
    action: str  # read, execute, write, delete
    allowed_tools: List[str] = Field(default_factory=list)
    requires_approval: bool = False


class AgentDefinition(BaseModel):
    agent_id: str = Field(default_factory=lambda: f"agent_{uuid.uuid4().hex[:8]}")
    name: str
    role: AgentRole = AgentRole.ANALYST
    description: str
    version: str = "1.0.0"
    capabilities: List[AgentCapability] = Field(default_factory=list)
    permissions: List[AgentPermission] = Field(default_factory=list)
    max_concurrent_tasks: int = 5
    is_active: bool = True
    created_at: float = Field(default_factory=time.time)


class AgentGoal(BaseModel):
    goal_id: str = Field(default_factory=lambda: f"goal_{uuid.uuid4().hex[:8]}")
    title: str
    description: str
    priority: int = 1  # 1 (Highest) to 5 (Lowest)
    deadline: Optional[float] = None
    success_criteria: List[str] = Field(default_factory=list)
    status: str = "PENDING"  # PENDING, IN_PROGRESS, ACHIEVED, FAILED, CANCELLED
    created_at: float = Field(default_factory=time.time)


class PlanStep(BaseModel):
    step_id: str = Field(default_factory=lambda: f"step_{uuid.uuid4().hex[:8]}")
    sequence_index: int
    action_type: str
    tool_name: Optional[str] = None
    parameters: Dict[str, Any] = Field(default_factory=dict)
    status: str = "PENDING"  # PENDING, EXECUTING, COMPLETED, FAILED
    error_message: Optional[str] = None


class AgentPlan(BaseModel):
    plan_id: str = Field(default_factory=lambda: f"plan_{uuid.uuid4().hex[:8]}")
    goal_id: str
    steps: List[PlanStep] = Field(default_factory=list)
    is_approved: bool = True
    created_at: float = Field(default_factory=time.time)


class AgentTask(BaseModel):
    task_id: str = Field(default_factory=lambda: f"task_{uuid.uuid4().hex[:8]}")
    goal_id: str
    agent_id: Optional[str] = None
    title: str
    parameters: Dict[str, Any] = Field(default_factory=dict)
    status: str = "PENDING"
    assigned_at: float = Field(default_factory=time.time)


class ToolDefinition(BaseModel):
    tool_name: str
    description: str
    input_schema: Dict[str, Any] = Field(default_factory=dict)
    output_schema: Dict[str, Any] = Field(default_factory=dict)
    required_permissions: List[str] = Field(default_factory=list)
    execution_timeout_sec: float = 30.0
    requires_sandbox: bool = True


class ToolInvocation(BaseModel):
    invocation_id: str = Field(default_factory=lambda: f"tinv_{uuid.uuid4().hex[:8]}")
    tool_name: str
    arguments: Dict[str, Any] = Field(default_factory=dict)
    agent_id: str
    invoked_at: float = Field(default_factory=time.time)


class ToolResult(BaseModel):
    invocation_id: str
    tool_name: str
    success: bool
    output: Dict[str, Any] = Field(default_factory=dict)
    error: Optional[str] = None
    execution_time_ms: float = 0.0
    completed_at: float = Field(default_factory=time.time)


class AgentAction(BaseModel):
    action_id: str = Field(default_factory=lambda: f"act_{uuid.uuid4().hex[:8]}")
    agent_id: str
    task_id: str
    tool_name: Optional[str] = None
    parameters: Dict[str, Any] = Field(default_factory=dict)
    status: str = "EXECUTING"


class AgentObservation(BaseModel):
    observation_id: str = Field(default_factory=lambda: f"obs_{uuid.uuid4().hex[:8]}")
    action_id: str
    data: Dict[str, Any] = Field(default_factory=dict)
    timestamp: float = Field(default_factory=time.time)


class AgentEvaluation(BaseModel):
    evaluation_id: str = Field(default_factory=lambda: f"eval_{uuid.uuid4().hex[:8]}")
    task_id: str
    success: bool
    score: float = 1.0
    feedback: str = "Execution succeeded"
    evaluated_at: float = Field(default_factory=time.time)


class AgentMemoryReference(BaseModel):
    reference_id: str
    source_subsystem: str  # EnterpriseMemory, RAG, KnowledgeGraph
    relevance_score: float = 0.95


class AgentContext(BaseModel):
    context_id: str = Field(default_factory=lambda: f"actx_{uuid.uuid4().hex[:8]}")
    goal_id: str
    active_task_id: Optional[str] = None
    memory_references: List[AgentMemoryReference] = Field(default_factory=list)
    graph_context: Dict[str, Any] = Field(default_factory=dict)
    system_policies: List[str] = Field(default_factory=list)
    token_count: int = 120
    created_at: float = Field(default_factory=time.time)


class AgentMessage(BaseModel):
    message_id: str = Field(default_factory=lambda: f"amsg_{uuid.uuid4().hex[:8]}")
    sender_agent_id: str
    recipient_agent_id: str
    message_type: str  # TASK_DELEGATION, INFORMATION_SHARING, COORDINATION
    payload: Dict[str, Any] = Field(default_factory=dict)
    correlation_id: str = Field(default_factory=lambda: f"corr_{uuid.uuid4().hex[:8]}")
    sent_at: float = Field(default_factory=time.time)


class ApprovalRequest(BaseModel):
    approval_id: str = Field(default_factory=lambda: f"appr_{uuid.uuid4().hex[:8]}")
    agent_id: str
    action_type: str
    parameters: Dict[str, Any] = Field(default_factory=dict)
    is_approved: bool = False
    requested_at: float = Field(default_factory=time.time)


class AgentError(BaseModel):
    error_id: str = Field(default_factory=lambda: f"aerr_{uuid.uuid4().hex[:8]}")
    agent_id: str
    task_id: Optional[str] = None
    error_code: str
    message: str
    timestamp: float = Field(default_factory=time.time)


class AgentMetrics(BaseModel):
    agent_id: str
    tasks_completed_count: int = 0
    tasks_failed_count: int = 0
    tools_invoked_count: int = 0
    average_task_latency_ms: float = 0.0
    uptime_seconds: float = 0.0


class AgentExecution(BaseModel):
    execution_id: str = Field(default_factory=lambda: f"aexec_{uuid.uuid4().hex[:8]}")
    agent_id: str
    goal_id: str
    state: AgentState = AgentState.IDLE
    current_plan: Optional[AgentPlan] = None
    started_at: float = Field(default_factory=time.time)
    completed_at: Optional[float] = None
