"""Evolution package initialization for Enterprise Self-Optimization Platform."""
from app.core.evolution.evolution_models import (
    CapabilityDimension,
    CapabilityScore,
    CapabilityProfile,
    EvaluationMetric,
    SelfEvaluationScore,
    OptimizationRecommendation,
    OptimizationPlan,
    TuningParameter,
    TuningSnapshot,
    LearningInsight,
    PerformanceLearningRecord,
    RecommendationCategory,
    SystemRecommendation,
    ExperimentVariant,
    ABExperiment,
    EvolutionSnapshot,
    EvolutionAnalyticsSummary,
)
from app.core.evolution.capability_analyzer import capability_analyzer, CapabilityAnalyzer
from app.core.evolution.self_evaluation import self_evaluation_engine, SelfEvaluationEngine
from app.core.evolution.optimization_engine import optimization_engine, OptimizationEngine
from app.core.evolution.adaptive_tuner import adaptive_tuner, AdaptiveTuner
from app.core.evolution.performance_learning import performance_learning_engine, PerformanceLearningEngine
from app.core.evolution.recommendation_engine import improvement_recommendation_engine, ImprovementRecommendationEngine
from app.core.evolution.experiment_manager import experiment_manager, ExperimentManager
from app.core.evolution.evolution_store import evolution_store, EvolutionStore
from app.core.evolution.evolution_analytics import evolution_analytics_tracker, EvolutionAnalyticsTracker
from app.core.evolution.evolution_orchestrator import evolution_orchestrator, EvolutionOrchestrator

__all__ = [
    # Models
    "CapabilityDimension",
    "CapabilityScore",
    "CapabilityProfile",
    "EvaluationMetric",
    "SelfEvaluationScore",
    "OptimizationRecommendation",
    "OptimizationPlan",
    "TuningParameter",
    "TuningSnapshot",
    "LearningInsight",
    "PerformanceLearningRecord",
    "RecommendationCategory",
    "SystemRecommendation",
    "ExperimentVariant",
    "ABExperiment",
    "EvolutionSnapshot",
    "EvolutionAnalyticsSummary",
    # Engines & Instances
    "capability_analyzer",
    "CapabilityAnalyzer",
    "self_evaluation_engine",
    "SelfEvaluationEngine",
    "optimization_engine",
    "OptimizationEngine",
    "adaptive_tuner",
    "AdaptiveTuner",
    "performance_learning_engine",
    "PerformanceLearningEngine",
    "improvement_recommendation_engine",
    "ImprovementRecommendationEngine",
    "experiment_manager",
    "ExperimentManager",
    "evolution_store",
    "EvolutionStore",
    "evolution_analytics_tracker",
    "EvolutionAnalyticsTracker",
    "evolution_orchestrator",
    "EvolutionOrchestrator",
]
