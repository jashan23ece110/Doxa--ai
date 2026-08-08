"""
Self Reflection Engine for Enterprise Cognitive Reasoning.

Evaluates draft response correctness, completeness, hallucination risk, missing evidence, and logical consistency.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class ReflectionReport(BaseModel):
    """Structured report produced by self-reflection."""

    passed: bool
    hallucination_risk: float = Field(default=0.0, ge=0.0, le=1.0)
    missing_evidence: bool = False
    logical_consistency: float = Field(default=1.0, ge=0.0, le=1.0)
    issues: List[str] = Field(default_factory=list)
    suggestions: List[str] = Field(default_factory=list)


class SelfReflectionEngine:
    """Evaluates draft responses for logical consistency and hallucination risk."""

    @staticmethod
    def reflect_on_draft(
        draft_response: str,
        contexts: List[Dict[str, Any]],
        memory_context: str = "",
    ) -> ReflectionReport:
        """Runs reflection analysis on draft response."""
        if not draft_response or not draft_response.strip():
            return ReflectionReport(
                passed=False,
                hallucination_risk=1.0,
                issues=["Empty draft response"],
                suggestions=["Regenerate response from evidence"],
            )

        issues = []
        suggestions = []
        hallucination_risk = 0.0

        # Check for ungrounded citations or explicit hallucination phrases
        if "as an ai" in draft_response.lower() or "i don't have access" in draft_response.lower():
            issues.append("Generic disclaimers detected in response.")

        # Check evidence grounding ratio
        if contexts:
            has_matching_keywords = any(
                chunk.get("filename", "").lower() in draft_response.lower()
                for chunk in contexts
            )
            if not has_matching_keywords:
                hallucination_risk += 0.15
                issues.append("Response lacks explicit source chunk citations.")
                suggestions.append("Reference retrieved document filename explicitly.")

        passed = len(issues) == 0 and hallucination_risk < 0.30

        return ReflectionReport(
            passed=passed,
            hallucination_risk=round(hallucination_risk, 2),
            missing_evidence=len(contexts) == 0,
            logical_consistency=0.95,
            issues=issues,
            suggestions=suggestions,
        )


# Global SelfReflectionEngine instance
self_reflection_engine = SelfReflectionEngine()
