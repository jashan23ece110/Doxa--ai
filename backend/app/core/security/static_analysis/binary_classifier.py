"""
Binary Classifier Engine.

Classifies binary files into:
Executable, Library, Driver, Firmware, Script, Installer, Archive, or Unknown
with confidence scoring.
"""

from typing import Dict, Any
from app.core.logging import security_logger
from app.core.security.security_types import BinaryMetadata, FileFormat


class BinaryClassifier:
    """Enterprise Binary Classifier Engine."""

    def classify(self, metadata: BinaryMetadata, file_bytes: bytes) -> Dict[str, Any]:
        """
        Determines binary category and classification confidence score.

        Returns:
            Dict containing classification, confidence, and details.
        """
        classification = "unknown"
        confidence = 0.5

        if metadata.format == FileFormat.PE:
            if metadata.subsystem.lower().startswith("driver") or "sys" in metadata.file_name.lower():
                classification = "driver"
                confidence = 0.95
            elif len(metadata.exports) > 0 and metadata.file_name.lower().endswith(".dll"):
                classification = "library"
                confidence = 0.95
            else:
                classification = "executable"
                confidence = 0.90

        elif metadata.format == FileFormat.ELF:
            if metadata.file_name.lower().endswith(".so"):
                classification = "library"
                confidence = 0.95
            else:
                classification = "executable"
                confidence = 0.90

        elif metadata.format == FileFormat.MACHO:
            if metadata.file_name.lower().endswith((".dylib", ".framework")):
                classification = "library"
                confidence = 0.95
            else:
                classification = "executable"
                confidence = 0.90

        elif file_bytes.startswith(b"PK\x03\x04"):
            classification = "archive"
            confidence = 0.98

        elif any(file_bytes.startswith(p) for p in [b"#!/bin/", b"#!/usr/", b"<?php", b"<html"]):
            classification = "script"
            confidence = 0.90

        security_logger.info(
            f"BinaryClassifier: Classified '{metadata.file_name}' as '{classification}' (confidence={confidence:.2f})."
        )

        return {
            "classification": classification,
            "confidence_score": confidence,
            "format": metadata.format.value,
            "architecture": metadata.architecture.value,
        }


# Global BinaryClassifier instance
binary_classifier = BinaryClassifier()
