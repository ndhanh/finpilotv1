"""
Service layer for plan template management.

Provides business logic for template operations.
"""

from typing import List, Optional
from ..config.templates import (
    PLAN_TEMPLATES,
    get_template_by_id,
    is_template_available,
    get_available_templates,
)
from ..schemas.template import TemplateResponse, TemplateListResponse


class TemplateService:
    """Service for managing plan templates."""

    def __init__(self):
        """Initialize template service."""
        self.templates = PLAN_TEMPLATES

    def get_all_templates(self) -> List[TemplateResponse]:
        """
        Get all available templates (including coming_soon).

        Returns:
            List of TemplateResponse objects
        """
        return [
            TemplateResponse(
                id=template["id"],
                name_vi=template["name_vi"],
                description_vi=template["description_vi"],
                icon=template["icon"],
                status=template["status"],
                wizard_steps=template["wizard_steps"],
            )
            for template in self.templates.values()
        ]

    def get_available_templates(self) -> List[TemplateResponse]:
        """
        Get only available templates (excluding coming_soon).

        Returns:
            List of TemplateResponse objects for available templates
        """
        available = get_available_templates()
        return [
            TemplateResponse(
                id=template["id"],
                name_vi=template["name_vi"],
                description_vi=template["description_vi"],
                icon=template["icon"],
                status=template["status"],
                wizard_steps=template["wizard_steps"],
            )
            for template in available.values()
        ]

    def get_template_by_id(self, template_id: str) -> Optional[TemplateResponse]:
        """
        Get a specific template by ID.

        Args:
            template_id: The template identifier

        Returns:
            TemplateResponse if found, None otherwise
        """
        template = get_template_by_id(template_id)
        if template is None:
            return None

        return TemplateResponse(
            id=template["id"],
            name_vi=template["name_vi"],
            description_vi=template["description_vi"],
            icon=template["icon"],
            status=template["status"],
            wizard_steps=template["wizard_steps"],
        )

    def validate_template_exists(self, template_id: str) -> bool:
        """
        Check if a template exists (regardless of availability status).

        Args:
            template_id: The template identifier

        Returns:
            True if template exists, False otherwise
        """
        return template_id in self.templates

    def validate_template_available(self, template_id: str) -> bool:
        """
        Check if a template is available for selection.

        Args:
            template_id: The template identifier

        Returns:
            True if template exists and is available, False otherwise
        """
        return is_template_available(template_id)

    def get_template_list_response(self) -> TemplateListResponse:
        """
        Get a formatted list response with all templates.

        Returns:
            TemplateListResponse with templates and count
        """
        templates = self.get_all_templates()
        return TemplateListResponse(
            templates=templates,
            total_count=len(templates),
        )
