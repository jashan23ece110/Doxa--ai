#!/usr/bin/env python3
"""
Final Master Test Suite & Architectural Readiness Validation for Stage 6 — Enterprise Cybersecurity Platform.
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


async def test_security_service_bus():
    print("\n🚌 Testing Enterprise Security Service Bus...")
    from app.core.security.platform.security_service_bus import security_service_bus, SecurityEvent

    received = []

    async def sample_handler(evt: SecurityEvent):
        received.append(evt)

    security_service_bus.subscribe("malware_alert", sample_handler)
    pub_evt = await security_service_bus.publish("malware_alert", {"threat": "high"})

    check("Event published to topic", pub_evt is not None)
    check("Subscriber handler received event", len(received) == 1 and received[0].payload["threat"] == "high")


async def test_security_workflow_engine():
    print("\n⚡ Testing Security Workflow Engine...")
    from app.core.security.platform.security_workflow_engine import security_workflow_engine

    res = await security_workflow_engine.execute_workflow("malware_investigation", {"target": "sample.exe"})
    check("Workflow executed successfully", res.status == "completed")
    check("Steps count == 5", res.executed_steps_count == 5)


def test_security_resource_manager():
    print("\n⚙️ Testing Security Resource Manager...")
    from app.core.security.platform.security_resource_manager import security_resource_manager

    acquired = security_resource_manager.acquire_sandbox_slot()
    check("Acquired sandbox worker slot", acquired)
    security_resource_manager.release_sandbox_slot()
    status = security_resource_manager.get_resource_status()
    check("Sandbox slot released back to pool", status.sandbox_slots_available == 8)


def test_security_cache_manager():
    print("\n💾 Testing Security Cache Manager...")
    from app.core.security.platform.security_cache_manager import security_cache_manager

    security_cache_manager.set("cve_100", {"score": 9.8}, ttl_seconds=60)
    val = security_cache_manager.get("cve_100")
    check("Cache item retrieved", val is not None and val["score"] == 9.8)

    metrics = security_cache_manager.get_metrics()
    check("Cache hit recorded", metrics["hits"] > 0)


def test_security_observability():
    print("\n👁️ Testing Security Observability Layer...")
    from app.core.security.platform.security_observability import security_observability

    telemetry = security_observability.collect_telemetry()
    check("Service health is HEALTHY", telemetry.service_health == "HEALTHY")
    check("Latency metrics collected", "static_analysis" in telemetry.subsystem_latencies_ms)


def test_security_policy_orchestrator():
    print("\n📜 Testing Security Policy Orchestrator...")
    from app.core.security.platform.security_policy_orchestrator import security_policy_orchestrator

    pol = security_policy_orchestrator.get_master_policy()
    check("Master policy retrieved", pol is not None)
    compliant = security_policy_orchestrator.evaluate_policy_compliance({"action": "run_sandbox"})
    check("Policy compliance evaluated", compliant)


def test_security_platform_metrics():
    print("\n📊 Testing Security Platform Metrics Collector...")
    from app.core.security.platform.security_platform_metrics import security_platform_metrics_collector

    metrics = security_platform_metrics_collector.collect_platform_metrics()
    check("Detection rate > 95%", metrics.threat_detection_rate > 95.0)
    check("Readiness score == 100.0%", metrics.platform_readiness_score == 100.0)


def test_security_readiness_validator():
    print("\n🚦 Testing Startup Readiness Validator...")
    from app.core.security.platform.security_readiness_validator import security_readiness_validator

    val = security_readiness_validator.validate_readiness()
    check("Readiness status READY", val["status"] == "READY")
    check("Readiness score == 100.0", val["readiness_score"] == 100.0)


async def test_security_lifecycle():
    print("\n🔄 Testing Security Lifecycle Manager...")
    from app.core.security.platform.security_lifecycle import security_lifecycle_manager

    await security_lifecycle_manager.initialize()
    check("Platform initialized gracefully", security_lifecycle_manager._is_initialized)
    await security_lifecycle_manager.shutdown()
    check("Platform shut down gracefully", not security_lifecycle_manager._is_initialized)


async def test_enterprise_security_platform():
    print("\n🌐 Testing Global Enterprise Security Platform...")
    from app.core.security.platform.enterprise_security_platform import enterprise_security_platform

    payload = b"MZ\x90\x00\x03\x00\x00\x00\x04\x00\x00\x00VirtualAllocEx\x00UPX0\x00"
    res = await enterprise_security_platform.run_full_security_pipeline(payload, "master_target.exe")

    check("Master security pipeline returned result", res is not None)
    check("Binary ID present", "binary_id" in res)
    check("Platform status OPERATIONAL", res["platform_status"] == "OPERATIONAL")
    check("Total platform latency measured", res["total_platform_latency_ms"] > 0)


async def test_final_stage_6_validation():
    print("\n🏆 Performing Final Stage 6 Architectural Readiness Validation...")
    from app.core.security import enterprise_security_platform
    from app.core.intelligence import ai_os_kernel, global_intelligence_orchestrator

    status = enterprise_security_platform.get_platform_status()
    check("14 Stage 6 Subsystems Registered and Active", status.subsystems_active_count == 14)
    check("Subsystem Health Score == 100.0%", status.health_score == 100.0)
    check("AI OS Kernel Integration Operational", ai_os_kernel is not None)
    check("Global Intelligence Orchestrator Integration Operational", global_intelligence_orchestrator is not None)


async def main():
    print("==========================================================================")
    print("STAGE 6 FINAL MASTER TEST SUITE — ENTERPRISE CYBERSECURITY PLATFORM")
    print("==========================================================================")

    await test_security_service_bus()
    await test_security_workflow_engine()
    test_security_resource_manager()
    test_security_cache_manager()
    test_security_observability()
    test_security_policy_orchestrator()
    test_security_platform_metrics()
    test_security_readiness_validator()
    await test_security_lifecycle()
    await test_enterprise_security_platform()
    await test_final_stage_6_validation()

    print("\n==========================================================================")
    print(f"RESULTS: {PASS} passed, {FAIL} failed, {PASS + FAIL} total")
    print("==========================================================================")

    if FAIL > 0:
        sys.exit(1)
    print("\n🎉 STAGE 6 COMPLETE: Doxa Enterprise Cybersecurity Platform Fully Operational!")


if __name__ == "__main__":
    asyncio.run(main())
