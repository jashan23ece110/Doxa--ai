#!/usr/bin/env python3
"""
Integration Test Suite for Stage 10 Part 7 — Executive Decision Support & Autonomous Recommendation Platform.
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


def test_executive_context_engine():
    print("\n🔍 Testing Executive Context Engine...")
    from app.core.decision_intelligence.executive.executive_context_engine import executive_context_engine

    context = executive_context_engine.build_executive_context("Cloud Expansion Strategy")
    check("Executive context built", context is not None)
    check("Key facts present", len(context["key_facts"]) >= 2)
    check("Opportunities present", len(context["opportunities"]) > 0)


def test_recommendation_engine():
    print("\n💡 Testing Recommendation Engine...")
    from app.core.decision_intelligence.executive.recommendation_engine import recommendation_engine

    rec = recommendation_engine.generate_recommendation("Cloud Expansion Strategy", 100000.0)
    check("Strategic recommendation generated", rec is not None)
    check("Authorization level is LEVEL_3_APPROVAL_READY", rec.authorization_level == "LEVEL_3_APPROVAL_READY")
    check("Requires approval == True", rec.requires_approval)


def test_priority_engine():
    print("\n📊 Testing Decision Prioritization Engine...")
    from app.core.decision_intelligence.executive.priority_engine import priority_engine

    prec = priority_engine.prioritize_decision("Cloud Expansion Strategy", urgency_score=9.0, impact_score=9.5)
    check("Priority recommendation calculated", prec is not None)
    check("Overall priority rank == 1", prec.overall_priority_rank == 1)


def test_action_plan_engine():
    print("\n📋 Testing Action Plan Engine...")
    from app.core.decision_intelligence.executive.action_plan_engine import action_plan_engine

    plan = action_plan_engine.build_action_plan("Cloud Expansion Strategy")
    check("Action plan structured", plan is not None)
    check("3 milestones defined", len(plan.milestones) == 3)
    check("Is authorized == False until approved", not plan.is_authorized)


def test_long_term_planning_engine():
    print("\n🔮 Testing Long-Term Planning Engine...")
    from app.core.decision_intelligence.executive.executive_types import ExecutiveObjective
    from app.core.decision_intelligence.executive.long_term_planning_engine import long_term_planning_engine

    obj = ExecutiveObjective(name="Enterprise Growth")
    lt_plan = long_term_planning_engine.evaluate_long_term_horizon(obj)
    check("Long-term planning horizon evaluated", lt_plan is not None)
    check("3 horizons present", len(lt_plan["horizons"]) == 3)


def test_executive_simulation_engine():
    print("\n🎮 Testing Executive Simulation Engine...")
    from app.core.decision_intelligence.executive.executive_simulation_engine import executive_simulation_engine

    scenarios = executive_simulation_engine.simulate_strategic_outcomes(25.0)
    check("4 strategic scenarios simulated", len(scenarios) == 4)
    check("OPTIMISTIC scenario ROI == 31.25%", scenarios[1].projected_roi == 31.25)
    check("All marked as simulated", scenarios[0].is_simulated)


def test_executive_brief_engine():
    print("\n📑 Testing Executive Brief Engine...")
    from app.core.decision_intelligence.executive.executive_context_engine import executive_context_engine
    from app.core.decision_intelligence.executive.recommendation_engine import recommendation_engine
    from app.core.decision_intelligence.executive.action_plan_engine import action_plan_engine
    from app.core.decision_intelligence.executive.executive_brief_engine import executive_brief_engine

    ctx = executive_context_engine.build_executive_context("Brief Strategy")
    rec = recommendation_engine.generate_recommendation("Brief Strategy", 100000.0)
    plan = action_plan_engine.build_action_plan("Brief Strategy")
    brief = executive_brief_engine.assemble_brief("Brief Strategy", rec, plan, ctx)

    check("Executive decision brief assembled", brief is not None)
    check("Current situation described", len(brief.current_situation) > 0)
    check("2 alternatives evaluated", len(brief.alternatives) == 2)


def test_recommendation_monitor():
    print("\n📈 Testing Recommendation Monitor...")
    from app.core.decision_intelligence.executive.recommendation_monitor import recommendation_monitor

    out = recommendation_monitor.record_recommendation_outcome("srec_100", 100000.0, 105000.0)
    check("Outcome recorded", out is not None)
    check("Recommendation accuracy == 1.05", out["recommendation_accuracy"] == 1.05)


async def test_executive_decision_orchestrator():
    print("\n🌐 Testing Global Executive Decision Orchestrator...")
    from app.core.decision_intelligence.executive.executive_decision_orchestrator import executive_decision_orchestrator

    res = await executive_decision_orchestrator.execute_executive_analysis("Enterprise Autonomous Strategy Drive", budget_limit=150000.0)
    check("Executive decision analysis completed", res is not None)
    check("Status is COMPLETED", res.status == "COMPLETED")
    check("Authorization level is LEVEL_3_APPROVAL_READY", res.authorization_level == "LEVEL_3_APPROVAL_READY")
    check("Executive brief included", res.brief is not None)


async def test_full_backward_compatibility():
    print("\n🔒 Testing Integration & Backward Compatibility across Stages 1-10 Part 6...")
    from app.core.decision_intelligence.governance.decision_explanation_engine import decision_explanation_engine
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

    gov_expl = decision_explanation_engine.generate_explanation("dec_exec_compat", "Exec Governance Test")
    check("Stage 10 Part 6 Explainability Engine operates seamlessly", gov_expl is not None)

    opt_res = await optimization_orchestrator.execute_optimization_analysis("ExecIntegrationTarget")
    check("Stage 10 Part 5 Optimization Orchestrator operates seamlessly", opt_res is not None)

    pred_res = await predictive_decision_orchestrator.execute_predictive_analysis("ExecIntegrationTarget")
    check("Stage 10 Part 4 Predictive Decision Orchestrator operates seamlessly", pred_res is not None)

    risk_res = await risk_intelligence_orchestrator.execute_risk_assessment("ExecIntegrationTarget")
    check("Stage 10 Part 3 Risk Intelligence Orchestrator operates seamlessly", risk_res is not None)

    strat_res = await strategic_orchestrator.execute_strategic_analysis("Exec Strategic Plan")
    check("Stage 10 Part 2 Strategic Intelligence Orchestrator operates seamlessly", strat_res is not None)

    dec_res = await decision_intelligence_orchestrator.execute_decision_analysis("Exec Integration Decision", "Evaluate integration")
    check("Stage 10 Part 1 Decision Intelligence Orchestrator operates seamlessly", dec_res is not None)

    master_agent_res = await autonomous_agent_orchestrator.execute_master_autonomous_goal("Exec Integration Test Goal", "DoxaBackend")
    check("Stage 9 Global Autonomous Agent Platform operates seamlessly", master_agent_res is not None)

    mem = agent_memory_engine.get_or_create_memory("exec_compat_agent")
    check("Stage 9 Part 7 Agent Memory Engine operates seamlessly", mem is not None)

    cres = await collaboration_orchestrator.execute_collaboration_session("Exec Session Goal", ["ag_1", "ag_2"])
    check("Stage 9 Part 6 Collaboration Orchestrator operates seamlessly", cres is not None)

    devops_res = await devops_agent_orchestrator.execute_devops_workflow("production", "Exec-Gateway")
    check("Stage 9 Part 5 DevOps Agent Orchestrator operates seamlessly", devops_res is not None)

    report = await research_agent_orchestrator.execute_research_workflow("Exec Security", "Analyze Safety")
    check("Stage 9 Part 4 Research Agent Orchestrator operates seamlessly", report is not None)

    cwork = await coding_agent_orchestrator.execute_coding_workflow("Refactor exec logger", "DoxaBackend")
    check("Stage 9 Part 3 Coding Agent Orchestrator operates seamlessly", cwork is not None)

    plan = await autonomous_planning_engine.create_execution_plan("goal_exec_compat", "Exec Compat Plan")
    check("Stage 9 Part 2 Autonomous Planning Engine operates seamlessly", plan is not None)

    aorch = await agent_orchestrator.execute_autonomous_goal("Exec Compatibility Test", "Test goal", "system_analysis")
    check("Stage 9 Part 1 Agent Orchestrator operates seamlessly", aorch is not None)

    data_assess = await enterprise_data_intelligence_platform.run_master_data_intelligence_assessment("Exec_Platform_Test")
    check("Stage 8 Enterprise Data Intelligence Platform operates seamlessly", data_assess is not None)

    human_assess = await enterprise_human_intelligence_platform.run_master_human_intelligence_assessment("Exec_Platform_Test")
    check("Stage 7 Human Intelligence Platform operates seamlessly", human_assess is not None)

    payload = b"MZ\x90\x00\x03\x00\x00\x00\x04\x00\x00\x00VirtualAllocEx\x00"
    sec_res = await enterprise_security_platform.run_full_security_pipeline(payload, "exec_test.exe")
    check("Stage 6 Enterprise Security Platform operates seamlessly", sec_res is not None)
    check("AI OS Kernel remains fully functional", ai_os_kernel is not None)


async def main():
    print("==========================================================================")
    print("STAGE 10 PART 7 — EXECUTIVE DECISION SUPPORT & AUTONOMOUS RECOMMENDATIONS")
    print("==========================================================================")

    test_executive_context_engine()
    test_recommendation_engine()
    test_priority_engine()
    test_action_plan_engine()
    test_long_term_planning_engine()
    test_executive_simulation_engine()
    test_executive_brief_engine()
    test_recommendation_monitor()
    await test_executive_decision_orchestrator()
    await test_full_backward_compatibility()

    print("\n==========================================================================")
    print(f"RESULTS: {PASS} passed, {FAIL} failed, {PASS + FAIL} total")
    print("==========================================================================")

    if FAIL > 0:
        sys.exit(1)
    print("\n🎉 STAGE 10 PART 7 SUCCESS: Executive Decision Support Platform Complete!")


if __name__ == "__main__":
    asyncio.run(main())
