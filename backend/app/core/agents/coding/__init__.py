"""
Enterprise Autonomous Coding & Software Engineering Agent Package Initialization.
"""

from app.core.agents.coding.coding_agent_types import (
    CodeAgent,
    RepositoryContext,
    Workspace,
    CodeTask,
    CodePlan,
    FileChange,
    Patch,
    TestExecution,
    BuildResult,
    StaticAnalysisResult,
    CodeReviewFinding,
    CodeReview,
    ErrorDiagnosis,
    DebugSession,
    RefactoringPlan,
    CodingMetrics,
)
from app.core.agents.coding.code_analysis_engine import code_analysis_engine, CodeAnalysisEngine
from app.core.agents.coding.code_search_engine import code_search_engine, CodeSearchEngine, CodeSearchResult
from app.core.agents.coding.coding_planner import coding_planner, CodingPlanner
from app.core.agents.coding.code_generation_engine import code_generation_engine, CodeGenerationEngine
from app.core.agents.coding.patch_manager import patch_manager, PatchManager
from app.core.agents.coding.test_execution_engine import test_execution_engine, TestExecutionEngine
from app.core.agents.coding.debugging_engine import debugging_engine, DebuggingEngine
from app.core.agents.coding.code_review_engine import code_review_engine, CodeReviewEngine
from app.core.agents.coding.coding_agent_orchestrator import coding_agent_orchestrator, CodingAgentOrchestrator, AutonomousCodingResult

__all__ = [
    "CodeAgent",
    "RepositoryContext",
    "Workspace",
    "CodeTask",
    "CodePlan",
    "FileChange",
    "Patch",
    "TestExecution",
    "BuildResult",
    "StaticAnalysisResult",
    "CodeReviewFinding",
    "CodeReview",
    "ErrorDiagnosis",
    "DebugSession",
    "RefactoringPlan",
    "CodingMetrics",
    "code_analysis_engine",
    "CodeAnalysisEngine",
    "code_search_engine",
    "CodeSearchEngine",
    "CodeSearchResult",
    "coding_planner",
    "CodingPlanner",
    "code_generation_engine",
    "CodeGenerationEngine",
    "patch_manager",
    "PatchManager",
    "test_execution_engine",
    "TestExecutionEngine",
    "debugging_engine",
    "DebuggingEngine",
    "code_review_engine",
    "CodeReviewEngine",
    "coding_agent_orchestrator",
    "CodingAgentOrchestrator",
    "AutonomousCodingResult",
]
