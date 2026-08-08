"""
Enterprise Autonomous DevOps & SRE Agent Types & Data Schemas.

Comprehensive Pydantic models for DevOpsAgent, InfrastructureTarget, Environment, DeploymentRequest,
DeploymentPlan, DeploymentStep, PipelineExecution, BuildArtifact, ServiceHealth, InfrastructureMetric,
Incident, RemediationPlan, RollbackPlan, ResourceOptimization, DevOpsAction, DevOpsApproval, and DevOpsMetrics.
"""

import time
import uuid
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class Environment(BaseModel):
    env_id: str = Field(default_factory=lambda: f"env_{uuid.uuid4().hex[:8]}")
    name: str = "production"
    is_production: bool = True
    region: str = "us-east-1"
    active_services_count: int = 15


class InfrastructureTarget(BaseModel):
    target_id: str = Field(default_factory=lambda: f"itarget_{uuid.uuid4().hex[:8]}")
    name: str
    target_type: str  # KUBERNETES_CLUSTER, VIRTUAL_MACHINE, CONTAINER_SERVICE, SERVERLESS
    environment_name: str = "production"
    health_status: str = "HEALTHY"
    ip_address: Optional[str] = "10.0.1.15"


class BuildArtifact(BaseModel):
    artifact_id: str = Field(default_factory=lambda: f"art_{uuid.uuid4().hex[:8]}")
    artifact_name: str
    version: str = "1.0.0"
    digest: str = Field(default_factory=lambda: f"sha256:{uuid.uuid4().hex}")
    created_at: float = Field(default_factory=time.time)


class DeploymentStep(BaseModel):
    step_id: str = Field(default_factory=lambda: f"dstep_{uuid.uuid4().hex[:8]}")
    sequence_index: int
    name: str
    step_type: str  # CANARY, ROLLING, HEALTH_CHECK, ROLLBACK_CHECKPOINT
    status: str = "COMPLETED"


class DeploymentPlan(BaseModel):
    plan_id: str = Field(default_factory=lambda: f"dplan_{uuid.uuid4().hex[:8]}")
    target_environment: str
    strategy: str = "ROLLING"  # CANARY, ROLLING, BLUE_GREEN
    steps: List[DeploymentStep] = Field(default_factory=list)
    requires_approval: bool = False
    is_approved: bool = True
    created_at: float = Field(default_factory=time.time)


class DeploymentRequest(BaseModel):
    request_id: str = Field(default_factory=lambda: f"dreq_{uuid.uuid4().hex[:8]}")
    artifact_id: str
    target_environment: str = "production"
    requested_by: str = "DevOpsAgent"
    requested_at: float = Field(default_factory=time.time)


class PipelineExecution(BaseModel):
    execution_id: str = Field(default_factory=lambda: f"pipe_{uuid.uuid4().hex[:8]}")
    pipeline_name: str
    status: str = "SUCCESS"  # SUCCESS, FAILED, RUNNING, CANCELLED
    duration_sec: float = 1.5
    executed_at: float = Field(default_factory=time.time)


class ServiceHealth(BaseModel):
    service_id: str
    service_name: str
    status: str = "HEALTHY"  # HEALTHY, DEGRADED, UNHEALTHY, DOWN
    latency_p95_ms: float = 45.0
    error_rate_pct: float = 0.01
    cpu_utilization_pct: float = 25.0
    memory_utilization_pct: float = 40.0
    checked_at: float = Field(default_factory=time.time)


class InfrastructureMetric(BaseModel):
    metric_id: str = Field(default_factory=lambda: f"met_{uuid.uuid4().hex[:8]}")
    resource_id: str
    metric_name: str
    value: float
    unit: str = "pct"
    timestamp: float = Field(default_factory=time.time)


class Incident(BaseModel):
    incident_id: str = Field(default_factory=lambda: f"inc_{uuid.uuid4().hex[:8]}")
    service_id: str
    severity: str = "MEDIUM"  # LOW, MEDIUM, HIGH, CRITICAL
    title: str
    description: str
    status: str = "OPEN"  # OPEN, MITIGATED, RESOLVED
    detected_at: float = Field(default_factory=time.time)


class RemediationPlan(BaseModel):
    remediation_id: str = Field(default_factory=lambda: f"rem_{uuid.uuid4().hex[:8]}")
    incident_id: str
    action_type: str  # RESTART_SERVICE, SCALE_OUT, ROLLBACK
    reason: str
    expected_impact: str = "Restores service latency to < 50ms"
    is_executed: bool = False
    created_at: float = Field(default_factory=time.time)


class RollbackPlan(BaseModel):
    rollback_id: str = Field(default_factory=lambda: f"rback_{uuid.uuid4().hex[:8]}")
    target_deployment_id: str
    previous_stable_version: str = "0.9.9"
    status: str = "READY"


class ResourceOptimization(BaseModel):
    optimization_id: str = Field(default_factory=lambda: f"ropt_{uuid.uuid4().hex[:8]}")
    resource_id: str
    recommendation: str = "Scale down idle container count from 10 to 4"
    potential_cost_savings_pct: float = 35.0


class DevOpsAction(BaseModel):
    action_id: str = Field(default_factory=lambda: f"doact_{uuid.uuid4().hex[:8]}")
    action_name: str
    target_resource: str
    status: str = "SUCCESS"


class DevOpsApproval(BaseModel):
    approval_id: str = Field(default_factory=lambda: f"doappr_{uuid.uuid4().hex[:8]}")
    request_id: str
    is_approved: bool = True
    approved_by: str = "SecOpsManager"


class DevOpsMetrics(BaseModel):
    deployments_completed_count: int = 0
    incidents_detected_count: int = 0
    remediations_executed_count: int = 0
    rollbacks_executed_count: int = 0
    average_deployment_duration_sec: float = 0.0


class DevOpsAgent(BaseModel):
    agent_id: str = Field(default_factory=lambda: f"doagent_{uuid.uuid4().hex[:8]}")
    name: str = "AutonomousDevOpsEngineer"
    role: str = "DEVOPS_ENGINEER"
    capabilities: List[str] = Field(default_factory=lambda: ["infra_discovery", "deployment_planning", "monitoring", "remediation", "rollback"])
    is_active: bool = True
