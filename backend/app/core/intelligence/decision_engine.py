"""
Adaptive Decision Engine for Doxa AI Operating System.

Dynamically evaluates request intent, complexity, latency budget, confidence metrics,
and past executions to construct an Adaptive Execution Graph instead of static execution pipelines.
"""

import asyncio
import re
import time
from typing import Dict, Any, List, Optional
from app.core.logging import logger
from app.core.config import settings
from app.core.intelligence.intelligence_types import (
    AdaptiveExecutionGraph,
    DecisionGraphNode,
    ExecutionMode,
)


class AdaptiveDecisionEngine:
    """Enterprise Adaptive Decision Engine."""

    # Key intent detection patterns
    _CODE_PATTERNS = [r"\bpython\b", r"\bdef\s+", r"\bimport\b", r"\bcalculate\b", r"\bscript\b", r"\bcode\b", r"```"]
    _SEARCH_PATTERNS = [r"\bsearch\b", r"\bnews\b", r"\blatest\b", r"\bcurrent\b", r"\bweather\b", r"\bwho is\b", r"\bwhat is the price\b"]
    _WORKFLOW_PATTERNS = [r"\bworkflow\b", r"\bpipeline\b", r"\bmulti-step\b", r"\bautomate\b", r"\bsequence\b"]
    _COMPLEX_PATTERNS = [r"\banalyze\b", r"\bcompare\b", r"\bevaluate\b", r"\bsynthesize\b", r"\bplan\b", r"\barchitect\b", r"\bpros and cons\b"]
    _MULTI_AGENT_PATTERNS = [r"\bcollab\b", r"\bteam\b", r"\breview and critique\b", r"\bmulti-perspective\b", r"\bdebate\b"]

    async def generate_execution_graph(
        self,
        prompt: str,
        user_context: Optional[Dict[str, Any]] = None,
        latency_budget_ms: float = 5000.0,
        cached_result_available: bool = False,
    ) -> AdaptiveExecutionGraph:
        """
        Constructs a dynamic Adaptive Execution Graph tailored to the request.

        Args:
            prompt: Incoming user prompt or task description.
            user_context: Additional runtime context (history, role, preferences).
            latency_budget_ms: Max latency budget allowed for this request.
            cached_result_available: Whether a full cache hit exists.

        Returns:
            AdaptiveExecutionGraph with nodes and subsystem activation flags.
        """
        if not settings.ADAPTIVE_DECISION_ENABLED:
            return self._fallback_default_graph(latency_budget_ms)

        start_time = time.time()
        ctx = user_context or {}
        prompt_lower = prompt.lower().strip()

        # Short-circuit if cached result is ready
        if cached_result_available:
            logger.info("AdaptiveDecisionEngine: Full cache hit available. Generating DIRECT mode graph.")
            return AdaptiveExecutionGraph(
                execution_mode=ExecutionMode.FAST,
                should_run_rag=False,
                should_run_memory=True,
                should_run_planner=False,
                should_run_multi_agent=False,
                should_execute_python=False,
                should_execute_web_search=False,
                should_execute_workflow=False,
                should_run_evaluation=False,
                should_update_long_term_memory=False,
                estimated_total_latency_ms=15.0,
                latency_budget_ms=latency_budget_ms,
                complexity_score=0.1,
            )

        # 1. Complexity Assessment (0.0 to 1.0)
        complexity_score = self._assess_complexity(prompt, ctx)

        # 2. Intent Detection
        has_code_intent = any(re.search(p, prompt_lower) for p in self._CODE_PATTERNS)
        has_search_intent = any(re.search(p, prompt_lower) for p in self._SEARCH_PATTERNS)
        has_workflow_intent = any(re.search(p, prompt_lower) for p in self._WORKFLOW_PATTERNS)
        has_multi_agent_intent = any(re.search(p, prompt_lower) for p in self._MULTI_AGENT_PATTERNS)

        # 3. Decision Logic for Subsystem Activation
        # RAG Activation
        should_run_rag = len(prompt) > 15 and not has_code_intent

        # Memory Activation
        should_run_memory = True  # Almost always active for context continuity

        # Planner Activation (High complexity or explicit workflow)
        should_run_planner = (complexity_score >= 0.65 or has_workflow_intent or len(prompt) > 250)

        # Multi-Agent Activation (Very high complexity or explicit multi-perspective request)
        should_run_multi_agent = (
            settings.MULTI_AGENT_ENABLED and 
            (complexity_score >= 0.8 or has_multi_agent_intent) and 
            latency_budget_ms >= 3000.0
        )

        # Python Sandbox Activation
        should_execute_python = has_code_intent or "math" in prompt_lower or "calculate" in prompt_lower

        # Web Search Activation
        should_execute_web_search = has_search_intent or "latest news" in prompt_lower

        # Workflow Activation
        should_execute_workflow = has_workflow_intent or (complexity_score >= 0.75 and not should_run_multi_agent)

        # Evaluation Activation
        should_run_evaluation = True

        # Long-Term Memory Update
        should_update_long_term_memory = len(prompt) > 20 and not (has_code_intent or has_search_intent)

        # 4. Mode Selection
        if should_run_multi_agent:
            mode = ExecutionMode.AUTONOMOUS_AGENT
        elif should_execute_workflow:
            mode = ExecutionMode.HYBRID_WORKFLOW
        elif complexity_score >= 0.7:
            mode = ExecutionMode.DEEP_REASONING
        elif complexity_score <= 0.3 and not should_run_rag:
            mode = ExecutionMode.FAST
        else:
            mode = ExecutionMode.BALANCED

        # 5. Build Graph Nodes
        nodes: List[DecisionGraphNode] = []
        
        # Memory node
        if should_run_memory:
            nodes.append(DecisionGraphNode(
                node_id="node_memory",
                subsystem="memory",
                enabled=True,
                estimated_latency_ms=10.0,
            ))

        # RAG node
        if should_run_rag:
            nodes.append(DecisionGraphNode(
                node_id="node_rag",
                subsystem="rag",
                enabled=True,
                estimated_latency_ms=40.0,
                prerequisites=["node_memory"] if should_run_memory else [],
            ))

        # Planner node
        if should_run_planner:
            nodes.append(DecisionGraphNode(
                node_id="node_planner",
                subsystem="planner",
                enabled=True,
                estimated_latency_ms=80.0,
                prerequisites=["node_rag"] if should_run_rag else [],
            ))

        # Multi-Agent node
        if should_run_multi_agent:
            nodes.append(DecisionGraphNode(
                node_id="node_multi_agent",
                subsystem="multi_agent",
                enabled=True,
                estimated_latency_ms=350.0,
                prerequisites=["node_planner"] if should_run_planner else [],
            ))

        # Workflow node
        if should_execute_workflow:
            nodes.append(DecisionGraphNode(
                node_id="node_workflow",
                subsystem="workflow",
                enabled=True,
                estimated_latency_ms=200.0,
                prerequisites=["node_planner"] if should_run_planner else [],
            ))

        # Tool execution nodes
        if should_execute_python:
            nodes.append(DecisionGraphNode(
                node_id="node_python",
                subsystem="python_sandbox",
                enabled=True,
                estimated_latency_ms=100.0,
            ))
        if should_execute_web_search:
            nodes.append(DecisionGraphNode(
                node_id="node_web_search",
                subsystem="web_search",
                enabled=True,
                estimated_latency_ms=250.0,
            ))

        # Reasoning / Core LLM node
        nodes.append(DecisionGraphNode(
            node_id="node_reasoning",
            subsystem="reasoning",
            enabled=True,
            estimated_latency_ms=300.0,
            prerequisites=[n.node_id for n in nodes if n.node_id != "node_reasoning"],
        ))

        # Evaluation & Long-term Memory nodes
        if should_run_evaluation:
            nodes.append(DecisionGraphNode(
                node_id="node_eval",
                subsystem="eval",
                enabled=True,
                estimated_latency_ms=20.0,
                prerequisites=["node_reasoning"],
            ))
        if should_update_long_term_memory:
            nodes.append(DecisionGraphNode(
                node_id="node_ltm",
                subsystem="long_term_memory",
                enabled=True,
                estimated_latency_ms=15.0,
                prerequisites=["node_reasoning"],
            ))

        estimated_total_latency = sum(n.estimated_latency_ms for n in nodes)

        graph = AdaptiveExecutionGraph(
            execution_mode=mode,
            nodes=nodes,
            should_run_rag=should_run_rag,
            should_run_memory=should_run_memory,
            should_run_planner=should_run_planner,
            should_run_multi_agent=should_run_multi_agent,
            should_execute_python=should_execute_python,
            should_execute_web_search=should_execute_web_search,
            should_execute_workflow=should_execute_workflow,
            should_run_evaluation=should_run_evaluation,
            should_update_long_term_memory=should_update_long_term_memory,
            estimated_total_latency_ms=estimated_total_latency,
            latency_budget_ms=latency_budget_ms,
            complexity_score=complexity_score,
        )

        elapsed_ms = (time.time() - start_time) * 1000
        logger.info(
            f"AdaptiveDecisionEngine created graph '{graph.graph_id}': "
            f"Mode={mode.value}, Complexity={complexity_score:.2f}, "
            f"Nodes={len(nodes)}, EstLatency={estimated_total_latency:.1f}ms, DecisionMs={elapsed_ms:.2f}ms"
        )

        return graph

    def _assess_complexity(self, prompt: str, ctx: Dict[str, Any]) -> float:
        """Estimates task complexity on a scale of 0.0 (trivial) to 1.0 (hyperscale/complex)."""
        score = 0.3  # Base score
        words = len(prompt.split())

        if words > 100:
            score += 0.25
        elif words > 40:
            score += 0.15

        complex_matches = sum(1 for p in self._COMPLEX_PATTERNS if re.search(p, prompt.lower()))
        if complex_matches > 0:
            score += min(0.45, complex_matches * 0.15)

        if "?" in prompt and prompt.count("?") > 1:
            score += 0.1

        if ctx.get("conversation_length", 0) > 10:
            score += 0.1

        return round(min(1.0, score), 2)

    def _fallback_default_graph(self, budget_ms: float) -> AdaptiveExecutionGraph:
        """Returns standard balanced execution graph as fallback."""
        return AdaptiveExecutionGraph(
            execution_mode=ExecutionMode.BALANCED,
            should_run_rag=True,
            should_run_memory=True,
            should_run_planner=False,
            should_run_multi_agent=False,
            should_execute_python=False,
            should_execute_web_search=False,
            should_execute_workflow=False,
            should_run_evaluation=True,
            should_update_long_term_memory=True,
            estimated_total_latency_ms=250.0,
            latency_budget_ms=budget_ms,
            complexity_score=0.5,
        )


# Global AdaptiveDecisionEngine instance
adaptive_decision_engine = AdaptiveDecisionEngine()
