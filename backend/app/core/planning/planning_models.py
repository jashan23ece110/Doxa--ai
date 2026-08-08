"""
Planning Data Models for Enterprise Planning & Reasoning Engine.

Defines strongly typed models for Goal, Objective, Task, SubTask, Action,
Dependency, Plan, ExecutionState, ReasoningNode, and DecisionNode.
"""

import time
import uuid
from enum import Enum
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    """Status enum for planning hierarchy nodes."""

    PENDING = "pending"
    RUNNING = "running"
    BLOCKED = "blocked"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    RETRYING = "retrying"


class Goal(BaseModel):
    """User goal representation."""

    goal_id: str = Field(default_factory=lambda: f"goal_{uuid.uuid4().hex[:8]}")
    description: str
    primary_objective: str
    secondary_objectives: List[str] = Field(default_factory=list)
    constraints: List[str] = Field(default_factory=list)
    deadlines: Optional[float] = None
    required_tools: List[str] = Field(default_factory=list)
    required_knowledge: List[str] = Field(default_factory=list)
    complexity: str = "medium"  # simple, medium, complex, research
    ambiguity_score: float = 0.20
    estimated_cost: float = 0.05
    confidence: float = 0.90


class Dependency(BaseModel):
    """Dependency relationship between tasks."""

    source_task_id: str
    target_task_id: str
    dependency_type: str = "finish_to_start"  # serial, parallel, optional, conditional


class Action(BaseModel):
    """Atomic low-level action node."""

    action_id: str = Field(default_factory=lambda: f"act_{uuid.uuid4().hex[:8]}")
    name: str
    tool_name: Optional[str] = None
    parameters: Dict[str, Any] = Field(default_factory=dict)
    status: TaskStatus = TaskStatus.PENDING
    output: Optional[Any] = None
    error_message: Optional[str] = None


class SubTask(BaseModel):
    """SubTask node level."""

    subtask_id: str = Field(default_factory=lambda: f"sub_{uuid.uuid4().hex[:8]}")
    name: str
    actions: List[Action] = Field(default_factory=list)
    status: TaskStatus = TaskStatus.PENDING


class Task(BaseModel):
    """Task node level."""

    task_id: str = Field(default_factory=lambda: f"task_{uuid.uuid4().hex[:8]}")
    name: str
    description: str
    priority: int = 1
    dependencies: List[str] = Field(default_factory=list)
    estimated_duration_s: float = 2.0
    confidence: float = 0.90
    required_tools: List[str] = Field(default_factory=list)
    required_knowledge: List[str] = Field(default_factory=list)
    status: TaskStatus = TaskStatus.PENDING
    retry_counter: int = 0
    subtasks: List[SubTask] = Field(default_factory=list)
    output: Optional[Any] = None


class Objective(BaseModel):
    """Objective node level."""

    objective_id: str = Field(default_factory=lambda: f"obj_{uuid.uuid4().hex[:8]}")
    title: str
    tasks: List[Task] = Field(default_factory=list)
    status: TaskStatus = TaskStatus.PENDING


class ReasoningNode(BaseModel):
    """Structured reasoning step node."""

    node_id: str = Field(default_factory=lambda: f"reason_{uuid.uuid4().hex[:8]}")
    reasoning_mode: str = "deductive"  # deductive, inductive, abductive, analogical, step_by_step, tree
    reason: str
    evidence: List[str] = Field(default_factory=list)
    confidence: float = 0.90
    assumptions: List[str] = Field(default_factory=list)
    alternatives: List[str] = Field(default_factory=list)


class DecisionNode(BaseModel):
    """Scored strategy decision node."""

    decision_id: str = Field(default_factory=lambda: f"dec_{uuid.uuid4().hex[:8]}")
    strategy_name: str  # fastest, cheapest, highest_quality, balanced
    score: float
    success_probability: float
    estimated_cost: float
    estimated_latency_s: float
    risk_score: float
    selected: bool = False


class Plan(BaseModel):
    """Complete hierarchical plan structure."""

    plan_id: str = Field(default_factory=lambda: f"plan_{uuid.uuid4().hex[:8]}")
    goal: Goal
    objectives: List[Objective] = Field(default_factory=list)
    dependencies: List[Dependency] = Field(default_factory=list)
    decision: Optional[DecisionNode] = None
    reasoning_trace: List[ReasoningNode] = Field(default_factory=list)
    status: TaskStatus = TaskStatus.PENDING
    created_at: float = Field(default_factory=time.time)


class ExecutionState(BaseModel):
    """Runtime execution state monitor."""

    plan_id: str
    total_tasks: int = 0
    completed_tasks: int = 0
    failed_tasks: int = 0
    running_tasks: int = 0
    blocked_tasks: int = 0
    replans_count: int = 0
    critical_path_length: int = 0
    progress_percentage: float = 0.0
