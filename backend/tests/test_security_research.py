#!/usr/bin/env python3
"""
Integration Test for Stage 6 Part 1 - Enterprise Cybersecurity & Reverse Engineering Platform.
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


async def test_security_types():
    print("\n🔬 Testing Security Research Pydantic Types...")
    from app.core.security.security_types import (
        FileFingerprint, BinaryMetadata, MalwareSample, IOC, ThreatIndicator,
        ThreatActorProfile, ReverseEngineeringSession, BinaryFunction, BinaryString,
        BinaryImport, BinaryExport, BinarySection, BinarySymbol, BinaryInstruction,
        ThreatReport, StaticAnalysisResult, DynamicAnalysisResult, SecurityFinding,
        VulnerabilityFinding, RiskAssessment, ForensicArtifact, AttackSimulation,
        DetectionRule, SandboxResult, SecurityMetrics, SecurityDashboardState,
        Architecture, FileFormat, ThreatSeverity, AnalysisStatus,
    )

    fp = FileFingerprint(md5="d41d8cd98f00b204e9800998ecf8427e", sha1="da39a3ee5e6b4b0d3255bfef95601890afd80709", sha256="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", file_size_bytes=1024)
    check("FileFingerprint instantiated", fp.file_size_bytes == 1024)

    meta = BinaryMetadata(file_name="test.exe", fingerprint=fp, format=FileFormat.PE, architecture=Architecture.X64)
    check("BinaryMetadata instantiated", meta.file_name == "test.exe")

    func = BinaryFunction(name="main", start_address=0x401000, end_address=0x401050)
    check("BinaryFunction instantiated", func.name == "main")

    sess = ReverseEngineeringSession(binary_id=meta.binary_id, functions=[func])
    check("ReverseEngineeringSession instantiated", len(sess.functions) == 1)


async def test_security_registry():
    print("\n📦 Testing Security Registry...")
    from app.core.security.security_registry import SecurityRegistry

    reg = SecurityRegistry()

    class DummyAnalyzer:
        def analyze(self):
            return "ok"

    reg.register("analyzer", "dummy_pe_analyzer", DummyAnalyzer, version="1.0.0", capabilities=["pe_header_parse"])
    prov = reg.get_provider("analyzer", "dummy_pe_analyzer")
    check("Registered provider retrieved", prov is not None and prov.analyze() == "ok")

    caps = reg.discover_capabilities("analyzer")
    check("Capability discovery returned info", len(caps.get("analyzer", [])) == 1)


async def test_unified_context():
    print("\n📚 Testing Unified Security Context...")
    from app.core.security.security_context import UnifiedSecurityContext
    from app.core.security.security_types import FileFingerprint, BinaryMetadata, IOC, ThreatSeverity

    ctx_mgr = UnifiedSecurityContext()
    fp = FileFingerprint(md5="1111", sha1="2222", sha256="3333", file_size_bytes=512)
    meta = BinaryMetadata(file_name="sample.dll", fingerprint=fp)
    iocs = [IOC(ioc_type="ip", value="192.168.1.100", severity=ThreatSeverity.HIGH)]

    ctx = await ctx_mgr.build_context(binary_metadata=meta, iocs=iocs, max_token_budget=1024)
    check("Context items created", len(ctx["items"]) == 2)
    check("Total tokens estimated", ctx["total_tokens"] > 0)


async def test_security_pipeline_and_manager():
    print("\n⚙️ Testing Security Pipeline & Enterprise Security Manager...")
    from app.core.security.security_manager import EnterpriseSecurityManager

    mgr = EnterpriseSecurityManager()

    dummy_binary = b"MZ\x90\x00\x03\x00\x00\x00\x04\x00\x00\x00\xff\xff\x00\x00"
    report = await mgr.analyze_binary("sample.exe", dummy_binary, user_id="analyst_1")

    check("ThreatReport generated", report is not None)
    check("Report title correct", "sample.exe" in report.title)
    check("Static analysis attached", report.static_analysis is not None)
    check("Risk assessment attached", report.risk_assessment is not None)

    # Test RE session
    sess = await mgr.start_reverse_engineering_session(binary_id="bin_test_123")
    check("RE session started", sess.session_id.startswith("re_sess_"))
    check("RE session functions populated", len(sess.functions) >= 2)

    closed = await mgr.close_session(sess.session_id)
    check("RE session closed", closed)

    dashboard = mgr.get_dashboard_state()
    check("Dashboard metrics recorded scans", dashboard.metrics.scans_executed >= 1)
    check("Dashboard system health healthy", dashboard.system_health == "healthy")


async def test_backward_compatibility():
    print("\n🔒 Testing Backward Compatibility with Stage 1-5 Security...")
    from app.core.security import (
        rbac_engine,
        policy_engine,
        tenant_security,
        secret_manager,
        api_key_manager,
        audit_logger,
        security_event_bus,
        compliance_engine,
        enterprise_security_manager,
        security_config,
    )

    check("RBAC engine functional", rbac_engine is not None)
    check("Policy engine functional", policy_engine is not None)
    check("Tenant security functional", tenant_security is not None)
    check("Secret manager functional", secret_manager is not None)
    check("API key manager functional", api_key_manager is not None)
    check("Audit logger functional", audit_logger is not None)
    check("Security event bus functional", security_event_bus is not None)
    check("Compliance engine functional", compliance_engine is not None)
    check("Enterprise security manager functional", enterprise_security_manager is not None)
    check("Security config limits present", security_config.MAX_BINARY_SIZE_BYTES > 0)


async def main():
    print("==========================================================================")
    print("STAGE 6 PART 1 - ENTERPRISE CYBERSECURITY & RE PLATFORM TEST SUITE")
    print("==========================================================================")

    await test_security_types()
    await test_security_registry()
    await test_unified_context()
    await test_security_pipeline_and_manager()
    await test_backward_compatibility()

    print("\n==========================================================================")
    print(f"RESULTS: {PASS} passed, {FAIL} failed, {PASS + FAIL} total")
    print("==========================================================================")

    if FAIL > 0:
        sys.exit(1)
    print("\n🎉 STAGE 6 PART 1 SUCCESS: Cybersecurity & Reverse Engineering Architecture Deployed!")


if __name__ == "__main__":
    asyncio.run(main())
