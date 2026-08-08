"""
Enterprise Global Autonomous Agent Platform Package Initialization.
"""

from app.core.agents.platform.autonomous_agent_platform import autonomous_agent_platform, AutonomousAgentPlatform, MasterPlatformAssessment
from app.core.agents.platform.agent_service_bus import agent_service_bus, AgentServiceBus, AgentEvent
from app.core.agents.platform.autonomous_workflow_engine import autonomous_workflow_engine, AutonomousWorkflowEngine, WorkflowExecutionResult
from app.core.agents.platform.agent_resource_manager import agent_resource_manager, AgentResourceManager, AgentResourceQuota
from app.core.agents.platform.agent_policy_orchestrator import agent_policy_orchestrator, AgentPolicyOrchestrator, AutonomyPolicy
from app.core.agents.platform.agent_evaluation_engine import agent_evaluation_engine, AgentEvaluationEngine, AgentEvaluationScore
from app.core.agents.platform.agent_recovery_manager import agent_recovery_manager, AgentRecoveryManager, RecoveryActionResult
from app.core.agents.platform.agent_observability import agent_observability_platform, AgentObservabilityPlatform, AgentObservabilitySnapshot
from app.core.agents.platform.agent_lifecycle_manager import agent_lifecycle_manager, AgentLifecycleManager, AgentLifecycleStatus
from app.core.agents.platform.autonomous_agent_orchestrator import autonomous_agent_orchestrator, AutonomousAgentOrchestrator, MasterAgentExecutionResult

__all__ = [
    "autonomous_agent_platform",
    "AutonomousAgentPlatform",
    "MasterPlatformAssessment",
    "agent_service_bus",
    "AgentServiceBus",
    "AgentEvent",
    "autonomous_workflow_engine",
    "AutonomousWorkflowEngine",
    "WorkflowExecutionResult",
    "agent_resource_manager",
    "AgentResourceManager",
    "AgentResourceQuota",
    "agent_policy_orchestrator",
    "AgentPolicyOrchestrator",
    "AutonomyPolicy",
    "agent_evaluation_engine",
    "AgentEvaluationEngine",
    "AgentEvaluationScore",
    "agent_recovery_manager",
    "AgentRecoveryManager",
    "RecoveryActionResult",
    "agent_observability_platform",
    "AgentObservabilityPlatform",
    "AgentObservabilitySnapshot",
    "agent_lifecycle_manager",
    "AgentLifecycleManager",
    "AgentLifecycleStatus",
    "autonomous_agent_orchestrator",
    "AutonomousAgentOrchestrator",
    "MasterAgentExecutionResult",
]
