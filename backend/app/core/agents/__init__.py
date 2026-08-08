"""
Enterprise Autonomous Agent Platform Package Initialization.
"""

from app.core.agents.agent_types import (
    AgentRole,
    AgentState,
    AgentCapability,
    AgentPermission,
    AgentDefinition,
    AgentGoal,
    PlanStep,
    AgentPlan,
    AgentTask,
    ToolDefinition,
    ToolInvocation,
    ToolResult,
    AgentAction,
    AgentObservation,
    AgentEvaluation,
    AgentMemoryReference,
    AgentContext,
    AgentMessage,
    ApprovalRequest,
    AgentError,
    AgentMetrics,
    AgentExecution,
)
from app.core.agents.agent_registry import agent_registry, AgentRegistry
from app.core.agents.agent_manager import agent_manager, AgentManager
from app.core.agents.goal_manager import goal_manager, GoalManager
from app.core.agents.agent_context_manager import agent_context_manager, AgentContextManager
from app.core.agents.agent_state_store import agent_state_store, AgentStateStore
from app.core.agents.agent_message_bus import agent_message_bus, AgentMessageBus
from app.core.agents.tool_registry import tool_registry, ToolRegistry
from app.core.agents.agent_execution_engine import agent_execution_engine, AgentExecutionEngine
from app.core.agents.agent_orchestrator import agent_orchestrator, AgentOrchestrator, AgentOrchestrationResult
from app.core.agents.platform import autonomous_agent_platform, AutonomousAgentPlatform, autonomous_agent_orchestrator, AutonomousAgentOrchestrator

__all__ = [
    "AgentRole",
    "AgentState",
    "AgentCapability",
    "AgentPermission",
    "AgentDefinition",
    "AgentGoal",
    "PlanStep",
    "AgentPlan",
    "AgentTask",
    "ToolDefinition",
    "ToolInvocation",
    "ToolResult",
    "AgentAction",
    "AgentObservation",
    "AgentEvaluation",
    "AgentMemoryReference",
    "AgentContext",
    "AgentMessage",
    "ApprovalRequest",
    "AgentError",
    "AgentMetrics",
    "AgentExecution",
    "agent_registry",
    "AgentRegistry",
    "agent_manager",
    "AgentManager",
    "goal_manager",
    "GoalManager",
    "agent_context_manager",
    "AgentContextManager",
    "agent_state_store",
    "AgentStateStore",
    "agent_message_bus",
    "AgentMessageBus",
    "tool_registry",
    "ToolRegistry",
    "agent_execution_engine",
    "AgentExecutionEngine",
    "agent_orchestrator",
    "AgentOrchestrator",
    "AgentOrchestrationResult",
    "autonomous_agent_platform",
    "AutonomousAgentPlatform",
    "autonomous_agent_orchestrator",
    "AutonomousAgentOrchestrator",
]
