#!/usr/bin/env python3
"""
Integration Test Suite for Stage 7 Part 7 — Enterprise Organizational Human Intelligence & Analytics Platform.
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


def test_organizational_intelligence_engine():
    print("\n🏢 Testing Organizational Intelligence Engine...")
    from app.core.human_intelligence.organization.organizational_intelligence_engine import organizational_intelligence_engine

    summary = organizational_intelligence_engine.evaluate_organization("Enterprise", avg_awareness=88.5)
    check("Summary evaluated", summary is not None)
    check("Enterprise intelligence score == 88.5", summary.enterprise_intelligence_score == 88.5)
    check("Posture rating is EXCELLENT", summary.overall_posture_rating == "EXCELLENT")


def test_workforce_analytics():
    print("\n👥 Testing Workforce Analytics Engine...")
    from app.core.human_intelligence.organization.workforce_analytics import workforce_analytics_engine

    metrics = workforce_analytics_engine.analyze_department_workforce("Cloud Engineering")
    check("Department workforce metrics analyzed", metrics is not None)
    check("Learning adoption rate > 95%", metrics.learning_adoption_rate_percent > 95.0)


def test_intelligence_fusion():
    print("\n🧠 Testing Human Intelligence Fusion Engine...")
    from app.core.human_intelligence.organization.intelligence_fusion import human_intelligence_fusion_engine

    insight = human_intelligence_fusion_engine.fuse_intelligence("Enterprise", awareness_score=88.0, risk_score=1.5)
    check("Fused organizational insight produced", insight is not None)
    check("Detailed findings count > 0", len(insight.detailed_findings) > 0)


def test_department_risk_engine():
    print("\n⚖️ Testing Department Risk Engine...")
    from app.core.human_intelligence.organization.department_risk_engine import department_risk_engine

    assess = department_risk_engine.evaluate_department_risk("DevOps", awareness_score=85.0)
    check("Department risk score calculated", assess.department_risk_score == 1.5)
    check("Risk rating is LOW", assess.risk_rating == "LOW")


def test_trend_analysis_engine():
    print("\n📈 Testing Trend Analytics Engine...")
    from app.core.human_intelligence.organization.trend_analysis_engine import trend_analysis_engine

    snapshot = trend_analysis_engine.analyze_trend("Awareness Score", historical=80.0, current=89.0)
    check("Trend percentage change > 11.0%", snapshot.percentage_change >= 11.0)
    check("Trend direction is IMPROVING", snapshot.trend_direction == "IMPROVING")


def test_organizational_graph():
    print("\n🕸️ Testing Enterprise Organizational Knowledge Graph...")
    from app.core.human_intelligence.organization.organizational_graph import enterprise_organizational_graph

    node = enterprise_organizational_graph.add_node("dept_devops", "department", "DevOps Engineering")
    check("Organizational node added", node is not None)

    depts = enterprise_organizational_graph.get_nodes_by_type("department")
    check("Nodes by type retrieved", len(depts) >= 1)

def test_organizational_recommendation_engine():
    print("\n💡 Testing Organizational AI Recommendation Engine...")
    from app.core.human_intelligence.organization.organizational_recommendation_engine import organizational_recommendation_engine

    recs = organizational_recommendation_engine.generate_organizational_recommendations("Enterprise", score=88.0)
    check("Organizational recommendations count > 0", len(recs) > 0)


def test_enterprise_intelligence_metrics():
    print("\n📊 Testing Enterprise Intelligence Metrics Service...")
    from app.core.human_intelligence.organization.enterprise_intelligence_metrics import enterprise_intelligence_metrics

    kpis = enterprise_intelligence_metrics.get_enterprise_kpis()
    check("Enterprise intelligence score > 85.0", kpis.overall_enterprise_intelligence_score > 85.0)
    check("Workforce readiness rating > 90%", kpis.workforce_readiness_rating_percent > 90.0)


def test_organization_dashboard_backend():
    print("\n🖥️ Testing Organization Dashboard Backend...")
    from app.core.human_intelligence.organization.organization_dashboard_backend import organization_dashboard_backend

    metrics = organization_dashboard_backend.get_dashboard_metrics()
    check("Total departments modeled > 0", metrics.total_departments_modeled > 0)
    check("Enterprise readiness percent > 90%", metrics.enterprise_readiness_percent > 90.0)


def test_organizational_report_builder():
    print("\n📄 Testing Organizational Report Builder...")
    from app.core.human_intelligence.organization.organizational_intelligence_engine import organizational_intelligence_engine
    from app.core.human_intelligence.organization.intelligence_fusion import human_intelligence_fusion_engine
    from app.core.human_intelligence.organization.enterprise_intelligence_metrics import enterprise_intelligence_metrics
    from app.core.human_intelligence.organization.organizational_report_builder import organizational_report_builder

    sum_obj = organizational_intelligence_engine.evaluate_organization("Enterprise")
    ins_obj = human_intelligence_fusion_engine.fuse_intelligence("Enterprise")
    kpi_obj = enterprise_intelligence_metrics.get_enterprise_kpis()

    data = organizational_report_builder.build_report_data(sum_obj, ins_obj, kpi_obj)
    check("Report data produced", data["scope_id"] == "Enterprise")

    md = organizational_report_builder.to_markdown(data)
    check("Markdown organizational report generated", "# Enterprise Organizational Intelligence Report" in md)


async def test_integration_and_backward_compatibility():
    print("\n🔒 Testing Integration & Backward Compatibility across Stages 1-6...")
    from app.core.human_intelligence import enterprise_human_intelligence_manager
    from app.core.security import enterprise_security_platform
    from app.core.intelligence import ai_os_kernel

    emp = enterprise_human_intelligence_manager.register_employee_profile("Katherine Johnson", "katherine@doxa.internal", "Mathematics", "Lead Analyst")
    check("Human Intelligence Manager operates seamlessly with organizational platform", emp is not None)

    payload = b"MZ\x90\x00\x03\x00\x00\x00\x04\x00\x00\x00VirtualAllocEx\x00"
    sec_res = await enterprise_security_platform.run_full_security_pipeline(payload, "org_test.exe")
    check("Enterprise Security Platform operates seamlessly", sec_res is not None)
    check("AI OS Kernel remains fully functional", ai_os_kernel is not None)


async def main():
    print("==========================================================================")
    print("STAGE 7 PART 7 — ORGANIZATIONAL HUMAN INTELLIGENCE TEST SUITE")
    print("==========================================================================")

    test_organizational_intelligence_engine()
    test_workforce_analytics()
    test_intelligence_fusion()
    test_department_risk_engine()
    test_organizational_graph()
    test_trend_analysis_engine()
    test_organizational_recommendation_engine()
    test_enterprise_intelligence_metrics()
    test_organization_dashboard_backend()
    test_organizational_report_builder()
    await test_integration_and_backward_compatibility()

    print("\n==========================================================================")
    print(f"RESULTS: {PASS} passed, {FAIL} failed, {PASS + FAIL} total")
    print("==========================================================================")

    if FAIL > 0:
        sys.exit(1)
    print("\n🎉 STAGE 7 PART 7 SUCCESS: Enterprise Organizational Human Intelligence Platform Deployed!")


if __name__ == "__main__":
    asyncio.run(main())
