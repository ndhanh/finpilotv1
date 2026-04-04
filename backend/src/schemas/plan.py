"""
Pydantic schemas for plan-related API operations.

Defines request/response models for financial plans management.
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from .goal import GoalResponse, GoalSummary


class PlanBase(BaseModel):
    """Base plan schema with common fields."""

    name: str = Field(..., min_length=1, max_length=100, description="Plan name")
    description: Optional[str] = Field(
        None, max_length=500, description="Plan description"
    )


class PlanCreate(PlanBase):
    """Schema for creating a new plan."""

    template_id: str = Field(
        default="home_purchase",
        description="ID of the plan template to use (home_purchase or emergency_fund)",
    )


class PlanUpdate(BaseModel):
    """Schema for updating an existing plan."""

    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)


class PlanResponse(PlanBase):
    """Schema for plan response data."""

    id: int = Field(..., description="Plan's unique identifier")
    user_id: int = Field(..., description="ID of the user who owns this plan")
    template_id: str = Field(..., description="ID of the plan template used")
    goals: List[GoalSummary] = Field(..., description="Goals associated with this plan")
    total_target_amount: int = Field(..., description="Sum of all goal target amounts")
    total_current_savings: int = Field(
        ..., description="Sum of all goal current savings"
    )
    overall_progress_percentage: float = Field(
        ..., ge=0, le=100, description="Overall progress across all goals (0-100%)"
    )
    created_at: datetime = Field(..., description="Plan creation timestamp")
    updated_at: datetime = Field(..., description="Plan last update timestamp")

    class Config:
        from_attributes = True


class PlanSummary(BaseModel):
    """Simplified plan summary for listings."""

    id: int
    name: str
    template_id: str
    total_target_amount: int
    total_current_savings: int
    overall_progress_percentage: float
    goal_count: int
    created_at: datetime
    updated_at: datetime
