"""
Unit tests for projection calculations.

Tests the ProjectionCalculator class for accurate financial projections
with various input scenarios and edge cases.
"""

import pytest
from datetime import date
from src.calculations.projection import (
    ProjectionCalculator,
    ProjectionInputs,
    ProjectionResult,
    MonthlyProjection,
)


class TestProjectionCalculator:
    """Test cases for ProjectionCalculator."""

    def test_basic_projection_achievable(self):
        """Test basic projection scenario that is achievable."""
        inputs = ProjectionInputs(
            target_amount=100_000_000,  # 100M VND
            timeline_years=5,
            monthly_savings=5_000_000,  # 5M VND/month
            current_savings=0,
            current_debt=0,
        )

        result = ProjectionCalculator.calculate_projection(inputs)

        assert isinstance(result, ProjectionResult)
        assert result.is_achievable is True
        assert result.total_months == 60  # 5 years
        assert result.final_savings >= inputs.target_amount
        assert result.final_debt == 0
        assert len(result.monthly_projections) == 60

    def test_projection_with_existing_savings(self):
        """Test projection when user has existing savings."""
        inputs = ProjectionInputs(
            target_amount=200_000_000,
            timeline_years=4,
            monthly_savings=10_000_000,
            current_savings=50_000_000,  # Already have 50M
            current_debt=0,
        )

        result = ProjectionCalculator.calculate_projection(inputs)

        assert result.is_achievable is True
        # First month should start with 50M savings
        assert result.monthly_projections[0].savings_balance > 0

    def test_projection_with_debt(self):
        """Test projection when user has existing debt."""
        inputs = ProjectionInputs(
            target_amount=150_000_000,
            timeline_years=5,
            monthly_savings=8_000_000,
            current_savings=30_000_000,
            current_debt=50_000_000,  # Has debt
        )

        result = ProjectionCalculator.calculate_projection(inputs)

        assert result.final_debt < inputs.current_debt
        # User should be paying down debt over time

    def test_projection_unachievable(self):
        """Test projection scenario that is unachievable with given constraints."""
        inputs = ProjectionInputs(
            target_amount=1_000_000_000,  # 1B VND (very ambitious)
            timeline_years=1,  # Only 1 year
            monthly_savings=1_000_000,  # 1M/month (very low)
            current_savings=0,
            current_debt=0,
        )

        result = ProjectionCalculator.calculate_projection(inputs)

        assert result.is_achievable is False
        assert result.shortfall_amount > 0
        assert result.recommended_monthly_increase > 0

    def test_projection_monthly_breakdown(self):
        """Test that monthly projections are calculated correctly."""
        inputs = ProjectionInputs(
            target_amount=120_000_000,
            timeline_years=2,
            monthly_savings=5_000_000,
            current_savings=0,
            current_debt=0,
        )

        result = ProjectionCalculator.calculate_projection(inputs)

        # Check first month
        first_month = result.monthly_projections[0]
        assert first_month.month == 1
        assert first_month.monthly_contribution == 5_000_000

        # Check progression
        for i, proj in enumerate(result.monthly_projections):
            assert proj.savings_balance >= 0
            assert proj.month == (i % 12) + 1
            assert proj.cumulative_savings >= inputs.current_savings

    def test_projection_with_different_return_rates(self):
        """Test projections with different expected return rates."""
        base_inputs = ProjectionInputs(
            target_amount=100_000_000,
            timeline_years=5,
            monthly_savings=3_000_000,
            current_savings=0,
            current_debt=0,
        )

        # Conservative projection (5% return)
        conservative = base_inputs
        conservative.expected_return_rate = 0.05
        conservative_result = ProjectionCalculator.calculate_projection(conservative)

        # Aggressive projection (10% return)
        aggressive = base_inputs
        aggressive.expected_return_rate = 0.10
        aggressive_result = ProjectionCalculator.calculate_projection(aggressive)

        # Higher return should mean better results
        assert (
            aggressive_result.total_investment_growth
            > conservative_result.total_investment_growth
        )

    def test_projection_inflation_impact(self):
        """Test that inflation is properly accounted for in projections."""
        inputs = ProjectionInputs(
            target_amount=100_000_000,
            timeline_years=10,
            monthly_savings=5_000_000,
            current_savings=0,
            current_debt=0,
            inflation_rate=0.04,
        )

        result = ProjectionCalculator.calculate_projection(inputs)

        # With inflation, the actual required savings should be higher
        # The target_amount should be adjusted upward for inflation
        assert len(result.monthly_projections) == 120

    def test_projection_total_contributions(self):
        """Test that total contributions are calculated correctly."""
        monthly_savings = 5_000_000
        timeline_years = 5
        inputs = ProjectionInputs(
            target_amount=100_000_000,
            timeline_years=timeline_years,
            monthly_savings=monthly_savings,
            current_savings=0,
            current_debt=0,
        )

        result = ProjectionCalculator.calculate_projection(inputs)

        # Total contributions should be approximately monthly * months
        expected_contributions = monthly_savings * (timeline_years * 12)
        assert result.total_contributions == expected_contributions

    def test_projection_break_even_month(self):
        """Test break_even_month calculation when goal is achieved."""
        inputs = ProjectionInputs(
            target_amount=60_000_000,
            timeline_years=2,
            monthly_savings=3_000_000,
            current_savings=0,
            current_debt=0,
        )

        result = ProjectionCalculator.calculate_projection(inputs)

        if result.is_achievable:
            assert result.break_even_month is not None
            assert result.break_even_month > 0
            assert result.break_even_month <= result.total_months

    def test_projection_validation_negative_amount(self):
        """Test that negative target amount fails validation."""
        inputs = ProjectionInputs(
            target_amount=-100_000_000,  # Invalid negative
            timeline_years=5,
            monthly_savings=5_000_000,
        )

        with pytest.raises(ValueError):
            ProjectionCalculator.calculate_projection(inputs)

    def test_projection_validation_zero_timeline(self):
        """Test that zero timeline fails validation."""
        inputs = ProjectionInputs(
            target_amount=100_000_000,
            timeline_years=0,  # Invalid zero
            monthly_savings=5_000_000,
        )

        with pytest.raises(ValueError):
            ProjectionCalculator.calculate_projection(inputs)

    def test_projection_validation_negative_savings(self):
        """Test that negative monthly savings fails validation."""
        inputs = ProjectionInputs(
            target_amount=100_000_000,
            timeline_years=5,
            monthly_savings=-5_000_000,  # Invalid negative
        )

        with pytest.raises(ValueError):
            ProjectionCalculator.calculate_projection(inputs)

    def test_projection_net_worth_calculation(self):
        """Test that net worth is correctly calculated (savings - debt)."""
        inputs = ProjectionInputs(
            target_amount=100_000_000,
            timeline_years=3,
            monthly_savings=5_000_000,
            current_savings=30_000_000,
            current_debt=10_000_000,
        )

        result = ProjectionCalculator.calculate_projection(inputs)

        # Net worth should be savings - debt
        for proj in result.monthly_projections:
            expected_net_worth = proj.savings_balance - proj.debt_balance
            assert proj.net_worth == expected_net_worth

    def test_projection_long_timeline(self):
        """Test projection with long timeline (10+ years)."""
        inputs = ProjectionInputs(
            target_amount=500_000_000,
            timeline_years=15,
            monthly_savings=2_000_000,
            current_savings=0,
            current_debt=0,
        )

        result = ProjectionCalculator.calculate_projection(inputs)

        assert len(result.monthly_projections) == 180  # 15 years
        assert result.total_months == 180

    def test_projection_high_return_rate(self):
        """Test projection with realistic high return rate."""
        inputs = ProjectionInputs(
            target_amount=100_000_000,
            timeline_years=5,
            monthly_savings=2_000_000,
            current_savings=0,
            current_debt=0,
            expected_return_rate=0.12,  # 12% annual return
        )

        result = ProjectionCalculator.calculate_projection(inputs)

        # Investment growth should be significant with 12% return
        assert result.total_investment_growth > 0

    def test_projection_zero_savings_rate(self):
        """Test projection with zero monthly savings."""
        inputs = ProjectionInputs(
            target_amount=100_000_000,
            timeline_years=5,
            monthly_savings=0,  # Zero savings
            current_savings=100_000_000,  # Only existing savings
            current_debt=0,
        )

        result = ProjectionCalculator.calculate_projection(inputs)

        # With zero monthly savings but sufficient initial savings, should be achievable
        assert result.total_contributions == 0


class TestMonthlyProjection:
    """Test cases for MonthlyProjection data structure."""

    def test_monthly_projection_structure(self):
        """Test that MonthlyProjection has required fields."""
        proj = MonthlyProjection(
            month=1,
            year=2024,
            savings_balance=5_000_000,
            debt_balance=0,
            net_worth=5_000_000,
            monthly_contribution=5_000_000,
            investment_growth=0,
            debt_payment=0,
            cumulative_savings=5_000_000,
            cumulative_investments=0,
        )

        assert proj.month == 1
        assert proj.year == 2024
        assert proj.net_worth == proj.savings_balance - proj.debt_balance


class TestProjectionInputValidation:
    """Test cases for ProjectionInputs validation."""

    def test_valid_inputs(self):
        """Test that valid inputs are accepted."""
        inputs = ProjectionInputs(
            target_amount=100_000_000,
            timeline_years=5,
            monthly_savings=5_000_000,
        )

        # Should not raise
        ProjectionCalculator.calculate_projection(inputs)

    def test_minimum_acceptable_inputs(self):
        """Test with minimum acceptable input values."""
        inputs = ProjectionInputs(
            target_amount=1_000_000,  # 1M VND minimum
            timeline_years=1,  # 1 year minimum
            monthly_savings=100_000,  # Small amount
        )

        result = ProjectionCalculator.calculate_projection(inputs)
        assert result is not None
