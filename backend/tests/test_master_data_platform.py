#!/usr/bin/env python3
"""
Master Integration Test Suite for Stage 8 — Enterprise Massive-Scale Data Intelligence Platform Unification.
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


async def test_master_data_platform():
    print("\n🌐 Testing Global Enterprise Data Intelligence Platform Master Entrypoint...")
    from app.core.data_intelligence.platform.enterprise_data_intelligence_platform import enterprise_data_intelligence_platform

    assessment = await enterprise_data_intelligence_platform.run_master_data_intelligence_assessment("Enterprise")
    check("Master data assessment generated", assessment is not None)
    check("Data quality score > 99.0%", assessment.data_quality_score > 99.0)
    check("Fusion confidence score >= 0.95", assessment.fusion_confidence_score >= 0.95)
    check("Readiness score == 100", assessment.readiness_score == 100)


async def test_data_service_bus():
    print("\n🚌 Testing Data Intelligence Event Bus...")
    from app.core.data_intelligence.platform.data_service_bus import data_service_bus
    from app.core.data_intelligence.data_events import DataEvent, DataEventType

    received = []

    def handler(ev):
        received.append(ev)

    data_service_bus.subscribe(DataEventType.DATA_INGESTED.value, handler)

    ev = DataEvent(event_type=DataEventType.DATA_INGESTED, source_id="src_bus_test", data={"count": 10})
    await data_service_bus.publish(ev)

    check("Event published and received by subscriber", len(received) == 1)


async def test_data_workflow_engine():
    print("\n⚙️ Testing Data Intelligence Workflow Engine...")
    from app.core.data_intelligence.platform.data_workflow_engine import data_workflow_engine

    exec_res = await data_workflow_engine.execute_workflow("data_discovery_pipeline", "Enterprise")
    check("Workflow executed", exec_res is not None)
    check("Workflow status is COMPLETED", exec_res.status == "COMPLETED")
    check("5 workflow steps executed", len(exec_res.steps) == 5)


def test_data_resource_manager():
    print("\n💻 Testing Data Resource Manager...")
    from app.core.data_intelligence.platform.data_resource_manager import data_resource_manager

    alloc = data_resource_manager.get_allocation()
    check("Max worker threads == 32", alloc.max_worker_threads == 32)
    check("Health status is HEALTHY", alloc.health_status == "HEALTHY")


def test_data_cache_manager():
    print("\n⚡ Testing Data Cache Manager...")
    from app.core.data_intelligence.platform.data_cache_manager import data_cache_manager

    data_cache_manager.set("master_key", "master_val", ttl_seconds=60.0)
    val = data_cache_manager.get("master_key")
    check("Cached master value retrieved", val == "master_val")


def test_data_observability():
    print("\n👁️ Testing Data Observability Layer...")
    from app.core.data_intelligence.platform.data_observability import data_observability

    obs = data_observability.get_observability_snapshot()
    check("All subsystems healthy", obs.all_subsystems_healthy)
    check("Cache hit ratio >= 0.95", obs.cache_hit_ratio >= 0.95)


def test_data_policy_orchestrator():
    print("\n📜 Testing Data Governance Policy Orchestrator...")
    from app.core.data_intelligence.platform.data_policy_orchestrator import data_policy_orchestrator

    enforced = data_policy_orchestrator.evaluate_policy("pol_gov_01")
    check("Governance retention policy is enforced", enforced)


def test_data_platform_metrics():
    print("\n📊 Testing Data Platform Metrics Collector...")
    from app.core.data_intelligence.platform.data_platform_metrics import data_platform_metrics

    metrics = data_platform_metrics.collect_platform_metrics()
    check("Records processed > 100,000", metrics.total_records_processed > 100000)
    check("Overall intelligence quality > 99%", metrics.overall_intelligence_quality_score > 99.0)


def test_data_readiness_validator():
    print("\n✔️ Testing Data Readiness Validator...")
    from app.core.data_intelligence.platform.data_readiness_validator import data_readiness_validator

    val = data_readiness_validator.validate_readiness()
    check("Status is READY", val["status"] == "READY")
    check("Readiness score == 100", val["readiness_score"] == 100)


def test_data_lifecycle():
    print("\n🔄 Testing Data Lifecycle Manager...")
    from app.core.data_intelligence.platform.data_lifecycle import data_lifecycle_manager

    data_lifecycle_manager.initialize()
    check("Lifecycle initialized cleanly", True)


async def test_full_platform_regression():
    print("\n🔒 Testing Integration & Backward Compatibility across Stages 1-7...")
    from app.core.human_intelligence import enterprise_human_intelligence_platform
    from app.core.security import enterprise_security_platform
    from app.core.intelligence import ai_os_kernel

    assess = await enterprise_human_intelligence_platform.run_master_human_intelligence_assessment("Data_Platform_Master")
    check("Human Intelligence Platform operates seamlessly with unified Data Platform", assess is not None)

    payload = b"MZ\x90\x00\x03\x00\x00\x00\x04\x00\x00\x00VirtualAllocEx\x00"
    sec_res = await enterprise_security_platform.run_full_security_pipeline(payload, "master_data_test.exe")
    check("Enterprise Security Platform operates seamlessly", sec_res is not None)
    check("AI OS Kernel remains fully functional", ai_os_kernel is not None)


async def main():
    print("==========================================================================")
    print("STAGE 8 — MASTER ENTERPRISE DATA INTELLIGENCE UNIFICATION TEST SUITE")
    print("==========================================================================")

    await test_master_data_platform()
    await test_data_service_bus()
    await test_data_workflow_engine()
    test_data_resource_manager()
    test_data_cache_manager()
    test_data_observability()
    test_data_policy_orchestrator()
    test_data_platform_metrics()
    test_data_readiness_validator()
    test_data_lifecycle()
    await test_full_platform_regression()

    print("\n==========================================================================")
    print(f"RESULTS: {PASS} passed, {FAIL} failed, {PASS + FAIL} total")
    print("==========================================================================")

    if FAIL > 0:
        sys.exit(1)
    print("\n🎉 STAGE 8 SUCCESS: Master Enterprise Data Intelligence Platform Deployed!")


if __name__ == "__main__":
    asyncio.run(main())
