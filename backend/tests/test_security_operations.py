#!/usr/bin/env python3
"""
Integration Test Suite for Stage 6 Part 5 - Security Operations, Response Playbooks, SIEM/SOAR & Telemetry.
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


async def test_playbook_engine():
    print("\n📜 Testing Response Playbook Engine...")
    from app.core.security.operations.playbook_engine import playbook_engine
    from app.core.security.security_types import RiskAssessment, ThreatSeverity

    risk = RiskAssessment(overall_risk_score=8.5, threat_level=ThreatSeverity.CRITICAL)
    res = await playbook_engine.run_playbook("inc_100", risk, ["1.1.1.1", "C:\\bad.dll"])

    check("Playbook execution completed", res.success)
    check("Actions executed count == 2", len(res.actions_executed) == 2)
    check("IP block action recorded", res.actions_executed[0].action_type == "block_ip")
    check("File quarantine action recorded", res.actions_executed[1].action_type == "quarantine_file")


def test_siem_soar_exporter():
    print("\n📡 Testing SIEM & SOAR Exporter...")
    from app.core.security.operations.siem_soar_exporter import siem_soar_exporter
    from app.core.security.security_types import ThreatReport, RiskAssessment, IOC, ThreatSeverity

    rep = ThreatReport(title="Test Alert Report", summary="Automated Threat Detection")
    risk = RiskAssessment(overall_risk_score=9.0, threat_level=ThreatSeverity.CRITICAL)
    iocs = [IOC(value="192.0.2.1", ioc_type="ip")]

    stix = siem_soar_exporter.to_stix21_bundle(rep, iocs)
    check("STIX 2.1 bundle type is bundle", stix.get("type") == "bundle")
    check("STIX objects count >= 2", len(stix.get("objects", [])) >= 2)

    cef = siem_soar_exporter.to_cef_syslog(rep, risk)
    check("CEF Syslog string formatted", cef.startswith("CEF:0|Doxa|AI_OS_Security"))

    misp = siem_soar_exporter.to_misp_event(rep, iocs)
    check("MISP event JSON exported", "Event" in misp)


async def test_telemetry_streamer():
    print("\n⚡ Testing Telemetry Streamer...")
    from app.core.security.operations.telemetry_streamer import telemetry_streamer

    received_events = []

    def on_event(evt):
        received_events.append(evt)

    telemetry_streamer.subscribe(on_event)
    evt = await telemetry_streamer.emit_event("threat_detected", {"ip": "1.1.1.1"}, severity="high")

    check("Event emitted successfully", evt is not None)
    check("Subscriber received event", len(received_events) >= 1)
    check("Recent event buffer stores event", len(telemetry_streamer.get_recent_events()) >= 1)


def test_soc_dashboard_backend():
    print("\n📊 Testing SOC Dashboard Backend...")
    from app.core.security.operations.soc_dashboard_backend import soc_dashboard_backend

    metrics = soc_dashboard_backend.get_dashboard_summary()
    check("SOC metrics retrieved", metrics.total_binaries_scanned > 0)
    check("System posture OPTIMAL", metrics.system_posture == "OPTIMAL")


async def test_security_operations_manager():
    print("\n🛡️ Testing Security Operations Manager...")
    from app.core.security.operations import security_operations_manager
    from app.core.security.security_types import ThreatReport, RiskAssessment, IOC, ThreatSeverity

    rep = ThreatReport(title="Incident #501", summary="Critical Infection Attempt")
    risk = RiskAssessment(overall_risk_score=9.5, threat_level=ThreatSeverity.CRITICAL)
    iocs = [IOC(value="10.0.0.1", ioc_type="ip")]

    res = await security_operations_manager.handle_security_incident("inc_501", rep, risk, iocs, ["10.0.0.1"])
    check("Incident handled cleanly", res is not None)
    check("Playbook result included", res["playbook_result"].success)
    check("STIX bundle present", res["stix_bundle"] is not None)


async def main():
    print("==========================================================================")
    print("STAGE 6 PART 5 - SECURITY OPERATIONS & SIEM/SOAR INTEGRATION TEST SUITE")
    print("==========================================================================")

    await test_playbook_engine()
    test_siem_soar_exporter()
    await test_telemetry_streamer()
    test_soc_dashboard_backend()
    await test_security_operations_manager()

    print("\n==========================================================================")
    print(f"RESULTS: {PASS} passed, {FAIL} failed, {PASS + FAIL} total")
    print("==========================================================================")

    if FAIL > 0:
        sys.exit(1)
    print("\n🎉 STAGE 6 FINAL COMPLETION: Complete Cybersecurity Platform Deployed!")


if __name__ == "__main__":
    asyncio.run(main())
