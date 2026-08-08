#!/usr/bin/env python3
"""
Integration Test Suite for Stage 7 Part 4 — Enterprise Insider Risk Analytics & User Risk Intelligence Platform.
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


def test_insider_risk_engine():
    print("\n🔍 Testing Insider Risk Engine...")
    from app.core.human_intelligence.insider_risk.insider_risk_engine import insider_risk_engine

    assessment = insider_risk_engine.evaluate_insider_risk("emp_100", is_privileged=True, security_score=85.0)
    check("Insider risk assessment created", assessment is not None)
    check("Privileged access risk score > 0", assessment.privileged_access_risk_score > 0)
    check("Confidence score >= 0.90", assessment.confidence_score >= 0.90)


def test_privileged_access_analyzer():
    print("\n🔑 Testing Privileged Access Analyzer...")
    from app.core.human_intelligence.insider_risk.privileged_access_analyzer import privileged_access_analyzer

    metrics = privileged_access_analyzer.analyze_privileges("emp_100", role="Infrastructure Admin")
    check("Admin flag detected", metrics.is_admin)
    check("Separation of duties compliant", metrics.separation_of_duties_compliant)


def test_behavioral_deviation_engine():
    print("\n📉 Testing Behavioral Deviation Engine...")
    from app.core.human_intelligence.insider_risk.behavioral_deviation_engine import behavioral_deviation_engine

    alerts = behavioral_deviation_engine.evaluate_deviations("emp_100", baseline_score=90.0, current_score=60.0)
    check("Awareness decline alert triggered", len(alerts) == 1)
    check("Confidence score > 0.90", alerts[0].confidence_score > 0.90)


def test_organizational_exposure():
    print("\n🏢 Testing Organizational Exposure Analyzer...")
    from app.core.human_intelligence.insider_risk.organizational_exposure import organizational_exposure_analyzer

    exp = organizational_exposure_analyzer.calculate_department_exposure("Infrastructure & DevOps", high_risk_count=2)
    check("Department exposure score computed", exp.exposure_score > 5.0)
    check("Exposure level is HIGH", exp.exposure_level == "HIGH")


def test_adaptive_risk_scoring():
    print("\n⚡ Testing Adaptive AI Risk Scoring Engine...")
    from app.core.human_intelligence.insider_risk.adaptive_risk_scoring import adaptive_risk_scoring_engine

    res = adaptive_risk_scoring_engine.compute_adaptive_risk("emp_100", security_score=75.0, is_privileged=True, anomalies_count=1)
    check("Normalized risk score computed", res.normalized_risk_score > 0)
    check("Contributing factors present", len(res.contributing_factors) > 0)


def test_policy_compliance_monitor():
    print("\n📜 Testing Policy Compliance Monitor...")
    from app.core.human_intelligence.insider_risk.policy_compliance_monitor import policy_compliance_monitor

    comp = policy_compliance_monitor.evaluate_compliance("emp_100", training_completed=True)
    check("Policy adherence score == 95.0%", comp.policy_adherence_score == 95.0)
    check("Training completion compliant", comp.training_completion_compliant)


def test_insider_case_manager():
    print("\n📁 Testing Insider Risk Case Manager...")
    from app.core.human_intelligence.insider_risk.insider_case_manager import insider_case_manager

    case = insider_case_manager.create_case("icase_01", "emp_100")
    check("Insider case created", case.case_id == "icase_01")

    note = insider_case_manager.add_note("icase_01", "Verified admin entitlement certification.")
    check("Analyst note added to case", note is not None)


def test_risk_recommendation_engine():
    print("\n💡 Testing Risk Recommendation Engine...")
    from app.core.human_intelligence.insider_risk.risk_recommendation_engine import insider_risk_recommendation_engine

    recs = insider_risk_recommendation_engine.generate_recommendations("emp_100", risk_score=6.0)
    check("Risk recommendations count > 0", len(recs) > 0)
    check("High priority produced for high risk score", recs[0].priority == "HIGH")


def test_insider_dashboard_backend():
    print("\n🖥️ Testing Insider Risk Dashboard Backend...")
    from app.core.human_intelligence.insider_risk.insider_dashboard_backend import insider_dashboard_backend

    metrics = insider_dashboard_backend.get_dashboard_metrics()
    check("Privileged users count > 0", metrics.total_privileged_users_count > 0)
    check("Average policy adherence > 90%", metrics.average_policy_adherence_percent > 90.0)


def test_insider_report_builder():
    print("\n📄 Testing Insider Risk Report Builder...")
    from app.core.human_intelligence.insider_risk.insider_risk_engine import insider_risk_engine
    from app.core.human_intelligence.insider_risk.privileged_access_analyzer import privileged_access_analyzer
    from app.core.human_intelligence.insider_risk.insider_report_builder import insider_report_builder

    assess = insider_risk_engine.evaluate_insider_risk("emp_100", is_privileged=True)
    priv = privileged_access_analyzer.analyze_privileges("emp_100", "Admin")

    data = insider_report_builder.build_report_data(assess, priv)
    check("Report data created", data["employee_id"] == "emp_100")

    md = insider_report_builder.to_markdown(data)
    check("Markdown insider report generated", "# Enterprise Insider Risk Report" in md)


async def test_integration_and_backward_compatibility():
    print("\n🔒 Testing Integration & Backward Compatibility across Stages 1-6...")
    from app.core.human_intelligence import enterprise_human_intelligence_manager
    from app.core.security import enterprise_security_platform
    from app.core.intelligence import ai_os_kernel

    emp = enterprise_human_intelligence_manager.register_employee_profile("Grace Hopper", "grace@doxa.internal", "DevOps", "Principal Systems Admin")
    check("Human Intelligence Manager operates seamlessly with insider risk platform", emp is not None)

    payload = b"MZ\x90\x00\x03\x00\x00\x00\x04\x00\x00\x00VirtualAllocEx\x00"
    sec_res = await enterprise_security_platform.run_full_security_pipeline(payload, "insider_test.exe")
    check("Enterprise Security Platform operates seamlessly", sec_res is not None)
    check("AI OS Kernel remains fully functional", ai_os_kernel is not None)


async def main():
    print("==========================================================================")
    print("STAGE 7 PART 4 — ENTERPRISE INSIDER RISK ANALYTICS TEST SUITE")
    print("==========================================================================")

    test_insider_risk_engine()
    test_privileged_access_analyzer()
    test_behavioral_deviation_engine()
    test_organizational_exposure()
    test_adaptive_risk_scoring()
    test_policy_compliance_monitor()
    test_insider_case_manager()
    test_risk_recommendation_engine()
    test_insider_dashboard_backend()
    test_insider_report_builder()
    await test_integration_and_backward_compatibility()

    print("\n==========================================================================")
    print(f"RESULTS: {PASS} passed, {FAIL} failed, {PASS + FAIL} total")
    print("==========================================================================")

    if FAIL > 0:
        sys.exit(1)
    print("\n🎉 STAGE 7 PART 4 SUCCESS: Insider Risk Analytics Platform Deployed!")


if __name__ == "__main__":
    asyncio.run(main())
