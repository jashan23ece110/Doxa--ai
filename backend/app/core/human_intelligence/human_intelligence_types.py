"""
Human Intelligence & Social Engineering Defense Platform Data Types & Pydantic Schemas.

Defines Pydantic models for employee profiles, organizational structures, human risk scores,
security awareness training records, behavioral observations, insider risk indicators, and dashboards.
"""

import time
import uuid
from enum import Enum
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class HumanRiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class EmployeeProfile(BaseModel):
    employee_id: str = Field(default_factory=lambda: f"emp_{uuid.uuid4().hex[:8]}")
    name: str
    email: str
    department: str
    role: str
    clearance_level: str = "standard"
    security_score: float = 85.0  # 0 to 100
    risk_level: HumanRiskLevel = HumanRiskLevel.LOW
    created_at: float = Field(default_factory=time.time)
    updated_at: float = Field(default_factory=time.time)


class DepartmentProfile(BaseModel):
    department_id: str
    department_name: str
    total_employees: int = 0
    average_security_score: float = 80.0
    high_risk_employee_count: int = 0


class OrganizationProfile(BaseModel):
    org_id: str
    org_name: str
    industry: str = "Technology"
    total_departments: int = 0
    overall_human_risk_score: float = 2.5  # 0 to 10 scale
    departments: List[DepartmentProfile] = Field(default_factory=list)


class BehaviorPattern(BaseModel):
    pattern_id: str
    category: str  # authentication, data_access, email_handling, device_usage
    description: str
    anomaly_score: float = 0.0  # 0.0 to 1.0
    observed_count: int = 1


class AwarenessAssessment(BaseModel):
    assessment_id: str = Field(default_factory=lambda: f"ass_{uuid.uuid4().hex[:8]}")
    employee_id: str
    topic: str  # phishing_awareness, password_hygiene, social_engineering
    score: float = 90.0  # % score
    passed: bool = True
    completed_at: float = Field(default_factory=time.time)


class SecurityTrainingRecord(BaseModel):
    record_id: str = Field(default_factory=lambda: f"trn_{uuid.uuid4().hex[:8]}")
    employee_id: str
    course_name: str
    status: str = "completed"  # assigned, in_progress, completed, expired
    completion_date: float = Field(default_factory=time.time)


class PhishingSimulation(BaseModel):
    simulation_id: str = Field(default_factory=lambda: f"psim_{uuid.uuid4().hex[:8]}")
    target_department: str
    scenario_type: str  # credential_harvesting_defense, spear_phishing_awareness
    employees_tested_count: int = 0
    click_rate_percent: float = 5.0
    reporting_rate_percent: float = 85.0
    conducted_at: float = Field(default_factory=time.time)


class SocialEngineeringScenario(BaseModel):
    scenario_id: str
    title: str
    vector: str  # email, phone, physical, messaging
    difficulty: str = "medium"
    defensive_guidance: str


class InsiderRiskIndicator(BaseModel):
    indicator_id: str = Field(default_factory=lambda: f"iri_{uuid.uuid4().hex[:8]}")
    employee_id: str
    risk_category: str  # unusual_data_exfiltration_attempt, policy_violation, off_hours_access
    severity: HumanRiskLevel = HumanRiskLevel.MEDIUM
    description: str
    detected_at: float = Field(default_factory=time.time)


class TrustRelationship(BaseModel):
    source_employee_id: str
    target_employee_id: str
    relationship_type: str  # manager, peer, cross_functional
    trust_score: float = 0.9


class OrganizationalHierarchy(BaseModel):
    org_id: str
    structure: Dict[str, List[str]] = Field(default_factory=dict)  # manager_id -> [direct_report_ids]


class HumanSecurityEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: f"hevt_{uuid.uuid4().hex[:8]}")
    employee_id: str
    event_type: str
    description: str
    timestamp: float = Field(default_factory=time.time)


class BehavioralObservation(BaseModel):
    observation_id: str = Field(default_factory=lambda: f"obs_{uuid.uuid4().hex[:8]}")
    employee_id: str
    observation_type: str
    anomaly_detected: bool = False
    details: Dict[str, Any] = Field(default_factory=dict)
    observed_at: float = Field(default_factory=time.time)


class HumanRiskProfile(BaseModel):
    employee_id: str
    overall_risk_score: float = 2.0  # 0.0 to 10.0 scale
    risk_level: HumanRiskLevel = HumanRiskLevel.LOW
    factors: List[str] = Field(default_factory=list)
    last_evaluated: float = Field(default_factory=time.time)


class HumanIntelligenceReport(BaseModel):
    report_id: str = Field(default_factory=lambda: f"hir_{uuid.uuid4().hex[:8]}")
    title: str
    employee_id: Optional[str] = None
    department_name: Optional[str] = None
    executive_summary: str
    risk_assessment: HumanRiskProfile
    recommended_trainings: List[str] = Field(default_factory=list)
    generated_at: float = Field(default_factory=time.time)


class SecurityRecommendation(BaseModel):
    recommendation_id: str = Field(default_factory=lambda: f"rec_{uuid.uuid4().hex[:8]}")
    target_type: str  # employee, department, organization
    target_id: str
    title: str
    priority: str = "HIGH"
    action_items: List[str] = Field(default_factory=list)


class HumanRiskMetrics(BaseModel):
    total_employees_monitored: int = 0
    average_org_security_score: float = 84.5
    high_risk_employees_count: int = 0
    phishing_susceptibility_percent: float = 4.2
    training_compliance_percent: float = 96.0
    updated_at: float = Field(default_factory=time.time)


class HumanDashboardState(BaseModel):
    metrics: HumanRiskMetrics = Field(default_factory=HumanRiskMetrics)
    recent_assessments: List[AwarenessAssessment] = Field(default_factory=list)
    top_risk_indicators: List[InsiderRiskIndicator] = Field(default_factory=list)
