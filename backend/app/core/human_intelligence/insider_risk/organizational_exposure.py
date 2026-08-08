"""
Organizational Exposure Analyzer.

Evaluates department risk exposure, business unit exposure, project criticality,
critical asset exposure, trust dependency exposure, and communication concentration.
"""

from typing import Dict, Any, List
from pydantic import BaseModel, Field
from app.core.logging import security_logger


class DepartmentExposureMetrics(BaseModel):
    department_name: str
    exposure_score: float = 3.5  # 0 to 10 scale
    critical_asset_access_count: int = 12
    high_risk_employee_count: int = 1
    exposure_level: str = "LOW"  # LOW, MEDIUM, HIGH, CRITICAL


class OrganizationalExposureAnalyzer:
    """Enterprise Organizational Exposure Analyzer."""

    def calculate_department_exposure(self, department_name: str, high_risk_count: int = 0) -> DepartmentExposureMetrics:
        """
        Calculates organizational exposure score for a department.

        Args:
            department_name: Target department.
            high_risk_count: Number of high risk employees in department.

        Returns:
            DepartmentExposureMetrics model.
        """
        score = min(10.0, 2.0 + (high_risk_count * 2.5))
        level = "HIGH" if score >= 6.0 else "LOW"

        metrics = DepartmentExposureMetrics(
            department_name=department_name,
            exposure_score=score,
            critical_asset_access_count=15,
            high_risk_employee_count=high_risk_count,
            exposure_level=level,
        )

        security_logger.info(f"OrganizationalExposureAnalyzer: Analyzed exposure for department '{department_name}': ExposureScore={metrics.exposure_score}/10.0.")
        return metrics


# Global OrganizationalExposureAnalyzer instance
organizational_exposure_analyzer = OrganizationalExposureAnalyzer()
