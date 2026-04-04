"""
Tests for template API endpoints.

Tests the GET /api/templates endpoints and response formats.
"""

import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.services.template_service import TemplateService

client = TestClient(app)


class TestTemplateEndpoints:
    """Test cases for template API endpoints."""

    def test_get_all_templates(self):
        """Test GET /api/templates returns all templates."""
        response = client.get("/api/templates")

        assert response.status_code == 200
        data = response.json()

        assert "templates" in data
        assert "total_count" in data
        assert len(data["templates"]) == 2
        assert data["total_count"] == 2

    def test_get_all_templates_structure(self):
        """Test that template response has correct structure."""
        response = client.get("/api/templates")
        data = response.json()

        for template in data["templates"]:
            assert "id" in template
            assert "name_vi" in template
            assert "description_vi" in template
            assert "icon" in template
            assert "status" in template
            assert "wizard_steps" in template

    def test_get_home_purchase_template(self):
        """Test GET /api/templates/home_purchase returns correct template."""
        response = client.get("/api/templates/home_purchase")

        assert response.status_code == 200
        data = response.json()

        assert data["id"] == "home_purchase"
        assert data["name_vi"] == "Kế hoạch mua nhà"
        assert data["status"] == "available"
        assert len(data["wizard_steps"]) > 0

    def test_get_emergency_fund_template(self):
        """Test GET /api/templates/emergency_fund returns correct template."""
        response = client.get("/api/templates/emergency_fund")

        assert response.status_code == 200
        data = response.json()

        assert data["id"] == "emergency_fund"
        assert data["name_vi"] == "Kế hoạch quỹ khẩn cấp"
        assert data["status"] == "coming_soon"

    def test_get_template_not_found(self):
        """Test GET /api/templates/{id} returns 404 for invalid template."""
        response = client.get("/api/templates/invalid_template")

        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_available_templates_endpoint(self):
        """Test GET /api/templates/available/list returns only available templates."""
        response = client.get("/api/templates/available/list")

        assert response.status_code == 200
        data = response.json()

        assert len(data["templates"]) == 1
        assert data["templates"][0]["id"] == "home_purchase"
        assert data["templates"][0]["status"] == "available"

    def test_template_contains_vietnamese_text(self):
        """Test that templates contain Vietnamese translations."""
        response = client.get("/api/templates/home_purchase")
        data = response.json()

        # Check Vietnamese characters
        assert "Kế hoạch" in data["name_vi"]
        assert "hoạch" in data["description_vi"]


class TestTemplateService:
    """Test cases for TemplateService class."""

    def test_get_all_templates_count(self):
        """Test that TemplateService returns correct number of templates."""
        service = TemplateService()
        templates = service.get_all_templates()

        assert len(templates) == 2

    def test_get_available_templates_count(self):
        """Test that only available templates are returned."""
        service = TemplateService()
        templates = service.get_available_templates()

        assert len(templates) == 1
        assert templates[0].id == "home_purchase"

    def test_get_template_by_id_valid(self):
        """Test getting a template by valid ID."""
        service = TemplateService()
        template = service.get_template_by_id("home_purchase")

        assert template is not None
        assert template.id == "home_purchase"
        assert template.status == "available"

    def test_get_template_by_id_invalid(self):
        """Test getting a template by invalid ID returns None."""
        service = TemplateService()
        template = service.get_template_by_id("invalid_id")

        assert template is None

    def test_validate_template_exists_true(self):
        """Test template validation for existing template."""
        service = TemplateService()

        assert service.validate_template_exists("home_purchase") is True
        assert service.validate_template_exists("emergency_fund") is True

    def test_validate_template_exists_false(self):
        """Test template validation for non-existing template."""
        service = TemplateService()

        assert service.validate_template_exists("invalid_id") is False

    def test_validate_template_available_true(self):
        """Test availability validation for available template."""
        service = TemplateService()

        assert service.validate_template_available("home_purchase") is True

    def test_validate_template_available_false(self):
        """Test availability validation for coming-soon template."""
        service = TemplateService()

        assert service.validate_template_available("emergency_fund") is False

    def test_get_template_list_response(self):
        """Test getting formatted template list response."""
        service = TemplateService()
        response = service.get_template_list_response()

        assert response.total_count == 2
        assert len(response.templates) == 2
