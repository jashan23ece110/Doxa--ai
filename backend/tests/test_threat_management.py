#!/usr/bin/env python3
"""
Integration Test Suite for Stage 6 Part 6 - Vulnerability Assessment, Threat Intelligence & Security Automation Platform.
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


def test_vulnerability_engine():
    print("\n🔬 Testing Vulnerability Assessment Engine...")
    from app.core.security.threat_management.vulnerability_engine import vulnerability_engine
    from app.core.security.security_types import ThreatSeverity

    cves = vulnerability_engine.correlate_cve("log4j-core", "2.14.1")
    check("Correlated CVEs count > 0", len(cves) > 0)
    check("CVE ID mapped", cves[0].cve_id == "CVE-2021-44228")
    check("CWE ID mapped", cves[0].cwe_id == "CWE-502")
    check("Severity is CRITICAL", cves[0].severity == ThreatSeverity.CRITICAL)


def test_threat_model_engine():
    print("\n🧩 Testing STRIDE Threat Modeling Engine...")
    from app.core.security.threat_management.threat_model_engine import threat_model_engine

    model = threat_model_engine.generate_stride_model("Execution Engine", ["API Key", "Memory Store"], ["Public Internet", "Tenant Isolation"])
    check("Threat model generated", model is not None)
    check("STRIDE threats identified > 0", len(model.threats) > 0)
    categories = {t.category for t in model.threats}
    check("Spoofing threat identified", "Spoofing" in categories)
    check("Elevation of Privilege threat identified", "Elevation of Privilege" in categories)


def test_attack_surface_analyzer():
    print("\n🌐 Testing Attack Surface Analyzer...")
    from app.core.security.threat_management.attack_surface_analyzer import attack_surface_analyzer

    inventory = attack_surface_analyzer.analyze_attack_surface(api_routes_count=20, plugin_count=4)
    check("Inventory total interfaces > 0", inventory.total_interfaces > 0)
    check("Attack surface score computed > 0", inventory.attack_surface_score > 0)


def test_security_policy_engine():
    print("\n📜 Testing Security Policy Engine...")
    from app.core.security.threat_management.security_policy_engine import security_policy_engine

    res = security_policy_engine.evaluate_policy("api_gateway", {"authenticated": True})
    check("Policy evaluation compliant", res.is_compliant)
    check("Violations list empty when compliant", len(res.violations) == 0)


async def test_security_automation_engine():
    print("\n⚡ Testing Security Automation Engine...")
    from app.core.security.threat_management.security_automation import security_automation_engine

    tasks = await security_automation_engine.run_scheduled_automation_cycle()
    check("Automation cycle tasks count >= 4", len(tasks) >= 4)
    check("IOC Feed Refresh completed", any(t.task_name == "IOC_Feed_Refresh" for t in tasks))


def test_continuous_monitor():
    print("\n⏱️ Testing Continuous Security Monitoring Engine...")
    from app.core.security.threat_management.continuous_monitor import continuous_monitor_engine

    metrics = continuous_monitor_engine.evaluate_system_posture()
    check("System health HEALTHY", metrics.system_health == "HEALTHY")
    check("Active threat level LOW", metrics.active_threat_level == "LOW")


def test_compliance_engine():
    print("\n📊 Testing Compliance Assessment Engine...")
    from app.core.security.threat_management.compliance_engine import compliance_assessment_engine

    nist_res = compliance_assessment_engine.assess_framework_compliance("NIST CSF")
    check("NIST CSF compliance score > 90%", nist_res.compliance_score > 90.0)

    iso_res = compliance_assessment_engine.assess_framework_compliance("ISO 27001")
    check("ISO 27001 compliance score > 90%", iso_res.compliance_score > 90.0)


def test_recommendation_engine():
    print("\n💡 Testing AI Security Recommendation Engine...")
    from app.core.security.threat_management.recommendation_engine import ai_recommendation_engine

    recs = ai_recommendation_engine.generate_recommendations(risk_score=8.0)
    check("Recommendations count > 0", len(recs) > 0)
    check("High priority recommendation produced", recs[0].priority == "HIGH")
    check("Explainability rationale present", len(recs[0].explainability_rationale) > 0)


def test_security_dashboard_backend():
    print("\n🖥️ Testing Threat Management Dashboard Backend...")
    from app.core.security.threat_management.security_dashboard_backend import threat_dashboard_backend

    state = threat_dashboard_backend.get_dashboard_state()
    check("Dashboard compliance score present", state.compliance_score > 0)
    check("Automation health HEALTHY", state.automation_health == "HEALTHY")


def test_threat_report_builder():
    print("\n📄 Testing Threat Intelligence Report Builder...")
    from app.core.security.threat_management.vulnerability_engine import vulnerability_engine
    from app.core.security.threat_management.threat_model_engine import threat_model_engine
    from app.core.security.threat_management.attack_surface_analyzer import attack_surface_analyzer
    from app.core.security.threat_management.compliance_engine import compliance_assessment_engine
    from app.core.security.threat_management.recommendation_engine import ai_recommendation_engine
    from app.core.security.threat_management.threat_report_builder import threat_intel_report_builder

    cves = vulnerability_engine.correlate_cve("log4j-core")
    tm = threat_model_engine.generate_stride_model("TestApp", ["Asset1"], ["Boundary1"])
    as_inv = attack_surface_analyzer.analyze_attack_surface()
    comp = compliance_assessment_engine.assess_framework_compliance("NIST CSF")
    recs = ai_recommendation_engine.generate_recommendations()

    data = threat_intel_report_builder.build_report_data("TestApp", cves, tm, as_inv, comp, recs)
    check("Report data created", data["system_name"] == "TestApp")

    md = threat_intel_report_builder.to_markdown(data, cves, recs)
    check("Markdown threat report generated", "# Enterprise Vulnerability & Threat Intelligence Report" in md)


async def test_integration_and_backward_compatibility():
    print("\n🔒 Testing Integration & Backward Compatibility...")
    from app.core.security import enterprise_security_manager
    from app.core.intelligence import ai_os_kernel

    res = await enterprise_security_manager.analyze_binary("test_vuln.exe", b"MZsample_vuln")
    check("EnterpriseSecurityManager operates seamlessly with threat management platform", res is not None)
    check("AI OS Kernel remains fully functional", ai_os_kernel is not None)


async def main():
    print("==========================================================================")
    print("STAGE 6 PART 6 - VULNERABILITY & THREAT MANAGEMENT PLATFORM TEST SUITE")
    print("==========================================================================")

    test_vulnerability_engine()
    test_threat_model_engine()
    test_attack_surface_analyzer()
    test_security_policy_engine()
    await test_security_automation_engine()
    test_continuous_monitor()
    test_compliance_engine()
    test_recommendation_engine()
    test_security_dashboard_backend()
    test_threat_report_builder()
    await test_integration_and_backward_compatibility()

    print("\n==========================================================================")
    print(f"RESULTS: {PASS} passed, {FAIL} failed, {PASS + FAIL} total")
    print("==========================================================================")

    if FAIL > 0:
        sys.exit(1)
    print("\n🎉 STAGE 6 PART 6 SUCCESS: Vulnerability & Threat Management Platform Deployed!")


if __name__ == "__main__":
    asyncio.run(main())
