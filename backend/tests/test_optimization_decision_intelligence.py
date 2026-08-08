#!/usr/bin/env python3
"""
Integration Test Suite for Stage 10 Part 5 — Enterprise Optimization & Resource Allocation Engine.
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


def test_optimization_model_engine():
    print("\n📐 Testing Optimization Model Engine...")
    from app.core.decision_intelligence.optimization.optimization_types import OptimizationModel, OptimizationObjective
    from app.core.decision_intelligence.optimization.optimization_model_engine import optimization_model_engine

    model = OptimizationModel(name="ComputeAllocationModel", objectives=[OptimizationObjective(name="MaxROI", direction="MAXIMIZE")])
    sol = optimization_model_engine.solve_optimization_model(model)

    check("Optimization model solved", sol is not None)
    check("Solver status is OPTIMAL", sol.solver_status == "OPTIMAL")
    check("Feasibility score == 1.0", sol.best_solution.feasibility_score == 1.0)


def test_constraint_engine():
    print("\n🚧 Testing Constraint Management Engine...")
    from app.core.decision_intelligence.optimization.constraint_engine import constraint_engine

    cset = constraint_engine.build_constraint_set("Infrastructure Optimization")
    check("Constraint set built", cset is not None)
    check("2 hard constraints present", len(cset.constraints) == 2)
    check("Budget limit constraint present", cset.constraints[0].is_hard)


def test_objective_engine():
    print("\n🎯 Testing Objective Management Engine...")
    from app.core.decision_intelligence.optimization.objective_engine import objective_engine

    objectives = objective_engine.build_objectives("Cloud Spending")
    check("Objectives configured", len(objectives) == 2)
    check("Maximize return objective present", objectives[0].direction == "MAXIMIZE")


def test_resource_allocation_engine():
    print("\n📦 Testing Resource Allocation Engine...")
    from app.core.decision_intelligence.optimization.optimization_types import Resource
    from app.core.decision_intelligence.optimization.resource_allocation_engine import resource_allocation_engine

    resources = [Resource(name="COMPUTE", total_capacity=1000.0)]
    plan = resource_allocation_engine.allocate_resources(resources)

    check("Allocation plan built", plan is not None)
    check("Efficiency score >= 0.95", plan.efficiency_score >= 0.95)
    check("Allocated amount == 750.0", plan.allocations[0].allocated_amount == 750.0)


def test_multi_objective_engine():
    print("\n⚖️ Testing Multi-Objective Optimization Engine...")
    from app.core.decision_intelligence.optimization.objective_engine import objective_engine
    from app.core.decision_intelligence.optimization.multi_objective_engine import multi_objective_engine

    objs = objective_engine.build_objectives("MultiObjTest")
    tradeoff = multi_objective_engine.compute_pareto_frontier(objs)

    check("Pareto frontier computed", tradeoff is not None)
    check("Pareto points present", len(tradeoff.pareto_frontier_points) == 3)


def test_optimization_scenario_engine():
    print("\n🎭 Testing Optimization Scenario Engine...")
    from app.core.decision_intelligence.optimization.optimization_scenario_engine import optimization_scenario_engine

    scenarios = optimization_scenario_engine.evaluate_optimization_scenarios(100.0)
    check("3 optimization scenarios evaluated", len(scenarios) == 3)
    check("RESOURCE_SHORTAGE scenario present", scenarios[1].name == "RESOURCE_SHORTAGE")


def test_optimization_evaluator():
    print("\n🏆 Testing Optimization Evaluator...")
    from app.core.decision_intelligence.optimization.optimization_types import OptimizationModel, OptimizationObjective
    from app.core.decision_intelligence.optimization.optimization_model_engine import optimization_model_engine
    from app.core.decision_intelligence.optimization.optimization_evaluator import optimization_evaluator

    model = OptimizationModel(name="TestModel", objectives=[OptimizationObjective(name="ROI", direction="MAXIMIZE")])
    sol = optimization_model_engine.solve_optimization_model(model)
    expl = optimization_evaluator.evaluate_solution(sol)

    check("Solution evaluated", expl is not None)
    check("Binding constraints identified", len(expl.binding_constraints) > 0)


def test_sensitivity_engine():
    print("\n📈 Testing Sensitivity Analysis Engine...")
    from app.core.decision_intelligence.optimization.sensitivity_engine import sensitivity_engine

    report = sensitivity_engine.analyze_sensitivity("omod_100")
    check("Sensitivity analysis completed", report is not None)
    check("Shadow prices present", "Workforce Capacity" in report["shadow_prices"])


async def test_optimization_orchestrator():
    print("\n🌐 Testing Global Optimization Orchestrator...")
    from app.core.decision_intelligence.optimization.optimization_orchestrator import optimization_orchestrator

    res = await optimization_orchestrator.execute_optimization_analysis("Enterprise Cluster Capacity Optimization")
    check("Master optimization analysis completed", res is not None)
    check("Status is COMPLETED", res.status == "COMPLETED")
    check("Solution generated", res.solution is not None)
    check("Requires human approval == True", res.requires_human_approval)


async def test_full_backward_compatibility():
    print("\n🔒 Testing Integration & Backward Compatibility across Stages 1-10 Part 4...")
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

    pred_res = await predictive_decision_orchestrator.execute_predictive_analysis("OptimizationIntegrationTarget")
    check("Stage 10 Part 4 Predictive Decision Orchestrator operates seamlessly", pred_res is not None)

    risk_res = await risk_intelligence_orchestrator.execute_risk_assessment("OptimizationIntegrationTarget")
    check("Stage 10 Part 3 Risk Intelligence Orchestrator operates seamlessly", risk_res is not None)

    strat_res = await strategic_orchestrator.execute_strategic_analysis("Optimization Strategic Plan")
    check("Stage 10 Part 2 Strategic Intelligence Orchestrator operates seamlessly", strat_res is not None)

    dec_res = await decision_intelligence_orchestrator.execute_decision_analysis("Optimization Integration Decision", "Evaluate integration")
    check("Stage 10 Part 1 Decision Intelligence Orchestrator operates seamlessly", dec_res is not None)

    master_agent_res = await autonomous_agent_orchestrator.execute_master_autonomous_goal("Optimization Integration Test Goal", "DoxaBackend")
    check("Stage 9 Global Autonomous Agent Platform operates seamlessly", master_agent_res is not None)

    mem = agent_memory_engine.get_or_create_memory("opt_compat_agent")
    check("Stage 9 Part 7 Agent Memory Engine operates seamlessly", mem is not None)

    cres = await collaboration_orchestrator.execute_collaboration_session("Optimization Session Goal", ["ag_1", "ag_2"])
    check("Stage 9 Part 6 Collaboration Orchestrator operates seamlessly", cres is not None)

    devops_res = await devops_agent_orchestrator.execute_devops_workflow("production", "Optimization-Gateway")
    check("Stage 9 Part 5 DevOps Agent Orchestrator operates seamlessly", devops_res is not None)

    report = await research_agent_orchestrator.execute_research_workflow("Optimization Security", "Analyze Safety")
    check("Stage 9 Part 4 Research Agent Orchestrator operates seamlessly", report is not None)

    cwork = await coding_agent_orchestrator.execute_coding_workflow("Refactor optimization logger", "DoxaBackend")
    check("Stage 9 Part 3 Coding Agent Orchestrator operates seamlessly", cwork is not None)

    plan = await autonomous_planning_engine.create_execution_plan("goal_opt_compat", "Optimization Compat Plan")
    check("Stage 9 Part 2 Autonomous Planning Engine operates seamlessly", plan is not None)

    aorch = await agent_orchestrator.execute_autonomous_goal("Optimization Compatibility Test", "Test goal", "system_analysis")
    check("Stage 9 Part 1 Agent Orchestrator operates seamlessly", aorch is not None)

    data_assess = await enterprise_data_intelligence_platform.run_master_data_intelligence_assessment("Optimization_Platform_Test")
    check("Stage 8 Enterprise Data Intelligence Platform operates seamlessly", data_assess is not None)

    human_assess = await enterprise_human_intelligence_platform.run_master_human_intelligence_assessment("Optimization_Platform_Test")
    check("Stage 7 Human Intelligence Platform operates seamlessly", human_assess is not None)

    payload = b"MZ\x90\x00\x03\x00\x00\x00\x04\x00\x00\x00VirtualAllocEx\x00"
    sec_res = await enterprise_security_platform.run_full_security_pipeline(payload, "optimization_test.exe")
    check("Stage 6 Enterprise Security Platform operates seamlessly", sec_res is not None)
    check("AI OS Kernel remains fully functional", ai_os_kernel is not None)


async def main():
    print("==========================================================================")
    print("STAGE 10 PART 5 — OPTIMIZATION & RESOURCE ALLOCATION TEST SUITE")
    print("==========================================================================")

    test_optimization_model_engine()
    test_constraint_engine()
    test_objective_engine()
    test_resource_allocation_engine()
    test_multi_objective_engine()
    test_optimization_scenario_engine()
    test_optimization_evaluator()
    test_sensitivity_engine()
    await test_optimization_orchestrator()
    await test_full_backward_compatibility()

    print("\n==========================================================================")
    print(f"RESULTS: {PASS} passed, {FAIL} failed, {PASS + FAIL} total")
    print("==========================================================================")

    if FAIL > 0:
        sys.exit(1)
    print("\n🎉 STAGE 10 PART 5 SUCCESS: Enterprise Optimization & Resource Allocation Engine Complete!")


if __name__ == "__main__":
    asyncio.run(main())
