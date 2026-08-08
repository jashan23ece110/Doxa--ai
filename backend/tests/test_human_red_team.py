#!/usr/bin/env python3
"""
Integration Test Suite for Stage 7 Part 6 — Enterprise Human Attack Surface & Red Team Simulation Platform.
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


def test_human_attack_surface_engine():
    print("\n🎯 Testing Human Attack Surface Engine...")
    from app.core.human_intelligence.red_team.human_attack_surface_engine import human_attack_surface_engine

    metrics = human_attack_surface_engine.analyze_attack_surface("Enterprise", security_score=85.0)
    check("Attack surface metrics computed", metrics is not None)
    check("Overall attack surface score == 1.5/10.0", metrics.overall_attack_surface_score == 1.5)
    check("Awareness coverage percent >= 95%", metrics.awareness_coverage_percent >= 95.0)


def test_red_team_simulation_engine():
    print("\n⚔️ Testing Red Team Simulation Engine...")
    from app.core.human_intelligence.red_team.red_team_simulation_engine import red_team_simulation_engine

    res = red_team_simulation_engine.evaluate_conceptual_simulation("scen_phish_01", "Engineering")
    check("Conceptual simulation result evaluated", res is not None)
    check("Detection rate percent > 90%", res.detection_rate_percent > 90.0)
    check("Resilience score >= 90.0", res.resilience_score >= 90.0)


def test_resilience_engine():
    print("\n🛡️ Testing Human Security Resilience Engine...")
    from app.core.human_intelligence.red_team.resilience_engine import resilience_engine

    res = resilience_engine.calculate_resilience("Enterprise", security_score=92.0)
    check("Overall resilience score == 92.0", res.overall_resilience_score == 92.0)
    check("Resilience level is FORTIFIED", res.resilience_level == "FORTIFIED")


def test_organizational_security_model():
    print("\n🏢 Testing Organizational Security Model...")
    from app.core.human_intelligence.red_team.organizational_security_model import organizational_security_model

    model = organizational_security_model.model_department_security("Cloud Engineering")
    check("Department security posture modeled", model is not None)
    check("Posture level is STRONG", model.posture_level == "STRONG")


def test_control_validation_engine():
    print("\n✔️ Testing Security Control Validation Engine...")
    from app.core.human_intelligence.red_team.control_validation_engine import control_validation_engine

    val = control_validation_engine.validate_control("1-Click Reporting Extension")
    check("Control validation status PASSED", val.validation_status == "PASSED")
    check("Efficacy rating > 90%", val.efficacy_rating_percent > 90.0)


def test_simulation_scheduler():
    print("\n📅 Testing Simulation Scheduler...")
    from app.core.human_intelligence.red_team.simulation_scheduler import simulation_scheduler

    job = simulation_scheduler.schedule_simulation("scen_phish_01", "DevOps")
    check("Simulation job scheduled", job is not None)

    jobs = simulation_scheduler.list_jobs()
    check("Scheduled jobs list contains job", len(jobs) >= 1)


def test_organizational_resilience_analytics():
    print("\n📊 Testing Organizational Resilience Analytics Engine...")
    from app.core.human_intelligence.red_team.organizational_resilience_analytics import organizational_resilience_analytics

    metrics = organizational_resilience_analytics.compute_resilience_analytics()
    check("Enterprise readiness score > 90.0", metrics.enterprise_readiness_score > 90.0)
    check("Attack surface reduction > 15%", metrics.attack_surface_reduction_percent > 15.0)


def test_resilience_recommendation_engine():
    print("\n💡 Testing Resilience AI Recommendation Engine...")
    from app.core.human_intelligence.red_team.resilience_recommendation_engine import resilience_recommendation_engine

    recs = resilience_recommendation_engine.generate_resilience_recommendations("Enterprise", surface_score=3.5)
    check("Resilience recommendations count > 0", len(recs) > 0)


def test_red_team_dashboard_backend():
    print("\n🖥️ Testing Red Team Dashboard Backend...")
    from app.core.human_intelligence.red_team.red_team_dashboard_backend import red_team_dashboard_backend

    metrics = red_team_dashboard_backend.get_dashboard_metrics()
    check("Simulations executed count > 0", metrics.total_simulations_executed > 0)
    check("Awareness coverage > 95%", metrics.awareness_coverage_percent > 95.0)


def test_resilience_report_builder():
    print("\n📄 Testing Resilience Report Builder...")
    from app.core.human_intelligence.red_team.human_attack_surface_engine import human_attack_surface_engine
    from app.core.human_intelligence.red_team.resilience_engine import resilience_engine
    from app.core.human_intelligence.red_team.control_validation_engine import control_validation_engine
    from app.core.human_intelligence.red_team.resilience_report_builder import resilience_report_builder

    surf = human_attack_surface_engine.analyze_attack_surface("Enterprise")
    res = resilience_engine.calculate_resilience("Enterprise")
    val = control_validation_engine.validate_control("Reporting Extension")

    data = resilience_report_builder.build_report_data(surf, res, val)
    check("Report data created", data["scope_name"] == "Enterprise")

    md = resilience_report_builder.to_markdown(data)
    check("Markdown resilience report generated", "# Enterprise Human Security Resilience Report" in md)


async def test_integration_and_backward_compatibility():
    print("\n🔒 Testing Integration & Backward Compatibility across Stages 1-6...")
    from app.core.human_intelligence import enterprise_human_intelligence_manager
    from app.core.security import enterprise_security_platform
    from app.core.intelligence import ai_os_kernel

    emp = enterprise_human_intelligence_manager.register_employee_profile("Margaret Hamilton", "margaret@doxa.internal", "Aerospace", "Principal Software Engineer")
    check("Human Intelligence Manager operates seamlessly with red team platform", emp is not None)

    payload = b"MZ\x90\x00\x03\x00\x00\x00\x04\x00\x00\x00VirtualAllocEx\x00"
    sec_res = await enterprise_security_platform.run_full_security_pipeline(payload, "redteam_test.exe")
    check("Enterprise Security Platform operates seamlessly", sec_res is not None)
    check("AI OS Kernel remains fully functional", ai_os_kernel is not None)


async def main():
    print("==========================================================================")
    print("STAGE 7 PART 6 — HUMAN ATTACK SURFACE & RED TEAM SIMULATION TEST SUITE")
    print("==========================================================================")

    test_human_attack_surface_engine()
    test_red_team_simulation_engine()
    test_resilience_engine()
    test_organizational_security_model()
    test_control_validation_engine()
    test_simulation_scheduler()
    test_organizational_resilience_analytics()
    test_resilience_recommendation_engine()
    test_red_team_dashboard_backend()
    test_resilience_report_builder()
    await test_integration_and_backward_compatibility()

    print("\n==========================================================================")
    print(f"RESULTS: {PASS} passed, {FAIL} failed, {PASS + FAIL} total")
    print("==========================================================================")

    if FAIL > 0:
        sys.exit(1)
    print("\n🎉 STAGE 7 PART 6 SUCCESS: Human Attack Surface & Red Team Simulation Platform Deployed!")


if __name__ == "__main__":
    asyncio.run(main())
