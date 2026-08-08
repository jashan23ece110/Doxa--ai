"""
Enterprise Agent Memory & Autonomy Types & Data Schemas.

Comprehensive Pydantic models for AgentMemory, MemoryEpisode, MemoryFact, LearnedSkill,
WorkflowTemplate, ExecutionPattern, FailurePattern, SuccessPattern, AgentExperience,
MemoryRetrieval, MemoryUpdate, WorkflowCheckpoint, and AutonomyMetrics.
"""

import time
import uuid
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class MemoryFact(BaseModel):
    fact_id: str = Field(default_factory=lambda: f"fact_{uuid.uuid4().hex[:8]}")
    subject: str
    predicate: str
    object_val: str
    confidence: float = 0.95
    provenance: str = "Agent_Observation"
    created_at: float = Field(default_factory=time.time)


class MemoryEpisode(BaseModel):
    episode_id: str = Field(default_factory=lambda: f"ep_{uuid.uuid4().hex[:8]}")
    goal_id: str
    agent_id: str
    action_taken: str
    result_outcome: str
    success: bool = True
    confidence: float = 0.92
    created_at: float = Field(default_factory=time.time)


class LearnedSkill(BaseModel):
    skill_id: str = Field(default_factory=lambda: f"skill_{uuid.uuid4().hex[:8]}")
    name: str
    category: str  # RESEARCH, CODING, TESTING, DEVOPS, ANALYSIS
    version: str = "1.0.0"
    required_capability: str
    description: str
    success_rate: float = 0.96
    registered_at: float = Field(default_factory=time.time)


class WorkflowTemplate(BaseModel):
    template_id: str = Field(default_factory=lambda: f"tmpl_{uuid.uuid4().hex[:8]}")
    name: str
    version: str = "1.0.0"
    steps: List[str] = Field(default_factory=list)
    agent_roles_required: List[str] = Field(default_factory=list)
    created_at: float = Field(default_factory=time.time)


class ExecutionPattern(BaseModel):
    pattern_id: str = Field(default_factory=lambda: f"epat_{uuid.uuid4().hex[:8]}")
    pattern_name: str
    is_successful: bool = True
    efficiency_score: float = 0.90


class FailurePattern(BaseModel):
    pattern_id: str = Field(default_factory=lambda: f"fpat_{uuid.uuid4().hex[:8]}")
    category: str  # TOOL_FAILURE, TIMEOUT, PERMISSION_DENIED
    root_cause: str
    prevention_recommendation: str


class SuccessPattern(BaseModel):
    pattern_id: str = Field(default_factory=lambda: f"spat_{uuid.uuid4().hex[:8]}")
    strategy_name: str
    success_count: int = 1


class AgentExperience(BaseModel):
    experience_id: str = Field(default_factory=lambda: f"exp_{uuid.uuid4().hex[:8]}")
    agent_id: str
    task_category: str
    outcomes_history: List[str] = Field(default_factory=list)
    average_score: float = 0.95


class MemoryRetrieval(BaseModel):
    query: str
    retrieved_facts: List[MemoryFact] = Field(default_factory=list)
    retrieved_episodes: List[MemoryEpisode] = Field(default_factory=list)
    latency_ms: float = 0.0


class MemoryUpdate(BaseModel):
    agent_id: str
    facts_added_count: int = 0
    episodes_added_count: int = 0


class WorkflowCheckpoint(BaseModel):
    checkpoint_id: str = Field(default_factory=lambda: f"achk_{uuid.uuid4().hex[:8]}")
    workflow_id: str
    step_index: int
    state_data: Dict[str, Any] = Field(default_factory=dict)
    timestamp: float = Field(default_factory=time.time)


class AutonomyMetrics(BaseModel):
    memories_stored_count: int = 0
    skills_registered_count: int = 0
    templates_created_count: int = 0
    failures_analyzed_count: int = 0
    workflows_recovered_count: int = 0
    autonomy_level: str = "BOUNDED_AUTONOMOUS"


class AgentMemory(BaseModel):
    memory_id: str = Field(default_factory=lambda: f"amem_{uuid.uuid4().hex[:8]}")
    agent_id: str
    facts: List[MemoryFact] = Field(default_factory=list)
    episodes: List[MemoryEpisode] = Field(default_factory=list)
    updated_at: float = Field(default_factory=time.time)
