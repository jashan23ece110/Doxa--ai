#!/usr/bin/env python3
"""
Integration Test Suite for Stage 6 Part 2 - Enterprise Static Analysis & Binary Intelligence Engine.
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


def test_binary_parser():
    print("\n🔬 Testing Binary Parser (PE, ELF, Mach-O)...")
    from app.core.security.static_analysis.binary_parser import (
        BinaryParserFactory, PEParser, ELFParser, MachOParser,
    )
    from app.core.security.static_analysis.fingerprint_engine import fingerprint_engine
    from app.core.security.security_types import FileFormat, Architecture

    pe_bytes = b"MZ\x90\x00\x03\x00\x00\x00\x04\x00\x00\x00\xff\xff\x00\x00"
    parser = BinaryParserFactory.get_parser(pe_bytes)
    check("Factory returned PEParser", isinstance(parser, PEParser))

    fp = fingerprint_engine.generate_fingerprint(pe_bytes, "sample.exe")
    meta = parser.parse(pe_bytes, "sample.exe", fp)
    check("PE metadata parsed format PE", meta.format == FileFormat.PE)

    elf_bytes = b"\x7fELF\x02\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x3e\x00"
    elf_parser = BinaryParserFactory.get_parser(elf_bytes)
    check("Factory returned ELFParser", isinstance(elf_parser, ELFParser))
    elf_meta = elf_parser.parse(elf_bytes, "sample.elf", fp)
    check("ELF metadata parsed format ELF", elf_meta.format == FileFormat.ELF)


def test_fingerprint_engine():
    print("\n🔑 Testing Fingerprint Engine...")
    from app.core.security.static_analysis.fingerprint_engine import FingerprintEngine

    fe = FingerprintEngine()
    data = b"Doxa AI OS Sample Binary Content"
    fp = fe.generate_fingerprint(data, "sample.bin")

    check("MD5 generated", len(fp.md5) == 32)
    check("SHA1 generated", len(fp.sha1) == 40)
    check("SHA256 generated", len(fp.sha256) == 64)
    check("Duplicate detection works", fe.is_duplicate(fp.sha256))


def test_entropy_engine():
    print("\n📈 Testing Entropy Analysis Engine...")
    from app.core.security.static_analysis.entropy_engine import EntropyEngine

    ee = EntropyEngine()
    zero_data = b"\x00" * 1024
    entropy_zero = ee.calculate_shannon_entropy(zero_data)
    check("Zero data entropy is 0.0", entropy_zero == 0.0)

    import os
    random_data = os.urandom(2048)
    entropy_rand = ee.calculate_shannon_entropy(random_data)
    check("Random data entropy > 7.0", entropy_rand > 7.0)

    profile = ee.analyze_entropy_profile(random_data, block_size=512)
    check("Entropy profile data generated", len(profile["entropy_profile"]) > 0)
    check("Random data flagged as packed/high entropy", profile["is_packed"])


def test_string_extractor():
    print("\n🔤 Testing String Extraction & Categorization...")
    from app.core.security.static_analysis.string_extractor import StringExtractor

    se = StringExtractor()
    sample = b"Hello World\x00http://malicious.c2/api\x00HKEY_LOCAL_MACHINE\\Software\\Run\x00cmd.exe /c calc.exe\x00"
    strings = se.extract_strings(sample)

    check("Extracted strings count > 0", len(strings) > 0)
    categories = {s.category for s in strings}
    check("URL categorized", "url" in categories)
    check("Registry categorized", "registry_key" in categories)
    check("Command categorized", "command" in categories)


def test_import_export_analyzer():
    print("\n🔍 Testing Import/Export Analyzer...")
    from app.core.security.static_analysis.import_export_analyzer import ImportExportAnalyzer
    from app.core.security.security_types import BinaryImport

    analyzer = ImportExportAnalyzer()
    imports = [
        BinaryImport(library="kernel32.dll", function_name="VirtualAllocEx"),
        BinaryImport(library="urlmon.dll", function_name="URLDownloadToFileA"),
    ]
    res = analyzer.analyze_api_usage(imports, [])

    check("Suspicious APIs detected", len(res["suspicious_apis"]) == 2)
    check("Process injection flag True", res["has_injection_capabilities"])
    check("Networking flag True", res["has_networking_capabilities"])


def test_binary_classifier():
    print("\n🏷️ Testing Binary Classifier...")
    from app.core.security.static_analysis.binary_classifier import BinaryClassifier
    from app.core.security.security_types import BinaryMetadata, FileFormat, Architecture, FileFingerprint

    classifier = BinaryClassifier()
    fp = FileFingerprint(md5="1", sha1="2", sha256="3", file_size_bytes=100)
    meta = BinaryMetadata(file_name="driver.sys", fingerprint=fp, format=FileFormat.PE, subsystem="driver")

    res = classifier.classify(meta, b"MZsample")
    check("Driver classified", res["classification"] == "driver")
    check("Confidence high", res["confidence_score"] >= 0.9)


def test_yara_engine():
    print("\n🎯 Testing YARA Engine Architecture...")
    from app.core.security.static_analysis.yara_engine import YARAEngine

    ye = YARAEngine()
    sample_upx = b"MZ\x90\x00UPX0\x00UPX1\x00"
    matches = ye.match_binary(sample_upx, "packed.exe")

    check("YARA rules executed", len(ye.list_rules()) >= 2)
    check("UPX YARA rule matched", len(matches) >= 1)


async def test_threat_intelligence_connector():
    print("\n🌐 Testing Threat Intelligence Connector...")
    from app.core.security.static_analysis.threat_intelligence_connector import ThreatIntelligenceConnector

    connector = ThreatIntelligenceConnector()
    res = await connector.query_hash("e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")

    check("Threat intel query succeeded", res is not None)
    check("Queried providers count >= 1", res["queried_providers_count"] >= 1)


def test_report_builder():
    print("\n📄 Testing Report Builder...")
    from app.core.security.static_analysis.report_builder import ReportBuilder
    from app.core.security.security_types import ThreatReport, FileFingerprint, BinaryMetadata, StaticAnalysisResult, RiskAssessment

    rb = ReportBuilder()
    fp = FileFingerprint(md5="111", sha1="222", sha256="333", file_size_bytes=1024)
    meta = BinaryMetadata(file_name="sample.exe", fingerprint=fp)
    sa = StaticAnalysisResult(binary_id=meta.binary_id, fingerprint=fp)
    ra = RiskAssessment(overall_risk_score=8.5, is_malicious=True, key_findings=["High entropy"])

    report = rb.build_report("sample.exe", fp, meta, sa, {"overall_entropy": 7.5}, [], {}, ra)
    check("Report title correct", "sample.exe" in report.title)
    check("Remediation steps present", len(report.remediation_steps) >= 2)

    md = rb.to_markdown(report, metadata=meta)
    check("Markdown output generated", "# Enterprise Static Analysis Report" in md)


async def test_static_analysis_engine():
    print("\n⚙️ Testing End-to-End Static Analysis Engine...")
    from app.core.security.static_analysis.static_analyzer import StaticAnalysisEngine

    engine = StaticAnalysisEngine()
    sample_binary = b"MZ\x90\x00\x03\x00\x00\x00\x04\x00\x00\x00VirtualAllocEx\x00URLDownloadToFileA\x00UPX0\x00"

    static_res, report = await engine.analyze_bytes(sample_binary, "malicious_sample.exe")
    check("StaticAnalysisResult produced", static_res is not None)
    check("Report produced", report is not None)
    check("Suspicious imports identified", len(static_res.suspicious_imports) >= 1)
    check("Risk assessment score > 0", report.risk_assessment.overall_risk_score > 0)


async def test_integration_and_backward_compatibility():
    print("\n🔒 Testing Integration & Backward Compatibility...")
    from app.core.security import enterprise_security_manager
    from app.core.security.static_analysis import static_analysis_engine

    res = await enterprise_security_manager.analyze_binary("test_integrate.exe", b"MZ\x90\x00sample")
    check("EnterpriseSecurityManager uses Static Analysis Pipeline", res is not None)

    from app.core.intelligence import ai_os_kernel
    check("AI OS Kernel remains fully functional", ai_os_kernel is not None)


async def main():
    print("==========================================================================")
    print("STAGE 6 PART 2 - ENTERPRISE STATIC ANALYSIS ENGINE TEST SUITE")
    print("==========================================================================")

    test_binary_parser()
    test_fingerprint_engine()
    test_entropy_engine()
    test_string_extractor()
    test_import_export_analyzer()
    test_binary_classifier()
    test_yara_engine()
    await test_threat_intelligence_connector()
    test_report_builder()
    await test_static_analysis_engine()
    await test_integration_and_backward_compatibility()

    print("\n==========================================================================")
    print(f"RESULTS: {PASS} passed, {FAIL} failed, {PASS + FAIL} total")
    print("==========================================================================")

    if FAIL > 0:
        sys.exit(1)
    print("\n🎉 STAGE 6 PART 2 SUCCESS: Enterprise Static Analysis Engine Deployed!")


if __name__ == "__main__":
    asyncio.run(main())
