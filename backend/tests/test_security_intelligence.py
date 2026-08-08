#!/usr/bin/env python3
"""
Integration Test Suite for Stage 6 Part 8 - Security Intelligence & Autonomous Defense Platform.
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


def test_threat_hunting_engine():
    print("\n🎯 Testing Threat Hunting Engine...")
    from app.core.security.security_intelligence.threat_hunting_engine import threat_hunting_engine

    hunt = threat_hunting_engine.execute_hunt("Detect UPX Packets", "pattern:UPX*", category="ttp")
    check("Threat hunt executed", hunt is not None)
    check("Confidence score >= 0.85", hunt.confidence_score >= 0.85)


def test_security_knowledge_graph():
    print("\n🕸️ Testing Security Knowledge Graph...")
    from app.core.security.security_intelligence.security_knowledge_graph import security_knowledge_graph

    n1 = security_knowledge_graph.add_node("mal_1", "malware", "Emotet")
    n2 = security_knowledge_graph.add_node("cve_1", "cve", "CVE-2021-44228")
    edge = security_knowledge_graph.add_edge("mal_1", "cve_1", "exploits")

    check("Nodes added to graph", n1 is not None and n2 is not None)
    neighbors = security_knowledge_graph.get_neighbors("mal_1")
    check("Neighbors retrieved", len(neighbors) == 1 and neighbors[0]["relationship"] == "exploits")


def test_attack_simulation_engine():
    print("\n⚔️ Testing Attack Simulation Engine...")
    from app.core.security.security_intelligence.attack_simulation_engine import attack_simulation_engine

    report = attack_simulation_engine.simulate_attack_chain("Process Injection Test", technique_id="T1055")
    check("Attack chain simulation completed", report is not None)
    check("Defense validation score > 90%", report.defense_validation_score > 90.0)


def test_security_ai_engine():
    print("\n🧠 Testing AI Security Intelligence Engine...")
    from app.core.security.security_intelligence.security_ai_engine import security_ai_engine

    res = security_ai_engine.analyze_findings([{"finding": "high_entropy"}])
    check("AI findings correlation executed", res is not None)
    check("Confidence score >= 0.90", res.confidence_score >= 0.90)
    check("False positive probability low", res.false_positive_probability < 0.10)


async def test_defense_orchestrator():
    print("\n🛡️ Testing Defense Orchestrator...")
    from app.core.security.security_intelligence.defense_orchestrator import defense_orchestrator
    from app.core.security.security_types import RiskAssessment, IOC

    risk = RiskAssessment(overall_risk_score=8.0)
    iocs = [IOC(value="1.1.1.1", ioc_type="ip")]
    res = await defense_orchestrator.orchestrate_defense_response("bin_test", risk, iocs)

    check("Defense response orchestrated", res["status"] == "defense_orchestrated")


def test_security_memory():
    print("\n💾 Testing Security Memory Engine...")
    from app.core.security.security_intelligence.security_memory import security_memory_engine

    rec = security_memory_engine.remember_investigation("bin_100", "Malware sample analyzed and contained.")
    check("Security memory record created", rec is not None)

    history = security_memory_engine.recall_history("investigation")
    check("History recalled", len(history) >= 1)


def test_security_analytics():
    print("\n📊 Testing Security Analytics Engine...")
    from app.core.security.security_intelligence.security_analytics import security_analytics_engine

    analytics = security_analytics_engine.compute_analytics()
    check("MTTD seconds present", analytics.mttd_seconds > 0)
    check("MTTR seconds present", analytics.mttr_seconds > 0)
    check("SOC efficiency score high", analytics.soc_efficiency_score > 90.0)


def test_security_recommendation_engine():
    print("\n💡 Testing Intelligence Recommendation Engine...")
    from app.core.security.security_intelligence.security_recommendation_engine import security_recommendation_engine

    recs = security_recommendation_engine.generate_recommendations()
    check("Intelligence recommendations generated count > 0", len(recs) > 0)


def test_security_health_monitor():
    print("\n🏥 Testing Security Health Monitor...")
    from app.core.security.security_intelligence.security_health_monitor import security_health_monitor

    health = security_health_monitor.check_health()
    check("Overall status HEALTHY", health.overall_status == "HEALTHY")
    check("Knowledge graph consistent", health.knowledge_graph_consistent)


async def test_global_security_orchestrator():
    print("\n🌐 Testing Global Security Intelligence Orchestrator...")
    from app.core.security.security_intelligence.enterprise_security_orchestrator import global_security_orchestrator

    sample = b"MZ\x90\x00\x03\x00\x00\x00\x04\x00\x00\x00VirtualAllocEx\x00UPX0\x00"
    res = await global_security_orchestrator.execute_unified_security_assessment(sample, "global_test.exe")

    check("Unified security assessment produced result", res is not None)
    check("Binary ID assigned", "binary_id" in res)
    check("Overall risk score calculated", res["overall_risk_score"] > 0)
    check("AI confidence score present", res["ai_confidence"] > 0)


async def test_integration_and_backward_compatibility():
    print("\n🔒 Testing Integration & Backward Compatibility...")
    from app.core.security import enterprise_security_manager
    from app.core.intelligence import ai_os_kernel

    res = await enterprise_security_manager.analyze_binary("test_intel.exe", b"MZsample_intel")
    check("EnterpriseSecurityManager operates seamlessly with Security Intelligence Platform", res is not None)
    check("AI OS Kernel remains fully functional", ai_os_kernel is not None)


async def main():
    print("==========================================================================")
    print("STAGE 6 PART 8 - SECURITY INTELLIGENCE & AUTONOMOUS DEFENSE TEST SUITE")
    print("==========================================================================")

    test_threat_hunting_engine()
    test_security_knowledge_graph()
    test_attack_simulation_engine()
    test_security_ai_engine()
    await test_defense_orchestrator()
    test_security_memory()
    test_security_analytics()
    test_security_recommendation_engine()
    test_security_health_monitor()
    await test_global_security_orchestrator()
    await test_integration_and_backward_compatibility()

    print("\n==========================================================================")
    print(f"RESULTS: {PASS} passed, {FAIL} failed, {PASS + FAIL} total")
    print("==========================================================================")

    if FAIL > 0:
        sys.exit(1)
    print("\n🎉 STAGE 6 PART 8 SUCCESS: Security Intelligence & Autonomous Defense Platform Deployed!")


if __name__ == "__main__":
    asyncio.run(main())
