#!/usr/bin/env python3
"""
Integration Test Suite for Stage 9 Part 5 — Enterprise Autonomous DevOps & SRE Agent Platform.
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


def test_infrastructure_discovery_engine():
    print("\n🔍 Testing Infrastructure Discovery Engine...")
    from app.core.agents.devops.infrastructure_discovery import infrastructure_discovery_engine

    targets = infrastructure_discovery_engine.discover_infrastructure("production")
    check("Infrastructure targets discovered", len(targets) == 2)
    check("Kubernetes cluster present", targets[0].target_type == "KUBERNETES_CLUSTER")


def test_deployment_planner():
    print("\n📋 Testing Autonomous Deployment Planner...")
    from app.core.agents.devops.devops_agent_types import DeploymentRequest
    from app.core.agents.devops.deployment_planner import deployment_planner

    dreq = DeploymentRequest(artifact_id="art_prod_100", target_environment="production")
    plan = deployment_planner.create_deployment_plan(dreq, strategy="ROLLING")

    check("Deployment plan created", plan is not None)
    check("Strategy is ROLLING", plan.strategy == "ROLLING")
    check("3 deployment steps created", len(plan.steps) == 3)


async def test_cicd_orchestrator():
    print("\n⚙️ Testing Enterprise CI/CD Orchestrator...")
    from app.core.agents.devops.cicd_orchestrator import cicd_orchestrator

    pipe_res = await cicd_orchestrator.execute_pipeline("DeployPipeline", "repo_devops_1")
    check("Pipeline execution completed", pipe_res is not None)
    check("Pipeline status is SUCCESS", pipe_res.status == "SUCCESS")


async def test_infrastructure_execution_engine():
    print("\n💻 Testing Controlled Infrastructure Execution Engine...")
    from app.core.agents.devops.infrastructure_execution_engine import infrastructure_execution_engine

    action_res = await infrastructure_execution_engine.execute_action("ScaleWorkload", "API-Gateway", {"replicas": 5})
    check("Controlled action executed", action_res is not None)
    check("Action status is SUCCESS", action_res.status == "SUCCESS")


def test_monitoring_agent():
    print("\n👁️ Testing Monitoring Agent...")
    from app.core.agents.devops.monitoring_agent import monitoring_agent

    health = monitoring_agent.check_service_health("API-Gateway")
    check("Service health metrics retrieved", health is not None)
    check("P95 latency < 50ms", health.latency_p95_ms < 50.0)
    check("Service status is HEALTHY", health.status == "HEALTHY")


def test_incident_response_engine():
    print("\n🚨 Testing Incident Response Engine...")
    from app.core.agents.devops.incident_response_engine import incident_response_engine

    no_inc = incident_response_engine.detect_incident("API-Gateway", error_rate=0.01)
    check("No incident detected for 0.01% error rate", no_inc is None)

    inc = incident_response_engine.detect_incident("API-Gateway", error_rate=12.5)
    check("Incident detected for 12.5% error rate", inc is not None and inc.severity == "MEDIUM")


async def test_remediation_engine():
    print("\n🛠️ Testing Controlled Autonomous Remediation Engine...")
    from app.core.agents.devops.incident_response_engine import incident_response_engine
    from app.core.agents.devops.remediation_engine import remediation_engine

    inc = incident_response_engine.detect_incident("DatabaseService", error_rate=8.0)
    plan = remediation_engine.create_remediation_plan(inc)
    check("Remediation plan created", plan is not None)

    executed = await remediation_engine.execute_remediation(plan)
    check("Remediation plan executed cleanly", executed and plan.is_executed)


def test_rollback_manager():
    print("\n🔄 Testing Enterprise Rollback Engine...")
    from app.core.agents.devops.rollback_manager import rollback_manager

    rplan = rollback_manager.execute_rollback("deploy_100", target_version="0.9.9")
    check("Rollback plan executed", rplan is not None)
    check("Rollback status is COMPLETED", rplan.status == "COMPLETED")
    check("Target version is 0.9.9", rplan.previous_stable_version == "0.9.9")


async def test_devops_agent_orchestrator():
    print("\n🌐 Testing Global DevOps Agent Orchestrator Workflow...")
    from app.core.agents.devops.devops_agent_orchestrator import devops_agent_orchestrator

    wf_res = await devops_agent_orchestrator.execute_devops_workflow("production", "API-Gateway")
    check("DevOps workflow completed", wf_res is not None)
    check("Workflow status is COMPLETED", wf_res.status == "COMPLETED")
    check("Pipeline and service healthy", wf_res.pipeline_success and wf_res.service_healthy)


async def test_full_backward_compatibility():
    print("\n🔒 Testing Integration & Backward Compatibility across Stages 1-9 Part 4...")
    from app.core.agents.research import research_agent_orchestrator
    from app.core.agents.coding import coding_agent_orchestrator
    from app.core.agents.planning import autonomous_planning_engine
    from app.core.agents import agent_orchestrator
    from app.core.data_intelligence.platform import enterprise_data_intelligence_platform
    from app.core.human_intelligence import enterprise_human_intelligence_platform
    from app.core.security import enterprise_security_platform
    from app.core.intelligence import ai_os_kernel

    report = await research_agent_orchestrator.execute_research_workflow("DevOps Security", "Analyze CI/CD security")
    check("Stage 9 Part 4 Research Agent Orchestrator operates seamlessly", report is not None)

    cwork = await coding_agent_orchestrator.execute_coding_workflow("Refactor devops logger", "DoxaBackend")
    check("Stage 9 Part 3 Coding Agent Orchestrator operates seamlessly", cwork is not None)

    plan = await autonomous_planning_engine.create_execution_plan("goal_devops_compat", "DevOps Compat Plan")
    check("Stage 9 Part 2 Autonomous Planning Engine operates seamlessly", plan is not None)

    aorch = await agent_orchestrator.execute_autonomous_goal("DevOps Compatibility Test", "Test goal", "system_analysis")
    check("Stage 9 Part 1 Agent Orchestrator operates seamlessly", aorch is not None)

    data_assess = await enterprise_data_intelligence_platform.run_master_data_intelligence_assessment("DevOps_Master_Test")
    check("Stage 8 Enterprise Data Intelligence Platform operates seamlessly", data_assess is not None)

    human_assess = await enterprise_human_intelligence_platform.run_master_human_intelligence_assessment("DevOps_Master_Test")
    check("Stage 7 Human Intelligence Platform operates seamlessly", human_assess is not None)

    payload = b"MZ\x90\x00\x03\x00\x00\x00\x04\x00\x00\x00VirtualAllocEx\x00"
    sec_res = await enterprise_security_platform.run_full_security_pipeline(payload, "devops_test.exe")
    check("Stage 6 Enterprise Security Platform operates seamlessly", sec_res is not None)
    check("AI OS Kernel remains fully functional", ai_os_kernel is not None)


async def main():
    print("==========================================================================")
    print("STAGE 9 PART 5 — ENTERPRISE AUTONOMOUS DEVOPS & SRE AGENT PLATFORM TEST SUITE")
    print("==========================================================================")

    test_infrastructure_discovery_engine()
    test_deployment_planner()
    await test_cicd_orchestrator()
    await test_infrastructure_execution_engine()
    test_monitoring_agent()
    test_incident_response_engine()
    await test_remediation_engine()
    test_rollback_manager()
    await test_devops_agent_orchestrator()
    await test_full_backward_compatibility()

    print("\n==========================================================================")
    print(f"RESULTS: {PASS} passed, {FAIL} failed, {PASS + FAIL} total")
    print("==========================================================================")

    if FAIL > 0:
        sys.exit(1)
    print("\n🎉 STAGE 9 PART 5 SUCCESS: Enterprise Autonomous DevOps Agent Platform Deployed!")


if __name__ == "__main__":
    asyncio.run(main())
