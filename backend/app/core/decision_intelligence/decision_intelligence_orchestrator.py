"""
Global Decision Intelligence Orchestrator.

Master orchestrator driving end-to-end enterprise decision intelligence workflows:
Decision Request -> Objective Definition -> Context Collection -> Evidence Analysis -> Alternative Generation -> Risk & Uncertainty Analysis -> Alternative Evaluation -> Recommendation -> Approval -> Outcome Tracking.
"""

import time
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from app.core.logging import security_logger
from app.core.decision_intelligence.decision_types import (
    DecisionRequest, DecisionRecommendation, DecisionConfidence, DecisionAlternative, DecisionEvaluation
)
from app.core.decision_intelligence.decision_context_engine import decision_context_engine
from app.core.decision_intelligence.decision_objective_engine import decision_objective_engine
from app.core.decision_intelligence.alternative_generation_engine import alternative_generation_engine
from app.core.decision_intelligence.evidence_engine import evidence_engine
from app.core.decision_intelligence.decision_model_engine import decision_model_engine
from app.core.decision_intelligence.uncertainty_engine import uncertainty_engine
from app.core.decision_intelligence.decision_evaluation_engine import decision_evaluation_engine
from app.core.decision_intelligence.decision_audit_engine import decision_audit_engine


class MasterDecisionResult(BaseModel):
    decision_id: str = Field(default_factory=lambda: f"mdec_{int(time.time() * 1000)}")
    request_title: str
    recommendation: DecisionRecommendation
    confidence: DecisionConfidence
    audit_id: str
    status: str = "COMPLETED"
    summary: str = "Decision recommendation generated with complete provenance."
    executed_at: float = Field(default_factory=time.time)


class DecisionIntelligenceOrchestrator:
    """Global Decision Intelligence Orchestrator Facade."""

    async def execute_decision_analysis(self, title: str, description: str) -> MasterDecisionResult:
        """
        Executes end-to-end decision intelligence analysis for enterprise request.

        Args:
            title: Decision request title string.
            description: Decision request description string.

        Returns:
            MasterDecisionResult object.
        """
        t0 = time.time()
        security_logger.info(f"DecisionIntelligenceOrchestrator: Initiating decision analysis for '{title}'.")

        # 1. Request & Objective Definition
        dreq = DecisionRequest(title=title, description=description)
        objectives = decision_objective_engine.structure_objectives(title)
        dreq.objectives = objectives

        # 2. Context Collection & Evidence Analysis
        ctx = await decision_context_engine.build_decision_context(dreq)
        ev_score = evidence_engine.evaluate_evidence_quality(ctx.relevant_evidences)

        # 3. Alternative Generation & Decision Modeling
        alts = alternative_generation_engine.generate_alternatives(title, objectives)
        evaluations = []
        for alt in alts:
            deval = decision_model_engine.evaluate_alternative(alt, model_type="WEIGHTED_SCORING")
            evaluations.append((alt, deval))

        # 4. Uncertainty Analysis & Alternative Evaluation
        confidence = uncertainty_engine.analyze_uncertainty(ctx.relevant_evidences)
        best_alt, best_eval = decision_evaluation_engine.select_best_alternative(evaluations)

        # 5. Recommendation Generation & Audit Lineage
        rec = DecisionRecommendation(
            recommended_alternative_id=best_alt.alternative_id,
            recommended_alternative_title=best_alt.title,
            rationale=f"Option '{best_alt.title}' achieved highest composite score ({best_eval.composite_score}) with high evidence quality ({ev_score}).",
            expected_outcome_summary=f"Expected net benefit score of {best_alt.expected_benefit} with low risk profile.",
            confidence=confidence,
            requires_human_approval=True,
        )

        steps = ["Request", "Objectives", "Context", "Evidence", "Alternatives", "Modeling", "Uncertainty", "Evaluation", "Recommendation"]
        audit = decision_audit_engine.record_decision_lineage(dreq.request_id, steps)

        res = MasterDecisionResult(
            request_title=title,
            recommendation=rec,
            confidence=confidence,
            audit_id=audit.audit_id,
            status="COMPLETED",
        )

        security_logger.info(f"DecisionIntelligenceOrchestrator: Completed decision analysis '{res.decision_id}' for '{title}' in {round((time.time() - t0)*1000, 2)}ms.")
        return res


# Global DecisionIntelligenceOrchestrator instance
decision_intelligence_orchestrator = DecisionIntelligenceOrchestrator()
