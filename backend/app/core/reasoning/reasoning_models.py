"""
Deliberative Reasoning Models for Enterprise Reasoning Engine.

Defines Pydantic data models for ThoughtNode, ThoughtTree, ReasoningGraph,
HypothesisCandidate, CounterfactualScenario, ConsensusResult, ReasoningScoreReport,
and DeliberativeReasoningResult.
"""

import time
import uuid
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class ThoughtNode(BaseModel):
    """Single node in a Tree or Graph of Thoughts."""

    node_id: str = Field(default_factory=lambda: f"tnode_{uuid.uuid4().hex[:8]}")
    thought_text: str
    score: float = 0.5
    depth: int = 0
    parent_id: Optional[str] = None
    children_ids: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ThoughtTree(BaseModel):
    """Tree of Thoughts structure."""

    tree_id: str = Field(default_factory=lambda: f"tree_{uuid.uuid4().hex[:8]}")
    root_node_id: str
    nodes: Dict[str, ThoughtNode] = Field(default_factory=dict)
    max_depth: int = 3
    best_path_node_ids: List[str] = Field(default_factory=list)


class ReasoningGraph(BaseModel):
    """Graph of Thoughts dependency structure."""

    graph_id: str = Field(default_factory=lambda: f"graph_{uuid.uuid4().hex[:8]}")
    nodes: Dict[str, ThoughtNode] = Field(default_factory=dict)
    edges: List[Dict[str, str]] = Field(default_factory=list)  # source -> target
    topological_order: List[str] = Field(default_factory=list)


class HypothesisCandidate(BaseModel):
    """Candidate explanation hypothesis."""

    hypothesis_id: str = Field(default_factory=lambda: f"hypo_{uuid.uuid4().hex[:8]}")
    statement: str
    plausibility_score: float = 0.5
    is_validated: bool = False
    evidence_grounding: List[str] = Field(default_factory=list)


class CounterfactualScenario(BaseModel):
    """What-if counterfactual scenario."""

    scenario_id: str = Field(default_factory=lambda: f"cfact_{uuid.uuid4().hex[:8]}")
    condition: str
    alternative_outcome: str
    risk_level: str = "low"  # low, medium, high


class ConsensusResult(BaseModel):
    """Consensus output synthesized across multiple reasoning branches."""

    consensus_id: str = Field(default_factory=lambda: f"cons_{uuid.uuid4().hex[:8]}")
    consensus_text: str
    confidence_score: float = 0.95
    participating_paradigms: List[str] = Field(default_factory=list)
    timestamp: float = Field(default_factory=time.time)


class ReasoningScoreReport(BaseModel):
    """Detailed evaluation score of a reasoning trajectory."""

    consistency: float = 0.95
    completeness: float = 0.90
    evidence_support: float = 0.92
    logical_quality: float = 0.94
    tool_correctness: float = 1.0
    overall_score: float = 0.94


class DeliberativeReasoningResult(BaseModel):
    """Final output from the Deliberative Reasoning Orchestrator."""

    result_id: str = Field(default_factory=lambda: f"delib_{uuid.uuid4().hex[:8]}")
    primary_mode: str = "tree_of_thoughts"
    final_answer: str
    consensus: ConsensusResult
    score_report: ReasoningScoreReport
    tree_snapshot: Optional[ThoughtTree] = None
    graph_snapshot: Optional[ReasoningGraph] = None
    hypotheses: List[HypothesisCandidate] = Field(default_factory=list)
    counterfactuals: List[CounterfactualScenario] = Field(default_factory=list)
    timestamp: float = Field(default_factory=time.time)
