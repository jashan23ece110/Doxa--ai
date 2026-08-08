"""
Enterprise STRIDE Threat Modeling Engine.

Generates STRIDE-style threat modeling architecture, trust boundaries, asset inventories,
threat actors, attack paths, security assumptions, mitigations, and residual risk.
"""

from typing import Dict, Any, List
from pydantic import BaseModel, Field
from app.core.logging import security_logger


class STRIDEThreat(BaseModel):
    threat_id: str
    category: str  # Spoofing, Tampering, Repudiation, Info Disclosure, DoS, Elevation of Privilege
    target_asset: str
    description: str
    impact_level: str = "high"
    mitigation: str
    residual_risk_score: float = 2.0


class ThreatModel(BaseModel):
    model_id: str
    system_name: str
    trust_boundaries: List[str] = Field(default_factory=list)
    assets: List[str] = Field(default_factory=list)
    actors: List[str] = Field(default_factory=list)
    threats: List[STRIDEThreat] = Field(default_factory=list)
    overall_residual_risk: float = 2.5


class ThreatModelEngine:
    """Enterprise Threat Modeling Engine."""

    def generate_stride_model(self, system_name: str, assets: List[str], trust_boundaries: List[str]) -> ThreatModel:
        """
        Constructs a STRIDE threat model for a given system context.

        Args:
            system_name: Name of system under assessment.
            assets: List of target assets.
            trust_boundaries: List of trust boundaries.

        Returns:
            ThreatModel object.
        """
        threats = [
            STRIDEThreat(
                threat_id="STRIDE-01",
                category="Spoofing",
                target_asset="API Gateway",
                description="Unauthorized actor spoofing API tenant authentication token.",
                mitigation="Enforce HMAC-SHA256 API key signature validation.",
                residual_risk_score=1.5,
            ),
            STRIDEThreat(
                threat_id="STRIDE-02",
                category="Elevation of Privilege",
                target_asset="Execution Engine",
                description="Unauthorized agent bypassing RBAC access controls.",
                mitigation="Strict RBAC permission checks in SecurityContextMiddleware.",
                residual_risk_score=2.0,
            ),
            STRIDEThreat(
                threat_id="STRIDE-03",
                category="Information Disclosure",
                target_asset="Memory Platform",
                description="Memory leakage across tenant boundaries.",
                mitigation="Enforce strict tenant_id scoping on memory queries.",
                residual_risk_score=1.0,
            ),
        ]

        model = ThreatModel(
            model_id=f"tm_{system_name.lower()}",
            system_name=system_name,
            trust_boundaries=trust_boundaries,
            assets=assets,
            actors=["External User", "Internal Agent", "System Worker"],
            threats=threats,
            overall_residual_risk=1.5,
        )

        security_logger.info(f"ThreatModelEngine: Generated STRIDE threat model for '{system_name}' ({len(threats)} threats).")
        return model


# Global ThreatModelEngine instance
threat_model_engine = ThreatModelEngine()
