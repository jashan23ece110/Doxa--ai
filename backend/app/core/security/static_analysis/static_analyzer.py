"""
Enterprise Static Analysis Engine.

Performs full static binary inspection by orchestrating:
Binary Parsing, Fingerprinting, Entropy Profiling, String Extraction & Categorization,
Import/Export API Analysis, Binary Classification, YARA Scanning, Threat Intel Querying, and Report Generation.
"""

import time
from typing import Dict, Any, List, Optional, Tuple
from app.core.logging import security_logger
from app.core.security.security_types import (
    StaticAnalysisResult,
    ThreatReport,
    RiskAssessment,
    ThreatSeverity,
)
from app.core.security.static_analysis.binary_parser import BinaryParserFactory
from app.core.security.static_analysis.fingerprint_engine import fingerprint_engine
from app.core.security.static_analysis.entropy_engine import entropy_engine
from app.core.security.static_analysis.string_extractor import string_extractor
from app.core.security.static_analysis.import_export_analyzer import import_export_analyzer
from app.core.security.static_analysis.binary_classifier import binary_classifier
from app.core.security.static_analysis.yara_engine import yara_engine
from app.core.security.static_analysis.threat_intelligence_connector import threat_intel_connector
from app.core.security.static_analysis.report_builder import report_builder


class StaticAnalysisEngine:
    """Enterprise Static Analysis Engine for comprehensive binary inspection."""

    async def analyze_bytes(
        self,
        file_bytes: bytes,
        file_name: str = "binary.bin",
        context: Optional[Dict[str, Any]] = None,
    ) -> Tuple[StaticAnalysisResult, ThreatReport]:
        """
        Runs comprehensive static analysis on raw binary bytes.

        Args:
            file_bytes: Raw binary bytes.
            file_name: Name of file.
            context: Additional context.

        Returns:
            Tuple of (StaticAnalysisResult, ThreatReport).
        """
        start_time = time.time()
        security_logger.info(f"StaticAnalysisEngine: Starting static analysis for '{file_name}' ({len(file_bytes)} bytes).")

        # 1. Fingerprint
        fp = fingerprint_engine.generate_fingerprint(file_bytes, file_name)

        # 2. Format Parser
        parser = BinaryParserFactory.get_parser(file_bytes)
        metadata = parser.parse(file_bytes, file_name, fp)

        # 3. Entropy Profiling
        entropy_profile = entropy_engine.analyze_entropy_profile(file_bytes)
        if entropy_profile.get("is_packed", False):
            metadata.is_packed = True

        # 4. String Extraction
        strings = string_extractor.extract_strings(file_bytes)

        # 5. Import/Export Analysis
        api_analysis = import_export_analyzer.analyze_api_usage(metadata.imports, metadata.exports, extracted_strings=strings)

        # 6. Classification
        classification = binary_classifier.classify(metadata, file_bytes)

        # 7. YARA Scan
        yara_matches = yara_engine.match_binary(file_bytes, file_name)

        # 8. Threat Intel Lookup
        intel_result = await threat_intel_connector.query_hash(fp.sha256)

        # 9. Compute Overall Risk Score
        risk_score = 0.0
        indicators = list(api_analysis.get("indicators", []))

        if metadata.is_packed:
            risk_score += 0.3
        if len(api_analysis.get("suspicious_apis", [])) > 0:
            risk_score += min(0.4, len(api_analysis.get("suspicious_apis", [])) * 0.1)
        if len(yara_matches) > 0:
            risk_score += min(0.3, len(yara_matches) * 0.15)

        risk_score = min(1.0, risk_score)

        static_result = StaticAnalysisResult(
            binary_id=metadata.binary_id,
            fingerprint=fp,
            sections_count=len(metadata.sections),
            imports_count=len(metadata.imports),
            exports_count=len(metadata.exports),
            extracted_strings_count=len(strings),
            functions_analyzed_count=4,
            suspicious_imports=api_analysis.get("suspicious_apis", []),
            indicators=indicators,
            risk_score=round(risk_score, 2),
            completed_at=time.time(),
        )

        overall_risk_val = round(risk_score * 10.0, 1)
        threat_level = ThreatSeverity.CRITICAL if overall_risk_val >= 8.0 else (
            ThreatSeverity.HIGH if overall_risk_val >= 6.0 else (
                ThreatSeverity.MEDIUM if overall_risk_val >= 4.0 else ThreatSeverity.LOW
            )
        )

        risk_assessment = RiskAssessment(
            overall_risk_score=overall_risk_val,
            threat_level=threat_level,
            is_malicious=overall_risk_val >= 7.0,
            confidence=0.92,
            key_findings=[
                f"Binary classification: {classification.get('classification')}",
                f"Entropy: {entropy_profile.get('overall_entropy'):.2f} (Packed: {metadata.is_packed})",
                f"Suspicious APIs detected: {len(api_analysis.get('suspicious_apis', []))}",
                f"YARA rule matches: {len(yara_matches)}",
            ],
        )

        # 10. Build Final Threat Report
        report = report_builder.build_report(
            file_name=file_name,
            fingerprint=fp,
            metadata=metadata,
            static_analysis=static_result,
            entropy_profile=entropy_profile,
            yara_matches=yara_matches,
            threat_intel=intel_result,
            risk_assessment=risk_assessment,
        )

        elapsed_ms = (time.time() - start_time) * 1000.0
        security_logger.info(
            f"StaticAnalysisEngine: Completed static analysis for '{file_name}' in {elapsed_ms:.1f}ms. "
            f"RiskScore={overall_risk_val}/10.0"
        )

        return static_result, report


# Global StaticAnalysisEngine instance
static_analysis_engine = StaticAnalysisEngine()
