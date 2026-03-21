"""
Deterministic financial projection calculations for FinPilot.

This module implements the core calculation engine that provides
explainable, deterministic financial projections based on user inputs.
All calculations follow Vietnamese financial context and regulations.
"""

from typing import Dict, List, Optional, Tuple
from decimal import Decimal, ROUND_HALF_UP
from dataclasses import dataclass
from datetime import datetime, date
import math


@dataclass
class ProjectionInputs:
    """Input parameters for financial projections"""

    target_amount: int  # VND
    timeline_years: int
    monthly_savings: int  # VND
    current_savings: int = 0  # VND
    current_debt: int = 0  # VND
    expected_return_rate: float = 0.07  # 7% annual return (conservative)
    inflation_rate: float = 0.04  # 4% annual inflation
    debt_interest_rate: float = 0.12  # 12% annual debt interest
    start_date: Optional[date] = None


@dataclass
class MonthlyProjection:
    """Monthly financial projection data"""

    month: int
    year: int
    savings_balance: int  # VND
    debt_balance: int  # VND
    net_worth: int  # VND
    monthly_contribution: int  # VND
    investment_growth: int  # VND
    debt_payment: int  # VND
    cumulative_savings: int  # VND
    cumulative_investments: int  # VND


@dataclass
class ProjectionResult:
    """Complete projection calculation result"""

    is_achievable: bool
    total_months: int
    final_savings: int  # VND
    final_debt: int  # VND
    final_net_worth: int  # VND
    total_contributions: int  # VND
    total_investment_growth: int  # VND
    monthly_projections: List[MonthlyProjection]
    shortfall_amount: int  # VND (if not achievable)
    recommended_monthly_increase: int  # VND (if not achievable)
    break_even_month: Optional[int]  # Month when goal is achieved


class ProjectionCalculator:
    """
    Deterministic financial projection calculator.

    Implements conservative, explainable financial projections
    following Vietnamese financial planning principles.
    """

    # Vietnamese financial constants
    MIN_MONTHLY_SAVINGS = 500_000  # VND (reasonable minimum)
    MAX_REALISTIC_RETURN = 0.12  # 12% maximum expected return
    INFLATION_RATE = 0.04  # 4% annual inflation
    DEBT_INTEREST_RATE = 0.12  # 12% annual debt interest

    @classmethod
    def calculate_projection(cls, inputs: ProjectionInputs) -> ProjectionResult:
        """
        Calculate complete financial projection.

        Returns deterministic projection with monthly breakdown.
        """
        # Validate inputs
        cls._validate_inputs(inputs)

        # Initialize calculation variables
        monthly_projections = []
        current_savings = inputs.current_savings
        current_debt = inputs.current_debt
        total_contributions = 0
        total_growth = 0

        # Calculate monthly rates
        monthly_return_rate = inputs.expected_return_rate / 12
        monthly_inflation_rate = inputs.inflation_rate / 12
        monthly_debt_rate = inputs.debt_interest_rate / 12

        # Adjust target for inflation
        adjusted_target = cls._adjust_for_inflation(
            inputs.target_amount, inputs.timeline_years, inputs.inflation_rate
        )

        total_months = inputs.timeline_years * 12
        break_even_month = None

        for month in range(1, total_months + 1):
            # Monthly contribution (adjusted for inflation)
            monthly_contribution = cls._calculate_monthly_contribution(
                inputs.monthly_savings, month, monthly_inflation_rate
            )

            # Investment growth on existing balance
            investment_growth = int(current_savings * monthly_return_rate)

            # Debt interest and payment allocation
            debt_interest = int(current_debt * monthly_debt_rate)
            # Assume 20% of monthly contribution goes to debt payment
            debt_payment = int(monthly_contribution * 0.2) if current_debt > 0 else 0

            # Update balances
            current_savings += monthly_contribution + investment_growth - debt_payment
            current_debt += debt_interest - min(
                debt_payment, current_debt + debt_interest
            )

            # Ensure non-negative balances
            current_savings = max(0, current_savings)
            current_debt = max(0, current_debt)

            # Track totals
            total_contributions += monthly_contribution
            total_growth += investment_growth

            # Create monthly projection
            monthly_proj = MonthlyProjection(
                month=month,
                year=(month - 1) // 12 + 1,
                savings_balance=current_savings,
                debt_balance=current_debt,
                net_worth=current_savings - current_debt,
                monthly_contribution=monthly_contribution,
                investment_growth=investment_growth,
                debt_payment=debt_payment,
                cumulative_savings=total_contributions,
                cumulative_investments=total_growth,
            )
            monthly_projections.append(monthly_proj)

            # Check if goal achieved
            if (
                break_even_month is None
                and current_savings - current_debt >= adjusted_target
            ):
                break_even_month = month

        # Determine achievability
        final_net_worth = current_savings - current_debt
        is_achievable = final_net_worth >= adjusted_target

        # Calculate shortfall and recommendations if not achievable
        shortfall_amount = max(0, adjusted_target - final_net_worth)
        recommended_monthly_increase = 0

        if not is_achievable and shortfall_amount > 0:
            # Calculate required monthly increase
            remaining_months = total_months
            required_monthly = int(shortfall_amount / remaining_months)
            recommended_monthly_increase = required_monthly

        return ProjectionResult(
            is_achievable=is_achievable,
            total_months=total_months,
            final_savings=current_savings,
            final_debt=current_debt,
            final_net_worth=final_net_worth,
            total_contributions=total_contributions,
            total_investment_growth=total_growth,
            monthly_projections=monthly_projections,
            shortfall_amount=shortfall_amount,
            recommended_monthly_increase=recommended_monthly_increase,
            break_even_month=break_even_month,
        )

    @classmethod
    def _validate_inputs(cls, inputs: ProjectionInputs) -> None:
        """Validate projection inputs"""
        if inputs.target_amount <= 0:
            raise ValueError("Target amount must be positive")
        if inputs.timeline_years <= 0 or inputs.timeline_years > 50:
            raise ValueError("Timeline must be between 1 and 50 years")
        if inputs.monthly_savings < 0:
            raise ValueError("Monthly savings cannot be negative")
        if (
            inputs.expected_return_rate < 0
            or inputs.expected_return_rate > cls.MAX_REALISTIC_RETURN
        ):
            raise ValueError(
                f"Expected return rate must be between 0% and {cls.MAX_REALISTIC_RETURN*100}%"
            )
        if inputs.current_savings < 0:
            raise ValueError("Current savings cannot be negative")
        if inputs.current_debt < 0:
            raise ValueError("Current debt cannot be negative")

    @classmethod
    def _adjust_for_inflation(
        cls, amount: int, years: int, inflation_rate: float
    ) -> int:
        """Adjust amount for inflation over time"""
        if years == 0:
            return amount
        inflation_factor = (1 + inflation_rate) ** years
        return int(amount * inflation_factor)

    @classmethod
    def _calculate_monthly_contribution(
        cls, base_amount: int, month: int, monthly_inflation: float
    ) -> int:
        """Calculate monthly contribution adjusted for inflation"""
        # Apply gradual inflation adjustment
        inflation_adjustment = (1 + monthly_inflation) ** month
        return int(base_amount * inflation_adjustment)

    @classmethod
    def get_projection_summary(cls, result: ProjectionResult) -> Dict:
        """Get human-readable projection summary"""
        return {
            "achievability": "Achievable" if result.is_achievable else "Not Achievable",
            "timeline_years": result.total_months // 12,
            "final_amount": cls._format_currency(result.final_net_worth),
            "total_saved": cls._format_currency(result.total_contributions),
            "investment_growth": cls._format_currency(result.total_investment_growth),
            "break_even": (
                f"Month {result.break_even_month}"
                if result.break_even_month
                else "Not achieved"
            ),
            "recommendation": cls._get_recommendation(result),
        }

    @classmethod
    def _format_currency(cls, amount: int) -> str:
        """Format amount as Vietnamese Dong"""
        return f"{amount:,.0f} VND"

    @classmethod
    def _get_recommendation(cls, result: ProjectionResult) -> str:
        """Generate recommendation based on projection results"""
        if result.is_achievable:
            if (
                result.break_even_month
                and result.break_even_month < result.total_months * 0.8
            ):
                return "Excellent! You're on track to achieve your goal well before the deadline."
            else:
                return "Good! You'll achieve your goal within the planned timeline."
        else:
            if result.recommended_monthly_increase > 0:
                increase_formatted = cls._format_currency(
                    result.recommended_monthly_increase
                )
                return f"Consider increasing monthly savings by {increase_formatted} to achieve your goal."
            else:
                return (
                    "Consider extending your timeline or reducing your target amount."
                )
