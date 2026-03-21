"""
Financial calculation engines for FinPilot.

This package contains deterministic calculation engines for:
- Financial projections and goal planning
- Investment return calculations
- Debt management projections
- Emergency fund planning
- House purchase planning

All calculations follow Vietnamese financial regulations and
provide explainable, deterministic results.
"""

from .projection import (
    ProjectionCalculator,
    ProjectionInputs,
    ProjectionResult,
    MonthlyProjection,
)

__all__ = [
    "ProjectionCalculator",
    "ProjectionInputs",
    "ProjectionResult",
    "MonthlyProjection",
]
