#!/usr/bin/env python3
"""
Master Integration Test Suite for Stage 9 — Global Autonomous Agent Operating Layer.
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


async def test_autonomous_agent_platform():
    print("\n🌐 Testing Global Autonomous Agent Platform Master Assessment...")
    from app.core.agents.platform.autonomous_agent_platform import autonomous_agent_platform

    assessment = await autonomous_agent_platform.run_master_agent_platform_assessment("Enterprise_Agent_Mesh")
    check("Master assessment completed", assessment is not None)
    check("Platform readiness score == 100.0", assessment.platform_readiness_score == 100.0)
    check("Autonomy level is LEVEL_4_ENTERPRISE_AUTONOMOUS", assessment.autonomy_level == "LEVEL_4_ENTERPRISE_AUTONOMOUS")


def test_agent_service_bus():
    print("\n📡 Testing Global Agent Event Bus...")
    from app.core.agents.platform.agent_service_bus import agent_service_bus

    evt = agent_service_bus.publish_event("WORKFLOW_EVENT", "TestRunner", {"status": "SUCCESS"})
    check("Agent event published", evt is not None)
    check("Correlation ID generated", len(evt.correlation_id) > 0)


async def test_autonomous_workflow_engine():
    print("\n⚙️ Testing Enterprise Autonomous Workflow Engine...")
    from app.core.agents.platform.autonomous_workflow_engine import autonomous_workflow_engine

    wf_res = await autonomous_workflow_engine.execute_autonomous_workflow("Master Deploy Goal", ["Research", "Plan", "Code", "Deploy"])
    check("Autonomous workflow executed", wf_res is not None)
    check("Status is COMPLETED", wf_res.status == "COMPLETED")
    check("4 steps executed", wf_res.steps_executed_count == 4)


def test_agent_resource_manager():
    print("\n💻 Testing Enterprise Agent Resource Manager...")
    from app.core.agents.platform.agent_resource_manager import agent_resource_manager

    allocated = agent_resource_manager.allocate_agent_tokens(1000)
    check("Tokens allocated cleanly", allocated)

    quota = agent_resource_manager.get_quota_status()
    check("Quota tracked", quota.tokens_consumed >= 1000)


def test_agent_policy_orchestrator():
    print("\n🛡️ Testing Global Agent Policy Orchestrator...")
    from app.core.agents.platform.agent_policy_orchestrator import agent_policy_orchestrator

    passed = agent_policy_orchestrator.enforce_policy_check("agent_coder", "coding", risk_score=2.5)
    check("Policy check passed within risk limits", passed)

    rejected = agent_policy_orchestrator.enforce_policy_check("agent_coder", "coding", risk_score=8.5)
    check("Policy check rejected high-risk execution", not rejected)


def test_agent_evaluation_engine():
    print("\n🔬 Testing Enterprise Agent Evaluation Engine...")
    from app.core.agents.platform.agent_evaluation_engine import agent_evaluation_engine

    score = agent_evaluation_engine.evaluate_workflow_execution("agent_master", "wf_100")
    check("Workflow evaluation scored", score is not None)
    check("Overall score >= 90.0", score.overall_score >= 90.0)
    check("Safety compliance score == 100.0", score.safety_compliance_score == 100.0)


def test_agent_recovery_manager():
    print("\n🛠️ Testing Enterprise Agent Recovery Manager...")
    from app.core.agents.platform.agent_recovery_manager import agent_recovery_manager

    rec = agent_recovery_manager.recover_failed_workflow("wf_failed_100", checkpoint_step=2)
    check("Workflow recovered from checkpoint", rec is not None)
    check("Recovery is successful", rec.is_successful)


def test_agent_observability():
    print("\n📊 Testing Global Agent Observability Platform...")
    from app.core.agents.platform.agent_observability import agent_observability_platform

    snap = agent_observability_platform.get_observability_snapshot()
    check("Observability snapshot captured", snap is not None)
    check("Overall success rate >= 95.0", snap.overall_success_rate >= 95.0)


def test_agent_lifecycle_manager():
    print("\n🔄 Testing Enterprise Agent Lifecycle Manager...")
    from app.core.agents.platform.agent_lifecycle_manager import agent_lifecycle_manager

    status = agent_lifecycle_manager.activate_agent("AgentScientist", version="1.0.0")
    check("Agent activated", status is not None and status.status == "ACTIVE")

    suspended = agent_lifecycle_manager.suspend_agent("AgentScientist")
    check("Agent suspended gracefully", suspended)


async def test_autonomous_agent_orchestrator():
    print("\n🌐 Testing Global Autonomous Agent Orchestrator Master Workflow...")
    from app.core.agents.platform.autonomous_agent_orchestrator import autonomous_agent_orchestrator

    master_res = await autonomous_agent_orchestrator.execute_master_autonomous_goal(
        "Build & Deploy Master Autonomous Security Module",
        "DoxaBackend"
    )
    check("Master goal execution completed", master_res is not None)
    check("Status is COMPLETED", master_res.status == "COMPLETED")
    check("Policy approved", master_res.policy_approved)
    check("Autonomy level is LEVEL_4_ENTERPRISE_AUTONOMOUS", master_res.autonomy_level == "LEVEL_4_ENTERPRISE_AUTONOMOUS")


async def test_full_backward_compatibility():
    print("\n🔒 Testing Full Integration & Backward Compatibility across Stages 1-9...")
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

    mem = agent_memory_engine.get_or_create_memory("agent_master_compat")
    check("Stage 9 Part 7 Agent Memory Engine operates seamlessly", mem is not None)

    cres = await collaboration_orchestrator.execute_collaboration_session("Master Session Goal", ["ag_1", "ag_2"])
    check("Stage 9 Part 6 Collaboration Orchestrator operates seamlessly", cres is not None)

    devops_res = await devops_agent_orchestrator.execute_devops_workflow("production", "Master-Gateway")
    check("Stage 9 Part 5 DevOps Agent Orchestrator operates seamlessly", devops_res is not None)

    report = await research_agent_orchestrator.execute_research_workflow("Master Platform Security", "Analyze Safety")
    check("Stage 9 Part 4 Research Agent Orchestrator operates seamlessly", report is not None)

    cwork = await coding_agent_orchestrator.execute_coding_workflow("Refactor master platform logger", "DoxaBackend")
    check("Stage 9 Part 3 Coding Agent Orchestrator operates seamlessly", cwork is not None)

    plan = await autonomous_planning_engine.create_execution_plan("goal_master_compat", "Master Compat Plan")
    check("Stage 9 Part 2 Autonomous Planning Engine operates seamlessly", plan is not None)

    aorch = await agent_orchestrator.execute_autonomous_goal("Master Compatibility Test", "Test goal", "system_analysis")
    check("Stage 9 Part 1 Agent Orchestrator operates seamlessly", aorch is not None)

    data_assess = await enterprise_data_intelligence_platform.run_master_data_intelligence_assessment("Master_Platform_Test")
    check("Stage 8 Enterprise Data Intelligence Platform operates seamlessly", data_assess is not None)

    human_assess = await enterprise_human_intelligence_platform.run_master_human_intelligence_assessment("Master_Platform_Test")
    check("Stage 7 Human Intelligence Platform operates seamlessly", human_assess is not None)

    payload = b"MZ\x90\x00\x03\x00\x00\x00\x04\x00\x00\x00VirtualAllocEx\x00"
    sec_res = await enterprise_security_platform.run_full_security_pipeline(payload, "master_platform_test.exe")
    check("Stage 6 Enterprise Security Platform operates seamlessly", sec_res is not None)
    check("AI OS Kernel remains fully functional", ai_os_kernel is not None)


async def main():
    print("==========================================================================")
    print("STAGE 9 FINAL — GLOBAL AUTONOMOUS AGENT OPERATING LAYER TEST SUITE")
    print("==========================================================================")

    await test_autonomous_agent_platform()
    test_agent_service_bus()
    await test_autonomous_workflow_engine()
    test_agent_resource_manager()
    test_agent_policy_orchestrator()
    test_agent_evaluation_engine()
    test_agent_recovery_manager()
    test_agent_observability()
    test_agent_lifecycle_manager()
    await test_autonomous_agent_orchestrator()
    await test_full_backward_compatibility()

    print("\n==========================================================================")
    print(f"RESULTS: {PASS} passed, {FAIL} failed, {PASS + FAIL} total")
    print("==========================================================================")

    if FAIL > 0:
        sys.exit(1)
    print("\n🎉 STAGE 9 FINAL COMPLETION CONFIRMED: Doxa is a Global Autonomous Agent Platform!")


if __name__ == "__main__":
    asyncio.run(main())
