"""
Pydantic schemas for goal-related API operations.

Defines request/response models for financial goals management.
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any
from datetime import date
from enum import Enum


class GoalType(str, Enum):
    """Types of financial goals supported by the system."""

    HOUSE_PURCHASE = "house_purchase"
    EMERGENCY_FUND = "emergency_fund"
    INVESTMENT = "investment"
    DEBT_PAYOFF = "debt_payoff"
    OTHER = "other"


class GoalStatus(str, Enum):
    """Status of a financial goal."""

    ACTIVE = "active"
    COMPLETED = "completed"
    PAUSED = "paused"
    CANCELLED = "cancelled"


class GoalBase(BaseModel):
    """Base goal schema with common fields."""

    name: str = Field(..., min_length=1, max_length=100, description="Goal name")
    description: Optional[str] = Field(
        None, max_length=500, description="Goal description"
    )
    goal_type: GoalType = Field(..., description="Type of financial goal")
    target_amount: int = Field(..., gt=0, description="Target amount in VND")
    target_date: date = Field(..., description="Target completion date")
    current_savings: int = Field(
        0, ge=0, description="Current savings toward goal in VND"
    )


class GoalCreate(GoalBase):
    """Schema for creating a new goal."""

    assumptions: Optional[Dict[str, Any]] = Field(
        None,
        description="Goal-specific assumptions (e.g., down payment %, inflation rate)",
    )

    @validator("target_date")
    def target_date_must_be_future(cls, v):
        if v <= date.today():
            raise ValueError("Target date must be in the future")
        return v


class GoalUpdate(BaseModel):
    """Schema for updating an existing goal."""

    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    target_amount: Optional[int] = Field(None, gt=0)
    target_date: Optional[date] = Field(None)
    current_savings: Optional[int] = Field(None, ge=0)
    status: Optional[GoalStatus] = Field(None)
    assumptions: Optional[Dict[str, Any]] = Field(None)

    @validator("target_date")
    def target_date_must_be_future(cls, v):
        if v and v <= date.today():
            raise ValueError("Target date must be in the future")
        return v


class GoalResponse(GoalBase):
    """Schema for goal response data."""

    id: int = Field(..., description="Goal's unique identifier")
    user_id: int = Field(..., description="ID of the user who owns this goal")
    status: GoalStatus = Field(..., description="Current status of the goal")
    assumptions: Dict[str, Any] = Field(..., description="Goal-specific assumptions")
    created_at: date = Field(..., description="Goal creation date")
    updated_at: date = Field(..., description="Goal last update date")
    progress_percentage: float = Field(
        ..., ge=0, le=100, description="Progress toward goal (0-100%)"
    )
    months_remaining: Optional[int] = Field(
        None, description="Months remaining to target date"
    )

    class Config:
        from_attributes = True


class GoalSummary(BaseModel):
    """Simplified goal summary for dashboard/overview."""

    id: int
    name: str
    goal_type: GoalType
    target_amount: int
    current_savings: int
    progress_percentage: float
    target_date: date
    status: GoalStatus
