"""
Workflow Models for Autonomous Workflow Execution Engine.

Defines Pydantic data models for Workflow, WorkflowNode, WorkflowTask,
WorkflowCheckpoint, WorkflowExecution, WorkflowResult, WorkflowArtifact, and WorkflowState.
"""

import time
import uuid
from enum import Enum
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class WorkflowState(str, Enum):
    """Workflow execution state enum."""

    PENDING = "pending"
    RUNNING = "running"
    WAITING_APPROVAL = "waiting_approval"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    RETRYING = "retrying"
    ROLLING_BACK = "rolling_back"


class WorkflowArtifact(BaseModel):
    """Versioned workflow output artifact."""

    artifact_id: str = Field(default_factory=lambda: f"art_{uuid.uuid4().hex[:8]}")
    name: str
    category: str = "document"  # document, code, reasoning, report, log, image, json
    content: Any
    version: int = 1
    created_at: float = Field(default_factory=time.time)


class WorkflowNode(BaseModel):
    """Execution DAG node in workflow."""

    node_id: str = Field(default_factory=lambda: f"node_{uuid.uuid4().hex[:8]}")
    name: str
    node_type: str = "task"  # task, parallel, conditional, checkpoint, approval
    dependencies: List[str] = Field(default_factory=list)
    status: WorkflowState = WorkflowState.PENDING
    assigned_agent: Optional[str] = None
    action_handler: Optional[str] = None
    input_data: Dict[str, Any] = Field(default_factory=dict)
    output: Optional[Any] = None
    error_message: Optional[str] = None
    is_reversible: bool = True
    retry_count: int = 0
    max_retries: int = 3
    latency_ms: float = 0.0


class WorkflowTask(WorkflowNode):
    """Task node specialization."""

    pass


class WorkflowCheckpoint(BaseModel):
    """Execution state progress snapshot."""

    checkpoint_id: str = Field(default_factory=lambda: f"chk_{uuid.uuid4().hex[:8]}")
    workflow_id: str
    completed_node_ids: List[str] = Field(default_factory=list)
    outputs: Dict[str, Any] = Field(default_factory=dict)
    memory_snapshot: Dict[str, Any] = Field(default_factory=dict)
    timestamp: float = Field(default_factory=time.time)


class WorkflowExecution(BaseModel):
    """Workflow execution tracker."""

    execution_id: str = Field(default_factory=lambda: f"exec_{uuid.uuid4().hex[:8]}")
    workflow_id: str
    active_node_ids: List[str] = Field(default_factory=list)
    progress_percentage: float = 0.0
    start_time: float = Field(default_factory=time.time)
    end_time: Optional[float] = None


class WorkflowResult(BaseModel):
    """Final workflow execution result."""

    workflow_id: str
    status: WorkflowState
    output: Any
    artifacts: List[WorkflowArtifact] = Field(default_factory=list)
    execution_duration_s: float = 0.0


class Workflow(BaseModel):
    """Complete executable workflow representation."""

    workflow_id: str = Field(default_factory=lambda: f"wf_{uuid.uuid4().hex[:8]}")
    name: str
    user_id: str = "default_user"
    status: WorkflowState = WorkflowState.PENDING
    nodes: Dict[str, WorkflowNode] = Field(default_factory=dict)
    checkpoints: List[WorkflowCheckpoint] = Field(default_factory=list)
    artifacts: List[WorkflowArtifact] = Field(default_factory=list)
    error_message: Optional[str] = None
    created_at: float = Field(default_factory=time.time)
