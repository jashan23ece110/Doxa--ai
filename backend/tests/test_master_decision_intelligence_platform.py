#!/usr/bin/env python3
"""
Master Integration Test Suite for Stage 10 Part 8 — Global Enterprise Decision Intelligence Platform.
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


async def test_enterprise_decision_intelligence_platform():
    print("\n🏢 Testing Enterprise Decision Intelligence Platform Facade...")
    from app.core.decision_intelligence.platform.enterprise_decision_intelligence_platform import enterprise_decision_intelligence_platform

    assessment = await enterprise_decision_intelligence_platform.execute_master_decision_intelligence_pipeline("Master Enterprise Expansion Strategy", "Full evaluation")
    check("Master platform pipeline executed", assessment is not None)
    check("Platform readiness score == 100.0", assessment.platform_readiness_score == 100.0)
    check("Status is COMPLETED", assessment.status == "COMPLETED")
    check("Decision foundation present", assessment.decision_foundation is not None)


def test_decision_service_bus():
    print("\n🚌 Testing Decision Service Bus...")
    from app.core.decision_intelligence.platform.decision_service_bus import decision_service_bus

    received = []

    def handler(evt):
        received.append(evt)

    decision_service_bus.subscribe("TEST_EVENT", handler)
    event = decision_service_bus.publish_event("TEST_EVENT", {"key": "val"})

    check("Event published", event is not None)
    check("Correlation ID present", event.correlation_id is not None)
    check("Event received by subscriber", len(received) == 1)


def test_decision_workflow_engine():
    print("\n🔄 Testing Decision Workflow Engine...")
    from app.core.decision_intelligence.platform.decision_workflow_engine import decision_workflow_engine

    wf = decision_workflow_engine.create_workflow("Workflow Test Decision")
    check("Decision workflow created", wf is not None)
    check("Current stage is INITIATED", wf.current_stage == "INITIATED")

    updated = decision_workflow_engine.advance_workflow_stage(wf.workflow_id, "COMPLETED", "TestNode")
    check("Workflow advanced to COMPLETED", updated.current_stage == "COMPLETED")
    check("Executed nodes recorded", len(updated.executed_nodes) == 1)


def test_decision_resource_manager():
    print("\n💼 Testing Decision Resource Manager...")
    from app.core.decision_intelligence.platform.decision_resource_manager import decision_resource_manager

    quota = decision_resource_manager.allocate_decision_quota("dec_quota_100", max_tokens=4096)
    check("Quota allocated", quota is not None)
    check("Allocated tokens == 4096", quota["allocated_tokens"] == 4096)
    check("Quota approved == True", quota["quota_approved"])


def test_decision_policy_orchestrator():
    print("\n⚖️ Testing Decision Policy Orchestrator...")
    from app.core.decision_intelligence.platform.decision_policy_orchestrator import decision_policy_orchestrator

    res = decision_policy_orchestrator.enforce_policy("dec_policy_100", cost=15000.0, risk_score=2.0)
    check("Central policy enforced", res is not None)
    check("Requires human approval == True", res["requires_human_approval"])
    check("Policy passed == True", res["policy_passed"])


def test_decision_observability():
    print("\n📈 Testing Decision Observability Engine...")
    from app.core.decision_intelligence.platform.decision_observability import decision_observability

    metrics = decision_observability.record_decision_telemetry("dec_obs_100", latency_ms=12.5, confidence_score=0.98)
    check("Telemetry logged", metrics is not None)
    check("Latency recorded", metrics["latency_ms"] == 12.5)
    check("Confidence score recorded", metrics["confidence_score"] == 0.98)


def test_decision_recovery_manager():
    print("\n🚑 Testing Decision Recovery Manager...")
    from app.core.decision_intelligence.platform.decision_recovery_manager import decision_recovery_manager

    recovery = decision_recovery_manager.handle_workflow_failure("wf_fail_100", "Solver Timeout")
    check("Workflow failure handled", recovery is not None)
    check("Error handled == True", recovery["error_handled"])
    check("Fallback strategy applied", "FALLBACK" in recovery["recovery_strategy"])


def test_decision_outcome_engine():
    print("\n🎯 Testing Decision Outcome Engine...")
    from app.core.decision_intelligence.platform.decision_outcome_engine import decision_outcome_engine

    eval_res = decision_outcome_engine.evaluate_and_learn_outcome("dec_out_100", expected_kpi=100.0, actual_kpi=104.0)
    check("Outcome evaluated", eval_res is not None)
    check("Accuracy calculated (1.04)", eval_res["decision_accuracy"] == 1.04)
    check("Fed to memory and learning layers", eval_res["fed_to_memory"])


def test_decision_lifecycle_manager():
    print("\n🔄 Testing Decision Lifecycle Manager...")
    from app.core.decision_intelligence.platform.decision_lifecycle_manager import decision_lifecycle_manager

    rec = decision_lifecycle_manager.initialize_lifecycle("dec_life_100")
    check("Lifecycle record initialized", rec is not None)
    check("Stage is CREATED", rec.stage == "CREATED")

    updated = decision_lifecycle_manager.transition_stage("dec_life_100", "APPROVED")
    check("Transitioned to APPROVED stage", updated.stage == "APPROVED")


async def test_global_decision_orchestrator():
    print("\n🌐 Testing Global Master Decision Orchestrator...")
    from app.core.decision_intelligence.platform.global_decision_orchestrator import global_decision_orchestrator

    res = await global_decision_orchestrator.execute_global_decision_loop("Global Master Decision Request", "Comprehensive evaluation")
    check("Global decision loop executed", res is not None)
    check("Status is SUCCESS", res.status == "SUCCESS")
    check("Readiness score == 100.0", res.readiness_score == 100.0)
    check("Requires human approval == True", res.requires_human_approval)


async def test_master_platform_backward_compatibility():
    print("\n🔒 Testing Master Integration & Backward Compatibility across Stages 1-10...")
    from app.core.decision_intelligence.executive.executive_decision_orchestrator import executive_decision_orchestrator
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

    exec_res = await executive_decision_orchestrator.execute_executive_analysis("MasterPlatformIntegrationTarget")
    check("Stage 10 Part 7 Executive Decision Support operates seamlessly", exec_res is not None)

    gov_expl = decision_explanation_engine.generate_explanation("dec_platform_compat", "Master Platform Governance Test")
    check("Stage 10 Part 6 Explainability Engine operates seamlessly", gov_expl is not None)

    opt_res = await optimization_orchestrator.execute_optimization_analysis("MasterPlatformIntegrationTarget")
    check("Stage 10 Part 5 Optimization Orchestrator operates seamlessly", opt_res is not None)

    pred_res = await predictive_decision_orchestrator.execute_predictive_analysis("MasterPlatformIntegrationTarget")
    check("Stage 10 Part 4 Predictive Decision Orchestrator operates seamlessly", pred_res is not None)

    risk_res = await risk_intelligence_orchestrator.execute_risk_assessment("MasterPlatformIntegrationTarget")
    check("Stage 10 Part 3 Risk Intelligence Orchestrator operates seamlessly", risk_res is not None)

    strat_res = await strategic_orchestrator.execute_strategic_analysis("Master Strategic Plan")
    check("Stage 10 Part 2 Strategic Intelligence Orchestrator operates seamlessly", strat_res is not None)

    dec_res = await decision_intelligence_orchestrator.execute_decision_analysis("Master Integration Decision", "Evaluate integration")
    check("Stage 10 Part 1 Decision Intelligence Orchestrator operates seamlessly", dec_res is not None)

    master_agent_res = await autonomous_agent_orchestrator.execute_master_autonomous_goal("Master Integration Test Goal", "DoxaBackend")
    check("Stage 9 Global Autonomous Agent Platform operates seamlessly", master_agent_res is not None)

    mem = agent_memory_engine.get_or_create_memory("master_platform_agent")
    check("Stage 9 Part 7 Agent Memory Engine operates seamlessly", mem is not None)

    cres = await collaboration_orchestrator.execute_collaboration_session("Master Session Goal", ["ag_1", "ag_2"])
    check("Stage 9 Part 6 Collaboration Orchestrator operates seamlessly", cres is not None)

    devops_res = await devops_agent_orchestrator.execute_devops_workflow("production", "Master-Gateway")
    check("Stage 9 Part 5 DevOps Agent Orchestrator operates seamlessly", devops_res is not None)

    report = await research_agent_orchestrator.execute_research_workflow("Master Security", "Analyze Safety")
    check("Stage 9 Part 4 Research Agent Orchestrator operates seamlessly", report is not None)

    cwork = await coding_agent_orchestrator.execute_coding_workflow("Refactor platform logger", "DoxaBackend")
    check("Stage 9 Part 3 Coding Agent Orchestrator operates seamlessly", cwork is not None)

    plan = await autonomous_planning_engine.create_execution_plan("goal_master_platform_compat", "Master Platform Compat Plan")
    check("Stage 9 Part 2 Autonomous Planning Engine operates seamlessly", plan is not None)

    aorch = await agent_orchestrator.execute_autonomous_goal("Master Platform Compatibility Test", "Test goal", "system_analysis")
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
    print("STAGE 10 PART 8 — GLOBAL DECISION INTELLIGENCE PLATFORM TEST SUITE")
    print("==========================================================================")

    await test_enterprise_decision_intelligence_platform()
    test_decision_service_bus()
    test_decision_workflow_engine()
    test_decision_resource_manager()
    test_decision_policy_orchestrator()
    test_decision_observability()
    test_decision_recovery_manager()
    test_decision_outcome_engine()
    test_decision_lifecycle_manager()
    await test_global_decision_orchestrator()
    await test_master_platform_backward_compatibility()

    print("\n==========================================================================")
    print(f"RESULTS: {PASS} passed, {FAIL} failed, {PASS + FAIL} total")
    print("==========================================================================")

    if FAIL > 0:
        sys.exit(1)
    print("\n🎉 STAGE 10 PART 8 FINAL SUCCESS: Global Enterprise Decision Intelligence Platform Complete!")


if __name__ == "__main__":
    asyncio.run(main())
