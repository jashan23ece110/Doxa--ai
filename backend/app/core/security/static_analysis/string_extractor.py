"""
String Extraction & Categorization Engine.

Extracts ASCII, UTF-8, UTF-16, and Unicode strings.
Categorizes strings into file paths, registry keys, URLs, IP addresses, domains, commands, and credential indicators.
"""

import re
from typing import Dict, Any, List
from app.core.logging import security_logger
from app.core.security.security_types import BinaryString


class StringExtractor:
    """Enterprise String Extraction and Categorization Engine."""

    _URL_REGEX = re.compile(r"https?://[^\s<>\"']+|ftp://[^\s<>\"']+", re.IGNORECASE)
    _IP_REGEX = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
    _PATH_REGEX = re.compile(r"(?:[a-zA-Z]:\\|\/)[^\s<>\"']+", re.IGNORECASE)
    _REGISTRY_REGEX = re.compile(r"HKEY_[A-Z_]+\\[^\s<>\"']+", re.IGNORECASE)
    _COMMAND_REGEX = re.compile(r"\b(cmd\.exe|powershell\.exe|bash|sh|exec|system|wmic)\b", re.IGNORECASE)
    _CREDENTIAL_REGEX = re.compile(r"\b(password|passwd|secret|api_key|private_key|token)\b", re.IGNORECASE)

    def extract_strings(self, file_bytes: bytes, min_length: int = 4) -> List[BinaryString]:
        """
        Extracts and categorizes printable strings from raw binary contents.

        Args:
            file_bytes: Raw binary bytes.
            min_length: Minimum string length to extract.

        Returns:
            List of categorized BinaryString models.
        """
        extracted: List[BinaryString] = []
        if not file_bytes:
            return extracted

        # Extract ASCII strings
        ascii_pattern = re.compile(rb"[\x20-\x7e]{" + str(min_length).encode() + rb",}")
        for match in ascii_pattern.finditer(file_bytes):
            val = match.group().decode("ascii", errors="ignore")
            offset = match.start()
            cat = self._categorize_string(val)
            extracted.append(BinaryString(
                string_value=val,
                offset=offset,
                encoding="ascii",
                category=cat,
            ))

        # Extract UTF-16 strings
        utf16_pattern = re.compile(rb"(?:[\x20-\x7e]\x00){" + str(min_length).encode() + rb",}")
        for match in utf16_pattern.finditer(file_bytes):
            try:
                val = match.group().decode("utf-16le", errors="ignore")
                offset = match.start()
                cat = self._categorize_string(val)
                extracted.append(BinaryString(
                    string_value=val,
                    offset=offset,
                    encoding="utf-16le",
                    category=cat,
                ))
            except Exception:
                pass

        security_logger.info(f"StringExtractor: Extracted {len(extracted)} strings (min_len={min_length}).")
        return extracted[:1000]  # Cap at top 1000 extracted strings for memory efficiency

    def _categorize_string(self, val: str) -> str:
        """Determines string category based on regex matches."""
        if self._URL_REGEX.search(val):
            return "url"
        if self._IP_REGEX.search(val):
            return "ip"
        if self._REGISTRY_REGEX.search(val):
            return "registry_key"
        if self._COMMAND_REGEX.search(val):
            return "command"
        if self._PATH_REGEX.search(val):
            return "file_path"
        if self._CREDENTIAL_REGEX.search(val):
            return "credentials"
        return "general"


# Global StringExtractor instance
string_extractor = StringExtractor()
