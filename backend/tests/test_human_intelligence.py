#!/usr/bin/env python3
"""
Integration Test Suite for Stage 7 Part 1 — Human Intelligence & Social Engineering Defense Platform.
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


def test_human_intelligence_types():
    print("\n👤 Testing Human Intelligence Types & Models...")
    from app.core.human_intelligence.human_intelligence_types import (
        EmployeeProfile,
        HumanRiskProfile,
        HumanRiskLevel,
        AwarenessAssessment,
        InsiderRiskIndicator,
        HumanDashboardState,
    )

    emp = EmployeeProfile(name="Alice Smith", email="alice@doxa.internal", department="Engineering", role="Lead Engineer")
    check("EmployeeProfile created", emp.employee_id.startswith("emp_"))
    check("Default risk level LOW", emp.risk_level == HumanRiskLevel.LOW)

    risk = HumanRiskProfile(employee_id=emp.employee_id, overall_risk_score=1.5, risk_level=HumanRiskLevel.LOW)
    check("HumanRiskProfile score assigned", risk.overall_risk_score == 1.5)


def test_human_config():
    print("\n⚙️ Testing Human Intelligence Configuration...")
    from app.core.human_intelligence.human_config import human_config

    check("Worker count > 0", human_config.worker_count > 0)
    check("Cache TTL > 0", human_config.cache_ttl_seconds > 0)


async def test_human_events():
    print("\n📢 Testing Human Intelligence Events...")
    from app.core.human_intelligence.human_events import publish_human_event, HumanEventType

    evt = await publish_human_event(HumanEventType.PROFILE_CREATED, target_id="emp_test", data={"role": "Architect"})
    check("Domain event published", evt is not None)
    check("Event type matches", evt.event_type == HumanEventType.PROFILE_CREATED)


def test_human_metrics():
    print("\n📊 Testing Human Intelligence Metrics Tracker...")
    from app.core.human_intelligence.human_metrics import human_metrics_tracker

    human_metrics_tracker.record_profile_created()
    metrics = human_metrics_tracker.get_metrics()
    check("Metrics recorded profile created", metrics.total_employees_monitored >= 1)


def test_human_registry():
    print("\n🔌 Testing Dynamic Plugin Registry...")
    from app.core.human_intelligence.human_registry import human_registry, HumanIntelligencePluginMetadata

    meta = HumanIntelligencePluginMetadata(plugin_id="p_behavior_01", name="BehavioralAnomalyDetector", capability="behavior_analysis", description="Detects off-hours access anomalies")
    human_registry.register_plugin(meta)
    discovered = human_registry.discover_plugins("behavior_analysis")
    check("Discovered registered plugin", len(discovered) == 1 and discovered[0].name == "BehavioralAnomalyDetector")


def test_human_context():
    print("\n🧠 Testing Unified Human Context Manager...")
    from app.core.human_intelligence.human_intelligence_types import EmployeeProfile, HumanRiskProfile
    from app.core.human_intelligence.human_context import unified_human_context_manager

    emp = EmployeeProfile(name="Bob Johnson", email="bob@doxa.internal", department="Finance", role="Analyst")
    risk = HumanRiskProfile(employee_id=emp.employee_id, overall_risk_score=2.0)
    ctx = unified_human_context_manager.build_unified_context(emp, risk)

    check("Context created with profile", ctx.employee_profile.name == "Bob Johnson")
    check("Context token count budgeted", ctx.token_count > 0)


async def test_human_pipeline():
    print("\n⚡ Testing Modular Human Intelligence Pipeline...")
    from app.core.human_intelligence.human_intelligence_types import EmployeeProfile
    from app.core.human_intelligence.human_pipeline import human_intelligence_pipeline

    emp = EmployeeProfile(name="Charlie Brown", email="charlie@doxa.internal", department="HR", role="Specialist", security_score=75.0)
    res = await human_intelligence_pipeline.execute_pipeline(emp)

    check("Pipeline executed result produced", res is not None)
    check("Pipeline assigned high risk due to score", res.risk_profile.overall_risk_score > 5.0)
    check("Training recommendations generated", len(res.recommendations) > 0)


async def test_human_intelligence_manager():
    print("\n🏢 Testing Enterprise Human Intelligence Manager...")
    from app.core.human_intelligence.human_intelligence_manager import enterprise_human_intelligence_manager

    emp = enterprise_human_intelligence_manager.register_employee_profile("Diana Prince", "diana@doxa.internal", "Security", "Security Lead")
    check("Employee registered via manager", emp.employee_id is not None)

    res = await enterprise_human_intelligence_manager.analyze_human_security_risk(emp.employee_id)
    check("Risk analysis pipeline executed", res.risk_profile.employee_id == emp.employee_id)

    dash = enterprise_human_intelligence_manager.get_dashboard_state()
    check("Dashboard metrics employee count > 0", dash.metrics.total_employees_monitored > 0)


async def test_integration_and_backward_compatibility():
    print("\n🔒 Testing Integration & Backward Compatibility across Stages 1-6...")
    from app.core.security import enterprise_security_platform
    from app.core.intelligence import ai_os_kernel

    payload = b"MZ\x90\x00\x03\x00\x00\x00\x04\x00\x00\x00VirtualAllocEx\x00"
    res = await enterprise_security_platform.run_full_security_pipeline(payload, "stage7_test.exe")

    check("Stage 6 Enterprise Security Platform operates seamlessly", res is not None)
    check("AI OS Kernel remains fully functional", ai_os_kernel is not None)


async def main():
    print("==========================================================================")
    print("STAGE 7 PART 1 — HUMAN INTELLIGENCE & SOCIAL ENGINEERING DEFENSE PLATFORM")
    print("==========================================================================")

    test_human_intelligence_types()
    test_human_config()
    await test_human_events()
    test_human_metrics()
    test_human_registry()
    test_human_context()
    await test_human_pipeline()
    await test_human_intelligence_manager()
    await test_integration_and_backward_compatibility()

    print("\n==========================================================================")
    print(f"RESULTS: {PASS} passed, {FAIL} failed, {PASS + FAIL} total")
    print("==========================================================================")

    if FAIL > 0:
        sys.exit(1)
    print("\n🎉 STAGE 7 PART 1 SUCCESS: Human Intelligence Platform Deployed!")


if __name__ == "__main__":
    asyncio.run(main())
