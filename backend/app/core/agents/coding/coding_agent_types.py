"""
Enterprise Autonomous Coding Agent Types & Data Schemas.

Comprehensive Pydantic models for CodeAgent, RepositoryContext, Workspace, CodeTask, CodePlan,
CodeChange, FileChange, Patch, TestExecution, BuildResult, StaticAnalysisResult, CodeReview,
DebugSession, ErrorDiagnosis, RefactoringPlan, and CodingMetrics.
"""

import time
import uuid
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class RepositoryContext(BaseModel):
    repo_id: str = Field(default_factory=lambda: f"repo_{uuid.uuid4().hex[:8]}")
    repo_name: str
    root_path: str
    language: str = "python"
    total_files_count: int = 150
    modules: List[str] = Field(default_factory=list)
    created_at: float = Field(default_factory=time.time)


class Workspace(BaseModel):
    workspace_id: str = Field(default_factory=lambda: f"wsp_{uuid.uuid4().hex[:8]}")
    repo_id: str
    branch_name: str = "doxa-agent-branch"
    is_sandboxed: bool = True
    created_at: float = Field(default_factory=time.time)


class FileChange(BaseModel):
    file_path: str
    change_type: str  # ADD, MODIFY, DELETE
    original_content: Optional[str] = None
    new_content: str = ""


class Patch(BaseModel):
    patch_id: str = Field(default_factory=lambda: f"patch_{uuid.uuid4().hex[:8]}")
    repo_id: str
    file_changes: List[FileChange] = Field(default_factory=list)
    summary: str = "Generated automated software change"
    is_applied: bool = False
    created_at: float = Field(default_factory=time.time)


class CodeTask(BaseModel):
    task_id: str = Field(default_factory=lambda: f"ctask_{uuid.uuid4().hex[:8]}")
    goal_description: str
    target_files: List[str] = Field(default_factory=list)
    status: str = "PENDING"  # PENDING, IN_PROGRESS, COMPLETED, FAILED
    created_at: float = Field(default_factory=time.time)


class CodePlan(BaseModel):
    plan_id: str = Field(default_factory=lambda: f"cplan_{uuid.uuid4().hex[:8]}")
    task_id: str
    steps: List[str] = Field(default_factory=list)
    target_files: List[str] = Field(default_factory=list)
    validation_strategy: str = "UNIT_TEST_AND_REVIEW"
    created_at: float = Field(default_factory=time.time)


class TestExecution(BaseModel):
    execution_id: str = Field(default_factory=lambda: f"texec_{uuid.uuid4().hex[:8]}")
    test_command: str = "pytest tests/"
    success: bool = True
    total_tests_count: int = 10
    passed_tests_count: int = 10
    failed_tests_count: int = 0
    duration_sec: float = 0.5
    executed_at: float = Field(default_factory=time.time)


class BuildResult(BaseModel):
    build_id: str = Field(default_factory=lambda: f"build_{uuid.uuid4().hex[:8]}")
    success: bool = True
    exit_code: int = 0
    stdout: str = "Build succeeded cleanly."
    stderr: str = ""
    built_at: float = Field(default_factory=time.time)


class StaticAnalysisResult(BaseModel):
    analysis_id: str = Field(default_factory=lambda: f"sanal_{uuid.uuid4().hex[:8]}")
    issues_found_count: int = 0
    lint_score: float = 10.0
    security_vulnerabilities_count: int = 0


class CodeReviewFinding(BaseModel):
    finding_id: str = Field(default_factory=lambda: f"crf_{uuid.uuid4().hex[:8]}")
    file_path: str
    line_number: int = 1
    severity: str = "LOW"  # INFO, LOW, MEDIUM, HIGH, CRITICAL
    message: str
    suggestion: Optional[str] = None


class CodeReview(BaseModel):
    review_id: str = Field(default_factory=lambda: f"crev_{uuid.uuid4().hex[:8]}")
    patch_id: str
    is_approved: bool = True
    score: float = 9.5
    findings: List[CodeReviewFinding] = Field(default_factory=list)
    reviewed_at: float = Field(default_factory=time.time)


class ErrorDiagnosis(BaseModel):
    diagnosis_id: str = Field(default_factory=lambda: f"diag_{uuid.uuid4().hex[:8]}")
    error_message: str
    root_cause_hypothesis: str
    suggested_fix: str
    confidence_score: float = 0.94


class DebugSession(BaseModel):
    session_id: str = Field(default_factory=lambda: f"debug_{uuid.uuid4().hex[:8]}")
    task_id: str
    diagnoses: List[ErrorDiagnosis] = Field(default_factory=list)
    status: str = "RESOLVED"


class RefactoringPlan(BaseModel):
    plan_id: str = Field(default_factory=lambda: f"refac_{uuid.uuid4().hex[:8]}")
    target_module: str
    refactoring_goal: str
    expected_improvements: List[str] = Field(default_factory=list)


class CodingMetrics(BaseModel):
    tasks_completed_count: int = 0
    patches_created_count: int = 0
    tests_executed_count: int = 0
    code_reviews_completed_count: int = 0
    average_patch_apply_latency_ms: float = 0.0


class CodeAgent(BaseModel):
    agent_id: str = Field(default_factory=lambda: f"cagent_{uuid.uuid4().hex[:8]}")
    name: str = "AutonomousSoftwareEngineer"
    role: str = "SOFTWARE_ENGINEER"
    capabilities: List[str] = Field(default_factory=lambda: ["code_analysis", "code_generation", "testing", "code_review"])
    is_active: bool = True
