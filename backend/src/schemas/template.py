"""
Pydantic schemas for plan templates.

Defines request/response models for plan template operations.
"""

from pydantic import BaseModel, Field
from typing import List


class TemplateResponse(BaseModel):
    """Schema for returning a single plan template."""

    id: str = Field(
        ..., description="Template unique identifier (e.g., 'home_purchase')"
    )
    name_vi: str = Field(..., description="Template name in Vietnamese")
    description_vi: str = Field(..., description="Template description in Vietnamese")
    icon: str = Field(..., description="Icon emoji or name representing the template")
    status: str = Field(
        ..., description="Template status: 'available' or 'coming_soon'"
    )
    wizard_steps: List[str] = Field(
        ...,
        description="List of form steps in the wizard (e.g., ['goal', 'amount', ...])",
    )

    class Config:
        from_attributes = True


class TemplateListResponse(BaseModel):
    """Schema for returning a list of plan templates."""

    templates: List[TemplateResponse] = Field(
        ..., description="List of available templates"
    )
    total_count: int = Field(..., description="Total number of templates")

    class Config:
        from_attributes = True
