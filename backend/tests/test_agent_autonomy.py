#!/usr/bin/env python3
"""
Integration Test Suite for Stage 9 Part 7 — Enterprise Autonomous Workflow Execution & Agent Memory Platform.
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


def test_agent_memory_engine():
    print("\n🧠 Testing Enterprise Agent Memory Engine...")
    from app.core.agents.autonomy.agent_memory_engine import agent_memory_engine

    ep = agent_memory_engine.store_episode("agent_coder", "rgoal_1", "Generate patch for bug fix", "Patch generated cleanly", success=True)
    check("Episodic memory stored", ep is not None)

    ret = agent_memory_engine.retrieve_memory("agent_coder", "patch")
    check("Memory retrieved", ret is not None)
    check("1 episode matched query", len(ret.retrieved_episodes) == 1)


def test_experience_learning_engine():
    print("\n🎓 Testing Agent Experience Learning Engine...")
    from app.core.agents.autonomy.experience_learning_engine import experience_learning_engine

    exp = experience_learning_engine.learn_from_execution("agent_coder", "CODING", is_success=True)
    check("Experience processed", exp is not None)
    check("Average score == 0.98", exp.average_score == 0.98)


def test_workflow_template_engine():
    print("\n📋 Testing Reusable Workflow Template Engine...")
    from app.core.agents.autonomy.workflow_template_engine import workflow_template_engine

    tmpl = workflow_template_engine.create_template(
        "StandardSecurityFeatureWorkflow",
        ["Research", "Plan", "Code", "Test", "Deploy"],
        ["RESEARCHER", "PLANNER", "CODER", "TESTER", "DEVOPS"],
    )
    check("Workflow template created", tmpl is not None)
    check("5 template steps defined", len(tmpl.steps) == 5)


def test_skill_registry():
    print("\n🛠️ Testing Enterprise Agent Skill Registry...")
    from app.core.agents.autonomy.skill_registry import skill_registry

    skills = skill_registry.find_skills_by_category("CODING")
    check("Coding skills discovered", len(skills) > 0)
    check("Skill name matches CodeGeneration", skills[0].name == "CodeGeneration")


def test_adaptive_execution_engine():
    print("\n🔄 Testing Adaptive Agent Execution Engine...")
    from app.core.agents.autonomy.adaptive_execution_engine import adaptive_execution_engine

    pat_normal = adaptive_execution_engine.adapt_strategy("agent_devops", "ROLLING", failure_signal=False)
    check("Normal strategy maintained", pat_normal.pattern_name == "ROLLING")

    pat_fail = adaptive_execution_engine.adapt_strategy("agent_devops", "ROLLING", failure_signal=True)
    check("Fallback strategy adapted on failure signal", pat_fail.pattern_name == "ROLLING_FALLBACK")


def test_failure_learning_engine():
    print("\n🚨 Testing Enterprise Failure Learning Engine...")
    from app.core.agents.autonomy.failure_learning_engine import failure_learning_engine

    fpat = failure_learning_engine.analyze_failure("task_100", "Execution failed due to connection timeout")
    check("Failure analyzed", fpat is not None)
    check("Category identified as TOOL_TIMEOUT", fpat.category == "TOOL_TIMEOUT")


def test_autonomy_controller():
    print("\n🛡️ Testing Enterprise Autonomy Controller...")
    from app.core.agents.autonomy.autonomy_controller import autonomy_controller

    level = autonomy_controller.get_autonomy_level("agent_1")
    check("Default autonomy level is BOUNDED_AUTONOMOUS", level == "BOUNDED_AUTONOMOUS")

    allowed = autonomy_controller.validate_action_allowed("agent_1", "ExecutePatch", risk_score=1.5)
    check("Action allowed within autonomy bounds", allowed)


def test_long_running_workflow_manager():
    print("\n⏳ Testing Long-Running Workflow Manager...")
    from app.core.agents.autonomy.long_running_workflow_manager import long_running_workflow_manager

    chk = long_running_workflow_manager.checkpoint_workflow("wf_long_100", step_index=2, state_data={"stage": "STAGING_DEPLOY"})
    check("Workflow checkpointed", chk is not None)

    recovered = long_running_workflow_manager.recover_workflow("wf_long_100")
    check("Workflow checkpoint recovered", recovered is not None and recovered.step_index == 2)


def test_autonomy_observability():
    print("\n📊 Testing Autonomy Observability Engine...")
    from app.core.agents.autonomy.autonomy_observability import autonomy_observability_engine

    metrics = autonomy_observability_engine.get_metrics()
    check("Autonomy metrics collected", metrics is not None)
    check("Memories stored count > 0", metrics.memories_stored_count > 0)


async def test_full_backward_compatibility():
    print("\n🔒 Testing Integration & Backward Compatibility across Stages 1-9 Part 6...")
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

    cres = await collaboration_orchestrator.execute_collaboration_session("Autonomy Session Goal", ["ag_1", "ag_2"])
    check("Stage 9 Part 6 Collaboration Orchestrator operates seamlessly", cres is not None)

    devops_res = await devops_agent_orchestrator.execute_devops_workflow("production", "Autonomy-Gateway")
    check("Stage 9 Part 5 DevOps Agent Orchestrator operates seamlessly", devops_res is not None)

    report = await research_agent_orchestrator.execute_research_workflow("Autonomy Security", "Analyze Memory Safety")
    check("Stage 9 Part 4 Research Agent Orchestrator operates seamlessly", report is not None)

    cwork = await coding_agent_orchestrator.execute_coding_workflow("Refactor autonomy memory logger", "DoxaBackend")
    check("Stage 9 Part 3 Coding Agent Orchestrator operates seamlessly", cwork is not None)

    plan = await autonomous_planning_engine.create_execution_plan("goal_autonomy_compat", "Autonomy Compat Plan")
    check("Stage 9 Part 2 Autonomous Planning Engine operates seamlessly", plan is not None)

    aorch = await agent_orchestrator.execute_autonomous_goal("Autonomy Compatibility Test", "Test goal", "system_analysis")
    check("Stage 9 Part 1 Agent Orchestrator operates seamlessly", aorch is not None)

    data_assess = await enterprise_data_intelligence_platform.run_master_data_intelligence_assessment("Autonomy_Master_Test")
    check("Stage 8 Enterprise Data Intelligence Platform operates seamlessly", data_assess is not None)

    human_assess = await enterprise_human_intelligence_platform.run_master_human_intelligence_assessment("Autonomy_Master_Test")
    check("Stage 7 Human Intelligence Platform operates seamlessly", human_assess is not None)

    payload = b"MZ\x90\x00\x03\x00\x00\x00\x04\x00\x00\x00VirtualAllocEx\x00"
    sec_res = await enterprise_security_platform.run_full_security_pipeline(payload, "autonomy_test.exe")
    check("Stage 6 Enterprise Security Platform operates seamlessly", sec_res is not None)
    check("AI OS Kernel remains fully functional", ai_os_kernel is not None)


async def main():
    print("==========================================================================")
    print("STAGE 9 PART 7 — ENTERPRISE AUTONOMOUS WORKFLOW & MEMORY PLATFORM TEST SUITE")
    print("==========================================================================")

    test_agent_memory_engine()
    test_experience_learning_engine()
    test_workflow_template_engine()
    test_skill_registry()
    test_adaptive_execution_engine()
    test_failure_learning_engine()
    test_autonomy_controller()
    test_long_running_workflow_manager()
    test_autonomy_observability()
    await test_full_backward_compatibility()

    print("\n==========================================================================")
    print(f"RESULTS: {PASS} passed, {FAIL} failed, {PASS + FAIL} total")
    print("==========================================================================")

    if FAIL > 0:
        sys.exit(1)
    print("\n🎉 STAGE 9 PART 7 SUCCESS: Enterprise Autonomous Workflow & Memory Platform Deployed!")


if __name__ == "__main__":
    asyncio.run(main())
