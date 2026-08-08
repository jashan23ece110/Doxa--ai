"""
Unified Autonomous Intelligence Core & AI Operating System Package Initialization.
"""

from app.core.intelligence.intelligence_types import (
    ExecutionMode,
    TaskPriority,
    TaskType,
    ExecutionStatus,
    DecisionGraphNode,
    AdaptiveExecutionGraph,
    ContextItem,
    UnifiedGlobalContext,
    IntelligenceTask,
    OptimizationCacheEntry,
    ComponentLatencyTrace,
    PipelineTrace,
    PolicyRecommendation,
    KnowledgeFlowStep,
    KnowledgeFlowRecord,
    KernelExecutionState,
    SystemDashboardMetrics,
)
from app.core.intelligence.decision_engine import adaptive_decision_engine, AdaptiveDecisionEngine
from app.core.intelligence.context_manager import global_context_manager, GlobalContextManager
from app.core.intelligence.scheduler import intelligence_scheduler, IntelligenceScheduler
from app.core.intelligence.optimizer import execution_optimizer, ExecutionOptimizer
from app.core.intelligence.pipeline_profiler import pipeline_profiler, PipelineProfiler
from app.core.intelligence.auto_optimizer import autonomous_optimizer, AutonomousOptimizer
from app.core.intelligence.knowledge_flow import knowledge_flow_engine, KnowledgeFlowEngine
from app.core.intelligence.dashboard_backend import operational_dashboard_backend, OperationalDashboardBackend
from app.core.intelligence.intelligence_core import global_intelligence_orchestrator, GlobalIntelligenceOrchestrator
from app.core.intelligence.kernel import ai_os_kernel, AIOSKernel

__all__ = [
    # Enums
    "ExecutionMode",
    "TaskPriority",
    "TaskType",
    "ExecutionStatus",
    # Models
    "DecisionGraphNode",
    "AdaptiveExecutionGraph",
    "ContextItem",
    "UnifiedGlobalContext",
    "IntelligenceTask",
    "OptimizationCacheEntry",
    "ComponentLatencyTrace",
    "PipelineTrace",
    "PolicyRecommendation",
    "KnowledgeFlowStep",
    "KnowledgeFlowRecord",
    "KernelExecutionState",
    "SystemDashboardMetrics",
    # Engines & Instances
    "adaptive_decision_engine",
    "AdaptiveDecisionEngine",
    "global_context_manager",
    "GlobalContextManager",
    "intelligence_scheduler",
    "IntelligenceScheduler",
    "execution_optimizer",
    "ExecutionOptimizer",
    "pipeline_profiler",
    "PipelineProfiler",
    "autonomous_optimizer",
    "AutonomousOptimizer",
    "knowledge_flow_engine",
    "KnowledgeFlowEngine",
    "operational_dashboard_backend",
    "OperationalDashboardBackend",
    "global_intelligence_orchestrator",
    "GlobalIntelligenceOrchestrator",
    "ai_os_kernel",
    "AIOSKernel",
]
