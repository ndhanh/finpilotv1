"""
API contract tests for projection endpoints.

Tests the projection calculation and retrieval endpoints,
verifying request/response contract and business logic.
"""

import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.schemas.projection import ProjectionInput

client = TestClient(app)


class TestProjectionEndpoints:
    """Test cases for projection API endpoints."""

    def test_calculate_projection_achievable(self):
        """Test calculating an achievable projection."""
        payload = {
            "target_amount": 100_000_000,
            "timeline_years": 5,
            "monthly_savings": 5_000_000,
            "current_savings": 0,
            "current_debt": 0,
        }

        response = client.post(
            "/api/v1/projections/calculate?goal_id=1&user_id=1",
            json=payload,
        )

        assert response.status_code == 201
        data = response.json()

        # Verify response structure
        assert "is_achievable" in data
        assert "total_months" in data
        assert "final_savings" in data
        assert "final_debt" in data
        assert "final_net_worth" in data
        assert "monthly_projections" in data

    def test_calculate_projection_response_structure(self):
        """Test that projection response has correct structure."""
        payload = {
            "target_amount": 100_000_000,
            "timeline_years": 5,
            "monthly_savings": 5_000_000,
            "current_savings": 0,
            "current_debt": 0,
        }

        response = client.post(
            "/api/v1/projections/calculate?goal_id=1&user_id=1",
            json=payload,
        )

        assert response.status_code == 201
        data = response.json()

        # Check all required fields
        assert isinstance(data["is_achievable"], bool)
        assert isinstance(data["total_months"], int)
        assert isinstance(data["final_savings"], int)
        assert isinstance(data["final_debt"], int)
        assert isinstance(data["final_net_worth"], int)
        assert isinstance(data["total_contributions"], int)
        assert isinstance(data["total_investment_growth"], int)
        assert isinstance(data["monthly_projections"], list)
        assert isinstance(data["shortfall_amount"], int)
        assert isinstance(data["recommended_monthly_increase"], int)

    def test_calculate_projection_with_existing_savings(self):
        """Test projection with existing savings."""
        payload = {
            "target_amount": 150_000_000,
            "timeline_years": 4,
            "monthly_savings": 5_000_000,
            "current_savings": 50_000_000,
            "current_debt": 0,
        }

        response = client.post(
            "/api/v1/projections/calculate?goal_id=1&user_id=1",
            json=payload,
        )

        assert response.status_code == 201
        data = response.json()
        assert data["is_achievable"] is True

    def test_calculate_projection_with_debt(self):
        """Test projection when user has existing debt."""
        payload = {
            "target_amount": 100_000_000,
            "timeline_years": 5,
            "monthly_savings": 5_000_000,
            "current_savings": 30_000_000,
            "current_debt": 50_000_000,
        }

        response = client.post(
            "/api/v1/projections/calculate?goal_id=1&user_id=1",
            json=payload,
        )

        assert response.status_code == 201
        data = response.json()
        assert data["final_debt"] < payload["current_debt"]

    def test_calculate_projection_unachievable_returns_shortfall(self):
        """Test that unachievable projection returns shortfall amount."""
        payload = {
            "target_amount": 1_000_000_000,
            "timeline_years": 1,
            "monthly_savings": 1_000_000,
            "current_savings": 0,
            "current_debt": 0,
        }

        response = client.post(
            "/api/v1/projections/calculate?goal_id=1&user_id=1",
            json=payload,
        )

        assert response.status_code == 201
        data = response.json()
        assert data["is_achievable"] is False
        assert data["shortfall_amount"] > 0
        assert data["recommended_monthly_increase"] > 0

    def test_calculate_projection_monthly_breakdown(self):
        """Test that monthly projections are returned."""
        payload = {
            "target_amount": 60_000_000,
            "timeline_years": 2,
            "monthly_savings": 3_000_000,
            "current_savings": 0,
            "current_debt": 0,
        }

        response = client.post(
            "/api/v1/projections/calculate?goal_id=1&user_id=1",
            json=payload,
        )

        assert response.status_code == 201
        data = response.json()

        # Should have 24 monthly projections (2 years * 12 months)
        assert len(data["monthly_projections"]) == 24

    def test_monthly_projection_structure(self):
        """Test that each monthly projection has required fields."""
        payload = {
            "target_amount": 60_000_000,
            "timeline_years": 1,
            "monthly_savings": 5_000_000,
            "current_savings": 0,
            "current_debt": 0,
        }

        response = client.post(
            "/api/v1/projections/calculate?goal_id=1&user_id=1",
            json=payload,
        )

        assert response.status_code == 201
        data = response.json()

        for month_proj in data["monthly_projections"]:
            assert "month" in month_proj
            assert "year" in month_proj
            assert "savings_balance" in month_proj
            assert "debt_balance" in month_proj
            assert "net_worth" in month_proj
            assert "monthly_contribution" in month_proj
            assert "investment_growth" in month_proj
            assert "debt_payment" in month_proj
            assert "cumulative_savings" in month_proj
            assert "cumulative_investments" in month_proj

    def test_projection_with_invalid_goal_id(self):
        """Test projection with non-existent goal ID."""
        payload = {
            "target_amount": 100_000_000,
            "timeline_years": 5,
            "monthly_savings": 5_000_000,
            "current_savings": 0,
            "current_debt": 0,
        }

        response = client.post(
            "/api/v1/projections/calculate?goal_id=99999&user_id=1",
            json=payload,
        )

        assert response.status_code == 404

    def test_projection_validation_negative_target(self):
        """Test projection with negative target amount."""
        payload = {
            "target_amount": -100_000_000,  # Invalid negative
            "timeline_years": 5,
            "monthly_savings": 5_000_000,
            "current_savings": 0,
            "current_debt": 0,
        }

        response = client.post(
            "/api/v1/projections/calculate?goal_id=1&user_id=1",
            json=payload,
        )

        assert response.status_code == 422  # Validation error

    def test_projection_validation_zero_timeline(self):
        """Test projection with zero timeline."""
        payload = {
            "target_amount": 100_000_000,
            "timeline_years": 0,  # Invalid zero
            "monthly_savings": 5_000_000,
            "current_savings": 0,
            "current_debt": 0,
        }

        response = client.post(
            "/api/v1/projections/calculate?goal_id=1&user_id=1",
            json=payload,
        )

        assert response.status_code == 422

    def test_projection_validation_missing_required_field(self):
        """Test projection with missing required field."""
        payload = {
            "target_amount": 100_000_000,
            "timeline_years": 5,
            # Missing monthly_savings
            "current_savings": 0,
            "current_debt": 0,
        }

        response = client.post(
            "/api/v1/projections/calculate?goal_id=1&user_id=1",
            json=payload,
        )

        assert response.status_code == 422

    def test_projection_calculation_consistency(self):
        """Test that same input produces same output."""
        payload = {
            "target_amount": 100_000_000,
            "timeline_years": 5,
            "monthly_savings": 5_000_000,
            "current_savings": 0,
            "current_debt": 0,
        }

        response1 = client.post(
            "/api/v1/projections/calculate?goal_id=1&user_id=1",
            json=payload,
        )

        response2 = client.post(
            "/api/v1/projections/calculate?goal_id=1&user_id=1",
            json=payload,
        )

        assert response1.status_code == response2.status_code == 201
        data1 = response1.json()
        data2 = response2.json()

        # Results should be consistent
        assert data1["is_achievable"] == data2["is_achievable"]
        assert data1["total_months"] == data2["total_months"]
        assert data1["final_savings"] == data2["final_savings"]

    def test_projection_total_contributions_calculation(self):
        """Test that total contributions are correctly calculated."""
        monthly_savings = 5_000_000
        timeline_years = 2
        payload = {
            "target_amount": 150_000_000,
            "timeline_years": timeline_years,
            "monthly_savings": monthly_savings,
            "current_savings": 0,
            "current_debt": 0,
        }

        response = client.post(
            "/api/v1/projections/calculate?goal_id=1&user_id=1",
            json=payload,
        )

        assert response.status_code == 201
        data = response.json()

        # Total contributions should be monthly * months
        expected_contributions = monthly_savings * (timeline_years * 12)
        assert data["total_contributions"] == expected_contributions

    def test_projection_net_worth_calculation(self):
        """Test that net worth is correctly calculated."""
        payload = {
            "target_amount": 100_000_000,
            "timeline_years": 3,
            "monthly_savings": 5_000_000,
            "current_savings": 30_000_000,
            "current_debt": 10_000_000,
        }

        response = client.post(
            "/api/v1/projections/calculate?goal_id=1&user_id=1",
            json=payload,
        )

        assert response.status_code == 201
        data = response.json()

        # Net worth should be final_savings - final_debt
        expected_net_worth = data["final_savings"] - data["final_debt"]
        assert data["final_net_worth"] == expected_net_worth

    def test_projection_with_long_timeline(self):
        """Test projection with long timeline (15 years)."""
        payload = {
            "target_amount": 500_000_000,
            "timeline_years": 15,
            "monthly_savings": 2_000_000,
            "current_savings": 0,
            "current_debt": 0,
        }

        response = client.post(
            "/api/v1/projections/calculate?goal_id=1&user_id=1",
            json=payload,
        )

        assert response.status_code == 201
        data = response.json()

        # Should have 180 monthly projections (15 years * 12 months)
        assert len(data["monthly_projections"]) == 180
        assert data["total_months"] == 180

    def test_projection_response_types(self):
        """Test that all numeric fields in response are proper types."""
        payload = {
            "target_amount": 100_000_000,
            "timeline_years": 5,
            "monthly_savings": 5_000_000,
            "current_savings": 0,
            "current_debt": 0,
        }

        response = client.post(
            "/api/v1/projections/calculate?goal_id=1&user_id=1",
            json=payload,
        )

        assert response.status_code == 201
        data = response.json()

        # All amount fields should be integers
        assert isinstance(data["final_savings"], int)
        assert isinstance(data["final_debt"], int)
        assert isinstance(data["final_net_worth"], int)
        assert isinstance(data["total_contributions"], int)
        assert isinstance(data["total_investment_growth"], int)
        assert isinstance(data["shortfall_amount"], int)
        assert isinstance(data["recommended_monthly_increase"], int)

        for month_proj in data["monthly_projections"]:
            assert isinstance(month_proj["savings_balance"], int)
            assert isinstance(month_proj["debt_balance"], int)
            assert isinstance(month_proj["net_worth"], int)

    def test_projection_with_zero_debt(self):
        """Test projection when user has no debt."""
        payload = {
            "target_amount": 100_000_000,
            "timeline_years": 5,
            "monthly_savings": 5_000_000,
            "current_savings": 0,
            "current_debt": 0,  # No debt
        }

        response = client.post(
            "/api/v1/projections/calculate?goal_id=1&user_id=1",
            json=payload,
        )

        assert response.status_code == 201
        data = response.json()
        assert data["final_debt"] == 0

    def test_projection_requires_authentication(self):
        """Test that projection calculation requires user_id and goal_id."""
        payload = {
            "target_amount": 100_000_000,
            "timeline_years": 5,
            "monthly_savings": 5_000_000,
            "current_savings": 0,
            "current_debt": 0,
        }

        # Missing query parameters should fail
        response = client.post(
            "/api/v1/projections/calculate",  # Missing goal_id and user_id
            json=payload,
        )

        assert response.status_code in [422, 404]  # Either validation or not found
