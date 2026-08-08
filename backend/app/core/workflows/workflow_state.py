"""
Workflow State and Data Models for Enterprise Autonomous Workflow Engine.

Defines WorkflowState enum, WorkflowTask, WorkflowCheckpoint, and WorkflowInstance Pydantic schemas.
"""

import time
import uuid
from enum import Enum
from typing import Dict, Any, List, Optional, Set
from pydantic import BaseModel, Field


class WorkflowState(str, Enum):
    """Execution status states for workflows and tasks."""

    PENDING = "pending"
    RUNNING = "running"
    WAITING = "waiting"  # Paused awaiting human approval or external trigger
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    RETRYING = "retrying"


class WorkflowTask(BaseModel):
    """Individual task node in a workflow execution DAG."""

    task_id: str
    name: str
    type: str  # agent_task, tool_task, approval_checkpoint, condition
    assigned_agent: Optional[str] = None
    dependencies: List[str] = Field(default_factory=list)
    status: WorkflowState = WorkflowState.PENDING
    retries: int = 0
    max_retries: int = 3
    timeout_seconds: float = 300.0
    output: Optional[Any] = None
    confidence: float = 1.0
    compensation_action: Optional[str] = None  # Reversible action name (e.g., delete_calendar_event)
    requires_approval: bool = False
    metadata: Dict[str, Any] = Field(default_factory=dict)
    latency_ms: float = 0.0


class WorkflowCheckpoint(BaseModel):
    """Progress snapshot for workflow resumption and rollback."""

    checkpoint_id: str = Field(default_factory=lambda: f"chk_{uuid.uuid4().hex[:8]}")
    workflow_id: str
    step_number: int
    completed_task_ids: List[str] = Field(default_factory=list)
    state_variables: Dict[str, Any] = Field(default_factory=dict)
    timestamp: float = Field(default_factory=time.time)


class WorkflowInstance(BaseModel):
    """Full persistent workflow execution container."""

    workflow_id: str = Field(default_factory=lambda: f"wf_{uuid.uuid4().hex[:10]}")
    name: str
    template_name: Optional[str] = None
    user_id: str = "default_user"
    status: WorkflowState = WorkflowState.PENDING
    tasks: Dict[str, WorkflowTask] = Field(default_factory=dict)
    state_variables: Dict[str, Any] = Field(default_factory=dict)
    checkpoints: List[WorkflowCheckpoint] = Field(default_factory=list)
    created_at: float = Field(default_factory=time.time)
    updated_at: float = Field(default_factory=time.time)
    error_message: Optional[str] = None

    def update_timestamp(self) -> None:
        """Updates the last modified timestamp."""
        self.updated_at = time.time()
