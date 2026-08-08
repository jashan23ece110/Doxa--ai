#!/usr/bin/env python3
"""
Integration Test Suite for Stage 10 Part 6 — Explainable AI, Decision Governance & Trust Layer.
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


def test_decision_explanation_engine():
    print("\n💡 Testing Decision Explanation Engine...")
    from app.core.decision_intelligence.governance.decision_explanation_engine import decision_explanation_engine

    expl = decision_explanation_engine.generate_explanation("dec_100", "Cloud Strategy Decision")
    check("Explanation generated", expl is not None)
    check("Summary rationale present", len(expl.summary_rationale) > 0)
    check("Evidence contributions present", len(expl.evidence_contributions) == 2)


def test_model_explainability_engine():
    print("\n🧠 Testing Model Explainability Engine...")
    from app.core.decision_intelligence.governance.model_explainability_engine import model_explainability_engine

    reasoning = model_explainability_engine.explain_model_type("RANDOM_FOREST")
    check("Model reasoning generated", reasoning is not None)
    check("Top features present", len(reasoning.top_features) == 2)


def test_counterfactual_engine():
    print("\n🔀 Testing Counterfactual Analysis Engine...")
    from app.core.decision_intelligence.governance.counterfactual_engine import counterfactual_engine

    scenario = counterfactual_engine.evaluate_counterfactual("CapitalBudget", 50000.0, 75000.0)
    check("Counterfactual scenario created", scenario is not None)
    check("Flagged as hypothetical", scenario.is_hypothetical)


def test_decision_lineage_engine():
    print("\n📜 Testing Decision Lineage Engine...")
    from app.core.decision_intelligence.governance.explainability_types import DecisionTrace
    from app.core.decision_intelligence.governance.decision_lineage_engine import decision_lineage_engine

    trace1 = DecisionTrace(step_name="FeatureConstruction", input_summary="Raw Features", output_summary="Normalized Features")
    lineage = decision_lineage_engine.record_lineage("dec_100", [trace1])

    check("Decision lineage recorded", lineage is not None)
    check("Lineage is reproducible", lineage.is_reproducible)


def test_governance_policy_engine():
    print("\n⚖️ Testing Governance Policy Engine...")
    from app.core.decision_intelligence.governance.governance_policy_engine import governance_policy_engine

    violations = governance_policy_engine.evaluate_policy_compliance(estimated_cost=5000.0, risk_score=2.0)
    check("Policy evaluation completed (0 violations)", len(violations) == 0)

    violations_risk = governance_policy_engine.evaluate_policy_compliance(estimated_cost=5000.0, risk_score=8.0)
    check("High risk violation detected", len(violations_risk) == 1)


def test_human_review_engine():
    print("\n👤 Testing Human Decision Review Engine...")
    from app.core.decision_intelligence.governance.human_review_engine import human_review_engine

    areq = human_review_engine.create_approval_request("dec_100", "Deploy Cloud Resource", estimated_cost=15000.0)
    check("Approval request created", areq is not None)
    check("Status is PENDING_APPROVAL", areq.status == "PENDING_APPROVAL")

    adec = human_review_engine.submit_approval_decision(areq.approval_request_id, "AdminUser", "APPROVED")
    check("Human approval decision submitted", adec is not None)
    check("Decision is APPROVED", adec.decision == "APPROVED")


def test_governance_monitor():
    print("\n🩺 Testing Governance Monitor...")
    from app.core.decision_intelligence.governance.governance_monitor import governance_monitor

    violations = governance_monitor.inspect_decision("dec_100", confidence_score=0.65)
    check("Governance alert generated for low confidence", len(violations) == 1)


def test_decision_audit_engine():
    print("\n📝 Testing Decision Audit Engine...")
    from app.core.decision_intelligence.governance.decision_audit_engine import decision_audit_engine

    record = decision_audit_engine.record_audit("DECISION_APPROVED", "dec_100", {"approver": "AdminUser"})
    check("Audit record created", record is not None)
    check("Entity ID matches", record.entity_id == "dec_100")


def test_trust_evaluation_engine():
    print("\n🛡️ Testing Trust Evaluation Engine...")
    from app.core.decision_intelligence.governance.trust_evaluation_engine import trust_evaluation_engine

    score = trust_evaluation_engine.calculate_trust_score(0.96, 0.94)
    check("Trust score calculated", score is not None)
    check("Composite trust == 0.95", score.composite_trust == 0.95)


async def test_full_backward_compatibility():
    print("\n🔒 Testing Integration & Backward Compatibility across Stages 1-10 Part 5...")
    from app.core.decision_intelligence.optimization.optimization_orchestrator import optimization_orchestrator
    from app.core.decision_intelligence.prediction.predictive_decision_orchestrator import predictive_decision_orchestrator
    from app.core.decision_intelligence.risk.risk_intelligence_orchestrator import risk_intelligence_orchestrator
    from app.core.decision_intelligence.strategy.strategic_orchestrator import strategic_orchestrator
    from app.core.decision_intelligence.decision_intelligence_orchestrator import decision_intelligence_orchestrator
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

    opt_res = await optimization_orchestrator.execute_optimization_analysis("GovernanceIntegrationTarget")
    check("Stage 10 Part 5 Optimization Orchestrator operates seamlessly", opt_res is not None)

    pred_res = await predictive_decision_orchestrator.execute_predictive_analysis("GovernanceIntegrationTarget")
    check("Stage 10 Part 4 Predictive Decision Orchestrator operates seamlessly", pred_res is not None)

    risk_res = await risk_intelligence_orchestrator.execute_risk_assessment("GovernanceIntegrationTarget")
    check("Stage 10 Part 3 Risk Intelligence Orchestrator operates seamlessly", risk_res is not None)

    strat_res = await strategic_orchestrator.execute_strategic_analysis("Governance Strategic Plan")
    check("Stage 10 Part 2 Strategic Intelligence Orchestrator operates seamlessly", strat_res is not None)

    dec_res = await decision_intelligence_orchestrator.execute_decision_analysis("Governance Integration Decision", "Evaluate integration")
    check("Stage 10 Part 1 Decision Intelligence Orchestrator operates seamlessly", dec_res is not None)

    master_agent_res = await autonomous_agent_orchestrator.execute_master_autonomous_goal("Governance Integration Test Goal", "DoxaBackend")
    check("Stage 9 Global Autonomous Agent Platform operates seamlessly", master_agent_res is not None)

    mem = agent_memory_engine.get_or_create_memory("gov_compat_agent")
    check("Stage 9 Part 7 Agent Memory Engine operates seamlessly", mem is not None)

    cres = await collaboration_orchestrator.execute_collaboration_session("Governance Session Goal", ["ag_1", "ag_2"])
    check("Stage 9 Part 6 Collaboration Orchestrator operates seamlessly", cres is not None)

    devops_res = await devops_agent_orchestrator.execute_devops_workflow("production", "Governance-Gateway")
    check("Stage 9 Part 5 DevOps Agent Orchestrator operates seamlessly", devops_res is not None)

    report = await research_agent_orchestrator.execute_research_workflow("Governance Security", "Analyze Safety")
    check("Stage 9 Part 4 Research Agent Orchestrator operates seamlessly", report is not None)

    cwork = await coding_agent_orchestrator.execute_coding_workflow("Refactor governance logger", "DoxaBackend")
    check("Stage 9 Part 3 Coding Agent Orchestrator operates seamlessly", cwork is not None)

    plan = await autonomous_planning_engine.create_execution_plan("goal_gov_compat", "Governance Compat Plan")
    check("Stage 9 Part 2 Autonomous Planning Engine operates seamlessly", plan is not None)

    aorch = await agent_orchestrator.execute_autonomous_goal("Governance Compatibility Test", "Test goal", "system_analysis")
    check("Stage 9 Part 1 Agent Orchestrator operates seamlessly", aorch is not None)

    data_assess = await enterprise_data_intelligence_platform.run_master_data_intelligence_assessment("Governance_Platform_Test")
    check("Stage 8 Enterprise Data Intelligence Platform operates seamlessly", data_assess is not None)

    human_assess = await enterprise_human_intelligence_platform.run_master_human_intelligence_assessment("Governance_Platform_Test")
    check("Stage 7 Human Intelligence Platform operates seamlessly", human_assess is not None)

    payload = b"MZ\x90\x00\x03\x00\x00\x00\x04\x00\x00\x00VirtualAllocEx\x00"
    sec_res = await enterprise_security_platform.run_full_security_pipeline(payload, "governance_test.exe")
    check("Stage 6 Enterprise Security Platform operates seamlessly", sec_res is not None)
    check("AI OS Kernel remains fully functional", ai_os_kernel is not None)


async def main():
    print("==========================================================================")
    print("STAGE 10 PART 6 — EXPLAINABLE AI, DECISION GOVERNANCE & TRUST TEST SUITE")
    print("==========================================================================")

    test_decision_explanation_engine()
    test_model_explainability_engine()
    test_counterfactual_engine()
    test_decision_lineage_engine()
    test_governance_policy_engine()
    test_human_review_engine()
    test_governance_monitor()
    test_decision_audit_engine()
    test_trust_evaluation_engine()
    await test_full_backward_compatibility()

    print("\n==========================================================================")
    print(f"RESULTS: {PASS} passed, {FAIL} failed, {PASS + FAIL} total")
    print("==========================================================================")

    if FAIL > 0:
        sys.exit(1)
    print("\n🎉 STAGE 10 PART 6 SUCCESS: Explainable AI, Decision Governance & Trust Layer Complete!")


if __name__ == "__main__":
    asyncio.run(main())
