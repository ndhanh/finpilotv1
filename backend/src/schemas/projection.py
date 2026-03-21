"""
Pydantic schemas for projection-related API operations.

Defines request/response models for financial projections and calculations.
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import date
from decimal import Decimal


class ProjectionInput(BaseModel):
    """Schema for projection calculation input."""

    target_amount: int = Field(..., gt=0, description="Target goal amount in VND")
    timeline_years: int = Field(
        ..., ge=1, le=30, description="Timeline in years (1-30)"
    )
    monthly_contribution: int = Field(
        ..., ge=0, description="Monthly savings contribution in VND"
    )
    current_savings: int = Field(0, ge=0, description="Current savings amount in VND")
    current_debt: int = Field(0, ge=0, description="Current debt amount in VND")
    expected_return_rate: float = Field(
        0.07, ge=0, le=0.12, description="Expected annual return rate (0-12%)"
    )
    inflation_rate: float = Field(
        0.04, ge=0, le=0.10, description="Expected annual inflation rate (0-10%)"
    )
    debt_interest_rate: float = Field(
        0.12, ge=0, le=0.24, description="Annual debt interest rate (0-24%)"
    )
    start_date: Optional[date] = Field(None, description="Projection start date")

    @validator("timeline_years")
    def validate_timeline(cls, v):
        if v < 1:
            raise ValueError("Timeline must be at least 1 year")
        if v > 30:
            raise ValueError("Timeline cannot exceed 30 years")
        return v

    @validator("expected_return_rate", "inflation_rate", "debt_interest_rate")
    def validate_rates(cls, v):
        if v < 0:
            raise ValueError("Rate cannot be negative")
        return v


class MonthlyProjectionData(BaseModel):
    """Schema for individual monthly projection data."""

    month: int = Field(..., ge=1, description="Month number in projection")
    year: int = Field(..., ge=2020, description="Year of projection")
    savings_balance: int = Field(
        ..., ge=0, description="Savings balance at end of month in VND"
    )
    debt_balance: int = Field(
        ..., ge=0, description="Debt balance at end of month in VND"
    )
    net_worth: int = Field(..., description="Net worth at end of month in VND")
    monthly_contribution: int = Field(
        ..., ge=0, description="Monthly contribution amount in VND"
    )
    investment_growth: int = Field(
        ..., ge=0, description="Investment growth for the month in VND"
    )
    debt_payment: int = Field(
        ..., ge=0, description="Debt payment for the month in VND"
    )
    cumulative_savings: int = Field(
        ..., ge=0, description="Cumulative savings to date in VND"
    )
    cumulative_investments: int = Field(
        ..., ge=0, description="Cumulative investment growth in VND"
    )


class ProjectionResult(BaseModel):
    """Schema for complete projection calculation result."""

    is_achievable: bool = Field(
        ..., description="Whether the goal is achievable with given inputs"
    )
    total_months: int = Field(
        ..., ge=0, description="Total months in projection timeline"
    )
    final_savings: int = Field(..., ge=0, description="Final savings balance in VND")
    final_debt: int = Field(..., ge=0, description="Final debt balance in VND")
    final_net_worth: int = Field(..., description="Final net worth in VND")
    total_contributions: int = Field(
        ..., ge=0, description="Total contributions over timeline in VND"
    )
    total_investment_growth: int = Field(
        ..., ge=0, description="Total investment growth over timeline in VND"
    )
    monthly_projections: List[MonthlyProjectionData] = Field(
        ..., description="Detailed monthly projection data"
    )
    shortfall_amount: int = Field(
        ..., ge=0, description="Amount short of goal if not achievable in VND"
    )
    recommended_monthly_increase: int = Field(
        0, ge=0, description="Recommended monthly increase to achieve goal in VND"
    )
    break_even_month: Optional[int] = Field(
        None, description="Month when goal is achieved"
    )


class ProjectionOutput(BaseModel):
    """Schema for projection API response."""

    input: ProjectionInput = Field(..., description="Original input parameters")
    result: ProjectionResult = Field(..., description="Calculation results")
    calculation_metadata: Dict[str, Any] = Field(
        ..., description="Metadata about the calculation (assumptions, version, etc.)"
    )


class ProjectionScenario(BaseModel):
    """Schema for projection scenario comparison."""

    name: str = Field(..., description="Scenario name")
    input: ProjectionInput = Field(..., description="Scenario input parameters")
    result: ProjectionResult = Field(..., description="Scenario calculation results")


class ProjectionComparison(BaseModel):
    """Schema for comparing multiple projection scenarios."""

    scenarios: List[ProjectionScenario] = Field(
        ..., description="List of scenarios to compare"
    )
    comparison_summary: Dict[str, Any] = Field(
        ..., description="Summary of differences between scenarios"
    )
