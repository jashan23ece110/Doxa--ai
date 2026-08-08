"""
Enterprise AI Compliance Engine.

Supports GDPR, SOC2, ISO 27001, and HIPAA-ready compliance with PII detection,
sensitive information classification, automatic redaction, and audit metadata generation.
"""

import asyncio
import re
import time
from typing import Dict, Any, List
from app.core.logging import logger
from app.core.config import settings
from app.core.safety.safety_types import (
    ComplianceStandard,
    ComplianceResult,
    PIIDetection,
    PIICategory,
    RedactionResult,
)


class ComplianceEngine:
    """Enterprise compliance engine with PII detection and automatic redaction."""

    # ── PII Detection Patterns ──
    _PII_PATTERNS: Dict[PIICategory, re.Pattern] = {
        PIICategory.EMAIL: re.compile(
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        ),
        PIICategory.PHONE: re.compile(
            r"\b(?:\+?1[-.\s]?)?(?:\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}\b"
        ),
        PIICategory.SSN: re.compile(
            r"\b\d{3}[-\s]?\d{2}[-\s]?\d{4}\b"
        ),
        PIICategory.CREDIT_CARD: re.compile(
            r"\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13}|6(?:011|5[0-9]{2})[0-9]{12})\b"
        ),
        PIICategory.IP_ADDRESS: re.compile(
            r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
        ),
        PIICategory.DATE_OF_BIRTH: re.compile(
            r"\b(?:0[1-9]|1[0-2])[/\-](?:0[1-9]|[12][0-9]|3[01])[/\-](?:19|20)\d{2}\b"
        ),
        PIICategory.CREDENTIALS: re.compile(
            r"(?:password|passwd|secret|api_key|token|auth)\s*[:=]\s*\S+",
            re.IGNORECASE,
        ),
        PIICategory.MEDICAL: re.compile(
            r"\b(?:diagnosis|prescription|patient\s+id|medical\s+record|mrn|icd[-\s]?\d{1,2})\b",
            re.IGNORECASE,
        ),
        PIICategory.FINANCIAL: re.compile(
            r"\b(?:account\s*(?:number|#|no)|routing\s*(?:number|#)|iban|swift|bic)\s*[:=]?\s*\S+\b",
            re.IGNORECASE,
        ),
    }

    # ── Compliance Check Definitions ──
    _COMPLIANCE_CHECKS: Dict[ComplianceStandard, List[Dict[str, Any]]] = {
        ComplianceStandard.GDPR: [
            {"name": "pii_protection", "description": "All PII must be detected and handled."},
            {"name": "data_minimization", "description": "Only necessary data should be processed."},
            {"name": "right_to_erasure", "description": "Data deletion must be supported."},
            {"name": "consent_tracking", "description": "Processing consent must be documented."},
            {"name": "breach_notification", "description": "Breach detection and notification ready."},
            {"name": "data_portability", "description": "Data export capability required."},
        ],
        ComplianceStandard.SOC2: [
            {"name": "access_controls", "description": "Role-based access controls enforced."},
            {"name": "audit_logging", "description": "Complete audit trail maintained."},
            {"name": "encryption", "description": "Data encrypted at rest and in transit."},
            {"name": "change_management", "description": "Change tracking and approval processes."},
            {"name": "incident_response", "description": "Incident detection and response procedures."},
        ],
        ComplianceStandard.ISO27001: [
            {"name": "risk_assessment", "description": "Information security risk assessment."},
            {"name": "access_management", "description": "Access management controls."},
            {"name": "cryptography", "description": "Cryptographic controls implemented."},
            {"name": "operations_security", "description": "Operational security procedures."},
            {"name": "communications_security", "description": "Network security controls."},
            {"name": "supplier_relations", "description": "Third-party security management."},
        ],
        ComplianceStandard.HIPAA: [
            {"name": "phi_protection", "description": "Protected Health Information safeguards."},
            {"name": "access_controls", "description": "Minimum necessary access controls."},
            {"name": "audit_controls", "description": "Hardware, software, and procedural audit."},
            {"name": "transmission_security", "description": "Data transmission encryption."},
            {"name": "breach_notification", "description": "Breach assessment and notification."},
            {"name": "business_associate", "description": "Business associate agreements."},
        ],
    }

    # ── PII Detection ──

    async def detect_pii(self, text: str) -> List[PIIDetection]:
        """
        Detects PII in the given text.

        Returns:
            List of PIIDetection instances with categories and positions.
        """
        detections: List[PIIDetection] = []
        if not text:
            return detections

        for category, pattern in self._PII_PATTERNS.items():
            for match in pattern.finditer(text):
                detections.append(PIIDetection(
                    category=category,
                    matched_text="[REDACTED]",
                    start_index=match.start(),
                    end_index=match.end(),
                    confidence=0.90 if category != PIICategory.IP_ADDRESS else 0.75,
                ))

        return detections

    # ── Redaction ──

    async def redact_text(self, text: str) -> RedactionResult:
        """
        Detects and redacts all PII from the given text.

        Returns:
            RedactionResult with redacted text and detection metadata.
        """
        if not text:
            return RedactionResult(redacted_text=text)

        detections = await self.detect_pii(text)
        if not detections:
            return RedactionResult(
                original_length=len(text),
                redacted_length=len(text),
                redacted_text=text,
                pii_found=False,
            )

        # Sort detections by start index descending to avoid offset issues
        sorted_detections = sorted(detections, key=lambda d: d.start_index, reverse=True)
        redacted = text
        for det in sorted_detections:
            placeholder = f"[{det.category.value.upper()}_REDACTED]"
            redacted = redacted[:det.start_index] + placeholder + redacted[det.end_index:]

        return RedactionResult(
            original_length=len(text),
            redacted_length=len(redacted),
            detections=detections,
            pii_found=True,
            redacted_text=redacted,
        )

    # ── Compliance Evaluation ──

    async def evaluate_compliance(
        self,
        standard: ComplianceStandard,
        context: Dict[str, Any] = None,
    ) -> ComplianceResult:
        """
        Evaluates compliance against a specific standard.

        Args:
            standard: The compliance standard to evaluate.
            context: Dict with keys like:
                - text (str): Text to scan for PII.
                - has_audit_logging (bool): Whether audit logging is active.
                - has_encryption (bool): Whether encryption is enabled.
                - has_access_controls (bool): Whether RBAC is enforced.
                - has_breach_notification (bool): Whether breach detection is active.
                - has_consent_tracking (bool): Whether consent is tracked.

        Returns:
            ComplianceResult with violation details.
        """
        if not settings.COMPLIANCE_ENABLED:
            return ComplianceResult(standard=standard, is_compliant=True)

        start = time.time()
        ctx = context or {}
        violations: List[str] = []

        checks = self._COMPLIANCE_CHECKS.get(standard, [])

        # Run text-level PII scan if text is provided
        text = ctx.get("text", "")
        pii_detections: List[PIIDetection] = []
        if text:
            pii_detections = await self.detect_pii(text)

        # Evaluate framework checks
        capability_map = {
            "access_controls": ctx.get("has_access_controls", True),
            "access_management": ctx.get("has_access_controls", True),
            "audit_logging": ctx.get("has_audit_logging", True),
            "audit_controls": ctx.get("has_audit_logging", True),
            "encryption": ctx.get("has_encryption", True),
            "cryptography": ctx.get("has_encryption", True),
            "transmission_security": ctx.get("has_encryption", True),
            "breach_notification": ctx.get("has_breach_notification", True),
            "incident_response": ctx.get("has_breach_notification", True),
            "consent_tracking": ctx.get("has_consent_tracking", True),
            "change_management": ctx.get("has_change_management", True),
            "risk_assessment": ctx.get("has_risk_assessment", True),
            "operations_security": ctx.get("has_operations_security", True),
            "communications_security": ctx.get("has_communications_security", True),
            "supplier_relations": ctx.get("has_supplier_relations", True),
            "data_minimization": ctx.get("has_data_minimization", True),
            "right_to_erasure": ctx.get("has_right_to_erasure", True),
            "data_portability": ctx.get("has_data_portability", True),
            "business_associate": ctx.get("has_business_associate", True),
        }

        for check in checks:
            check_name = check["name"]
            # PII / PHI checks
            if check_name in ("pii_protection", "phi_protection"):
                if pii_detections:
                    violations.append(
                        f"{check_name}: {len(pii_detections)} PII instance(s) detected — "
                        f"redaction required."
                    )
                continue

            # Capability checks
            if check_name in capability_map and not capability_map[check_name]:
                violations.append(f"{check_name}: {check['description']} — NOT IMPLEMENTED.")

        elapsed = (time.time() - start) * 1000

        result = ComplianceResult(
            standard=standard,
            is_compliant=len(violations) == 0,
            violations=violations,
            pii_detections=pii_detections,
            redaction_applied=False,
            audit_metadata={
                "standard": standard.value,
                "checks_performed": len(checks),
                "violations_found": len(violations),
                "pii_instances": len(pii_detections),
                "evaluation_duration_ms": round(elapsed, 2),
            },
        )

        logger.info(
            f"ComplianceEngine evaluated {standard.value}: "
            f"Compliant={result.is_compliant}, Violations={len(violations)}, "
            f"PII={len(pii_detections)}, Duration={elapsed:.2f}ms"
        )
        return result

    async def evaluate_all_standards(
        self,
        context: Dict[str, Any] = None,
    ) -> List[ComplianceResult]:
        """Evaluates compliance across all supported standards."""
        results = []
        for standard in ComplianceStandard:
            result = await self.evaluate_compliance(standard, context)
            results.append(result)
        return results


# Global ComplianceEngine instance
compliance_engine = ComplianceEngine()
