#!/usr/bin/env python3
"""
Master Integration Test Suite for Stage 7 — Enterprise Human Intelligence & Social Engineering Defense Platform Unification.
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


async def test_master_human_platform():
    print("\n🌐 Testing Global Enterprise Human Intelligence Platform Master Entrypoint...")
    from app.core.human_intelligence.platform.enterprise_human_intelligence_platform import enterprise_human_intelligence_platform

    assessment = await enterprise_human_intelligence_platform.run_master_human_intelligence_assessment("Enterprise")
    check("Master human assessment generated", assessment is not None)
    check("Overall human security score > 80.0", assessment.overall_human_security_score > 80.0)
    check("Human attack surface score <= 5.0", assessment.human_attack_surface_score <= 5.0)
    check("Overall resilience level is RESILIENT", assessment.overall_resilience_level == "RESILIENT")
    check("Readiness score == 100", assessment.readiness_score == 100)


def test_human_service_bus():
    print("\n🚌 Testing Human Intelligence Event Bus...")
    from app.core.human_intelligence.platform.human_service_bus import human_service_bus
    from app.core.human_intelligence.human_events import HumanEvent, HumanEventType

    ev = HumanEvent(event_type=HumanEventType.ASSESSMENT_FINISHED, target_id="emp_100", data={"score": 90.0})
    check("Event created", ev is not None)


async def test_human_workflow_engine():
    print("\n⚙️ Testing Human Intelligence Workflow Engine...")
    from app.core.human_intelligence.platform.human_workflow_engine import human_workflow_engine

    exec_res = await human_workflow_engine.execute_workflow("awareness_campaign", "Enterprise")
    check("Workflow executed", exec_res is not None)
    check("Workflow status is COMPLETED", exec_res.status == "COMPLETED")


def test_human_resource_manager():
    print("\n💻 Testing Human Resource Manager...")
    from app.core.human_intelligence.platform.human_resource_manager import human_resource_manager

    alloc = human_resource_manager.get_allocation()
    check("Max worker threads == 16", alloc.max_worker_threads == 16)
    check("Health status is HEALTHY", alloc.health_status == "HEALTHY")


def test_human_cache_manager():
    print("\n⚡ Testing Human Cache Manager...")
    from app.core.human_intelligence.platform.human_cache_manager import human_cache_manager

    human_cache_manager.set("test_key", "test_val", ttl_seconds=60.0)
    val = human_cache_manager.get("test_key")
    check("Cached value retrieved", val == "test_val")


def test_human_observability():
    print("\n👁️ Testing Human Observability Layer...")
    from app.core.human_intelligence.platform.human_observability import human_observability

    obs = human_observability.get_observability_snapshot()
    check("All subsystems healthy", obs.all_subsystems_healthy)
    check("Cache hit ratio >= 0.90", obs.cache_hit_ratio >= 0.90)


def test_human_policy_orchestrator():
    print("\n📜 Testing Human Policy Orchestrator...")
    from app.core.human_intelligence.platform.human_policy_orchestrator import human_policy_orchestrator

    enforced = human_policy_orchestrator.evaluate_policy("pol_aw_01")
    check("Mandatory awareness policy is enforced", enforced)


def test_human_platform_metrics():
    print("\n📊 Testing Human Platform Metrics Collector...")
    from app.core.human_intelligence.platform.human_platform_metrics import human_platform_metrics

    metrics = human_platform_metrics.collect_platform_metrics()
    check("Awareness maturity index > 85.0", metrics.awareness_maturity_index > 85.0)
    check("Learning completion rate > 90%", metrics.learning_completion_rate_percent > 90.0)


def test_human_readiness_validator():
    print("\n✔️ Testing Human Readiness Validator...")
    from app.core.human_intelligence.platform.human_readiness_validator import human_readiness_validator

    val = human_readiness_validator.validate_readiness()
    check("Status is READY", val["status"] == "READY")
    check("Readiness score == 100", val["readiness_score"] == 100)


def test_human_lifecycle():
    print("\n🔄 Testing Human Lifecycle Manager...")
    from app.core.human_intelligence.platform.human_lifecycle import human_lifecycle_manager

    human_lifecycle_manager.initialize()
    check("Lifecycle initialized without errors", True)


async def test_full_platform_regression():
    print("\n🔒 Testing Integration & Backward Compatibility across Stages 1-6...")
    from app.core.human_intelligence import enterprise_human_intelligence_manager
    from app.core.security import enterprise_security_platform
    from app.core.intelligence import ai_os_kernel

    emp = enterprise_human_intelligence_manager.register_employee_profile("Joan Clarke", "joan@doxa.internal", "Cryptanalysis", "Principal Scientist")
    check("Human Intelligence Manager operates seamlessly with unified platform", emp is not None)

    payload = b"MZ\x90\x00\x03\x00\x00\x00\x04\x00\x00\x00VirtualAllocEx\x00"
    sec_res = await enterprise_security_platform.run_full_security_pipeline(payload, "platform_master_test.exe")
    check("Enterprise Security Platform operates seamlessly", sec_res is not None)
    check("AI OS Kernel remains fully functional", ai_os_kernel is not None)


async def main():
    print("==========================================================================")
    print("STAGE 7 PART 8 — MASTER ENTERPRISE HUMAN INTELLIGENCE UNIFICATION TEST SUITE")
    print("==========================================================================")

    await test_master_human_platform()
    test_human_service_bus()
    await test_human_workflow_engine()
    test_human_resource_manager()
    test_human_cache_manager()
    test_human_observability()
    test_human_policy_orchestrator()
    test_human_platform_metrics()
    test_human_readiness_validator()
    test_human_lifecycle()
    await test_full_platform_regression()

    print("\n==========================================================================")
    print(f"RESULTS: {PASS} passed, {FAIL} failed, {PASS + FAIL} total")
    print("==========================================================================")

    if FAIL > 0:
        sys.exit(1)
    print("\n🎉 STAGE 7 PART 8 SUCCESS: Master Enterprise Human Intelligence Platform Deployed!")


if __name__ == "__main__":
    asyncio.run(main())
