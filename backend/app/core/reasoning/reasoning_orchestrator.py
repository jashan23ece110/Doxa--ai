"""
Deliberative Reasoning Orchestrator for Enterprise Reasoning Engine.

Responsible for selecting reasoning mode, launching reasoning branches,
monitoring execution, aggregating outputs, and producing the final reasoning result.
"""

from typing import Dict, Any, List
from app.core.logging import logger
from app.core.reasoning.consensus_engine import consensus_engine
from app.core.reasoning.counterfactual import counterfactual_engine
from app.core.reasoning.graph_of_thoughts import graph_of_thoughts_engine
from app.core.reasoning.hypothesis_engine import hypothesis_engine
from app.core.reasoning.hypothesis_validator import hypothesis_validator
from app.core.reasoning.reasoning_cache import reasoning_cache
from app.core.reasoning.reasoning_models import DeliberativeReasoningResult
from app.core.reasoning.reasoning_score import reasoning_score_engine
from app.core.reasoning.tree_of_thoughts import tree_of_thoughts_engine


class DeliberativeReasoningOrchestrator:
    """Central orchestrator for multi-paradigm deliberative reasoning."""

    @staticmethod
    def execute_deliberative_reasoning(
        prompt: str,
        mode: str = "tree_of_thoughts",
    ) -> DeliberativeReasoningResult:
        """
        Launches multi-branch deliberative reasoning paradigms and synthesizes final answer.
        """
        # Check cache
        cache_key = f"delib_{hash(prompt)}"
        cached = reasoning_cache.get(cache_key)
        if cached:
            logger.info("DeliberativeReasoningOrchestrator returning cached reasoning result.")
            return cached

        logger.info(f"DeliberativeReasoningOrchestrator executing mode '{mode}' for prompt: '{prompt[:50]}...'")

        # 1. Tree & Graph of Thoughts
        tree = tree_of_thoughts_engine.build_thought_tree(prompt)
        graph = graph_of_thoughts_engine.build_reasoning_graph(prompt)

        # 2. Hypothesis & Counterfactual Generation
        hypos = hypothesis_engine.generate_hypotheses(prompt)
        validated_hypos = hypothesis_validator.validate_hypotheses(hypos)
        counterfactuals = counterfactual_engine.evaluate_counterfactuals(prompt)

        # 3. Consensus & Scoring
        branch_texts = [
            f"Tree best path node: {tree.nodes[tree.best_path_node_ids[-1]].thought_text}",
            f"Validated hypothesis: {validated_hypos[0].statement}",
            f"Counterfactual risk check: {counterfactuals[0].alternative_outcome}",
        ]
        consensus = consensus_engine.synthesize_consensus(branch_texts)
        score_report = reasoning_score_engine.score_reasoning()

        res = DeliberativeReasoningResult(
            primary_mode=mode,
            final_answer=consensus.consensus_text,
            consensus=consensus,
            score_report=score_report,
            tree_snapshot=tree,
            graph_snapshot=graph,
            hypotheses=validated_hypos,
            counterfactuals=counterfactuals,
        )

        reasoning_cache.set(cache_key, res)
        logger.info(f"DeliberativeReasoningOrchestrator completed execution (Result ID: {res.result_id}).")
        return res


# Global DeliberativeReasoningOrchestrator instance
deliberative_reasoning_orchestrator = DeliberativeReasoningOrchestrator()
