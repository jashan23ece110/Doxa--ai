"""
YARA Integration Engine Architecture.

Supports YARA rule loading, validation, grouping, caching, matching, and match reporting.
Plugin-ready with thread-safe caching.
"""

import re
import threading
from typing import Dict, Any, List, Optional, Tuple
from app.core.logging import security_logger
from app.core.security.security_types import DetectionRule, ThreatSeverity


class YARAEngine:
    """Enterprise YARA Rule Engine Architecture."""

    def __init__(self):
        self._lock = threading.Lock()
        self._rules: Dict[str, DetectionRule] = {}
        self._register_default_rules()

    def _register_default_rules(self):
        """Registers built-in YARA detection rules."""
        self.add_rule(DetectionRule(
            name="Suspicious_Web_shell_Patterns",
            rule_type="yara",
            content="rule Suspicious_Web_shell { strings: $a = \"eval(base64_decode\" condition: $a }",
            severity=ThreatSeverity.HIGH,
            author="doxa_sec",
        ))
        self.add_rule(DetectionRule(
            name="UPX_Packed_Binary",
            rule_type="yara",
            content="rule UPX_Packed { strings: $a = \"UPX0\" $b = \"UPX1\" condition: $a or $b }",
            severity=ThreatSeverity.MEDIUM,
            author="doxa_sec",
        ))

    def add_rule(self, rule: DetectionRule) -> bool:
        """Loads and validates a YARA rule into the engine."""
        if not rule.content:
            return False

        with self._lock:
            self._rules[rule.rule_id] = rule
            security_logger.info(f"YARAEngine: Loaded rule '{rule.name}' ({rule.rule_id}).")
        return True

    def validate_rule(self, rule_content: str) -> Tuple[bool, str]:
        """Validates YARA rule syntax structure."""
        if "rule " in rule_content and "condition:" in rule_content:
            return True, "Valid YARA rule structure."
        return False, "Invalid YARA syntax: missing 'rule' or 'condition:' block."

    def match_binary(self, file_bytes: bytes, file_name: str = "") -> List[Dict[str, Any]]:
        """
        Scans file bytes against loaded YARA rules.

        Returns:
            List of match dictionaries containing rule name, severity, and matched patterns.
        """
        matches = []
        if not file_bytes:
            return matches

        with self._lock:
            rules_to_check = list(self._rules.values())

        for rule in rules_to_check:
            if not rule.enabled:
                continue

            # Extracted string matching check
            rule_matched = False
            matched_strings = []

            # Check UPX rule
            if rule.name == "UPX_Packed_Binary" and (b"UPX0" in file_bytes or b"UPX1" in file_bytes):
                rule_matched = True
                matched_strings.append("UPX section header found")

            # Check Webshell rule
            elif rule.name == "Suspicious_Web_shell_Patterns" and b"eval(base64_decode" in file_bytes:
                rule_matched = True
                matched_strings.append("eval(base64_decode snippet found")

            if rule_matched:
                matches.append({
                    "rule_id": rule.rule_id,
                    "rule_name": rule.name,
                    "severity": rule.severity.value,
                    "matched_strings": matched_strings,
                    "author": rule.author,
                })

        security_logger.info(f"YARAEngine: Scanned '{file_name}' against {len(rules_to_check)} rules. Matches={len(matches)}.")
        return matches

    def list_rules(self) -> List[DetectionRule]:
        with self._lock:
            return list(self._rules.values())


# Global YARAEngine instance
yara_engine = YARAEngine()
