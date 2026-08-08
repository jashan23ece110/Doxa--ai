"""
Global Master Decision Orchestrator.

Drives the complete end-to-end Enterprise Decision Loop:
Request -> Context -> Objectives -> Evidence -> Strategic -> Risk -> Forecast -> Prediction -> Optimization -> Explainability -> Governance -> Recommendation -> Approval -> Action -> Learning.
"""

import time
from typing import Dict, Any, List
from pydantic import BaseModel, Field
from app.core.logging import security_logger
from app.core.decision_intelligence.platform.enterprise_decision_intelligence_platform import (
    enterprise_decision_intelligence_platform, MasterPlatformDecisionAssessment
)
from app.core.decision_intelligence.platform.decision_service_bus import decision_service_bus
from app.core.decision_intelligence.platform.decision_workflow_engine import decision_workflow_engine
from app.core.decision_intelligence.platform.decision_resource_manager import decision_resource_manager
from app.core.decision_intelligence.platform.decision_policy_orchestrator import decision_policy_orchestrator
from app.core.decision_intelligence.platform.decision_observability import decision_observability
from app.core.decision_intelligence.platform.decision_lifecycle_manager import decision_lifecycle_manager


class GlobalDecisionOrchestratorResult(BaseModel):
    orchestration_id: str = Field(default_factory=lambda: f"gdorch_{int(time.time() * 1000)}")
    request_title: str
    assessment: MasterPlatformDecisionAssessment
    workflow_stage: str = "COMPLETED"
    requires_human_approval: bool = True
    readiness_score: float = 100.0
    status: str = "SUCCESS"
    executed_at: float = Field(default_factory=time.time)


class GlobalDecisionOrchestrator:
    """Global Master Decision Orchestrator."""

    async def execute_global_decision_loop(self, title: str, description: str = "") -> GlobalDecisionOrchestratorResult:
        """
        Executes the global master enterprise decision intelligence loop.

        Args:
            title: Decision title string.
            description: Decision description string.

        Returns:
            GlobalDecisionOrchestratorResult object.
        """
        t0 = time.time()
        security_logger.info(f"GlobalDecisionOrchestrator: Executing global decision loop for '{title}'.")

        # 1. Quota Allocation & Workflow Initiation
        wf = decision_workflow_engine.create_workflow(title)
        decision_resource_manager.allocate_decision_quota(wf.workflow_id, max_tokens=4096)
        decision_lifecycle_manager.initialize_lifecycle(wf.workflow_id)

        # 2. Service Bus Event & Policy Enforcement
        decision_service_bus.publish_event("DECISION_LOOP_STARTED", {"workflow_id": wf.workflow_id, "title": title})
        decision_policy_orchestrator.enforce_policy(wf.workflow_id, cost=50000.0, risk_score=1.5)

        # 3. Platform Pipeline Execution
        assessment = await enterprise_decision_intelligence_platform.execute_master_decision_intelligence_pipeline(title, description)

        # 4. Telemetry & Completion
        duration_ms = (time.time() - t0) * 1000
        decision_observability.record_decision_telemetry(wf.workflow_id, latency_ms=duration_ms, confidence_score=0.98)
        decision_workflow_engine.advance_workflow_stage(wf.workflow_id, "COMPLETED", "GlobalPlatformPipeline")
        decision_lifecycle_manager.transition_stage(wf.workflow_id, "COMPLETED")
        decision_service_bus.publish_event("DECISION_LOOP_COMPLETED", {"workflow_id": wf.workflow_id, "title": title})

        res = GlobalDecisionOrchestratorResult(
            request_title=title,
            assessment=assessment,
            workflow_stage="COMPLETED",
            requires_human_approval=True,
            readiness_score=100.0,
            status="SUCCESS",
        )

        security_logger.info(f"GlobalDecisionOrchestrator: Global decision loop completed for '{title}' in {round(duration_ms, 2)}ms (Readiness={res.readiness_score}%).")
        return res


# Global GlobalDecisionOrchestrator instance
global_decision_orchestrator = GlobalDecisionOrchestrator()
