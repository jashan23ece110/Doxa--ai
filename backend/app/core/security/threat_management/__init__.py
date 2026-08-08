"""
Enterprise Vulnerability Assessment, Threat Intelligence & Security Automation Platform Package Initialization.
"""

from app.core.security.threat_management.vulnerability_engine import (
    vulnerability_engine,
    VulnerabilityEngine,
    VulnerabilityMetadata,
)
from app.core.security.threat_management.threat_model_engine import (
    threat_model_engine,
    ThreatModelEngine,
    ThreatModel,
    STRIDEThreat,
)
from app.core.security.threat_management.attack_surface_analyzer import (
    attack_surface_analyzer,
    AttackSurfaceAnalyzer,
    AttackSurfaceInventory,
    ExposedInterface,
)
from app.core.security.threat_management.security_policy_engine import (
    security_policy_engine,
    SecurityPolicyEngine,
    SecurityPolicyRule,
    PolicyEvaluationResult,
)
from app.core.security.threat_management.security_automation import (
    security_automation_engine,
    SecurityAutomationEngine,
    AutomationTaskResult,
)
from app.core.security.threat_management.continuous_monitor import (
    continuous_monitor_engine,
    ContinuousMonitorEngine,
    ContinuousMonitoringMetrics,
)
from app.core.security.threat_management.compliance_engine import (
    compliance_assessment_engine,
    ComplianceAssessmentEngine,
    FrameworkComplianceResult,
)
from app.core.security.threat_management.recommendation_engine import (
    ai_recommendation_engine,
    AIRecommendationEngine,
    SecurityRecommendation,
)
from app.core.security.threat_management.security_dashboard_backend import (
    threat_dashboard_backend,
    ThreatDashboardBackend,
    ThreatManagementDashboardMetrics,
)
from app.core.security.threat_management.threat_report_builder import (
    threat_intel_report_builder,
    ThreatIntelligenceReportBuilder,
)

__all__ = [
    "vulnerability_engine",
    "VulnerabilityEngine",
    "VulnerabilityMetadata",
    "threat_model_engine",
    "ThreatModelEngine",
    "ThreatModel",
    "STRIDEThreat",
    "attack_surface_analyzer",
    "AttackSurfaceAnalyzer",
    "AttackSurfaceInventory",
    "ExposedInterface",
    "security_policy_engine",
    "SecurityPolicyEngine",
    "SecurityPolicyRule",
    "PolicyEvaluationResult",
    "security_automation_engine",
    "SecurityAutomationEngine",
    "AutomationTaskResult",
    "continuous_monitor_engine",
    "ContinuousMonitorEngine",
    "ContinuousMonitoringMetrics",
    "compliance_assessment_engine",
    "ComplianceAssessmentEngine",
    "FrameworkComplianceResult",
    "ai_recommendation_engine",
    "AIRecommendationEngine",
    "SecurityRecommendation",
    "threat_dashboard_backend",
    "ThreatDashboardBackend",
    "ThreatManagementDashboardMetrics",
    "threat_intel_report_builder",
    "ThreatIntelligenceReportBuilder",
]
