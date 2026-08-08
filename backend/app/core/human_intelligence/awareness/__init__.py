"""
Enterprise Security Awareness, Phishing Simulation & Assessment Package Initialization.
"""

from app.core.human_intelligence.awareness.campaign_manager import (
    campaign_manager,
    CampaignManager,
    AwarenessCampaign,
)
from app.core.human_intelligence.awareness.phishing_simulation_engine import (
    phishing_simulation_engine,
    PhishingSimulationEngine,
    MockSimulationResult,
)
from app.core.human_intelligence.awareness.assessment_engine import (
    assessment_engine,
    AssessmentEngine,
    AssessmentQuizQuestion,
    AssessmentEvaluationResult,
)
from app.core.human_intelligence.awareness.training_engine import (
    enterprise_training_engine,
    EnterpriseTrainingEngine,
    TrainingModule,
)
from app.core.human_intelligence.awareness.awareness_scoring import (
    awareness_scoring_engine,
    AwarenessScoringEngine,
    DetailedAwarenessScore,
)
from app.core.human_intelligence.awareness.scenario_library import (
    scenario_library,
    ScenarioLibrary,
)
from app.core.human_intelligence.awareness.learning_analytics import (
    learning_analytics_engine,
    LearningAnalyticsEngine,
    DepartmentLearningMetrics,
)
from app.core.human_intelligence.awareness.recommendation_engine import (
    ai_learning_recommendation_engine,
    AILearningRecommendationEngine,
)
from app.core.human_intelligence.awareness.awareness_dashboard_backend import (
    awareness_dashboard_backend,
    AwarenessDashboardBackend,
    AwarenessDashboardStateMetrics,
)
from app.core.human_intelligence.awareness.awareness_report_builder import (
    awareness_report_builder,
    AwarenessReportBuilder,
)

__all__ = [
    "campaign_manager",
    "CampaignManager",
    "AwarenessCampaign",
    "phishing_simulation_engine",
    "PhishingSimulationEngine",
    "MockSimulationResult",
    "assessment_engine",
    "AssessmentEngine",
    "AssessmentQuizQuestion",
    "AssessmentEvaluationResult",
    "enterprise_training_engine",
    "EnterpriseTrainingEngine",
    "TrainingModule",
    "awareness_scoring_engine",
    "AwarenessScoringEngine",
    "DetailedAwarenessScore",
    "scenario_library",
    "ScenarioLibrary",
    "learning_analytics_engine",
    "LearningAnalyticsEngine",
    "DepartmentLearningMetrics",
    "ai_learning_recommendation_engine",
    "AILearningRecommendationEngine",
    "awareness_dashboard_backend",
    "AwarenessDashboardBackend",
    "AwarenessDashboardStateMetrics",
    "awareness_report_builder",
    "AwarenessReportBuilder",
]
