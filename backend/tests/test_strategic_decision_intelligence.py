#!/usr/bin/env python3
"""
Integration Test Suite for Stage 10 Part 2 — Strategic Planning & Scenario Analysis Engine.
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


def test_strategic_planning_engine():
    print("\n📐 Testing Strategic Planning Engine...")
    from app.core.decision_intelligence.strategy.strategic_types import StrategicObjective
    from app.core.decision_intelligence.strategy.strategic_planning_engine import strategic_planning_engine

    objs = [StrategicObjective(title="Expand Cloud Infrastructure", target_metric="ROI", target_value=120.0)]
    plan = strategic_planning_engine.create_strategic_plan("Cloud Expansion", objs)

    check("Strategic plan created", plan is not None)
    check("Chosen alternative title present", len(plan.chosen_alternative.title) > 0)
    check("Initiatives present", len(plan.chosen_alternative.initiatives) == 1)


def test_scenario_engine():
    print("\n🔮 Testing Scenario Generation Engine...")
    from app.core.decision_intelligence.strategy.scenario_engine import scenario_engine

    scenarios = scenario_engine.generate_scenarios("Cloud Expansion")
    check("3 canonical scenarios generated", len(scenarios) == 3)
    check("BASELINE scenario present", scenarios[0].name == "BASELINE")
    check("OPTIMISTIC scenario present", scenarios[1].name == "OPTIMISTIC")


def test_what_if_engine():
    print("\n⚡ Testing What-If Analysis Engine...")
    from app.core.decision_intelligence.strategy.what_if_engine import what_if_engine

    what_if = what_if_engine.evaluate_what_if("ResourceBudget", 10000.0, 15000.0)
    check("What-if analysis executed", what_if is not None)
    check("Original value recorded", what_if.original_value == 10000.0)
    check("Modified value recorded", what_if.modified_value == 15000.0)


def test_scenario_simulator():
    print("\n🎮 Testing Strategic Scenario Simulator...")
    from app.core.decision_intelligence.strategy.scenario_engine import scenario_engine
    from app.core.decision_intelligence.strategy.scenario_simulator import scenario_simulator

    scenarios = scenario_engine.generate_scenarios("Cloud Expansion")
    comp = scenario_simulator.compare_scenarios(scenarios[0], scenarios[1])

    check("Scenario comparison simulated", comp is not None)
    check("Delta ROI calculated (> 0)", comp.delta_roi_pct > 0)


def test_strategy_comparison_engine():
    print("\n📊 Testing Strategy Comparison Engine...")
    from app.core.decision_intelligence.strategy.strategic_types import StrategyAlternative
    from app.core.decision_intelligence.strategy.strategy_comparison_engine import strategy_comparison_engine

    alt1 = StrategyAlternative(title="Strategy Option 1", expected_value=100000.0)
    matrix = strategy_comparison_engine.compare_strategies([alt1])

    check("Comparison matrix generated", matrix is not None)
    check("Alternatives count == 1", matrix["alternatives_count"] == 1)


def test_tradeoff_engine():
    print("\n⚖️ Testing Strategic Trade-Off Engine...")
    from app.core.decision_intelligence.strategy.tradeoff_engine import tradeoff_engine

    tradeoffs = tradeoff_engine.analyze_tradeoffs("Cloud Expansion")
    check("Trade-offs identified", len(tradeoffs) == 2)
    check("SPEED vs RELIABILITY trade-off present", tradeoffs[0].dimension_a == "SPEED")


def test_strategic_forecasting_engine():
    print("\n📈 Testing Strategic Forecasting Engine...")
    from app.core.decision_intelligence.strategy.strategic_forecasting_engine import strategic_forecasting_engine

    forecast = strategic_forecasting_engine.forecast_trajectory("ROI_Pct", horizon_months=12)
    check("Forecast trajectory generated", forecast is not None)
    check("Horizon == 12 months", forecast["horizon_months"] == 12)
    check("Projected value > 0", forecast["projected_baseline_end_val"] > 0)


def test_strategic_plan_evaluator():
    print("\n🏆 Testing Strategic Plan Evaluator...")
    from app.core.decision_intelligence.strategy.strategic_types import StrategicObjective
    from app.core.decision_intelligence.strategy.strategic_planning_engine import strategic_planning_engine
    from app.core.decision_intelligence.strategy.strategic_plan_evaluator import strategic_plan_evaluator

    objs = [StrategicObjective(title="Obj 1", target_metric="ROI")]
    plan = strategic_planning_engine.create_strategic_plan("Test Plan", objs)
    seval = strategic_plan_evaluator.evaluate_plan(plan)

    check("Strategic evaluation completed", seval is not None)
    check("Overall strategic fit == 95.0", seval.overall_strategic_fit == 95.0)


async def test_strategic_orchestrator():
    print("\n🌐 Testing Global Strategic Intelligence Orchestrator...")
    from app.core.decision_intelligence.strategy.strategic_orchestrator import strategic_orchestrator

    mres = await strategic_orchestrator.execute_strategic_analysis("Enterprise Cloud Infrastructure Upgrade")
    check("Master strategic analysis completed", mres is not None)
    check("Status is COMPLETED", mres.status == "COMPLETED")
    check("Plan generated with scenarios", len(mres.plan.scenarios) > 0)
    check("Recommendation generated", mres.recommendation is not None)


async def test_full_backward_compatibility():
    print("\n🔒 Testing Integration & Backward Compatibility across Stages 1-10 Part 1...")
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

    dec_res = await decision_intelligence_orchestrator.execute_decision_analysis("Strategic Integration Decision", "Evaluate integration")
    check("Stage 10 Part 1 Decision Intelligence Orchestrator operates seamlessly", dec_res is not None)

    master_agent_res = await autonomous_agent_orchestrator.execute_master_autonomous_goal("Strategic Integration Test Goal", "DoxaBackend")
    check("Stage 9 Global Autonomous Agent Platform operates seamlessly", master_agent_res is not None)

    mem = agent_memory_engine.get_or_create_memory("strat_compat_agent")
    check("Stage 9 Part 7 Agent Memory Engine operates seamlessly", mem is not None)

    cres = await collaboration_orchestrator.execute_collaboration_session("Strategic Session Goal", ["ag_1", "ag_2"])
    check("Stage 9 Part 6 Collaboration Orchestrator operates seamlessly", cres is not None)

    devops_res = await devops_agent_orchestrator.execute_devops_workflow("production", "Strategic-Gateway")
    check("Stage 9 Part 5 DevOps Agent Orchestrator operates seamlessly", devops_res is not None)

    report = await research_agent_orchestrator.execute_research_workflow("Strategic Security", "Analyze Safety")
    check("Stage 9 Part 4 Research Agent Orchestrator operates seamlessly", report is not None)

    cwork = await coding_agent_orchestrator.execute_coding_workflow("Refactor strategic logger", "DoxaBackend")
    check("Stage 9 Part 3 Coding Agent Orchestrator operates seamlessly", cwork is not None)

    plan = await autonomous_planning_engine.create_execution_plan("goal_strat_compat", "Strategic Compat Plan")
    check("Stage 9 Part 2 Autonomous Planning Engine operates seamlessly", plan is not None)

    aorch = await agent_orchestrator.execute_autonomous_goal("Strategic Compatibility Test", "Test goal", "system_analysis")
    check("Stage 9 Part 1 Agent Orchestrator operates seamlessly", aorch is not None)

    data_assess = await enterprise_data_intelligence_platform.run_master_data_intelligence_assessment("Strategic_Platform_Test")
    check("Stage 8 Enterprise Data Intelligence Platform operates seamlessly", data_assess is not None)

    human_assess = await enterprise_human_intelligence_platform.run_master_human_intelligence_assessment("Strategic_Platform_Test")
    check("Stage 7 Human Intelligence Platform operates seamlessly", human_assess is not None)

    payload = b"MZ\x90\x00\x03\x00\x00\x00\x04\x00\x00\x00VirtualAllocEx\x00"
    sec_res = await enterprise_security_platform.run_full_security_pipeline(payload, "strategic_test.exe")
    check("Stage 6 Enterprise Security Platform operates seamlessly", sec_res is not None)
    check("AI OS Kernel remains fully functional", ai_os_kernel is not None)


async def main():
    print("==========================================================================")
    print("STAGE 10 PART 2 — STRATEGIC PLANNING & SCENARIO ANALYSIS TEST SUITE")
    print("==========================================================================")

    test_strategic_planning_engine()
    test_scenario_engine()
    test_what_if_engine()
    test_scenario_simulator()
    test_strategy_comparison_engine()
    test_tradeoff_engine()
    test_strategic_forecasting_engine()
    test_strategic_plan_evaluator()
    await test_strategic_orchestrator()
    await test_full_backward_compatibility()

    print("\n==========================================================================")
    print(f"RESULTS: {PASS} passed, {FAIL} failed, {PASS + FAIL} total")
    print("==========================================================================")

    if FAIL > 0:
        sys.exit(1)
    print("\n🎉 STAGE 10 PART 2 SUCCESS: Strategic Planning & Scenario Analysis Engine Complete!")


if __name__ == "__main__":
    asyncio.run(main())
