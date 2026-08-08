"""
Enterprise AI Safety Manager — Central Orchestrator.

Coordinates the Policy Engine, Trust Engine, Governance Engine,
Compliance Engine, Safety Checker, Audit Logger, and Explainability Engine
through a single entry point for comprehensive execution assessment.
"""

import asyncio
import time
from typing import Dict, Any, List, Optional
from app.core.logging import logger
from app.core.config import settings
from app.core.safety.safety_types import (
    SafetyEvent,
    RiskAssessment,
    TrustScore,
    GovernanceDecision,
    GovernanceAction,
    ComplianceResult,
    ComplianceStandard,
    PolicyScope,
    SafetyVerdict,
    RiskLevel,
    ExplainabilityReport,
    AgentDecisionRecord,
)
from app.core.safety.policy_engine import safety_policy_engine
from app.core.safety.trust_engine import trust_engine
from app.core.safety.safety_checker import safety_checker
from app.core.safety.compliance_engine import compliance_engine
from app.core.safety.governance_engine import governance_engine
from app.core.safety.audit_logger import safety_audit_logger
from app.core.safety.explainability import explainability_engine


class SafetyManager:
    """
    Central orchestrator for the Enterprise AI Safety, Governance,
    Compliance & Trust Layer.

    Provides a single entry point that coordinates all safety subsystems
    with graceful fallback if any subsystem fails.
    """

    async def assess_execution(
        self,
        context: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        """
        Performs a comprehensive safety assessment for an execution request.

        Orchestrates:
        1. Safety Check (risk assessment)
        2. Trust Scoring
        3. Policy Evaluation
        4. Governance Decision
        5. Compliance Evaluation
        6. Explainability Report
        7. Audit Logging

        Args:
            context: Execution context dict. Supported keys:
                - prompt (str): User prompt text.
                - user_id (str): User identifier.
                - tenant_id (str): Tenant identifier.
                - agent_id (str): Agent identifier.
                - request_id (str): Request identifier.
                - tools_used (List[str]): Tools being invoked.
                - tool_chain (List[str]): Ordered tool sequence.
                - requested_tools (List[str]): Requested tools.
                - memory_updates (List[dict]): Proposed memory writes.
                - retrieval_texts (List[str]): Retrieved document chunks.
                - retrieval_confidence (float): Average retrieval confidence.
                - has_citations (bool): Response includes citations.
                - citation_count (int): Number of citations.
                - reasoning_steps (int): Number of reasoning steps.
                - reasoning_coherence (float): Reasoning coherence score.
                - resource_type (str): Primary resource type (tool, memory, etc.).
                - resource_id (str): Primary resource identifier.
                - compliance_standard (str): Specific standard to check.
                - model_selected (str): Model being used.
                - confidence (float): Overall confidence.
                - user_role (str): Role of the user.

        Returns:
            Dict containing all assessment results:
                - risk_assessment: RiskAssessment dict
                - trust_score: TrustScore dict
                - governance_decision: GovernanceDecision dict
                - compliance_result: ComplianceResult dict (if applicable)
                - explainability_report: ExplainabilityReport dict
                - safety_verdict: SafetyVerdict value
                - total_latency_ms: Total assessment duration
                - is_safe: bool
        """
        if not settings.SAFETY_ENABLED:
            return self._safe_bypass_result()

        start = time.time()
        ctx = context or {}
        user_id = ctx.get("user_id", "anonymous")
        agent_id = ctx.get("agent_id")
        request_id = ctx.get("request_id")
        resource_type = ctx.get("resource_type", "execution")
        resource_id = ctx.get("resource_id", "")

        # ── Step 1: Safety Check (Risk Assessment) ──
        risk_assessment = await self._safe_call(
            safety_checker.assess_risk(context=ctx),
            fallback=RiskAssessment(is_acceptable=True),
            label="SafetyChecker",
        )

        # ── Step 2: Trust Scoring ──
        trust_score = await self._safe_call(
            trust_engine.compute_trust(context=ctx),
            fallback=TrustScore(overall_score=1.0, is_trustworthy=True),
            label="TrustEngine",
        )

        # ── Step 3: Governance Decision ──
        governance_ctx = {
            **ctx,
            "risk_score": risk_assessment.overall_risk_score,
            "trust_score": trust_score.overall_score,
        }
        governance_decision = await self._safe_call(
            governance_engine.evaluate(
                resource_type=resource_type,
                resource_id=resource_id,
                context=governance_ctx,
            ),
            fallback=GovernanceDecision(
                action=GovernanceAction.APPROVE,
                resource_type=resource_type,
                resource_id=resource_id,
                reason="Governance fallback: approved by default.",
            ),
            label="GovernanceEngine",
        )

        # ── Step 4: Compliance Evaluation (if standard specified or text present) ──
        compliance_result = None
        standard_str = ctx.get("compliance_standard", "")
        text_to_check = ctx.get("prompt", "") or ctx.get("response_text", "")
        if standard_str or text_to_check:
            standard = self._resolve_standard(standard_str)
            compliance_ctx = {**ctx, "text": text_to_check}
            compliance_result = await self._safe_call(
                compliance_engine.evaluate_compliance(
                    standard=standard,
                    context=compliance_ctx,
                ),
                fallback=ComplianceResult(standard=standard, is_compliant=True),
                label="ComplianceEngine",
            )

        # ── Step 5: Explainability Report ──
        explainability_report = await self._safe_call(
            explainability_engine.generate_report(context=ctx),
            fallback=ExplainabilityReport(),
            label="ExplainabilityEngine",
        )

        # ── Step 6: Determine Overall Verdict ──
        verdict = self._determine_verdict(
            risk_assessment=risk_assessment,
            trust_score=trust_score,
            governance_decision=governance_decision,
        )
        is_safe = verdict in (SafetyVerdict.SAFE, SafetyVerdict.CAUTION)

        elapsed = (time.time() - start) * 1000

        # ── Step 7: Audit Logging (fire-and-forget) ──
        asyncio.ensure_future(self._log_audit(
            event_type="execution_assessment",
            user_id=user_id,
            agent_id=agent_id,
            request_id=request_id,
            decision=governance_decision.action.value,
            risk_score=risk_assessment.overall_risk_score,
            trust_score=trust_score.overall_score,
            latency_ms=elapsed,
            outcome="approved" if is_safe else "blocked",
            details={
                "verdict": verdict.value,
                "risk_level": risk_assessment.overall_risk_level.value,
                "risks_found": len(risk_assessment.individual_risks),
                "governance_action": governance_decision.action.value,
                "compliance_checked": compliance_result is not None,
                "resource_type": resource_type,
                "resource_id": resource_id,
            },
        ))

        logger.info(
            f"SafetyManager assessment complete: verdict={verdict.value}, "
            f"risk={risk_assessment.overall_risk_score:.4f}, "
            f"trust={trust_score.overall_score:.4f}, "
            f"governance={governance_decision.action.value}, "
            f"safe={is_safe}, latency={elapsed:.2f}ms"
        )

        return {
            "risk_assessment": risk_assessment.model_dump(),
            "trust_score": trust_score.model_dump(),
            "governance_decision": governance_decision.model_dump(),
            "compliance_result": compliance_result.model_dump() if compliance_result else None,
            "explainability_report": explainability_report.model_dump(),
            "safety_verdict": verdict.value,
            "total_latency_ms": round(elapsed, 2),
            "is_safe": is_safe,
        }

    async def assess_tool_execution(
        self,
        tool_name: str,
        user_id: str = "anonymous",
        agent_id: Optional[str] = None,
        context: Dict[str, Any] = None,
    ) -> GovernanceDecision:
        """
        Convenience method for assessing tool execution safety.

        Returns:
            GovernanceDecision for the tool.
        """
        ctx = context or {}
        ctx.update({
            "resource_type": "tool",
            "resource_id": tool_name,
            "requested_tools": [tool_name],
            "user_id": user_id,
            "agent_id": agent_id,
        })
        result = await self.assess_execution(context=ctx)
        return GovernanceDecision.model_validate(result["governance_decision"])

    async def assess_memory_access(
        self,
        operation: str,
        user_id: str = "anonymous",
        tenant_id: str = "default",
        context: Dict[str, Any] = None,
    ) -> GovernanceDecision:
        """
        Convenience method for assessing memory access safety.

        Returns:
            GovernanceDecision for the memory operation.
        """
        ctx = context or {}
        ctx.update({
            "resource_type": "memory",
            "resource_id": operation,
            "user_id": user_id,
            "tenant_id": tenant_id,
            "resource_tenant_id": ctx.get("resource_tenant_id", tenant_id),
        })
        result = await self.assess_execution(context=ctx)
        return GovernanceDecision.model_validate(result["governance_decision"])

    async def check_compliance(
        self,
        text: str,
        standard: ComplianceStandard = ComplianceStandard.GDPR,
    ) -> ComplianceResult:
        """
        Convenience method for standalone compliance checking.

        Returns:
            ComplianceResult for the specified standard.
        """
        return await compliance_engine.evaluate_compliance(
            standard=standard,
            context={"text": text},
        )

    async def record_agent_decision(
        self,
        agent_id: str,
        decision_type: str,
        chosen_option: str,
        alternatives: List[str] = None,
        reasoning_summary: str = "",
        confidence: float = 0.0,
        context: Dict[str, Any] = None,
    ) -> AgentDecisionRecord:
        """
        Records an agent decision with full governance and trust context.

        Returns:
            AgentDecisionRecord with attached assessments.
        """
        ctx = context or {}
        risk = await self._safe_call(
            safety_checker.assess_risk(context=ctx),
            fallback=RiskAssessment(is_acceptable=True),
            label="SafetyChecker",
        )
        trust = await self._safe_call(
            trust_engine.compute_trust(context=ctx),
            fallback=TrustScore(overall_score=1.0, is_trustworthy=True),
            label="TrustEngine",
        )
        gov = await self._safe_call(
            governance_engine.evaluate(
                resource_type=decision_type,
                resource_id=chosen_option,
                context={**ctx, "risk_score": risk.overall_risk_score, "trust_score": trust.overall_score},
            ),
            fallback=GovernanceDecision(
                action=GovernanceAction.APPROVE,
                resource_type=decision_type,
                resource_id=chosen_option,
            ),
            label="GovernanceEngine",
        )

        record = AgentDecisionRecord(
            agent_id=agent_id,
            decision_type=decision_type,
            chosen_option=chosen_option,
            alternatives_considered=alternatives or [],
            reasoning_summary=reasoning_summary,
            confidence=confidence,
            risk_assessment=risk,
            trust_score=trust,
            governance_decision=gov,
        )

        # Audit log the decision
        asyncio.ensure_future(safety_audit_logger.log_event(
            event_type="agent_decision",
            actor=agent_id,
            user_id=ctx.get("user_id", "anonymous"),
            agent_id=agent_id,
            decision=gov.action.value,
            risk_score=risk.overall_risk_score,
            trust_score=trust.overall_score,
            details={
                "decision_type": decision_type,
                "chosen": chosen_option,
                "confidence": confidence,
            },
        ))

        return record

    async def flush_audit(self) -> None:
        """Forces flush of all pending audit records to disk."""
        await safety_audit_logger.flush()

    def get_audit_statistics(self) -> Dict[str, Any]:
        """Returns audit statistics summary."""
        return safety_audit_logger.get_statistics()

    # ── Internal Helpers ──

    @staticmethod
    def _determine_verdict(
        risk_assessment: RiskAssessment,
        trust_score: TrustScore,
        governance_decision: GovernanceDecision,
    ) -> SafetyVerdict:
        """Determines the overall safety verdict from subsystem results."""
        if governance_decision.action == GovernanceAction.DENY:
            return SafetyVerdict.BLOCKED

        if governance_decision.action == GovernanceAction.ESCALATE:
            return SafetyVerdict.REVIEW_REQUIRED

        if risk_assessment.overall_risk_level in (RiskLevel.CRITICAL, RiskLevel.HIGH):
            if not risk_assessment.is_acceptable:
                return SafetyVerdict.BLOCKED
            return SafetyVerdict.CAUTION

        if not trust_score.is_trustworthy:
            return SafetyVerdict.CAUTION

        if risk_assessment.overall_risk_level == RiskLevel.MEDIUM:
            return SafetyVerdict.CAUTION

        return SafetyVerdict.SAFE

    @staticmethod
    async def _safe_call(coro, fallback, label: str):
        """
        Executes an async coroutine with graceful fallback on failure.
        Ensures the safety subsystem never crashes the main execution path.
        """
        try:
            return await coro
        except Exception as e:
            logger.error(f"SafetyManager: {label} failed with error: {e}. Using fallback.")
            return fallback

    async def _log_audit(self, **kwargs) -> None:
        """Fire-and-forget audit log wrapper with error suppression."""
        try:
            await safety_audit_logger.log_event(**kwargs)
        except Exception as e:
            logger.error(f"SafetyManager: Audit logging failed: {e}")

    @staticmethod
    def _safe_bypass_result() -> Dict[str, Any]:
        """Returns a safe bypass result when the safety layer is disabled."""
        return {
            "risk_assessment": RiskAssessment(is_acceptable=True).model_dump(),
            "trust_score": TrustScore(overall_score=1.0, is_trustworthy=True).model_dump(),
            "governance_decision": GovernanceDecision(
                action=GovernanceAction.APPROVE,
                resource_type="execution",
                reason="Safety layer disabled.",
            ).model_dump(),
            "compliance_result": None,
            "explainability_report": ExplainabilityReport().model_dump(),
            "safety_verdict": SafetyVerdict.SAFE.value,
            "total_latency_ms": 0.0,
            "is_safe": True,
        }

    @staticmethod
    def _resolve_standard(standard_str: str) -> ComplianceStandard:
        """Resolves a string to a ComplianceStandard enum."""
        mapping = {
            "gdpr": ComplianceStandard.GDPR,
            "soc2": ComplianceStandard.SOC2,
            "iso27001": ComplianceStandard.ISO27001,
            "hipaa": ComplianceStandard.HIPAA,
        }
        return mapping.get(standard_str.lower(), ComplianceStandard.GDPR)


# Global SafetyManager instance
safety_manager = SafetyManager()
