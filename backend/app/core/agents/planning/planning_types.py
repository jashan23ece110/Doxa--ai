"""
Enterprise Autonomous Planning Types & Data Schemas.

Comprehensive Pydantic models for PlanningRequest, PlanningContext, GoalDecomposition, TaskGraph,
TaskNode, TaskDependency, TaskConstraint, ExecutionPlan, PlanRevision, PlanValidationResult,
PlanRiskAssessment, ResourceRequirement, AgentAssignment, PlanCheckpoint, ReplanningEvent, and PlanningMetrics.
"""

import time
import uuid
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class TaskConstraint(BaseModel):
    constraint_id: str = Field(default_factory=lambda: f"cnst_{uuid.uuid4().hex[:8]}")
    name: str
    constraint_type: str  # PERMISSION, TIME, TOOL, RESOURCE
    parameters: Dict[str, Any] = Field(default_factory=dict)


class TaskDependency(BaseModel):
    dependency_id: str = Field(default_factory=lambda: f"dep_{uuid.uuid4().hex[:8]}")
    source_task_id: str
    target_task_id: str
    dependency_type: str = "FINISH_TO_START"


class TaskNode(BaseModel):
    task_id: str = Field(default_factory=lambda: f"tnode_{uuid.uuid4().hex[:8]}")
    title: str
    description: str = ""
    assigned_agent_id: Optional[str] = None
    required_capability: Optional[str] = None
    required_tool: Optional[str] = None
    status: str = "PENDING"  # PENDING, READY, EXECUTING, COMPLETED, FAILED, BLOCKED
    priority: int = 1
    constraints: List[TaskConstraint] = Field(default_factory=list)
    created_at: float = Field(default_factory=time.time)


class TaskGraph(BaseModel):
    graph_id: str = Field(default_factory=lambda: f"tgraph_{uuid.uuid4().hex[:8]}")
    nodes: List[TaskNode] = Field(default_factory=list)
    dependencies: List[TaskDependency] = Field(default_factory=list)
    is_valid_dag: bool = True
    critical_path_task_ids: List[str] = Field(default_factory=list)


class ResourceRequirement(BaseModel):
    requirement_id: str = Field(default_factory=lambda: f"rreq_{uuid.uuid4().hex[:8]}")
    resource_name: str
    required_quantity: int = 1
    max_execution_time_sec: float = 60.0


class AgentAssignment(BaseModel):
    assignment_id: str = Field(default_factory=lambda: f"asgn_{uuid.uuid4().hex[:8]}")
    task_id: str
    agent_id: str
    confidence_score: float = 0.95
    match_reason: str = "Matched required capability and role"
    assigned_at: float = Field(default_factory=time.time)


class PlanRiskAssessment(BaseModel):
    assessment_id: str = Field(default_factory=lambda: f"prisk_{uuid.uuid4().hex[:8]}")
    overall_risk_score: float = 0.15  # 0.0 (Low) to 1.0 (Critical)
    high_impact_actions_count: int = 0
    requires_human_approval: bool = False
    risk_factors: List[str] = Field(default_factory=list)


class PlanValidationResult(BaseModel):
    validation_id: str = Field(default_factory=lambda: f"pval_{uuid.uuid4().hex[:8]}")
    is_valid: bool = True
    requires_approval: bool = False
    requires_replanning: bool = False
    validation_errors: List[str] = Field(default_factory=list)
    validated_at: float = Field(default_factory=time.time)


class ExecutionPlan(BaseModel):
    plan_id: str = Field(default_factory=lambda: f"eplan_{uuid.uuid4().hex[:8]}")
    goal_id: str
    task_graph: TaskGraph
    assignments: List[AgentAssignment] = Field(default_factory=list)
    risk_assessment: PlanRiskAssessment = Field(default_factory=PlanRiskAssessment)
    version: int = 1
    status: str = "APPROVED"  # DRAFT, VALIDATED, APPROVED, EXECUTING, COMPLETED, REPLANNED
    created_at: float = Field(default_factory=time.time)


class PlanRevision(BaseModel):
    revision_id: str = Field(default_factory=lambda: f"prev_{uuid.uuid4().hex[:8]}")
    original_plan_id: str
    revised_plan_id: str
    reason: str
    revised_at: float = Field(default_factory=time.time)


class PlanningContext(BaseModel):
    context_id: str = Field(default_factory=lambda: f"pctx_{uuid.uuid4().hex[:8]}")
    goal_id: str
    available_agent_ids: List[str] = Field(default_factory=list)
    available_tools: List[str] = Field(default_factory=list)
    organizational_policies: List[str] = Field(default_factory=list)


class GoalDecomposition(BaseModel):
    decomposition_id: str = Field(default_factory=lambda: f"gdec_{uuid.uuid4().hex[:8]}")
    goal_id: str
    depth: int = 1
    sub_goals: List[str] = Field(default_factory=list)
    tasks: List[TaskNode] = Field(default_factory=list)


class PlanCheckpoint(BaseModel):
    checkpoint_id: str = Field(default_factory=lambda: f"pcp_{uuid.uuid4().hex[:8]}")
    plan_id: str
    completed_task_ids: List[str] = Field(default_factory=list)
    checkpointed_at: float = Field(default_factory=time.time)


class ReplanningEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: f"revent_{uuid.uuid4().hex[:8]}")
    plan_id: str
    trigger_reason: str
    triggered_at: float = Field(default_factory=time.time)


class PlanningMetrics(BaseModel):
    plans_generated_count: int = 0
    tasks_generated_count: int = 0
    average_decomposition_depth: float = 1.0
    replanning_frequency: float = 0.0
    planning_latency_ms: float = 0.0
