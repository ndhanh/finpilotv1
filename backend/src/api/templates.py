"""
API endpoints for plan template management.

Provides endpoints for browsing and retrieving available plan templates.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from ..services.template_service import TemplateService
from ..schemas.template import TemplateResponse, TemplateListResponse

router = APIRouter()


def get_template_service() -> TemplateService:
    """Dependency injection for TemplateService."""
    return TemplateService()


@router.get("/templates", response_model=TemplateListResponse, status_code=200)
async def get_all_templates(
    service: TemplateService = Depends(get_template_service),
) -> TemplateListResponse:
    """Get all available plan templates.

    Returns both "available" and "coming_soon" templates so users can see
    what templates are planned for the future.

    Returns:
        TemplateListResponse containing all templates and count

    Example:
        GET /api/templates
        Response:
        {
            "templates": [
                {
                    "id": "home_purchase",
                    "name_vi": "Kế hoạch mua nhà",
                    "description_vi": "...",
                    "icon": "🏠",
                    "status": "available",
                    "wizard_steps": [...]
                },
                {
                    "id": "emergency_fund",
                    "name_vi": "Kế hoạch quỹ khẩn cấp",
                    "description_vi": "...",
                    "icon": "🚨",
                    "status": "coming_soon",
                    "wizard_steps": []
                }
            ],
            "total_count": 2
        }
    """
    return service.get_template_list_response()


@router.get(
    "/templates/{template_id}", response_model=TemplateResponse, status_code=200
)
async def get_template_by_id(
    template_id: str,
    service: TemplateService = Depends(get_template_service),
) -> TemplateResponse:
    """Get a specific plan template by ID.

    Args:
        template_id: The template identifier (e.g., 'home_purchase', 'emergency_fund')

    Returns:
        TemplateResponse with template details

    Raises:
        HTTPException: 404 if template not found

    Example:
        GET /api/templates/home_purchase
        Response:
        {
            "id": "home_purchase",
            "name_vi": "Kế hoạch mua nhà",
            "description_vi": "Lập kế hoạch mua nhà của bạn với các bước chi tiết",
            "icon": "🏠",
            "status": "available",
            "wizard_steps": ["goal", "amount", "assets", "debt", "savings", "timeline", "results", "review"]
        }
    """
    template = service.get_template_by_id(template_id)

    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Template '{template_id}' not found",
        )

    return template


@router.get(
    "/templates/available/list", response_model=TemplateListResponse, status_code=200
)
async def get_available_templates_only(
    service: TemplateService = Depends(get_template_service),
) -> TemplateListResponse:
    """Get only available plan templates (excluding coming_soon).

    This endpoint is useful when you only want to show templates that users
    can actually select to create a plan.

    Returns:
        TemplateListResponse containing only available templates

    Example:
        GET /api/templates/available/list
        Response:
        {
            "templates": [
                {
                    "id": "home_purchase",
                    "name_vi": "Kế hoạch mua nhà",
                    "description_vi": "...",
                    "icon": "🏠",
                    "status": "available",
                    "wizard_steps": [...]
                }
            ],
            "total_count": 1
        }
    """
    templates = service.get_available_templates()
    return TemplateListResponse(
        templates=templates,
        total_count=len(templates),
    )
