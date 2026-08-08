#!/usr/bin/env python3
"""
Integration Test Suite for Stage 6 Part 4 - Enterprise Dynamic Analysis, Sandbox & Threat Intelligence Platform.
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


async def test_sandbox_manager():
    print("\n📦 Testing Sandbox Manager...")
    from app.core.security.dynamic_analysis.sandbox_manager import (
        sandbox_manager, SandboxConfig, IsolatedVirtualSandboxProvider,
    )

    res = await sandbox_manager.run_in_sandbox("bin_sample_1", b"MZsample", config=SandboxConfig(timeout_seconds=30))
    check("Sandbox execution result returned", res is not None)
    check("Process tree contains process entries", len(res.process_tree) >= 2)
    check("Modified registry keys captured", len(res.modified_registry_keys) >= 1)
    check("Network connections captured", len(res.network_connections) >= 1)


def test_behavior_analyzer():
    print("\n🔍 Testing Behavior Analyzer...")
    from app.core.security.dynamic_analysis.sandbox_manager import SandboxExecutionResult
    from app.core.security.dynamic_analysis.behavior_analyzer import behavior_analyzer

    res = SandboxExecutionResult(
        execution_id="exec_test",
        sandbox_provider="test_provider",
        process_tree=[{"pid": 100, "name": "cmd.exe", "command_line": "cmd.exe /c whoami"}],
        created_files=["C:\\temp\\file.tmp"],
        modified_registry_keys=["HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run\\Persist"],
        network_connections=[{"dst_ip": "1.1.1.1", "dst_port": 443}],
    )

    report = behavior_analyzer.analyze_sandbox_result(res)
    check("Persistence detected", report.has_persistence)
    check("Privilege escalation detected", report.has_privilege_escalation)
    check("Network activity detected", report.has_network_activity)
    check("Behaviors cataloged count > 0", len(report.detected_behaviors) > 0)


def test_ioc_engine():
    print("\n🎯 Testing IOC Engine...")
    from app.core.security.dynamic_analysis.sandbox_manager import SandboxExecutionResult
    from app.core.security.dynamic_analysis.ioc_engine import ioc_engine

    res = SandboxExecutionResult(
        execution_id="exec_ioc",
        sandbox_provider="test_provider",
        created_files=["C:\\temp\\dropped.dll"],
        modified_registry_keys=["HKEY_LOCAL_MACHINE\\Software\\Run"],
        network_connections=[{"dst_ip": "192.0.2.1", "dst_port": 80}],
    )

    iocs = ioc_engine.extract_iocs_from_sandbox(res)
    check("Extracted IOCs count >= 3", len(iocs) >= 3)
    types = {i.ioc_type for i in iocs}
    check("IP address IOC extracted", "ip" in types)
    check("File path IOC extracted", "file_path" in types)
    check("Registry key IOC extracted", "registry_key" in types)


def test_threat_correlation():
    print("\n🌐 Testing Threat Correlation Engine...")
    from app.core.security.dynamic_analysis.behavior_analyzer import BehavioralReport
    from app.core.security.dynamic_analysis.threat_correlation import threat_correlation_engine
    from app.core.security.security_types import IOC

    br = BehavioralReport(
        execution_id="exec_corr",
        has_persistence=True,
        has_network_activity=True,
        has_privilege_escalation=True,
    )
    iocs = [IOC(value="1.1.1.1", ioc_type="ip")]

    assessment = threat_correlation_engine.correlate_findings("bin_corr", br, iocs)
    check("Threat assessment created", assessment is not None)
    check("Risk assessment score high", assessment.risk_assessment.overall_risk_score >= 8.0)


def test_forensic_timeline():
    print("\n⏱️ Testing Forensic Timeline Generator...")
    from app.core.security.dynamic_analysis.sandbox_manager import SandboxExecutionResult
    from app.core.security.dynamic_analysis.forensic_timeline import forensic_timeline_generator

    res = SandboxExecutionResult(
        execution_id="exec_time",
        sandbox_provider="test",
        process_tree=[{"pid": 1, "name": "app.exe"}],
        created_files=["C:\\file.txt"],
        modified_registry_keys=["HKCU\\Run"],
        network_connections=[{"dst_ip": "2.2.2.2"}],
    )

    timeline = forensic_timeline_generator.generate_timeline("bin_time", res)
    check("Timeline generated events > 0", timeline.total_events >= 4)
    check("Timeline events sorted chronologically", timeline.events[0].timestamp <= timeline.events[-1].timestamp)


async def test_evidence_repository():
    print("\n💾 Testing Evidence Storage Repository...")
    from app.core.security.dynamic_analysis.evidence_repository import evidence_repository

    artifact = await evidence_repository.store_evidence("bin_ev", "behavioral_log", {"key": "value"})
    check("Evidence artifact stored", artifact is not None)
    check("SHA256 hash generated", len(artifact.sha256_hash) == 64)

    retrieved = await evidence_repository.get_evidence(artifact.artifact_id)
    check("Retrieved evidence matches", retrieved.artifact_id == artifact.artifact_id)


def test_risk_scoring_engine():
    print("\n📊 Testing Risk Scoring Engine...")
    from app.core.security.dynamic_analysis.behavior_analyzer import BehavioralReport
    from app.core.security.dynamic_analysis.risk_scoring_engine import risk_scoring_engine

    br = BehavioralReport(
        execution_id="exec_risk",
        has_persistence=True,
        has_network_activity=True,
        has_privilege_escalation=True,
    )

    risk = risk_scoring_engine.calculate_risk(br, ioc_count=5)
    check("Normalized risk score > 70", risk.normalized_score > 70.0)
    check("Threat category CRITICAL or HIGH", risk.threat_category in ("CRITICAL", "HIGH"))


def test_threat_intelligence_fusion():
    print("\n🔗 Testing Threat Intelligence Fusion Engine...")
    from app.core.security.dynamic_analysis.threat_intelligence_fusion import threat_intel_fusion_engine
    from app.core.security.security_types import IOC

    iocs_a = [IOC(value="1.1.1.1", ioc_type="ip")]
    iocs_b = [IOC(value="1.1.1.1", ioc_type="ip"), IOC(value="2.2.2.2", ioc_type="ip")]

    fused = threat_intel_fusion_engine.fuse_intelligence("bin_fuse", iocs_a, iocs_b, [])
    check("Fused unique IOCs count is 2 (deduplicated)", len(fused.fused_iocs) == 2)


def test_investigation_workspace():
    print("\n📁 Testing Investigation Workspace...")
    from app.core.security.dynamic_analysis.investigation_workspace import investigation_workspace

    case = investigation_workspace.create_case("case_101", "Suspicious Process Activity", "bin_case")
    check("Case created", case.case_id == "case_101")

    linked = investigation_workspace.link_evidence("case_101", "art_12345")
    check("Evidence linked to case", linked)


def test_dynamic_report_builder():
    print("\n📄 Testing Dynamic Report Builder...")
    from app.core.security.dynamic_analysis.behavior_analyzer import BehavioralReport
    from app.core.security.dynamic_analysis.forensic_timeline import ForensicTimeline
    from app.core.security.dynamic_analysis.risk_scoring_engine import OrganizationalRiskScore
    from app.core.security.dynamic_analysis.dynamic_report_builder import dynamic_report_builder

    br = BehavioralReport(execution_id="e1", detected_behaviors=["Behavior 1"])
    ft = ForensicTimeline(binary_id="bin_rep", total_events=5)
    rs = OrganizationalRiskScore(
        normalized_score=85.0,
        threat_category="HIGH",
        exploitability_estimate=80.0,
        persistence_likelihood=90.0,
        lateral_movement_risk=70.0,
        privilege_escalation_risk=80.0,
    )

    data = dynamic_report_builder.build_report_data("bin_rep", br, ft, rs, 3)
    check("Report data built", data["binary_id"] == "bin_rep")

    md = dynamic_report_builder.to_markdown(data)
    check("Markdown report generated", "# Enterprise Dynamic Sandbox" in md)


async def test_integration_and_backward_compatibility():
    print("\n🔒 Testing Integration & Backward Compatibility...")
    from app.core.security import enterprise_security_manager
    from app.core.intelligence import ai_os_kernel

    res = await enterprise_security_manager.analyze_binary("test_dynamic.exe", b"MZsample_dynamic")
    check("EnterpriseSecurityManager handles full pipeline execution", res is not None)
    check("AI OS Kernel remains functional", ai_os_kernel is not None)


async def main():
    print("==========================================================================")
    print("STAGE 6 PART 4 - ENTERPRISE DYNAMIC ANALYSIS & SANDBOX PLATFORM TEST SUITE")
    print("==========================================================================")

    await test_sandbox_manager()
    test_behavior_analyzer()
    test_ioc_engine()
    test_threat_correlation()
    test_forensic_timeline()
    await test_evidence_repository()
    test_risk_scoring_engine()
    test_threat_intelligence_fusion()
    test_investigation_workspace()
    test_dynamic_report_builder()
    await test_integration_and_backward_compatibility()

    print("\n==========================================================================")
    print(f"RESULTS: {PASS} passed, {FAIL} failed, {PASS + FAIL} total")
    print("==========================================================================")

    if FAIL > 0:
        sys.exit(1)
    print("\n🎉 STAGE 6 PART 4 SUCCESS: Enterprise Dynamic Analysis & Sandbox Platform Deployed!")


if __name__ == "__main__":
    asyncio.run(main())
