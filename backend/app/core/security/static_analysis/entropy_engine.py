"""
Entropy Analysis Engine.

Detects packed binaries, encrypted sections, compressed payloads,
and abnormal entropy distributions. Generates visual entropy profile data.
"""

import math
from typing import Dict, Any, List
from app.core.logging import security_logger
from app.core.security.security_types import BinarySection


class EntropyEngine:
    """Enterprise Entropy Analysis Engine."""

    @staticmethod
    def calculate_shannon_entropy(data: bytes) -> float:
        """Calculates Shannon entropy for byte buffer (0.0 to 8.0)."""
        if not data:
            return 0.0
        counts = [0] * 256
        for b in data:
            counts[b] += 1
        entropy = 0.0
        length = len(data)
        for c in counts:
            if c > 0:
                p = c / length
                entropy -= p * math.log2(p)
        return round(entropy, 4)

    def analyze_entropy_profile(self, file_bytes: bytes, block_size: int = 1024) -> Dict[str, Any]:
        """
        Generates a block-by-block entropy distribution profile for visualization.

        Args:
            file_bytes: Full binary contents.
            block_size: Size of block slice in bytes.

        Returns:
            Dict containing average entropy, max entropy, and chunk profile data points.
        """
        if not file_bytes:
            return {"overall_entropy": 0.0, "is_packed": False, "entropy_profile": []}

        overall_entropy = self.calculate_shannon_entropy(file_bytes)
        profile_data: List[float] = []

        for i in range(0, len(file_bytes), block_size):
            chunk = file_bytes[i:i + block_size]
            profile_data.append(self.calculate_shannon_entropy(chunk))

        is_packed = overall_entropy >= 7.2 or any(score >= 7.6 for score in profile_data)
        has_encrypted_sections = any(score >= 7.8 for score in profile_data)

        security_logger.info(
            f"EntropyEngine: Analyzed {len(file_bytes)} bytes across {len(profile_data)} blocks. "
            f"Overall Entropy={overall_entropy:.2f}, Packed={is_packed}"
        )

        return {
            "overall_entropy": overall_entropy,
            "max_block_entropy": max(profile_data) if profile_data else 0.0,
            "is_packed": is_packed,
            "has_encrypted_sections": has_encrypted_sections,
            "total_blocks": len(profile_data),
            "entropy_profile": profile_data[:100],  # Return up to 100 data points for UI plotting
        }

    def inspect_sections(self, sections: List[BinarySection]) -> List[Dict[str, Any]]:
        """Inspects binary sections for abnormal high-entropy characteristics."""
        anomalies = []
        for sec in sections:
            if sec.entropy >= 7.0:
                anomalies.append({
                    "section_name": sec.name,
                    "entropy": sec.entropy,
                    "reason": "High entropy indicates compression or encryption payload.",
                })
        return anomalies


# Global EntropyEngine instance
entropy_engine = EntropyEngine()
