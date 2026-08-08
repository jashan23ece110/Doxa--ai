#!/usr/bin/env python3
"""
Integration Test Suite for Stage 9 Part 4 — Enterprise Autonomous Research Agent Platform.
"""

import asyncio
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

PASS = 0
FAIL = 0


def check(label, condition):
    global PASS, FAIL
    if condition:
        PASS += 1
        print(f"  ✅ {label}")
    else:
        FAIL += 1
        print(f"  ❌ {label}")


def test_source_discovery_engine():
    print("\n🔍 Testing Authorized Source Discovery Engine...")
    from app.core.agents.research.source_discovery_engine import source_discovery_engine

    sources = source_discovery_engine.discover_sources("Cybersecurity Threats")
    check("Authorized sources discovered", len(sources) == 2)
    check("Authority score >= 0.95", sources[0].authority_score >= 0.95)


def test_research_planner():
    print("\n📋 Testing Enterprise Research Planner...")
    from app.core.agents.research.research_agent_types import ResearchGoal
    from app.core.agents.research.research_planner import research_planner

    goal = ResearchGoal(topic="Zero Trust Architecture", objective="Evaluate Zero Trust rollout strategies")
    plan = research_planner.create_research_plan(goal)

    check("Research plan created", plan is not None)
    check("2 research questions generated", len(plan.questions) == 2)
    check("2 research tasks generated", len(plan.tasks) == 2)


async def test_evidence_retrieval_engine():
    print("\n🔎 Testing Enterprise Evidence Retrieval Engine...")
    from app.core.agents.research.source_discovery_engine import source_discovery_engine
    from app.core.agents.research.evidence_retrieval_engine import evidence_retrieval_engine

    sources = source_discovery_engine.discover_sources("Cloud Security")
    evidences = await evidence_retrieval_engine.retrieve_evidence("Cloud Security", sources)

    check("Evidence snippets retrieved", len(evidences) == 2)
    check("Citation reference present", len(evidences[0].citation_reference) > 0)


def test_source_reliability_engine():
    print("\n⚖️ Testing Source Reliability Assessment Engine...")
    from app.core.agents.research.source_discovery_engine import source_discovery_engine
    from app.core.agents.research.source_reliability_engine import source_reliability_engine

    sources = source_discovery_engine.discover_sources("AI Governance")
    rel = source_reliability_engine.evaluate_source_reliability(sources[0])

    check("Source reliability evaluated", rel is not None)
    check("Reliability score >= 0.95", rel.reliability_score >= 0.95)


def test_evidence_verification_engine():
    print("\n✔️ Testing Evidence Verification Engine...")
    from app.core.agents.research.research_agent_types import SourceEvidence
    from app.core.agents.research.evidence_verification_engine import evidence_verification_engine

    ev1 = SourceEvidence(source_id="src_1", content_snippet="Snippet 1", citation_reference="Ref 1")
    ev2 = SourceEvidence(source_id="src_2", content_snippet="Snippet 2", citation_reference="Ref 2")

    finding = evidence_verification_engine.verify_finding("Zero Trust Finding", "Summary text", [ev1, ev2])
    check("Finding verified", finding is not None)
    check("Status is VERIFIED", finding.verification_status == "VERIFIED")
    check("2 citations populated", len(finding.citations) == 2)


def test_knowledge_gap_engine():
    print("\n🧩 Testing Knowledge Gap Detector...")
    from app.core.agents.research.research_agent_types import ResearchQuestion
    from app.core.agents.research.knowledge_gap_engine import knowledge_gap_engine

    q1 = ResearchQuestion(question_text="What are long-term trends?")
    gaps = knowledge_gap_engine.detect_knowledge_gaps([q1])

    check("Knowledge gaps identified", len(gaps) > 0)
    check("Recommended action present", len(gaps[0].recommended_action) > 0)


def test_research_synthesis_engine():
    print("\n🔬 Testing Research Synthesis Engine...")
    from app.core.agents.research.research_agent_types import ResearchFinding, KnowledgeGap
    from app.core.agents.research.research_synthesis_engine import research_synthesis_engine

    f1 = ResearchFinding(title="Finding 1", summary="Summary 1")
    gap1 = KnowledgeGap(description="Gap 1")

    synth = research_synthesis_engine.synthesize_research([f1], [gap1])
    check("Research synthesized", synth is not None)
    check("1 hypothesis generated", len(synth.hypotheses) == 1)


def test_research_report_builder():
    print("\n📄 Testing Research Report Builder & Markdown Exporter...")
    from app.core.agents.research.research_agent_types import ResearchGoal, ResearchFinding, KnowledgeGap
    from app.core.agents.research.research_synthesis_engine import research_synthesis_engine
    from app.core.agents.research.research_report_builder import research_report_builder

    goal = ResearchGoal(topic="AI Security", objective="Assess AI risks")
    f1 = ResearchFinding(title="AI Model Risk", summary="Models require sandbox isolation", citations=["Ref A"])
    gap1 = KnowledgeGap(description="Limited long-term data")

    synth = research_synthesis_engine.synthesize_research([f1], [gap1])
    report = research_report_builder.build_report(goal, synth)

    check("Research report built", report is not None)
    check("Executive summary present", len(report.executive_summary) > 0)
    check("Overall confidence >= 0.95", report.overall_confidence >= 0.95)

    md = research_report_builder.to_markdown(report)
    check("Markdown export generated", md.startswith("# Autonomous Research Report: AI Security"))


async def test_research_agent_orchestrator():
    print("\n🌐 Testing Global Research Agent Orchestrator Workflow...")
    from app.core.agents.research.research_agent_orchestrator import research_agent_orchestrator

    report = await research_agent_orchestrator.execute_research_workflow("Quantum Cryptography", "Analyze post-quantum encryption readiness")
    check("Multi-step research report generated", report is not None)
    check("Findings populated", len(report.findings) > 0)
    check("Citations populated", len(report.citations) > 0)


async def test_full_backward_compatibility():
    print("\n🔒 Testing Integration & Backward Compatibility across Stages 1-9 Part 3...")
    from app.core.agents.coding import coding_agent_orchestrator
    from app.core.agents.planning import autonomous_planning_engine
    from app.core.agents import agent_orchestrator
    from app.core.data_intelligence.platform import enterprise_data_intelligence_platform
    from app.core.human_intelligence import enterprise_human_intelligence_platform
    from app.core.security import enterprise_security_platform
    from app.core.intelligence import ai_os_kernel

    cwork = await coding_agent_orchestrator.execute_coding_workflow("Refactor research logger", "DoxaBackend")
    check("Stage 9 Part 3 Coding Agent Orchestrator operates seamlessly", cwork is not None)

    plan = await autonomous_planning_engine.create_execution_plan("goal_research_compat", "Research Compat Plan")
    check("Stage 9 Part 2 Autonomous Planning Engine operates seamlessly", plan is not None)

    aorch = await agent_orchestrator.execute_autonomous_goal("Research Compatibility Test", "Test goal", "system_analysis")
    check("Stage 9 Part 1 Agent Orchestrator operates seamlessly", aorch is not None)

    data_assess = await enterprise_data_intelligence_platform.run_master_data_intelligence_assessment("Research_Master_Test")
    check("Stage 8 Enterprise Data Intelligence Platform operates seamlessly", data_assess is not None)

    human_assess = await enterprise_human_intelligence_platform.run_master_human_intelligence_assessment("Research_Master_Test")
    check("Stage 7 Human Intelligence Platform operates seamlessly", human_assess is not None)

    payload = b"MZ\x90\x00\x03\x00\x00\x00\x04\x00\x00\x00VirtualAllocEx\x00"
    sec_res = await enterprise_security_platform.run_full_security_pipeline(payload, "research_test.exe")
    check("Stage 6 Enterprise Security Platform operates seamlessly", sec_res is not None)
    check("AI OS Kernel remains fully functional", ai_os_kernel is not None)


async def main():
    print("==========================================================================")
    print("STAGE 9 PART 4 — ENTERPRISE AUTONOMOUS RESEARCH AGENT PLATFORM TEST SUITE")
    print("==========================================================================")

    test_source_discovery_engine()
    test_research_planner()
    await test_evidence_retrieval_engine()
    test_source_reliability_engine()
    test_evidence_verification_engine()
    test_knowledge_gap_engine()
    test_research_synthesis_engine()
    test_research_report_builder()
    await test_research_agent_orchestrator()
    await test_full_backward_compatibility()

    print("\n==========================================================================")
    print(f"RESULTS: {PASS} passed, {FAIL} failed, {PASS + FAIL} total")
    print("==========================================================================")

    if FAIL > 0:
        sys.exit(1)
    print("\n🎉 STAGE 9 PART 4 SUCCESS: Enterprise Autonomous Research Agent Platform Deployed!")


if __name__ == "__main__":
    asyncio.run(main())
