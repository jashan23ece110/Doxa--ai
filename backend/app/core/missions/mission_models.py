"""
Mission Models for Autonomous Mission Control System.

Defines Pydantic data models for Mission, GoalItem, Milestone, ProgressSnapshot,
MissionState, and MissionRecoveryEvent.
"""

import time
import uuid
from enum import Enum
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class MissionState(str, Enum):
    """Mission lifecycle state enum."""

    PENDING = "pending"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    ARCHIVED = "archived"


class Milestone(BaseModel):
    """Milestone marker within a mission."""

    milestone_id: str = Field(default_factory=lambda: f"ms_{uuid.uuid4().hex[:8]}")
    title: str
    description: str
    target_goal_ids: List[str] = Field(default_factory=list)
    completed: bool = False
    reward_score: float = 1.0
    completed_at: Optional[float] = None


class GoalItem(BaseModel):
    """Hierarchical goal item node."""

    goal_id: str = Field(default_factory=lambda: f"goal_{uuid.uuid4().hex[:8]}")
    title: str
    description: str
    parent_goal_id: Optional[str] = None
    sub_goal_ids: List[str] = Field(default_factory=list)
    dependencies: List[str] = Field(default_factory=list)
    priority_score: float = 0.80
    business_value: float = 1.0
    urgency: float = 0.50
    risk_score: float = 0.10
    completed: bool = False
    workflow_id: Optional[str] = None
    output: Optional[Any] = None


class ProgressSnapshot(BaseModel):
    """Snapshot of mission progress percentage over time."""

    snapshot_id: str = Field(default_factory=lambda: f"snap_{uuid.uuid4().hex[:8]}")
    mission_id: str
    progress_percentage: float
    completed_goals_count: int
    total_goals_count: int
    timestamp: float = Field(default_factory=time.time)


class MissionRecoveryEvent(BaseModel):
    """Failure recovery event record."""

    event_id: str = Field(default_factory=lambda: f"rec_{uuid.uuid4().hex[:8]}")
    mission_id: str
    failed_component: str
    error_message: str
    recovery_action: str
    timestamp: float = Field(default_factory=time.time)


class Mission(BaseModel):
    """Long-horizon mission control instance."""

    mission_id: str = Field(default_factory=lambda: f"mission_{uuid.uuid4().hex[:8]}")
    name: str
    user_id: str = "default_user"
    status: MissionState = MissionState.PENDING
    primary_goal: str
    goals: Dict[str, GoalItem] = Field(default_factory=dict)
    milestones: List[Milestone] = Field(default_factory=list)
    snapshots: List[ProgressSnapshot] = Field(default_factory=list)
    recovery_events: List[MissionRecoveryEvent] = Field(default_factory=list)
    overall_progress_percentage: float = 0.0
    created_at: float = Field(default_factory=time.time)
    updated_at: float = Field(default_factory=time.time)
