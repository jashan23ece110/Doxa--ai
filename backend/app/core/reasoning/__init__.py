"""Reasoning package initialization."""
from app.core.reasoning.evidence_verifier import evidence_verifier, EvidenceVerifier
from app.core.reasoning.contradiction_detector import contradiction_detector, ContradictionDetector
from app.core.reasoning.confidence_estimator import confidence_estimator, ConfidenceEstimator
from app.core.reasoning.reflection_engine import reflection_engine, ReflectionEngine
from app.core.reasoning.reasoning_metrics import reasoning_metrics_tracker, ReasoningMetricsTracker
from app.core.reasoning.task_decomposer import task_decomposer, TaskDecomposer, SubTask
from app.core.reasoning.reasoning_graph import ReasoningGraph, ReasoningGraphNode
from app.core.reasoning.planner import planning_engine, PlanningEngine
from app.core.reasoning.executor import graph_executor, GraphExecutor
from app.core.reasoning.self_reflection import self_reflection_engine, SelfReflectionEngine, ReflectionReport
from app.core.reasoning.verifier import verification_engine, VerificationEngine
from app.core.reasoning.answer_reviser import answer_reviser, AnswerReviser
from app.core.reasoning.confidence_engine import confidence_engine, ConfidenceEngine
from app.core.reasoning.reasoning_engine import reasoning_engine, ReasoningEngine

# Deliberative Reasoning Exports
from app.core.reasoning.reasoning_models import (
    ThoughtNode,
    ThoughtTree,
    ReasoningGraph as DeliberativeReasoningGraph,
    HypothesisCandidate,
    CounterfactualScenario,
    ConsensusResult,
    ReasoningScoreReport,
    DeliberativeReasoningResult,
)
from app.core.reasoning.tree_of_thoughts import tree_of_thoughts_engine, TreeOfThoughtsEngine
from app.core.reasoning.graph_of_thoughts import graph_of_thoughts_engine, GraphOfThoughtsEngine
from app.core.reasoning.hypothesis_engine import hypothesis_engine, HypothesisEngine
from app.core.reasoning.hypothesis_validator import hypothesis_validator, HypothesisValidator
from app.core.reasoning.counterfactual import counterfactual_engine, CounterfactualEngine
from app.core.reasoning.recursive_reasoner import recursive_reasoner, RecursiveReasoner
from app.core.reasoning.consensus_engine import consensus_engine, ConsensusEngine
from app.core.reasoning.reasoning_score import reasoning_score_engine, ReasoningScoreEngine
from app.core.reasoning.reasoning_cache import reasoning_cache, ReasoningCache
from app.core.reasoning.reasoning_analytics import reasoning_analytics_tracker, ReasoningAnalyticsTracker
from app.core.reasoning.reasoning_orchestrator import deliberative_reasoning_orchestrator, DeliberativeReasoningOrchestrator

__all__ = [
    "evidence_verifier",
    "EvidenceVerifier",
    "contradiction_detector",
    "ContradictionDetector",
    "confidence_estimator",
    "ConfidenceEstimator",
    "reflection_engine",
    "ReflectionEngine",
    "reasoning_metrics_tracker",
    "ReasoningMetricsTracker",
    "task_decomposer",
    "TaskDecomposer",
    "SubTask",
    "ReasoningGraph",
    "ReasoningGraphNode",
    "planning_engine",
    "PlanningEngine",
    "graph_executor",
    "GraphExecutor",
    "self_reflection_engine",
    "SelfReflectionEngine",
    "ReflectionReport",
    "verification_engine",
    "VerificationEngine",
    "answer_reviser",
    "AnswerReviser",
    "confidence_engine",
    "ConfidenceEngine",
    "reasoning_engine",
    "ReasoningEngine",
    # Deliberative exports
    "ThoughtNode",
    "ThoughtTree",
    "DeliberativeReasoningGraph",
    "HypothesisCandidate",
    "CounterfactualScenario",
    "ConsensusResult",
    "ReasoningScoreReport",
    "DeliberativeReasoningResult",
    "tree_of_thoughts_engine",
    "TreeOfThoughtsEngine",
    "graph_of_thoughts_engine",
    "GraphOfThoughtsEngine",
    "hypothesis_engine",
    "HypothesisEngine",
    "hypothesis_validator",
    "HypothesisValidator",
    "counterfactual_engine",
    "CounterfactualEngine",
    "recursive_reasoner",
    "RecursiveReasoner",
    "consensus_engine",
    "ConsensusEngine",
    "reasoning_score_engine",
    "ReasoningScoreEngine",
    "reasoning_cache",
    "ReasoningCache",
    "reasoning_analytics_tracker",
    "ReasoningAnalyticsTracker",
    "deliberative_reasoning_orchestrator",
    "DeliberativeReasoningOrchestrator",
]
