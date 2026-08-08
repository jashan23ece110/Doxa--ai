"""
Enterprise AI Explainability Engine.

Generates structured reasoning summaries explaining why tools were selected,
why memories were used, why documents were retrieved, why workflow paths changed,
and why models were selected — without exposing internal chain-of-thought.
"""

import asyncio
import time
from typing import Dict, Any, List, Optional
from app.core.logging import logger
from app.core.config import settings
from app.core.safety.safety_types import ExplainabilityReport


class ExplainabilityEngine:
    """Generates structured, user-safe explanations of AI decisions."""

    # ── Explanation Templates ──

    _TOOL_TEMPLATES: Dict[str, str] = {
        "web_search": "A web search was performed to retrieve up-to-date information relevant to the query.",
        "calculator": "A calculation tool was used to provide precise numerical results.",
        "python_sandbox": "A sandboxed code execution was used to compute or transform data programmatically.",
        "file_read": "A file was read to access stored document content relevant to the request.",
        "file_write": "Content was written to a file as requested by the operation.",
        "rag_retrieval": "Document retrieval was used to ground the response in stored knowledge.",
        "memory_read": "Historical context was retrieved from memory to maintain conversation continuity.",
        "memory_write": "Information was stored in memory for future reference and continuity.",
        "timer": "A timer was set as requested by the user.",
        "calendar": "Calendar operations were performed to manage scheduling.",
        "default": "A specialized tool was selected based on the requirements of the task.",
    }

    _MEMORY_TEMPLATES: List[str] = [
        "Memory was accessed to retrieve context from prior interactions.",
        "Historical information was used to maintain continuity and avoid redundant queries.",
        "Previously stored preferences and facts informed the current response.",
    ]

    _RETRIEVAL_TEMPLATES: List[str] = [
        "Documents were retrieved to ground the response in factual, stored knowledge.",
        "Retrieved content was ranked by semantic similarity to the query.",
        "Multiple document chunks were evaluated to select the most relevant context.",
    ]

    _WORKFLOW_TEMPLATES: Dict[str, str] = {
        "branch": "The workflow branched to handle a conditional requirement.",
        "parallel": "Parallel execution was chosen to improve response time.",
        "sequential": "Sequential execution was chosen to maintain dependency ordering.",
        "retry": "A workflow step was retried after a transient failure.",
        "fallback": "A fallback path was activated after the primary path was unavailable.",
        "default": "The workflow path was determined by task requirements and system policy.",
    }

    _MODEL_TEMPLATES: Dict[str, str] = {
        "complexity": "A more capable model was selected due to query complexity.",
        "speed": "A faster model was selected to optimize response latency.",
        "cost": "A cost-efficient model was selected for this routine query.",
        "capability": "The selected model has specific capabilities required for this task.",
        "fallback": "An alternative model was selected because the primary model was unavailable.",
        "default": "The model was selected based on the platform's routing policy.",
    }

    async def generate_report(
        self,
        context: Dict[str, Any] = None,
    ) -> ExplainabilityReport:
        """
        Generates a structured explainability report for an execution.

        Args:
            context: Dict containing:
                - request_id (str): The request identifier.
                - tools_used (List[str]): Names of tools invoked.
                - tool_reasons (Dict[str, str]): Custom per-tool reason overrides.
                - memories_accessed (int): Number of memory reads.
                - memory_types (List[str]): Types of memory accessed.
                - retrievals_performed (int): Number of RAG retrievals.
                - retrieval_scores (List[float]): Similarity scores.
                - workflow_type (str): Type of workflow path taken.
                - workflow_reason (str): Custom workflow path reason.
                - model_selected (str): Name of the model used.
                - model_reason (str): Reason for model selection.
                - confidence (float): Overall confidence score.
                - risk_score (float): Overall risk score.
                - trust_score (float): Overall trust score.

        Returns:
            ExplainabilityReport with per-dimension rationale lists.
        """
        if not settings.EXPLAINABILITY_ENABLED:
            return ExplainabilityReport()

        start = time.time()
        ctx = context or {}

        # ── Tool Selection Rationale ──
        tool_rationale: List[str] = []
        tools_used = ctx.get("tools_used", [])
        tool_reasons = ctx.get("tool_reasons", {})
        for tool in tools_used:
            if tool in tool_reasons:
                tool_rationale.append(f"{tool}: {tool_reasons[tool]}")
            elif tool in self._TOOL_TEMPLATES:
                tool_rationale.append(f"{tool}: {self._TOOL_TEMPLATES[tool]}")
            else:
                tool_rationale.append(f"{tool}: {self._TOOL_TEMPLATES['default']}")

        # ── Memory Usage Rationale ──
        memory_rationale: List[str] = []
        memories_accessed = ctx.get("memories_accessed", 0)
        if memories_accessed > 0:
            memory_rationale.append(self._MEMORY_TEMPLATES[0])
            memory_types = ctx.get("memory_types", [])
            if "episodic" in memory_types:
                memory_rationale.append(
                    "Episodic memory was used to recall specific past events and interactions."
                )
            if "semantic" in memory_types:
                memory_rationale.append(
                    "Semantic memory was used to apply learned facts and concepts."
                )
            if "working" in memory_types:
                memory_rationale.append(
                    "Working memory was used for active context management within this session."
                )
            if memories_accessed > 3:
                memory_rationale.append(
                    f"{memories_accessed} memory items were consulted to build comprehensive context."
                )

        # ── Retrieval Rationale ──
        retrieval_rationale: List[str] = []
        retrievals_performed = ctx.get("retrievals_performed", 0)
        if retrievals_performed > 0:
            retrieval_rationale.append(self._RETRIEVAL_TEMPLATES[0])
            retrieval_rationale.append(self._RETRIEVAL_TEMPLATES[1])
            scores = ctx.get("retrieval_scores", [])
            if scores:
                avg_score = sum(scores) / len(scores)
                retrieval_rationale.append(
                    f"{len(scores)} chunks evaluated with average relevance score of {avg_score:.2f}."
                )
            if retrievals_performed > 5:
                retrieval_rationale.append(
                    "A broad retrieval was performed to cover multiple aspects of the query."
                )

        # ── Workflow Rationale ──
        workflow_rationale: List[str] = []
        workflow_type = ctx.get("workflow_type", "")
        if workflow_type:
            custom_reason = ctx.get("workflow_reason", "")
            if custom_reason:
                workflow_rationale.append(custom_reason)
            elif workflow_type in self._WORKFLOW_TEMPLATES:
                workflow_rationale.append(self._WORKFLOW_TEMPLATES[workflow_type])
            else:
                workflow_rationale.append(self._WORKFLOW_TEMPLATES["default"])

        # ── Model Selection Rationale ──
        model_rationale: List[str] = []
        model_selected = ctx.get("model_selected", "")
        if model_selected:
            custom_model_reason = ctx.get("model_reason", "")
            if custom_model_reason:
                model_rationale.append(f"Model '{model_selected}': {custom_model_reason}")
            else:
                # Infer reason from model name patterns
                reason_key = self._infer_model_reason(model_selected, ctx)
                model_rationale.append(
                    f"Model '{model_selected}': {self._MODEL_TEMPLATES.get(reason_key, self._MODEL_TEMPLATES['default'])}"
                )

        # ── Confidence / Risk / Trust Explanation ──
        confidence = ctx.get("confidence", 0.0)
        risk_score = ctx.get("risk_score", 0.0)
        trust_score = ctx.get("trust_score", 1.0)

        confidence_explanation = ""
        if confidence > 0:
            if confidence >= 0.9:
                confidence_explanation = f"High confidence ({confidence:.2f}): The system has strong supporting evidence for this response."
            elif confidence >= 0.7:
                confidence_explanation = f"Moderate confidence ({confidence:.2f}): The response is well-supported but some aspects may benefit from verification."
            else:
                confidence_explanation = f"Lower confidence ({confidence:.2f}): The response may require additional verification."

        risk_explanation = ""
        if risk_score > 0:
            risk_explanation = (
                f"Risk assessment score: {risk_score:.4f}. "
                f"{'Within acceptable limits.' if risk_score <= settings.RISK_THRESHOLD else 'Above risk threshold — additional review recommended.'}"
            )

        trust_explanation = ""
        if trust_score < 1.0:
            trust_explanation = (
                f"Trust score: {trust_score:.4f}. "
                f"{'Response is trustworthy.' if trust_score >= settings.TRUST_THRESHOLD else 'Trust score is below threshold — treat with caution.'}"
            )

        elapsed = (time.time() - start) * 1000

        report = ExplainabilityReport(
            request_id=ctx.get("request_id"),
            tool_selection_rationale=tool_rationale,
            memory_usage_rationale=memory_rationale,
            retrieval_rationale=retrieval_rationale,
            workflow_rationale=workflow_rationale,
            model_selection_rationale=model_rationale,
            confidence_explanation=confidence_explanation,
            risk_explanation=risk_explanation,
            trust_explanation=trust_explanation,
        )

        logger.debug(
            f"ExplainabilityEngine generated '{report.report_id}': "
            f"Tools={len(tool_rationale)}, Memory={len(memory_rationale)}, "
            f"Retrieval={len(retrieval_rationale)}, Workflow={len(workflow_rationale)}, "
            f"Model={len(model_rationale)}, Duration={elapsed:.2f}ms"
        )
        return report

    @staticmethod
    def _infer_model_reason(model_name: str, ctx: Dict[str, Any]) -> str:
        """Infers why a model was selected based on naming patterns."""
        name_lower = model_name.lower()
        if any(kw in name_lower for kw in ["turbo", "flash", "mini", "small", "lite"]):
            return "speed"
        if any(kw in name_lower for kw in ["pro", "large", "opus", "ultra"]):
            return "complexity"
        if any(kw in name_lower for kw in ["free", "cheap"]):
            return "cost"
        if ctx.get("is_fallback", False):
            return "fallback"
        return "default"


# Global ExplainabilityEngine instance
explainability_engine = ExplainabilityEngine()
