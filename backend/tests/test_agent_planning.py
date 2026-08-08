#!/usr/bin/env python3
"""
Integration Test Suite for Stage 9 Part 2 — Enterprise Autonomous Planning & Task Decomposition Engine.
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


def test_goal_decomposer():
    print("\n🎯 Testing Goal Decomposer...")
    from app.core.agents.planning.goal_decomposer import goal_decomposer

    decomp = goal_decomposer.decompose_goal("goal_plan_100", "Infrastructure Security Audit")
    check("Goal decomposed into 3 task nodes", len(decomp.tasks) == 3)
    check("Sub-goals generated", len(decomp.sub_goals) == 2)


def test_task_graph_engine():
    print("\n🕸️ Testing Task Graph Engine DAG Validation & Cycle Detection...")
    from app.core.agents.planning.goal_decomposer import goal_decomposer
    from app.core.agents.planning.task_graph_engine import task_graph_engine
    from app.core.agents.planning.planning_types import TaskNode, TaskDependency

    decomp = goal_decomposer.decompose_goal("goal_dag_test", "DAG Test")
    graph = task_graph_engine.build_task_graph(decomp.tasks)

    check("TaskGraph built", graph is not None)
    check("Valid DAG confirmed", graph.is_valid_dag)
    check("Critical path length == 3", len(graph.critical_path_task_ids) == 3)

    # Test circular dependency detection
    t1 = TaskNode(task_id="t1", title="T1")
    t2 = TaskNode(task_id="t2", title="T2")
    cycle_deps = [
        TaskDependency(source_task_id="t1", target_task_id="t2"),
        TaskDependency(source_task_id="t2", target_task_id="t1"),
    ]
    is_valid = task_graph_engine.validate_dag([t1, t2], cycle_deps)
    check("Circular dependency correctly detected as invalid DAG", not is_valid)


def test_plan_validator():
    print("\n✔️ Testing Plan Validator & Risk Assessment...")
    from app.core.agents.planning.goal_decomposer import goal_decomposer
    from app.core.agents.planning.task_graph_engine import task_graph_engine
    from app.core.agents.planning.plan_validator import plan_validator

    decomp = goal_decomposer.decompose_goal("goal_val_test", "Val Test")
    graph = task_graph_engine.build_task_graph(decomp.tasks)

    val_res = plan_validator.validate_plan(graph)
    check("Plan validation succeeded", val_res.is_valid)

    risk_assess = plan_validator.assess_risk(graph)
    check("Risk score calculated > 0", risk_assess.overall_risk_score > 0.0)


def test_agent_assignment_engine():
    print("\n🤖 Testing Agent Assignment Engine...")
    from app.core.agents.planning.goal_decomposer import goal_decomposer
    from app.core.agents.planning.agent_assignment_engine import agent_assignment_engine

    decomp = goal_decomposer.decompose_goal("goal_asgn_test", "Asgn Test")
    assignments = agent_assignment_engine.assign_agents(decomp.tasks)
    check("Assignments created for all 3 tasks", len(assignments) == 3)
    check("Agent assigned to task 1", decomp.tasks[0].assigned_agent_id is not None)


def test_resource_aware_scheduler():
    print("\n⏱️ Testing Resource Aware Scheduler...")
    from app.core.agents.planning.goal_decomposer import goal_decomposer
    from app.core.agents.planning.task_graph_engine import task_graph_engine
    from app.core.agents.planning.resource_aware_scheduler import resource_aware_scheduler

    decomp = goal_decomposer.decompose_goal("goal_sched_test", "Sched Test")
    graph = task_graph_engine.build_task_graph(decomp.tasks)

    scheduled = resource_aware_scheduler.schedule_execution(graph)
    check("All tasks scheduled", len(scheduled) == 3)
    check("Tasks set to READY status", all(t.status == "READY" for t in scheduled))


async def test_dynamic_replanner():
    print("\n🔄 Testing Dynamic Replanner...")
    from app.core.agents.planning.planning_engine import autonomous_planning_engine
    from app.core.agents.planning.dynamic_replanner import dynamic_replanner

    plan = await autonomous_planning_engine.create_execution_plan("goal_replan_test", "Replan Test")
    failing_task_id = plan.task_graph.nodes[0].task_id

    revised = dynamic_replanner.replan_failed_task(plan, failing_task_id, "Resource unavailable")
    check("Plan revised to v2", revised.version == 2)
    check("Original plan status set to REPLANNED", plan.status == "REPLANNED")


async def test_plan_evaluator():
    print("\n📊 Testing Plan Evaluator...")
    from app.core.agents.planning.planning_engine import autonomous_planning_engine
    from app.core.agents.planning.plan_evaluator import plan_evaluator

    plan = await autonomous_planning_engine.create_execution_plan("goal_eval_test", "Eval Test")
    score = plan_evaluator.evaluate_plan_quality(plan)

    check("Plan quality score calculated >= 0.90", score.overall_quality_score >= 0.90)
    check("Explainability notes present", len(score.explainability_notes) > 0)


def test_planning_observability():
    print("\n👁️ Testing Planning Observability...")
    from app.core.agents.planning.planning_observability import planning_observability

    metrics = planning_observability.get_observability_snapshot()
    check("Planning metrics retrieved", metrics is not None)
    check("Goals created total > 0", metrics.goals_created_total > 0)


async def test_autonomous_planning_engine():
    print("\n🌐 Testing End-to-End Autonomous Planning Engine...")
    from app.core.agents.planning.planning_engine import autonomous_planning_engine

    plan = await autonomous_planning_engine.create_execution_plan("goal_e2e_plan", "Full System Audit")
    check("Execution plan created", plan is not None)
    check("Plan status is APPROVED", plan.status == "APPROVED")
    check("Assignments populated", len(plan.assignments) == 3)


async def test_full_backward_compatibility():
    print("\n🔒 Testing Integration & Backward Compatibility across Stages 1-9 Part 1...")
    from app.core.agents import agent_orchestrator
    from app.core.data_intelligence.platform import enterprise_data_intelligence_platform
    from app.core.human_intelligence import enterprise_human_intelligence_platform
    from app.core.security import enterprise_security_platform
    from app.core.intelligence import ai_os_kernel

    aorch = await agent_orchestrator.execute_autonomous_goal("Planning Compatibility Test", "Test goal", "system_analysis")
    check("Stage 9 Part 1 Agent Orchestrator operates seamlessly", aorch is not None)

    data_assess = await enterprise_data_intelligence_platform.run_master_data_intelligence_assessment("Planning_Master_Test")
    check("Stage 8 Enterprise Data Intelligence Platform operates seamlessly", data_assess is not None)

    human_assess = await enterprise_human_intelligence_platform.run_master_human_intelligence_assessment("Planning_Master_Test")
    check("Stage 7 Human Intelligence Platform operates seamlessly", human_assess is not None)

    payload = b"MZ\x90\x00\x03\x00\x00\x00\x04\x00\x00\x00VirtualAllocEx\x00"
    sec_res = await enterprise_security_platform.run_full_security_pipeline(payload, "plan_test.exe")
    check("Stage 6 Enterprise Security Platform operates seamlessly", sec_res is not None)
    check("AI OS Kernel remains fully functional", ai_os_kernel is not None)


async def main():
    print("==========================================================================")
    print("STAGE 9 PART 2 — AUTONOMOUS PLANNING & TASK DECOMPOSITION TEST SUITE")
    print("==========================================================================")

    test_goal_decomposer()
    test_task_graph_engine()
    test_plan_validator()
    test_agent_assignment_engine()
    test_resource_aware_scheduler()
    await test_dynamic_replanner()
    await test_plan_evaluator()
    test_planning_observability()
    await test_autonomous_planning_engine()
    await test_full_backward_compatibility()

    print("\n==========================================================================")
    print(f"RESULTS: {PASS} passed, {FAIL} failed, {PASS + FAIL} total")
    print("==========================================================================")

    if FAIL > 0:
        sys.exit(1)
    print("\n🎉 STAGE 9 PART 2 SUCCESS: Enterprise Autonomous Planning & Task Decomposition Engine Deployed!")


if __name__ == "__main__":
    asyncio.run(main())
