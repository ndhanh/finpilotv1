"""
Template configuration for financial planning.

Defines available plan templates and their properties.
"""

# Template definitions
PLAN_TEMPLATES = {
    "home_purchase": {
        "id": "home_purchase",
        "name_vi": "Kế hoạch mua nhà",
        "description_vi": "Lập kế hoạch mua nhà của bạn với các bước chi tiết",
        "icon": "🏠",
        "status": "available",
        "wizard_steps": [
            "goal",
            "amount",
            "assets",
            "debt",
            "savings",
            "timeline",
            "results",
            "review",
        ],
    },
    "emergency_fund": {
        "id": "emergency_fund",
        "name_vi": "Kế hoạch quỹ khẩn cấp",
        "description_vi": "Xây dựng quỹ dự phòng cho tình huống khẩn cấp",
        "icon": "🚨",
        "status": "coming_soon",
        "wizard_steps": [],
    },
}


def get_available_templates():
    """Get list of available (non-coming-soon) templates."""
    return {k: v for k, v in PLAN_TEMPLATES.items() if v["status"] == "available"}


def get_template_by_id(template_id: str):
    """Get a template by its ID."""
    return PLAN_TEMPLATES.get(template_id)


def is_template_available(template_id: str) -> bool:
    """Check if a template is available for selection."""
    template = get_template_by_id(template_id)
    return template is not None and template["status"] == "available"
