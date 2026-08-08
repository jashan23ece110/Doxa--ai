"""
Enterprise Static Analysis Report Builder.

Generates comprehensive Static Analysis Threat Reports containing binary summaries,
fingerprints, metadata, entropy analysis, imported APIs, extracted strings, YARA matches,
threat indicators, confidence scores, risk assessments, analyst notes, timelines, and recommendations.
Supports JSON and Markdown formatting.
"""

import json
import time
from typing import Dict, Any, List, Optional
from app.core.logging import security_logger
from app.core.security.security_types import ThreatReport, StaticAnalysisResult, RiskAssessment, FileFingerprint, BinaryMetadata


class ReportBuilder:
    """Enterprise Static Analysis Report Builder."""

    def build_report(
        self,
        file_name: str,
        fingerprint: FileFingerprint,
        metadata: BinaryMetadata,
        static_analysis: StaticAnalysisResult,
        entropy_profile: Dict[str, Any],
        yara_matches: List[Dict[str, Any]],
        threat_intel: Dict[str, Any],
        risk_assessment: RiskAssessment,
        analyst_notes: Optional[str] = None,
    ) -> ThreatReport:
        """
        Builds a comprehensive structured ThreatReport object.
        """
        summary = (
            f"Static binary analysis completed for '{file_name}'. "
            f"Format: {metadata.format.value.upper()} ({metadata.architecture.value}), "
            f"Entropy: {entropy_profile.get('overall_entropy', 0.0):.2f}, "
            f"Packed: {metadata.is_packed or entropy_profile.get('is_packed', False)}, "
            f"YARA Matches: {len(yara_matches)}, "
            f"Risk Score: {risk_assessment.overall_risk_score:.1f}/10.0 ({risk_assessment.threat_level.value.upper()})."
        )

        remediations = [
            "Maintain active endpoint detection and response (EDR) agents.",
            "Enforce strict execution controls on packed or high-entropy binaries.",
        ]
        if risk_assessment.is_malicious:
            remediations.append("Quarantine binary sample immediately.")
            remediations.append("Block associated network indicators across perimeter firewalls.")

        report = ThreatReport(
            title=f"Enterprise Static Analysis Report — {file_name}",
            binary_id=metadata.binary_id,
            risk_assessment=risk_assessment,
            static_analysis=static_analysis,
            summary=summary,
            remediation_steps=remediations,
            generated_at=time.time(),
        )

        security_logger.info(f"ReportBuilder: Built report '{report.report_id}' for '{file_name}'.")
        return report

    def to_markdown(self, report: ThreatReport, metadata: Optional[BinaryMetadata] = None, yara_matches: Optional[List[Dict[str, Any]]] = None) -> str:
        """Renders ThreatReport as formatted GitHub Markdown."""
        lines = [
            f"# {report.title}",
            f"**Report ID**: `{report.report_id}`  ",
            f"**Generated At**: {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime(report.generated_at))}  ",
            "",
            "## 🛡️ Executive Summary",
            report.summary,
            "",
        ]

        if report.risk_assessment:
            ra = report.risk_assessment
            lines.extend([
                "## ⚠️ Risk Assessment",
                f"- **Overall Risk Score**: `{ra.overall_risk_score:.1f} / 10.0`",
                f"- **Threat Level**: `{ra.threat_level.value.upper()}`",
                f"- **Is Malicious**: `{ra.is_malicious}`",
                f"- **Assessment Confidence**: `{ra.confidence * 100:.0f}%`",
                "",
                "### Key Findings",
            ])
            for f in ra.key_findings:
                lines.append(f"- {f}")
            lines.append("")

        if metadata:
            lines.extend([
                "## 🔍 Binary Metadata",
                f"- **File Name**: `{metadata.file_name}`",
                f"- **SHA256**: `{metadata.fingerprint.sha256}`",
                f"- **MD5**: `{metadata.fingerprint.md5}`",
                f"- **Format**: `{metadata.format.value.upper()}`",
                f"- **Architecture**: `{metadata.architecture.value}`",
                f"- **Is Packed**: `{metadata.is_packed}`",
                f"- **Sections Count**: `{len(metadata.sections)}`",
                "",
            ])

        if yara_matches:
            lines.extend([
                "## 🎯 YARA Rule Matches",
                f"Total Matches: **{len(yara_matches)}**",
            ])
            for m in yara_matches:
                lines.append(f"- **{m.get('rule_name')}** (Severity: {m.get('severity')})")
            lines.append("")

        lines.extend([
            "## 💡 Remediation Recommendations",
        ])
        for step in report.remediation_steps:
            lines.append(f"1. {step}")

        return "\n".join(lines)

    def to_json(self, report: ThreatReport) -> str:
        """Renders ThreatReport as JSON string."""
        return json.dumps(report.model_dump(), indent=2, default=str)


# Global ReportBuilder instance
report_builder = ReportBuilder()
