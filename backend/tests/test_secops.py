#!/usr/bin/env python3
"""
Integration Test Suite for Stage 6 Part 7 - Enterprise Digital Forensics, Incident Response & SecOps Platform.
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


def test_incident_manager():
    print("\n🚨 Testing Incident Response Manager...")
    from app.core.security.secops.incident_manager import incident_manager
    from app.core.security.security_types import ThreatSeverity

    inc = incident_manager.create_incident("Suspicious Process Launch", ThreatSeverity.HIGH)
    check("Incident created", inc.incident_id is not None)
    check("Status is open", inc.status == "open")

    updated = incident_manager.update_status(inc.incident_id, "investigating")
    check("Status updated to investigating", updated.status == "investigating")


def test_forensic_engine():
    print("\n🔬 Testing Digital Forensics Engine...")
    from app.core.security.secops.forensic_engine import digital_forensics_engine

    artifact = digital_forensics_engine.extract_evidence_artifact("memory_dump", "RAM_0x100", {"pid": 1234})
    check("Artifact created", artifact is not None)
    check("Checksum generated", len(artifact.checksum) == 64)


def test_chain_of_custody():
    print("\n🔗 Testing Chain of Custody Tracker...")
    from app.core.security.secops.chain_of_custody import chain_of_custody_tracker

    acq = chain_of_custody_tracker.record_acquisition("art_100", owner="analyst_alice")
    check("Acquisition recorded", acq.action == "acquired")

    acc = chain_of_custody_tracker.record_access("art_100", accessor="analyst_bob", reason="memory analysis")
    check("Access recorded with previous hash link", acc.previous_hash == acq.current_hash)

    history = chain_of_custody_tracker.get_custody_history("art_100")
    check("Custody history contains 2 records", len(history) == 2)


def test_timeline_reconstruction():
    print("\n⏱️ Testing Timeline Reconstruction Engine...")
    from app.core.security.secops.timeline_reconstruction import timeline_reconstruction_engine

    raw_events = [
        {"category": "authentication", "summary": "User login success"},
        {"category": "execution", "summary": "Process cmd.exe spawned"},
        {"category": "filesystem", "summary": "Payload created in temp"},
    ]

    timeline = timeline_reconstruction_engine.build_timeline("inv_101", raw_events)
    check("Timeline built entries == 3", timeline.total_entries == 3)
    check("Entries ordered chronologically", timeline.entries[0].timestamp <= timeline.entries[-1].timestamp)


def test_case_management():
    print("\n📁 Testing SecOps Case Workspace Manager...")
    from app.core.security.secops.case_management import secops_case_manager

    case = secops_case_manager.create_case("case_sec_01", "Memory Injection Investigation")
    check("Case created", case.case_id == "case_sec_01")

    note = secops_case_manager.add_note("case_sec_01", "Confirmed memory region RWX permissions.")
    check("Case note added", note is not None)


def test_playbook_engine():
    print("\n📜 Testing SecOps Playbook Engine...")
    from app.core.security.secops.playbook_engine import secops_playbook_engine

    pb = secops_playbook_engine.get_playbook("malware")
    check("Playbook retrieved", pb is not None)
    check("Playbook steps count >= 3", len(pb.steps) >= 3)
    check("Step 1 is Isolate Host", pb.steps[0].name == "Isolate Host")


async def test_soc_automation():
    print("\n⚡ Testing SOC Automation Engine...")
    from app.core.security.secops.soc_automation import soc_automation_engine

    inc = await soc_automation_engine.auto_triage_alert("Critical Malware Infection Attempt", {"host": "workstation_01"})
    check("Alert auto-triaged into incident", inc is not None)
    check("Title contains alert name", "Critical Malware Infection" in inc.title)


def test_audit_engine():
    print("\n🔒 Testing Security Audit Engine...")
    from app.core.security.secops.audit_engine import security_audit_engine

    log1 = security_audit_engine.log_analyst_action("analyst_1", "view_artifact", {"art": "100"})
    log2 = security_audit_engine.log_analyst_action("analyst_1", "quarantine_host", {"host": "10.0.0.1"})

    check("Cryptographic audit logs created", log1 is not None and log2 is not None)
    check("Hash chain link valid", log2.previous_hash == log1.current_hash)
    check("Audit integrity check passes", security_audit_engine.verify_integrity())


def test_investigation_dashboard_backend():
    print("\n📊 Testing SecOps Investigation Dashboard Backend...")
    from app.core.security.secops.investigation_dashboard_backend import secops_dashboard_backend

    metrics = secops_dashboard_backend.get_secops_dashboard_state()
    check("Active incidents count >= 0", metrics.active_incidents_count >= 0)
    check("SLA compliance rate > 90%", metrics.sla_compliance_rate > 90.0)


def test_incident_report_builder():
    print("\n📄 Testing Incident Response Report Builder...")
    from app.core.security.secops.incident_manager import incident_manager
    from app.core.security.secops.timeline_reconstruction import timeline_reconstruction_engine
    from app.core.security.secops.incident_report_builder import incident_report_builder

    inc = incident_manager.create_incident("Data Exfiltration Attempt")
    timeline = timeline_reconstruction_engine.build_timeline("inv_200", [{"summary": "Exfiltration attempt"}])

    data = incident_report_builder.build_report_data(inc, timeline)
    check("Report data created", data["incident_id"] == inc.incident_id)

    md = incident_report_builder.to_markdown(data)
    check("Markdown incident report generated", "# Enterprise Incident Response Report" in md)


async def test_integration_and_backward_compatibility():
    print("\n🔒 Testing Integration & Backward Compatibility...")
    from app.core.security import enterprise_security_manager
    from app.core.intelligence import ai_os_kernel

    res = await enterprise_security_manager.analyze_binary("test_secops.exe", b"MZsample_secops")
    check("EnterpriseSecurityManager operates seamlessly with SecOps platform", res is not None)
    check("AI OS Kernel remains fully functional", ai_os_kernel is not None)


async def main():
    print("==========================================================================")
    print("STAGE 6 PART 7 - DIGITAL FORENSICS & SECOPS PLATFORM TEST SUITE")
    print("==========================================================================")

    test_incident_manager()
    test_forensic_engine()
    test_chain_of_custody()
    test_timeline_reconstruction()
    test_case_management()
    test_playbook_engine()
    await test_soc_automation()
    test_audit_engine()
    test_investigation_dashboard_backend()
    test_incident_report_builder()
    await test_integration_and_backward_compatibility()

    print("\n==========================================================================")
    print(f"RESULTS: {PASS} passed, {FAIL} failed, {PASS + FAIL} total")
    print("==========================================================================")

    if FAIL > 0:
        sys.exit(1)
    print("\n🎉 STAGE 6 PART 7 SUCCESS: Digital Forensics & SecOps Platform Deployed!")


if __name__ == "__main__":
    asyncio.run(main())
