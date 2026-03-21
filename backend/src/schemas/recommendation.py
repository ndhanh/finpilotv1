"""
Pydantic schemas for recommendation-related API operations.

Defines request/response models for financial recommendations.
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any
from enum import Enum


class RecommendationPriority(str, Enum):
    """Priority levels for recommendations."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class RecommendationCategory(str, Enum):
    """Categories of recommendations."""

    FEASIBILITY = "feasibility"
    DEBT_MANAGEMENT = "debt_management"
    SAVINGS_RATE = "savings_rate"
    TIMELINE = "timeline"
    RISK_ASSESSMENT = "risk_assessment"


class RecommendationItem(BaseModel):
    """Schema for individual recommendation."""

    category: RecommendationCategory = Field(..., description="Recommendation category")
    priority: RecommendationPriority = Field(..., description="Recommendation priority")
    title: str = Field(..., description="Recommendation title")
    description: str = Field(..., description="Detailed recommendation description")
    actionable_steps: List[str] = Field(..., description="Specific actionable steps")
    impact_score: int = Field(
        ..., ge=1, le=10, description="Impact score (1-10) indicating potential benefit"
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional context data for the recommendation",
    )


class RecommendationResponse(BaseModel):
    """Schema for recommendation API response."""

    recommendations: List[RecommendationItem] = Field(
        ..., description="List of personalized recommendations"
    )
    summary: Dict[str, Any] = Field(
        ..., description="Summary statistics about the recommendations"
    )


class RecommendationContext(BaseModel):
    """Schema for recommendation generation context."""

    target_amount: int = Field(..., gt=0, description="Goal target amount in VND")
    timeline_months: int = Field(..., gt=0, description="Goal timeline in months")
    monthly_contribution: int = Field(
        ..., ge=0, description="Monthly savings contribution in VND"
    )
    current_savings: int = Field(0, ge=0, description="Current savings in VND")
    current_debt: int = Field(0, ge=0, description="Current debt in VND")
    is_achievable: bool = Field(..., description="Whether goal is currently achievable")
    shortfall_amount: int = Field(
        0, ge=0, description="Shortfall amount if not achievable in VND"
    )
    estimated_monthly_income: Optional[int] = Field(
        None, description="Estimated monthly income in VND"
    )


class RecommendationFilter(BaseModel):
    """Schema for filtering recommendations."""

    categories: Optional[List[RecommendationCategory]] = Field(
        None, description="Filter by recommendation categories"
    )
    min_priority: Optional[RecommendationPriority] = Field(
        None, description="Minimum priority level to include"
    )
    max_impact_score: Optional[int] = Field(
        None, ge=1, le=10, description="Maximum impact score to include"
    )
