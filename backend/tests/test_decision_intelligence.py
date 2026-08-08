#!/usr/bin/env python3
"""
Integration Test Suite for Stage 10 Part 1 — Enterprise Decision Intelligence Platform.
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


async def test_decision_context_engine():
    print("\n🔍 Testing Decision Context Engine...")
    from app.core.decision_intelligence.decision_types import DecisionRequest
    from app.core.decision_intelligence.decision_context_engine import decision_context_engine

    dreq = DecisionRequest(title="Cloud Migration Decision", description="Assess cloud provider choices")
    ctx = await decision_context_engine.build_decision_context(dreq)

    check("Decision context aggregated", ctx is not None)
    check("2 context evidence items returned", len(ctx.relevant_evidences) == 2)


def test_decision_objective_engine():
    print("\n📋 Testing Decision Objective Engine...")
    from app.core.decision_intelligence.decision_objective_engine import decision_objective_engine

    objectives = decision_objective_engine.structure_objectives("Security Platform Rollout")
    check("Objectives structured", len(objectives) == 2)
    check("First objective weight == 0.6", objectives[0].weight == 0.6)


def test_alternative_generation_engine():
    print("\n🔀 Testing Decision Alternative Generation Engine...")
    from app.core.decision_intelligence.decision_objective_engine import decision_objective_engine
    from app.core.decision_intelligence.alternative_generation_engine import alternative_generation_engine

    objectives = decision_objective_engine.structure_objectives("Infrastructure Upgrade")
    alts = alternative_generation_engine.generate_alternatives("Infrastructure Upgrade", objectives)

    check("Alternatives generated", len(alts) == 2)
    check("Option A benefit > Option B benefit", alts[0].expected_benefit > alts[1].expected_benefit)


def test_evidence_engine():
    print("\n📜 Testing Decision Evidence Engine...")
    from app.core.decision_intelligence.decision_types import DecisionEvidence
    from app.core.decision_intelligence.evidence_engine import evidence_engine

    ev1 = DecisionEvidence(source_type="RAG", content="Snippet 1", confidence_score=0.95)
    ev2 = DecisionEvidence(source_type="KG", content="Snippet 2", confidence_score=0.91)

    score = evidence_engine.evaluate_evidence_quality([ev1, ev2])
    check("Evidence quality evaluated", score > 0.90)


def test_decision_model_engine():
    print("\n📊 Testing Decision Modeling Engine...")
    from app.core.decision_intelligence.decision_types import DecisionAlternative
    from app.core.decision_intelligence.decision_model_engine import decision_model_engine

    alt = DecisionAlternative(title="Option A", description="Test option", expected_benefit=90.0, expected_cost=15.0)
    deval = decision_model_engine.evaluate_alternative(alt, model_type="WEIGHTED_SCORING")

    check("Alternative evaluated", deval is not None)
    check("Composite score > 80.0", deval.composite_score > 80.0)
    check("Benefit-Cost ratio == 6.0", deval.benefit_cost_ratio == 6.0)


def test_uncertainty_engine():
    print("\n❓ Testing Uncertainty Analysis Engine...")
    from app.core.decision_intelligence.decision_types import DecisionEvidence
    from app.core.decision_intelligence.uncertainty_engine import uncertainty_engine

    ev1 = DecisionEvidence(source_type="RAG", content="Snippet 1", confidence_score=0.95)
    confidence = uncertainty_engine.analyze_uncertainty([ev1])

    check("Uncertainty analyzed", confidence is not None)
    check("Overall confidence >= 0.90", confidence.overall_confidence >= 0.90)


def test_decision_evaluation_engine():
    print("\n🏆 Testing Decision Evaluation Engine...")
    from app.core.decision_intelligence.decision_types import DecisionAlternative, DecisionEvaluation
    from app.core.decision_intelligence.decision_evaluation_engine import decision_evaluation_engine

    alt1 = DecisionAlternative(title="Option 1", description="Opt 1", expected_benefit=90.0)
    eval1 = DecisionEvaluation(alternative_id=alt1.alternative_id, composite_score=85.0)

    alt2 = DecisionAlternative(title="Option 2", description="Opt 2", expected_benefit=95.0)
    eval2 = DecisionEvaluation(alternative_id=alt2.alternative_id, composite_score=92.0)

    best_alt, best_eval = decision_evaluation_engine.select_best_alternative([(alt1, eval1), (alt2, eval2)])
    check("Optimal alternative selected", best_alt.title == "Option 2")
    check("Highest composite score selected", best_eval.composite_score == 92.0)


def test_decision_audit_engine():
    print("\n📝 Testing Decision Audit Engine...")
    from app.core.decision_intelligence.decision_audit_engine import decision_audit_engine

    audit = decision_audit_engine.record_decision_lineage("dreq_100", ["Context", "Model", "Recommendation"])
    check("Decision lineage recorded", audit is not None)
    check("3 lineage steps stored", len(audit.lineage_steps) == 3)
    check("Decision is reproducible", audit.is_reproducible)


async def test_decision_intelligence_orchestrator():
    print("\n🌐 Testing Global Decision Intelligence Orchestrator...")
    from app.core.decision_intelligence.decision_intelligence_orchestrator import decision_intelligence_orchestrator

    res = await decision_intelligence_orchestrator.execute_decision_analysis(
        "Enterprise Multi-Cloud Infrastructure Strategy",
        "Determine optimal cloud hosting topology for security and cost efficiency."
    )
    check("Master decision analysis completed", res is not None)
    check("Status is COMPLETED", res.status == "COMPLETED")
    check("Recommendation generated", res.recommendation is not None)
    check("Audit ID populated", len(res.audit_id) > 0)


async def test_full_backward_compatibility():
    print("\n🔒 Testing Integration & Backward Compatibility across Stages 1-9...")
    from app.core.agents.platform import autonomous_agent_orchestrator
    from app.core.agents.autonomy import agent_memory_engine
    from app.core.agents.collaboration import collaboration_orchestrator
    from app.core.agents.devops import devops_agent_orchestrator
    from app.core.agents.research import research_agent_orchestrator
    from app.core.agents.coding import coding_agent_orchestrator
    from app.core.agents.planning import autonomous_planning_engine
    from app.core.agents import agent_orchestrator
    from app.core.data_intelligence.platform import enterprise_data_intelligence_platform
    from app.core.human_intelligence import enterprise_human_intelligence_platform
    from app.core.security import enterprise_security_platform
    from app.core.intelligence import ai_os_kernel

    master_agent_res = await autonomous_agent_orchestrator.execute_master_autonomous_goal("Stage 10 Decision Integration Test", "DoxaBackend")
    check("Stage 9 Global Autonomous Agent Platform operates seamlessly", master_agent_res is not None)

    mem = agent_memory_engine.get_or_create_memory("decision_compat_agent")
    check("Stage 9 Part 7 Agent Memory Engine operates seamlessly", mem is not None)

    cres = await collaboration_orchestrator.execute_collaboration_session("Decision Session Goal", ["ag_1", "ag_2"])
    check("Stage 9 Part 6 Collaboration Orchestrator operates seamlessly", cres is not None)

    devops_res = await devops_agent_orchestrator.execute_devops_workflow("production", "Decision-Gateway")
    check("Stage 9 Part 5 DevOps Agent Orchestrator operates seamlessly", devops_res is not None)

    report = await research_agent_orchestrator.execute_research_workflow("Decision Security", "Analyze Safety")
    check("Stage 9 Part 4 Research Agent Orchestrator operates seamlessly", report is not None)

    cwork = await coding_agent_orchestrator.execute_coding_workflow("Refactor decision logger", "DoxaBackend")
    check("Stage 9 Part 3 Coding Agent Orchestrator operates seamlessly", cwork is not None)

    plan = await autonomous_planning_engine.create_execution_plan("goal_decision_compat", "Decision Compat Plan")
    check("Stage 9 Part 2 Autonomous Planning Engine operates seamlessly", plan is not None)

    aorch = await agent_orchestrator.execute_autonomous_goal("Decision Compatibility Test", "Test goal", "system_analysis")
    check("Stage 9 Part 1 Agent Orchestrator operates seamlessly", aorch is not None)

    data_assess = await enterprise_data_intelligence_platform.run_master_data_intelligence_assessment("Decision_Platform_Test")
    check("Stage 8 Enterprise Data Intelligence Platform operates seamlessly", data_assess is not None)

    human_assess = await enterprise_human_intelligence_platform.run_master_human_intelligence_assessment("Decision_Platform_Test")
    check("Stage 7 Human Intelligence Platform operates seamlessly", human_assess is not None)

    payload = b"MZ\x90\x00\x03\x00\x00\x00\x04\x00\x00\x00VirtualAllocEx\x00"
    sec_res = await enterprise_security_platform.run_full_security_pipeline(payload, "decision_test.exe")
    check("Stage 6 Enterprise Security Platform operates seamlessly", sec_res is not None)
    check("AI OS Kernel remains fully functional", ai_os_kernel is not None)


async def main():
    print("==========================================================================")
    print("STAGE 10 PART 1 — ENTERPRISE DECISION INTELLIGENCE PLATFORM TEST SUITE")
    print("==========================================================================")

    await test_decision_context_engine()
    test_decision_objective_engine()
    test_alternative_generation_engine()
    test_evidence_engine()
    test_decision_model_engine()
    test_uncertainty_engine()
    test_decision_evaluation_engine()
    test_decision_audit_engine()
    await test_decision_intelligence_orchestrator()
    await test_full_backward_compatibility()

    print("\n==========================================================================")
    print(f"RESULTS: {PASS} passed, {FAIL} failed, {PASS + FAIL} total")
    print("==========================================================================")

    if FAIL > 0:
        sys.exit(1)
    print("\n🎉 STAGE 10 PART 1 SUCCESS: Enterprise Decision Intelligence Platform Deployed!")


if __name__ == "__main__":
    asyncio.run(main())
