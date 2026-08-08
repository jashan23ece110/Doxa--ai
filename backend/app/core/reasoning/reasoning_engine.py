"""
Enterprise Cognitive Reasoning Engine Orchestrator.

Orchestrates multi-stage cognitive reasoning pipelines: Complexity Detection -> Task Decomposition ->
DAG Planning -> Async Parallel Execution -> Verification & Reflection -> Targeted Answer Revision ->
Calibrated Confidence Scoring with automatic graceful fallbacks and 100% backward compatibility.
"""

import time
from typing import List, Dict, Any, Optional
from app.core.config import settings
from app.core.diagnostics import DiagnosticSpan
from app.core.logging import logger
from app.core.reasoning.answer_reviser import answer_reviser
from app.core.reasoning.confidence_engine import confidence_engine
from app.core.reasoning.confidence_estimator import confidence_estimator
from app.core.reasoning.contradiction_detector import contradiction_detector
from app.core.reasoning.evidence_verifier import evidence_verifier
from app.core.reasoning.executor import graph_executor
from app.core.reasoning.planner import planning_engine
from app.core.reasoning.reasoning_metrics import reasoning_metrics_tracker
from app.core.reasoning.reflection_engine import reflection_engine
from app.core.reasoning.self_reflection import self_reflection_engine
from app.core.reasoning.verifier import verification_engine


class ReasoningEngine:
    """Orchestrates multi-stage cognitive reasoning, verification, and reflection."""

    @staticmethod
    def process_and_verify_response(
        draft_response: str,
        query: str,
        contexts: List[Dict[str, Any]],
        memory_context: str = "",
    ) -> str:
        """
        Backward-compatible verification pass.
        Executes internal verification and reflection pass over draft response.
        Returns final verified response without exposing internal reasoning or CoT traces.
        """
        if not settings.REASONING_ENGINE_ENABLED or not draft_response or not draft_response.strip():
            return draft_response

        try:
            with DiagnosticSpan(span_name="reasoning_engine_verification", slow_threshold_ms=50.0, category="general"):
                # 1. Evidence Support Verification
                evidence_info = evidence_verifier.verify_draft_evidence(draft_response, contexts, memory_context)

                # 2. Contradiction Detection
                contradictions = contradiction_detector.detect_contradictions(draft_response, memory_context)

                # 3. Confidence Estimation
                confidence = confidence_estimator.estimate_confidence(contexts, evidence_info, contradictions)

                logger.debug(
                    f"Internal Reasoning: Grounded Ratio={evidence_info.get('grounded_ratio')}, "
                    f"Contradictions={len(contradictions)}, Internal Confidence={confidence:.2f}"
                )

                # 4. Reflection Pass & Refinement
                final_response = reflection_engine.refine_response_draft(
                    draft_response=draft_response,
                    query=query,
                    contexts=contexts,
                    memory_context=memory_context,
                    contradictions=contradictions,
                )

                return final_response

        except Exception as e:
            logger.warning(f"ReasoningEngine verification failed ({e}). Returning initial response draft.")
            return draft_response

    async def run_cognitive_pipeline(
        self,
        query: str,
        draft_response: str = "",
        user_id: str = "default_user",
    ) -> Dict[str, Any]:
        """
        Executes full multi-stage cognitive reasoning pipeline:
        1. Complexity & Intent Detection
        2. Task Decomposition & DAG Planning
        3. Async Parallel Graph Execution
        4. Verification & Self Reflection
        5. Targeted Answer Revision
        6. Calibrated Confidence Scoring
        """
        start_time = time.time()
        complexity_level, reasoning_mode, graph = planning_engine.create_reasoning_plan(query)

        # Fast Mode Bypass for Simple Queries
        if reasoning_mode == "fast" and draft_response:
            return {
                "query": query,
                "complexity_level": complexity_level,
                "reasoning_mode": reasoning_mode,
                "final_response": draft_response,
                "confidence_score": 0.95,
                "latency_ms": 0.0,
            }

        try:
            with DiagnosticSpan(span_name="cognitive_reasoning_pipeline", slow_threshold_ms=1000.0, category="general"):
                # 1. Async DAG Graph Execution
                exec_results = await graph_executor.execute_graph(graph, query, user_id=user_id)
                contexts = exec_results.get("contexts", [])
                memory_context = exec_results.get("memory_context", "")

                current_draft = draft_response or f"Verified cognitive response for query '{query}'."

                # 2. Verification Pass
                verification_res = verification_engine.verify_response_evidence(
                    current_draft, contexts, memory_context
                )

                # 3. Self Reflection
                reflection_report = self_reflection_engine.reflect_on_draft(
                    current_draft, contexts, memory_context
                )

                # 4. Targeted Answer Revision
                final_output, revisions_count = answer_reviser.revise_draft_response(
                    draft_response=current_draft,
                    query=query,
                    contexts=contexts,
                    memory_context=memory_context,
                    verification_result=verification_res,
                )

                # 5. Calibrated Confidence Scoring
                overall_confidence = confidence_engine.calculate_confidence(
                    contexts=contexts,
                    verification_result=verification_res,
                    reflection_passed=reflection_report.passed,
                )

                duration_ms = (time.time() - start_time) * 1000
                reasoning_metrics_tracker.record_run(
                    success=True,
                    latency_ms=duration_ms,
                    confidence=overall_confidence,
                    revisions=revisons_count if 'revisons_count' in locals() else revisions_count,
                    hallucination_found=reflection_report.hallucination_risk > 0.30,
                )

                logger.info(
                    f"Cognitive Reasoning complete: Complexity={complexity_level}, Mode={reasoning_mode}, "
                    f"Confidence={overall_confidence:.2f}, Latency={duration_ms:.2f}ms"
                )

                return {
                    "query": query,
                    "complexity_level": complexity_level,
                    "reasoning_mode": reasoning_mode,
                    "contexts": contexts,
                    "memory_context": memory_context,
                    "verification": verification_res,
                    "reflection": reflection_report.model_dump(),
                    "final_response": final_output,
                    "confidence_score": overall_confidence,
                    "latency_ms": round(duration_ms, 2),
                }

        except Exception as e:
            logger.error(f"Cognitive Reasoning pipeline failed ({e}). Returning graceful fallback.")
            duration_ms = (time.time() - start_time) * 1000
            reasoning_metrics_tracker.record_run(success=False, latency_ms=duration_ms, confidence=0.50)
            return {
                "query": query,
                "complexity_level": complexity_level,
                "reasoning_mode": reasoning_mode,
                "final_response": draft_response or query,
                "confidence_score": 0.50,
                "latency_ms": round(duration_ms, 2),
            }


# Global ReasoningEngine instance
reasoning_engine = ReasoningEngine()
