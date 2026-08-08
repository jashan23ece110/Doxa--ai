"""
Runtime Data Models for Enterprise AI Operating System Runtime.

Defines Pydantic data models for ClusterNode, NodeHealth, ServiceEndpoint, BackupSnapshot,
RecoveryPlan, DeploymentRelease, ScalingRule, SystemRegistryState, ValidationResult, and SystemReport.
"""

import time
import uuid
from enum import Enum
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class NodeRole(str, Enum):
    """Cluster node role enum."""

    LEADER = "leader"
    FOLLOWER = "follower"
    WORKER = "worker"


class NodeHealth(str, Enum):
    """Cluster node health state."""

    HEALTHY = "healthy"
    DEGRADED = "degraded"
    OFFLINE = "offline"


class ClusterNode(BaseModel):
    """Cluster node membership record."""

    node_id: str = Field(default_factory=lambda: f"node_{uuid.uuid4().hex[:8]}")
    hostname: str = "node-1.doxa.internal"
    ip_address: str = "127.0.0.1"
    role: NodeRole = NodeRole.LEADER
    health: NodeHealth = NodeHealth.HEALTHY
    active_workers: int = 16
    last_heartbeat: float = Field(default_factory=time.time)


class ServiceEndpoint(BaseModel):
    """Discovered service endpoint record."""

    service_name: str
    endpoint_url: str
    is_active: bool = True
    latency_ms: float = 0.0


class BackupSnapshot(BaseModel):
    """System data backup snapshot metadata."""

    backup_id: str = Field(default_factory=lambda: f"bak_{uuid.uuid4().hex[:8]}")
    components_included: List[str] = Field(default_factory=list)
    file_path: str
    size_bytes: int = 0
    created_at: float = Field(default_factory=time.time)


class RecoveryPlan(BaseModel):
    """Disaster recovery plan."""

    plan_id: str = Field(default_factory=lambda: f"recplan_{uuid.uuid4().hex[:8]}")
    target_backup_id: str
    recovery_status: str = "COMPLETED"
    restored_at: float = Field(default_factory=time.time)


class DeploymentRelease(BaseModel):
    """Release management deployment record."""

    release_id: str = Field(default_factory=lambda: f"rel_{uuid.uuid4().hex[:8]}")
    version: str = "4.8.0"
    strategy: str = "canary"  # rolling, blue-green, canary
    status: str = "DEPLOYED"
    deployed_at: float = Field(default_factory=time.time)


class ScalingRule(BaseModel):
    """Auto-scaling rule definition."""

    rule_id: str = Field(default_factory=lambda: f"scale_{uuid.uuid4().hex[:8]}")
    target_metric: str = "cpu_usage"
    threshold_pct: float = 80.0
    action: str = "scale_up"
    min_workers: int = 4
    max_workers: int = 64


class SystemRegistryState(BaseModel):
    """Summary of registered runtime components."""

    total_agents: int = 10
    total_providers: int = 4
    total_tools: int = 5
    total_services: int = 12
    total_workers: int = 16


class ValidationResult(BaseModel):
    """Production readiness validation result."""

    is_ready: bool = True
    passed_checks_count: int = 15
    failed_checks_count: int = 0
    warnings: List[str] = Field(default_factory=list)
    timestamp: float = Field(default_factory=time.time)


class SystemReport(BaseModel):
    """Comprehensive 8-stage operational report."""

    report_id: str = Field(default_factory=lambda: f"report_{uuid.uuid4().hex[:8]}")
    platform_name: str = "Doxa Enterprise AI Operating System"
    version: str = "4.8.0"
    enterprise_readiness_score: int = 100
    runtime_health: str = "HEALTHY"
    cluster_nodes_count: int = 1
    active_workflows_count: int = 0
    audit_logs_count: int = 1
    timestamp: float = Field(default_factory=time.time)
