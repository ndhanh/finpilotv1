"""
Tests for TemplateService.

Tests the business logic for template management.
"""

import pytest
from src.services.template_service import TemplateService
from src.schemas.template import TemplateResponse, TemplateListResponse


class TestTemplateServiceInit:
    """Test TemplateService initialization."""

    def test_service_initializes(self):
        """Test that TemplateService initializes without errors."""
        service = TemplateService()
        assert service is not None
        assert service.templates is not None

    def test_templates_loaded(self):
        """Test that templates are loaded on initialization."""
        service = TemplateService()
        assert len(service.templates) == 2


class TestGetAllTemplates:
    """Test get_all_templates method."""

    def test_returns_list(self):
        """Test that get_all_templates returns a list."""
        service = TemplateService()
        result = service.get_all_templates()
        assert isinstance(result, list)

    def test_returns_correct_count(self):
        """Test that all templates are returned."""
        service = TemplateService()
        result = service.get_all_templates()
        assert len(result) == 2

    def test_returns_template_responses(self):
        """Test that returned items are TemplateResponse objects."""
        service = TemplateService()
        result = service.get_all_templates()
        assert all(isinstance(t, TemplateResponse) for t in result)

    def test_includes_home_purchase(self):
        """Test that home_purchase template is included."""
        service = TemplateService()
        result = service.get_all_templates()
        ids = [t.id for t in result]
        assert "home_purchase" in ids

    def test_includes_emergency_fund(self):
        """Test that emergency_fund template is included."""
        service = TemplateService()
        result = service.get_all_templates()
        ids = [t.id for t in result]
        assert "emergency_fund" in ids


class TestGetAvailableTemplates:
    """Test get_available_templates method."""

    def test_returns_only_available(self):
        """Test that only available templates are returned."""
        service = TemplateService()
        result = service.get_available_templates()

        assert len(result) == 1
        assert result[0].status == "available"

    def test_excludes_coming_soon(self):
        """Test that coming_soon templates are excluded."""
        service = TemplateService()
        result = service.get_available_templates()

        ids = [t.id for t in result]
        assert "emergency_fund" not in ids

    def test_returns_home_purchase_only(self):
        """Test that home_purchase is the only available template."""
        service = TemplateService()
        result = service.get_available_templates()

        assert len(result) == 1
        assert result[0].id == "home_purchase"


class TestGetTemplateById:
    """Test get_template_by_id method."""

    def test_returns_template_response(self):
        """Test that method returns TemplateResponse object."""
        service = TemplateService()
        result = service.get_template_by_id("home_purchase")

        assert isinstance(result, TemplateResponse)

    def test_returns_correct_template(self):
        """Test that correct template is returned."""
        service = TemplateService()
        result = service.get_template_by_id("home_purchase")

        assert result.id == "home_purchase"
        assert result.name_vi == "Kế hoạch mua nhà"

    def test_returns_none_for_invalid_id(self):
        """Test that None is returned for invalid ID."""
        service = TemplateService()
        result = service.get_template_by_id("invalid_id")

        assert result is None

    def test_returns_coming_soon_template(self):
        """Test that coming_soon templates can be retrieved."""
        service = TemplateService()
        result = service.get_template_by_id("emergency_fund")

        assert result is not None
        assert result.status == "coming_soon"


class TestValidateTemplateExists:
    """Test validate_template_exists method."""

    def test_returns_true_for_existing_template(self):
        """Test that True is returned for existing templates."""
        service = TemplateService()

        assert service.validate_template_exists("home_purchase") is True
        assert service.validate_template_exists("emergency_fund") is True

    def test_returns_false_for_non_existing_template(self):
        """Test that False is returned for non-existing templates."""
        service = TemplateService()

        assert service.validate_template_exists("invalid_id") is False
        assert service.validate_template_exists("") is False

    def test_validates_all_templates(self):
        """Test validation for all known templates."""
        service = TemplateService()

        for template_id in service.templates.keys():
            assert service.validate_template_exists(template_id) is True


class TestValidateTemplateAvailable:
    """Test validate_template_available method."""

    def test_returns_true_for_available_template(self):
        """Test that True is returned for available templates."""
        service = TemplateService()

        assert service.validate_template_available("home_purchase") is True

    def test_returns_false_for_coming_soon_template(self):
        """Test that False is returned for coming_soon templates."""
        service = TemplateService()

        assert service.validate_template_available("emergency_fund") is False

    def test_returns_false_for_non_existing_template(self):
        """Test that False is returned for non-existing templates."""
        service = TemplateService()

        assert service.validate_template_available("invalid_id") is False


class TestGetTemplateListResponse:
    """Test get_template_list_response method."""

    def test_returns_template_list_response(self):
        """Test that method returns TemplateListResponse object."""
        service = TemplateService()
        result = service.get_template_list_response()

        assert isinstance(result, TemplateListResponse)

    def test_response_has_correct_count(self):
        """Test that response contains correct total count."""
        service = TemplateService()
        result = service.get_template_list_response()

        assert result.total_count == 2
        assert len(result.templates) == result.total_count

    def test_response_templates_are_valid(self):
        """Test that all templates in response are valid."""
        service = TemplateService()
        result = service.get_template_list_response()

        assert all(isinstance(t, TemplateResponse) for t in result.templates)
        assert all(t.id is not None for t in result.templates)
        assert all(t.name_vi is not None for t in result.templates)


class TestTemplateWizardSteps:
    """Test template wizard steps."""

    def test_home_purchase_has_wizard_steps(self):
        """Test that home_purchase template has wizard steps defined."""
        service = TemplateService()
        result = service.get_template_by_id("home_purchase")

        assert len(result.wizard_steps) > 0
        assert "goal" in result.wizard_steps
        assert "amount" in result.wizard_steps

    def test_emergency_fund_has_no_wizard_steps(self):
        """Test that emergency_fund template has no wizard steps (coming soon)."""
        service = TemplateService()
        result = service.get_template_by_id("emergency_fund")

        assert len(result.wizard_steps) == 0
