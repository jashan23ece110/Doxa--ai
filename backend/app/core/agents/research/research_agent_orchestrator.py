"""
Global Research Agent Orchestrator.

Master research orchestrator driving end-to-end multi-step autonomous research workflows:
Research Goal -> Question Decomposition -> Research Planning -> Source Discovery -> Evidence Retrieval -> Source Evaluation -> Evidence Verification -> Knowledge Gap Detection -> Synthesis -> Evaluation -> Final Report.
"""

import time
from typing import Dict, Any, Optional
from app.core.logging import security_logger
from app.core.agents.research.research_agent_types import (
    ResearchGoal, ResearchPlan, ResearchReport, ResearchFinding
)
from app.core.agents.research.research_planner import research_planner
from app.core.agents.research.source_discovery_engine import source_discovery_engine
from app.core.agents.research.evidence_retrieval_engine import evidence_retrieval_engine
from app.core.agents.research.source_reliability_engine import source_reliability_engine
from app.core.agents.research.evidence_verification_engine import evidence_verification_engine
from app.core.agents.research.knowledge_gap_engine import knowledge_gap_engine
from app.core.agents.research.research_synthesis_engine import research_synthesis_engine
from app.core.agents.research.research_report_builder import research_report_builder


class ResearchAgentOrchestrator:
    """Global Research Agent Orchestrator Facade."""

    async def execute_research_workflow(self, topic: str, objective: str) -> ResearchReport:
        """
        Executes end-to-end multi-step autonomous research workflow over target topic.

        Args:
            topic: Target research topic string.
            objective: Research objective string.

        Returns:
            ResearchReport object.
        """
        t0 = time.time()
        security_logger.info(f"ResearchAgentOrchestrator: Starting research workflow for topic '{topic}'.")

        # 1. Goal & Question Decomposition
        goal = ResearchGoal(topic=topic, objective=objective)
        plan = research_planner.create_research_plan(goal)

        # 2. Source Discovery & Reliability Assessment
        sources = source_discovery_engine.discover_sources(topic)
        for src in sources:
            source_reliability_engine.evaluate_source_reliability(src)

        # 3. Evidence Retrieval
        evidences = await evidence_retrieval_engine.retrieve_evidence(topic, sources)

        # 4. Evidence Verification
        finding = evidence_verification_engine.verify_finding(
            title=f"Verified Findings on {topic}",
            summary=f"Analysis confirms key objective metrics for '{topic}'.",
            evidences=evidences,
        )

        # 5. Knowledge Gap Detection
        gaps = knowledge_gap_engine.detect_knowledge_gaps(plan.questions)

        # 6. Synthesis & Report Generation
        synthesis = research_synthesis_engine.synthesize_research([finding], gaps)
        report = research_report_builder.build_report(goal, synthesis)

        security_logger.info(f"ResearchAgentOrchestrator: Completed research report '{report.report_id}' for '{topic}' in {round((time.time() - t0)*1000, 2)}ms.")
        return report


# Global ResearchAgentOrchestrator instance
research_agent_orchestrator = ResearchAgentOrchestrator()
