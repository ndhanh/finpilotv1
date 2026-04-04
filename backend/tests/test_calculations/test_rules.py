"""
Unit tests for recommendation rules engine.

Tests the RecommendationEngine class for generating accurate,
rule-based financial recommendations based on user context.
"""

import pytest
from src.calculations.rules import (
    RecommendationEngine,
    RecommendationContext,
    RecommendationPriority,
    RecommendationCategory,
)


class TestRecommendationEngine:
    """Test cases for RecommendationEngine."""

    def test_generate_recommendations_achievable_goal(self):
        """Test recommendations for achievable goal."""
        context = RecommendationContext(
            target_amount=100_000_000,
            timeline_months=60,
            monthly_contribution=5_000_000,
            current_savings=0,
            current_debt=0,
            is_achievable=True,
            shortfall_amount=0,
            final_savings=300_000_000,
            final_debt=0,
        )

        recommendations = RecommendationEngine.generate_recommendations(context)

        assert len(recommendations) > 0
        # Should have positive recommendations for achievable goals
        assert any(
            rec.priority == RecommendationPriority.HIGH for rec in recommendations
        )

    def test_generate_recommendations_unachievable_goal(self):
        """Test recommendations for unachievable goal."""
        context = RecommendationContext(
            target_amount=500_000_000,
            timeline_months=12,
            monthly_contribution=1_000_000,
            current_savings=0,
            current_debt=0,
            is_achievable=False,
            shortfall_amount=488_000_000,  # Large shortfall
            final_savings=12_000_000,
            final_debt=0,
        )

        recommendations = RecommendationEngine.generate_recommendations(context)

        assert len(recommendations) > 0
        # Should have critical recommendations for unachievable goals
        assert any(
            rec.priority == RecommendationPriority.CRITICAL for rec in recommendations
        )

    def test_recommendations_have_required_fields(self):
        """Test that recommendations have all required fields."""
        context = RecommendationContext(
            target_amount=100_000_000,
            timeline_months=60,
            monthly_contribution=5_000_000,
            current_savings=0,
            current_debt=0,
            is_achievable=True,
            shortfall_amount=0,
            final_savings=300_000_000,
            final_debt=0,
        )

        recommendations = RecommendationEngine.generate_recommendations(context)

        for rec in recommendations:
            assert hasattr(rec, "category")
            assert hasattr(rec, "priority")
            assert hasattr(rec, "title")
            assert hasattr(rec, "description")
            assert hasattr(rec, "actionable_steps")
            assert hasattr(rec, "impact_score")
            assert hasattr(rec, "metadata")
            assert isinstance(rec.actionable_steps, list)
            assert len(rec.actionable_steps) > 0

    def test_recommendations_with_high_debt(self):
        """Test recommendations when user has significant debt."""
        context = RecommendationContext(
            target_amount=100_000_000,
            timeline_months=60,
            monthly_contribution=3_000_000,
            current_savings=20_000_000,
            current_debt=50_000_000,  # High debt
            is_achievable=True,
            shortfall_amount=0,
            final_savings=200_000_000,
            final_debt=20_000_000,  # Still some debt remaining
        )

        recommendations = RecommendationEngine.generate_recommendations(context)

        # Should have debt management recommendations
        debt_recommendations = [
            rec
            for rec in recommendations
            if rec.category == RecommendationCategory.DEBT_MANAGEMENT
        ]
        assert len(debt_recommendations) > 0

    def test_recommendations_with_low_savings_rate(self):
        """Test recommendations when monthly contribution is very low."""
        context = RecommendationContext(
            target_amount=100_000_000,
            timeline_months=60,
            monthly_contribution=500_000,  # Very low savings rate
            current_savings=0,
            current_debt=0,
            is_achievable=False,
            shortfall_amount=70_000_000,
            final_savings=30_000_000,  # Falls short
            final_debt=0,
        )

        recommendations = RecommendationEngine.generate_recommendations(context)

        # Should have savings rate recommendations
        savings_recommendations = [
            rec
            for rec in recommendations
            if rec.category == RecommendationCategory.SAVINGS_RATE
        ]
        assert len(savings_recommendations) > 0

    def test_recommendations_with_aggressive_timeline(self):
        """Test recommendations for aggressive (short) timeline."""
        context = RecommendationContext(
            target_amount=100_000_000,
            timeline_months=12,  # Very aggressive - 1 year
            monthly_contribution=10_000_000,  # Need high contribution
            current_savings=0,
            current_debt=0,
            is_achievable=True,
            shortfall_amount=0,
            final_savings=120_000_000,
            final_debt=0,
        )

        recommendations = RecommendationEngine.generate_recommendations(context)

        # Should have timeline-related recommendations
        timeline_recommendations = [
            rec
            for rec in recommendations
            if rec.category == RecommendationCategory.TIMELINE
        ]
        assert len(timeline_recommendations) > 0

    def test_recommendations_with_relaxed_timeline(self):
        """Test recommendations for relaxed (long) timeline."""
        context = RecommendationContext(
            target_amount=100_000_000,
            timeline_months=240,  # 20 years
            monthly_contribution=500_000,  # Can be lower with long timeline
            current_savings=0,
            current_debt=0,
            is_achievable=True,
            shortfall_amount=0,
            final_savings=150_000_000,
            final_debt=0,
        )

        recommendations = RecommendationEngine.generate_recommendations(context)

        assert len(recommendations) > 0
        # Should have manageable recommendations for relaxed timeline

    def test_recommendation_priority_levels(self):
        """Test that recommendations have appropriate priority levels."""
        context = RecommendationContext(
            target_amount=100_000_000,
            timeline_months=60,
            monthly_contribution=3_000_000,
            current_savings=0,
            current_debt=0,
            is_achievable=True,
            shortfall_amount=0,
            final_savings=200_000_000,
            final_debt=0,
        )

        recommendations = RecommendationEngine.generate_recommendations(context)

        # Should have varying priority levels
        priorities = {rec.priority for rec in recommendations}
        assert len(priorities) > 1  # Multiple priority levels

    def test_recommendations_actionable_steps(self):
        """Test that recommendations have concrete actionable steps."""
        context = RecommendationContext(
            target_amount=100_000_000,
            timeline_months=60,
            monthly_contribution=3_000_000,
            current_savings=0,
            current_debt=0,
            is_achievable=False,
            shortfall_amount=50_000_000,
            final_savings=150_000_000,
            final_debt=0,
        )

        recommendations = RecommendationEngine.generate_recommendations(context)

        for rec in recommendations:
            assert len(rec.actionable_steps) > 0
            # Each step should be a string
            for step in rec.actionable_steps:
                assert isinstance(step, str)
                assert len(step) > 0

    def test_recommendations_impact_score(self):
        """Test that all recommendations have valid impact scores."""
        context = RecommendationContext(
            target_amount=100_000_000,
            timeline_months=60,
            monthly_contribution=5_000_000,
            current_savings=0,
            current_debt=0,
            is_achievable=True,
            shortfall_amount=0,
            final_savings=300_000_000,
            final_debt=0,
        )

        recommendations = RecommendationEngine.generate_recommendations(context)

        for rec in recommendations:
            assert isinstance(rec.impact_score, int)
            assert 1 <= rec.impact_score <= 10

    def test_recommendations_with_minimal_savings(self):
        """Test recommendations when user has very minimal savings ability."""
        context = RecommendationContext(
            target_amount=100_000_000,
            timeline_months=60,
            monthly_contribution=100_000,  # Minimal
            current_savings=0,
            current_debt=0,
            is_achievable=False,
            shortfall_amount=94_000_000,
            final_savings=6_000_000,
            final_debt=0,
        )

        recommendations = RecommendationEngine.generate_recommendations(context)

        # Should have recommendations on feasibility and savings rate
        assert len(recommendations) > 0

    def test_recommendations_with_existing_large_debt(self):
        """Test recommendations when user has large existing debt."""
        context = RecommendationContext(
            target_amount=100_000_000,
            timeline_months=60,
            monthly_contribution=5_000_000,
            current_savings=10_000_000,
            current_debt=200_000_000,  # Very large debt
            is_achievable=False,
            shortfall_amount=150_000_000,
            final_savings=310_000_000,
            final_debt=150_000_000,  # Debt reduction
        )

        recommendations = RecommendationEngine.generate_recommendations(context)

        # Should prioritize debt management
        assert any(
            rec.priority == RecommendationPriority.CRITICAL for rec in recommendations
        )

    def test_recommendation_categories_coverage(self):
        """Test that recommendations cover multiple categories."""
        context = RecommendationContext(
            target_amount=100_000_000,
            timeline_months=60,
            monthly_contribution=3_000_000,
            current_savings=0,
            current_debt=50_000_000,
            is_achievable=False,
            shortfall_amount=40_000_000,
            final_savings=150_000_000,
            final_debt=40_000_000,
        )

        recommendations = RecommendationEngine.generate_recommendations(context)

        categories = {rec.category for rec in recommendations}
        # Should have recommendations from multiple categories
        assert len(categories) >= 2

    def test_recommendations_vietnamese_context(self):
        """Test that recommendations are sensitive to Vietnamese financial context."""
        context = RecommendationContext(
            target_amount=500_000_000,  # House purchase (high amount)
            timeline_months=60,
            monthly_contribution=5_000_000,
            current_savings=0,
            current_debt=0,
            is_achievable=True,
            shortfall_amount=0,
            final_savings=600_000_000,
            final_debt=0,
        )

        recommendations = RecommendationEngine.generate_recommendations(context)

        # Should generate relevant recommendations for Vietnamese context
        assert len(recommendations) > 0

    def test_recommendations_consistency(self):
        """Test that same context produces consistent recommendations."""
        context = RecommendationContext(
            target_amount=100_000_000,
            timeline_months=60,
            monthly_contribution=5_000_000,
            current_savings=0,
            current_debt=0,
            is_achievable=True,
            shortfall_amount=0,
            final_savings=300_000_000,
            final_debt=0,
        )

        recommendations1 = RecommendationEngine.generate_recommendations(context)
        recommendations2 = RecommendationEngine.generate_recommendations(context)

        # Same context should produce same number of recommendations
        assert len(recommendations1) == len(recommendations2)
        # Same titles in same order
        assert [r.title for r in recommendations1] == [
            r.title for r in recommendations2
        ]


class TestRecommendationContext:
    """Test cases for RecommendationContext data structure."""

    def test_context_with_all_fields(self):
        """Test RecommendationContext with all fields populated."""
        context = RecommendationContext(
            target_amount=100_000_000,
            timeline_months=60,
            monthly_contribution=5_000_000,
            current_savings=20_000_000,
            current_debt=10_000_000,
            is_achievable=True,
            shortfall_amount=0,
            final_savings=320_000_000,
            final_debt=0,
            estimated_monthly_income=20_000_000,
            estimated_monthly_expenses=10_000_000,
        )

        assert context.target_amount == 100_000_000
        assert context.monthly_contribution == 5_000_000
        assert context.estimated_monthly_income == 20_000_000

    def test_context_with_optional_fields(self):
        """Test RecommendationContext with optional fields as None."""
        context = RecommendationContext(
            target_amount=100_000_000,
            timeline_months=60,
            monthly_contribution=5_000_000,
            current_savings=0,
            current_debt=0,
            is_achievable=True,
            shortfall_amount=0,
            final_savings=300_000_000,
            final_debt=0,
            estimated_monthly_income=None,
            estimated_monthly_expenses=None,
        )

        assert context.estimated_monthly_income is None
        assert context.estimated_monthly_expenses is None
