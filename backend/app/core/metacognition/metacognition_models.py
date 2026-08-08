"""
Meta-Cognitive Models for Enterprise AI Operating System.

Defines Pydantic data models for CognitiveStrategy, CognitiveStateSnapshot, ConfidenceAssessment,
UncertaintyDetection, CritiqueResult, ReflectionPlan, and MetaAnalyticsSummary.
"""

import time
import uuid
from enum import Enum
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class CognitiveStrategy(str, Enum):
    """Reasoning strategy type enum."""

    DIRECT_QA = "direct_qa"
    RAG = "rag"
    TOOL_CALLING = "tool_calling"
    PYTHON_REASONING = "python_reasoning"
    WORKFLOW_ENGINE = "workflow_engine"
    MULTI_AGENT = "multi_agent"
    TREE_OF_THOUGHTS = "tree_of_thoughts"
    GRAPH_REASONING = "graph_reasoning"
    REFLECTION = "reflection"
    SELF_CRITIQUE = "self_critique"


class CognitiveStateSnapshot(BaseModel):
    """Snapshot of current cognitive state and resource allocation."""

    state_id: str = Field(default_factory=lambda: f"cogstate_{uuid.uuid4().hex[:8]}")
    active_strategy: CognitiveStrategy = CognitiveStrategy.DIRECT_QA
    reasoning_depth: int = 1
    uncertainty_score: float = 0.0
    confidence_score: float = 1.0
    tool_usage_count: int = 0
    memory_usage_count: int = 0
    active_workflows_count: int = 0
    updated_at: float = Field(default_factory=time.time)


class ConfidenceAssessment(BaseModel):
    """Confidence calculation assessment."""

    assessment_id: str = Field(default_factory=lambda: f"conf_{uuid.uuid4().hex[:8]}")
    overall_confidence: float = 0.95
    retrieval_quality_score: float = 0.90
    reasoning_agreement_score: float = 0.95
    tool_reliability_score: float = 1.0
    memory_confidence_score: float = 0.90
    hallucination_risk_score: float = 0.05
    explanation: str = "High reasoning agreement and strong retrieval ground truth."
    timestamp: float = Field(default_factory=time.time)


class UncertaintyDetection(BaseModel):
    """Uncertainty detection report."""

    detection_id: str = Field(default_factory=lambda: f"uncert_{uuid.uuid4().hex[:8]}")
    has_missing_knowledge: bool = False
    has_contradictions: bool = False
    is_ambiguous_query: bool = False
    uncertainty_level: float = 0.1
    reasons: List[str] = Field(default_factory=list)
    timestamp: float = Field(default_factory=time.time)


class CritiqueResult(BaseModel):
    """Self-critique evaluation result."""

    critique_id: str = Field(default_factory=lambda: f"crit_{uuid.uuid4().hex[:8]}")
    is_logically_consistent: bool = True
    is_factually_consistent: bool = True
    reasoning_quality_score: float = 0.92
    critique_notes: List[str] = Field(default_factory=list)
    timestamp: float = Field(default_factory=time.time)


class ReflectionPlan(BaseModel):
    """Self-reflection optimization plan."""

    reflection_id: str = Field(default_factory=lambda: f"refl_{uuid.uuid4().hex[:8]}")
    original_reasoning: str
    identified_weaknesses: List[str] = Field(default_factory=list)
    improved_reasoning_path: str
    quality_gain: float = 0.15
    timestamp: float = Field(default_factory=time.time)


class MetaAnalyticsSummary(BaseModel):
    """Summary of meta-cognitive analytics performance."""

    summary_id: str = Field(default_factory=lambda: f"meta_sum_{uuid.uuid4().hex[:8]}")
    strategy_success_rate: float = 0.98
    confidence_calibration_accuracy: float = 0.94
    reflection_improvements_count: int = 12
    hallucination_frequency_pct: float = 0.5
    timestamp: float = Field(default_factory=time.time)
