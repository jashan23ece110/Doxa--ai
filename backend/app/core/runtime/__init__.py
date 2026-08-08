"""Runtime package initialization."""
from app.core.runtime.runtime_models import (
    NodeRole,
    NodeHealth,
    ClusterNode,
    ServiceEndpoint,
    BackupSnapshot,
    RecoveryPlan,
    DeploymentRelease,
    ScalingRule,
    SystemRegistryState,
    ValidationResult,
    SystemReport,
)
from app.core.runtime.cluster_manager import cluster_manager, ClusterManager
from app.core.runtime.service_discovery import service_discovery, ServiceDiscovery
from app.core.runtime.config_center import config_center, ConfigCenter
from app.core.runtime.backup_manager import backup_manager, BackupManager
from app.core.runtime.disaster_recovery import disaster_recovery, DisasterRecovery
from app.core.runtime.release_manager import release_manager, ReleaseManager
from app.core.runtime.scaling import scaling_engine, ScalingEngine
from app.core.runtime.registry import system_registry, SystemRegistry
from app.core.runtime.validator import production_validator, ProductionValidator
from app.core.runtime.system_report import system_report_engine, SystemReportEngine
from app.core.runtime.runtime import ai_runtime, AIRuntime

__all__ = [
    "NodeRole",
    "NodeHealth",
    "ClusterNode",
    "ServiceEndpoint",
    "BackupSnapshot",
    "RecoveryPlan",
    "DeploymentRelease",
    "ScalingRule",
    "SystemRegistryState",
    "ValidationResult",
    "SystemReport",
    "cluster_manager",
    "ClusterManager",
    "service_discovery",
    "ServiceDiscovery",
    "config_center",
    "ConfigCenter",
    "backup_manager",
    "BackupManager",
    "disaster_recovery",
    "DisasterRecovery",
    "release_manager",
    "ReleaseManager",
    "scaling_engine",
    "ScalingEngine",
    "system_registry",
    "SystemRegistry",
    "production_validator",
    "ProductionValidator",
    "system_report_engine",
    "SystemReportEngine",
    "ai_runtime",
    "AIRuntime",
]
