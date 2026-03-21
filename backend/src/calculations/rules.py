"""
Rule-based recommendation engine for FinPilot.

This module implements deterministic, explainable recommendation logic
based on user inputs and projection results. All recommendations are
rule-based and transparent, following Vietnamese financial planning context.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum


class RecommendationPriority(Enum):
    """Priority levels for recommendations"""

    CRITICAL = "critical"  # Must address immediately
    HIGH = "high"  # Should address soon
    MEDIUM = "medium"  # Consider addressing
    LOW = "low"  # Nice to have
    INFO = "info"  # Informational only


class RecommendationCategory(Enum):
    """Categories of recommendations"""

    FEASIBILITY = "feasibility"
    DEBT_MANAGEMENT = "debt_management"
    SAVINGS_RATE = "savings_rate"
    TIMELINE = "timeline"
    RISK_ASSESSMENT = "risk_assessment"


@dataclass
class Recommendation:
    """Individual recommendation with explanation"""

    category: RecommendationCategory
    priority: RecommendationPriority
    title: str
    description: str
    actionable_steps: List[str]
    impact_score: int  # 1-10 scale of potential impact
    metadata: Dict[str, Any]  # Additional context data


@dataclass
class RecommendationContext:
    """Context data for generating recommendations"""

    # Goal information
    target_amount: int  # VND
    timeline_months: int
    monthly_contribution: int  # VND
    current_savings: int  # VND
    current_debt: int  # VND

    # Projection results
    is_achievable: bool
    shortfall_amount: int  # VND
    final_savings: int  # VND
    final_debt: int  # VND

    # User context (estimated)
    estimated_monthly_income: Optional[int] = None  # VND
    estimated_monthly_expenses: Optional[int] = None  # VND


class RecommendationEngine:
    """
    Rule-based recommendation engine for financial planning.

    Generates personalized, actionable recommendations based on
    deterministic rules and Vietnamese financial planning principles.
    """

    # Vietnamese financial planning constants
    MIN_MONTHLY_SAVINGS = 500_000  # VND
    MAX_AGGRESSIVE_SAVINGS_RATE = 0.50  # 50% of income
    HIGH_DEBT_RATIO_THRESHOLD = 0.20  # 20% of surplus
    MIN_REALISTIC_TIMELINE = 6  # months
    MAX_REALISTIC_TIMELINE = 360  # months (30 years)

    @classmethod
    def generate_recommendations(
        cls, context: RecommendationContext
    ) -> List[Recommendation]:
        """
        Generate comprehensive recommendations based on user context.

        Returns prioritized list of recommendations with actionable steps.
        """
        recommendations = []

        # Core feasibility assessment
        recommendations.extend(cls._assess_feasibility(context))

        # Debt management recommendations
        recommendations.extend(cls._assess_debt_management(context))

        # Savings rate validation
        recommendations.extend(cls._assess_savings_rate(context))

        # Timeline validation
        recommendations.extend(cls._assess_timeline(context))

        # Risk assessment
        recommendations.extend(cls._assess_risks(context))

        # Sort by priority and impact
        return cls._prioritize_recommendations(recommendations)

    @classmethod
    def _assess_feasibility(
        cls, context: RecommendationContext
    ) -> List[Recommendation]:
        """Assess goal feasibility and provide recommendations."""
        recommendations = []

        if context.is_achievable:
            if context.shortfall_amount < 0:  # Will achieve early
                months_early = (
                    abs(context.shortfall_amount) // context.monthly_contribution
                )
                recommendations.append(
                    Recommendation(
                        category=RecommendationCategory.FEASIBILITY,
                        priority=RecommendationPriority.INFO,
                        title="You're on track to achieve your goal early!",
                        description=f"You'll reach your goal {months_early} months ahead of schedule.",
                        actionable_steps=[
                            "Consider increasing your timeline for more flexibility",
                            "Explore additional financial goals you could achieve",
                            "Review your emergency fund while maintaining this momentum",
                        ],
                        impact_score=3,
                        metadata={"months_early": months_early},
                    )
                )
            else:  # Exactly on track
                recommendations.append(
                    Recommendation(
                        category=RecommendationCategory.FEASIBILITY,
                        priority=RecommendationPriority.INFO,
                        title="Perfect! You're on track for your goal.",
                        description="Your current savings rate will achieve your goal exactly on time.",
                        actionable_steps=[
                            "Continue your current savings discipline",
                            "Monitor your progress quarterly",
                            "Consider building an emergency fund alongside this goal",
                        ],
                        impact_score=2,
                        metadata={},
                    )
                )
        else:
            # Calculate required adjustments
            if context.monthly_contribution > 0:
                months_to_cover_gap = math.ceil(
                    context.shortfall_amount / context.monthly_contribution
                )
            else:
                months_to_cover_gap = float("inf")

            if months_to_cover_gap <= 24:  # Doable with focus
                recommendations.append(
                    Recommendation(
                        category=RecommendationCategory.FEASIBILITY,
                        priority=RecommendationPriority.HIGH,
                        title="Your goal is achievable with focused effort",
                        description=f"You need to save consistently for {months_to_cover_gap} more months to reach your goal.",
                        actionable_steps=[
                            "Maintain consistent monthly contributions",
                            "Track progress monthly to stay motivated",
                            "Consider temporary lifestyle adjustments to increase savings",
                        ],
                        impact_score=8,
                        metadata={"additional_months": months_to_cover_gap},
                    )
                )
            elif months_to_cover_gap <= 60:  # Challenging but possible
                recommended_increase = math.ceil(
                    context.shortfall_amount / context.timeline_months
                )
                recommendations.append(
                    Recommendation(
                        category=RecommendationCategory.FEASIBILITY,
                        priority=RecommendationPriority.CRITICAL,
                        title="Increase your monthly savings to reach your goal",
                        description=f"You need to increase monthly savings by {cls._format_vnd(recommended_increase)} to stay on track.",
                        actionable_steps=[
                            f"Find ways to save an additional {cls._format_vnd(recommended_increase)} per month",
                            "Review and reduce discretionary expenses",
                            "Consider side income opportunities",
                            "Extend your timeline if needed as a backup plan",
                        ],
                        impact_score=9,
                        metadata={"required_increase": recommended_increase},
                    )
                )
            else:  # Very challenging
                min_monthly_needed = math.ceil(
                    context.target_amount / context.timeline_months
                )
                recommendations.append(
                    Recommendation(
                        category=RecommendationCategory.FEASIBILITY,
                        priority=RecommendationPriority.CRITICAL,
                        title="Your timeline may be too ambitious",
                        description=f"To reach your goal in {context.timeline_months} months, you'd need to save {cls._format_vnd(min_monthly_needed)} monthly.",
                        actionable_steps=[
                            f"Consider extending your timeline beyond {context.timeline_months} months",
                            "Reevaluate your target amount or down payment requirements",
                            "Focus on debt reduction first if you have high-interest obligations",
                            "Consult with a financial advisor for personalized guidance",
                        ],
                        impact_score=10,
                        metadata={"minimum_monthly": min_monthly_needed},
                    )
                )

        return recommendations

    @classmethod
    def _assess_debt_management(
        cls, context: RecommendationContext
    ) -> List[Recommendation]:
        """Assess debt situation and provide recommendations."""
        recommendations = []

        if context.current_debt > 0:
            # Estimate monthly debt payment (rough approximation)
            estimated_debt_payment = max(
                500_000, context.current_debt // 60
            )  # Assume 5-year payoff

            if context.estimated_monthly_income and context.monthly_contribution > 0:
                debt_ratio = estimated_debt_payment / (
                    context.estimated_monthly_income * 0.3
                )  # 30% of take-home

                if debt_ratio > cls.HIGH_DEBT_RATIO_THRESHOLD:
                    recommendations.append(
                        Recommendation(
                            category=RecommendationCategory.DEBT_MANAGEMENT,
                            priority=RecommendationPriority.CRITICAL,
                            title="High-interest debt is impacting your savings",
                            description="Your debt payments are consuming a significant portion of your income, reducing savings capacity.",
                            actionable_steps=[
                                "Prioritize paying off high-interest debt (credit cards, personal loans)",
                                "Consider debt consolidation options",
                                "Create a debt payoff plan before aggressive saving",
                                "Focus on debt reduction for 6-12 months",
                            ],
                            impact_score=9,
                            metadata={
                                "debt_ratio": debt_ratio,
                                "estimated_payment": estimated_debt_payment,
                            },
                        )
                    )

            # Debt relative to savings
            if context.current_debt > context.current_savings * 2:
                recommendations.append(
                    Recommendation(
                        category=RecommendationCategory.DEBT_MANAGEMENT,
                        priority=RecommendationPriority.HIGH,
                        title="Your debt exceeds your savings significantly",
                        description="Building savings while carrying substantial debt may be challenging.",
                        actionable_steps=[
                            "Build a small emergency fund (3-6 months expenses) first",
                            "Then focus on debt reduction before major goal saving",
                            "Consider balance transfer options for lower interest rates",
                        ],
                        impact_score=7,
                        metadata={
                            "debt_to_savings_ratio": context.current_debt
                            / max(context.current_savings, 1)
                        },
                    )
                )

        return recommendations

    @classmethod
    def _assess_savings_rate(
        cls, context: RecommendationContext
    ) -> List[Recommendation]:
        """Assess savings rate and provide recommendations."""
        recommendations = []

        # Minimum savings check
        if context.monthly_contribution < cls.MIN_MONTHLY_SAVINGS:
            recommendations.append(
                Recommendation(
                    category=RecommendationCategory.SAVINGS_RATE,
                    priority=RecommendationPriority.MEDIUM,
                    title="Consider increasing your monthly savings",
                    description="Your current savings rate is below recommended minimums for meaningful progress.",
                    actionable_steps=[
                        f"Aim to save at least {cls._format_vnd(cls.MIN_MONTHLY_SAVINGS)} per month",
                        "Track your expenses for one month to find savings opportunities",
                        "Set up automatic transfers to a savings account",
                        "Start small and increase gradually",
                    ],
                    impact_score=6,
                    metadata={
                        "current_savings": context.monthly_contribution,
                        "recommended_minimum": cls.MIN_MONTHLY_SAVINGS,
                    },
                )
            )

        # Aggressive savings check
        if (
            context.estimated_monthly_income
            and context.monthly_contribution
            > context.estimated_monthly_income * cls.MAX_AGGRESSIVE_SAVINGS_RATE
        ):
            recommendations.append(
                Recommendation(
                    category=RecommendationCategory.SAVINGS_RATE,
                    priority=RecommendationPriority.HIGH,
                    title="Your savings rate may not be sustainable",
                    description="Saving more than 50% of your income long-term may lead to burnout or financial stress.",
                    actionable_steps=[
                        "Reevaluate your monthly expense tracking",
                        "Consider if your income estimate is accurate",
                        "Look for ways to increase income rather than cut expenses further",
                        "Build in flexibility for unexpected expenses",
                    ],
                    impact_score=8,
                    metadata={
                        "savings_rate": context.monthly_contribution
                        / context.estimated_monthly_income
                    },
                )
            )

        # Savings to debt ratio
        if (
            context.current_debt > 0
            and context.monthly_contribution < context.current_debt // 120
        ):  # Less than 10-year payoff
            recommendations.append(
                Recommendation(
                    category=RecommendationCategory.SAVINGS_RATE,
                    priority=RecommendationPriority.MEDIUM,
                    title="Balance savings with debt reduction",
                    description="Your savings rate should support both goal achievement and debt management.",
                    actionable_steps=[
                        "Allocate savings between debt payoff and goal saving",
                        "Consider debt consolidation to reduce interest costs",
                        "Review your overall financial priorities",
                    ],
                    impact_score=5,
                    metadata={},
                )
            )

        return recommendations

    @classmethod
    def _assess_timeline(cls, context: RecommendationContext) -> List[Recommendation]:
        """Assess timeline realism and provide recommendations."""
        recommendations = []

        if context.timeline_months < cls.MIN_REALISTIC_TIMELINE:
            recommendations.append(
                Recommendation(
                    category=RecommendationCategory.TIMELINE,
                    priority=RecommendationPriority.CRITICAL,
                    title="Your timeline is very aggressive",
                    description=f"A {context.timeline_months}-month timeline creates significant pressure and risk.",
                    actionable_steps=[
                        f"Consider extending to at least {cls.MIN_REALISTIC_TIMELINE} months for more realistic planning",
                        "Reevaluate your goal amount or down payment requirements",
                        "Focus on building momentum with achievable milestones",
                        "Consider if this timeline aligns with your life circumstances",
                    ],
                    impact_score=9,
                    metadata={
                        "current_timeline": context.timeline_months,
                        "recommended_minimum": cls.MIN_REALISTIC_TIMELINE,
                    },
                )
            )

        if context.timeline_months > cls.MAX_REALISTIC_TIMELINE:
            recommendations.append(
                Recommendation(
                    category=RecommendationCategory.TIMELINE,
                    priority=RecommendationPriority.MEDIUM,
                    title="Long timelines require sustained commitment",
                    description=f"A {context.timeline_months}-month timeline ({context.timeline_months//12} years) requires long-term discipline.",
                    actionable_steps=[
                        "Break down your goal into smaller milestones",
                        "Set up regular progress reviews (quarterly or annually)",
                        "Consider if this goal remains a priority over such a long period",
                        "Build in flexibility for life changes",
                    ],
                    impact_score=4,
                    metadata={"timeline_years": context.timeline_months // 12},
                )
            )

        # Timeline vs savings rate balance
        if context.monthly_contribution > 0:
            months_needed = math.ceil(
                context.target_amount / context.monthly_contribution
            )
            if (
                months_needed < context.timeline_months * 0.5
            ):  # Could achieve in half the time
                recommendations.append(
                    Recommendation(
                        category=RecommendationCategory.TIMELINE,
                        priority=RecommendationPriority.LOW,
                        title="You could achieve your goal sooner",
                        description=f"At your current savings rate, you could reach your goal in {months_needed} months.",
                        actionable_steps=[
                            "Consider accelerating your timeline if circumstances allow",
                            "Reevaluate if you want to increase other financial goals",
                            "Use extra time for more conservative planning",
                        ],
                        impact_score=3,
                        metadata={"possible_months": months_needed},
                    )
                )

        return recommendations

    @classmethod
    def _assess_risks(cls, context: RecommendationContext) -> List[Recommendation]:
        """Assess financial risks and provide recommendations."""
        recommendations = []

        # Emergency fund consideration
        if context.current_savings < 10_000_000:  # Less than 10M VND emergency fund
            recommendations.append(
                Recommendation(
                    category=RecommendationCategory.RISK_ASSESSMENT,
                    priority=RecommendationPriority.MEDIUM,
                    title="Consider building an emergency fund first",
                    description="Having 3-6 months of expenses saved provides financial security.",
                    actionable_steps=[
                        "Aim to save 3-6 months of essential expenses",
                        "Keep emergency funds in liquid, accessible accounts",
                        "Build this fund before or alongside your main goal",
                        "Review your expense tracking to determine appropriate amount",
                    ],
                    impact_score=7,
                    metadata={"current_savings": context.current_savings},
                )
            )

        # Debt concentration risk
        if context.current_debt > context.target_amount * 0.5:
            recommendations.append(
                Recommendation(
                    category=RecommendationCategory.RISK_ASSESSMENT,
                    priority=RecommendationPriority.HIGH,
                    title="High debt relative to your goal amount",
                    description="Your debt represents a significant portion of your target goal.",
                    actionable_steps=[
                        "Prioritize debt reduction in your financial plan",
                        "Consider how interest rates affect your overall plan",
                        "Build a debt payoff strategy alongside savings",
                        "Monitor interest rate changes that could impact debt costs",
                    ],
                    impact_score=8,
                    metadata={
                        "debt_ratio": context.current_debt / context.target_amount
                    },
                )
            )

        return recommendations

    @classmethod
    def _prioritize_recommendations(
        cls, recommendations: List[Recommendation]
    ) -> List[Recommendation]:
        """Sort recommendations by priority and impact."""
        priority_order = {
            RecommendationPriority.CRITICAL: 0,
            RecommendationPriority.HIGH: 1,
            RecommendationPriority.MEDIUM: 2,
            RecommendationPriority.LOW: 3,
            RecommendationPriority.INFO: 4,
        }

        return sorted(
            recommendations, key=lambda r: (priority_order[r.priority], -r.impact_score)
        )

    @staticmethod
    def _format_vnd(amount: int) -> str:
        """Format VND amount with proper separators."""
        return f"{amount:,} VND"


# Convenience functions for external use
def generate_financial_recommendations(
    target_amount: int,
    timeline_months: int,
    monthly_contribution: int,
    current_savings: int = 0,
    current_debt: int = 0,
    is_achievable: bool = True,
    shortfall_amount: int = 0,
    estimated_income: Optional[int] = None,
) -> List[Recommendation]:
    """
    Generate recommendations with simplified interface.

    This is the main entry point for generating financial recommendations.
    """
    context = RecommendationContext(
        target_amount=target_amount,
        timeline_months=timeline_months,
        monthly_contribution=monthly_contribution,
        current_savings=current_savings,
        current_debt=current_debt,
        is_achievable=is_achievable,
        shortfall_amount=shortfall_amount,
        final_savings=current_savings + (monthly_contribution * timeline_months),
        final_debt=current_debt,  # Simplified - no debt payoff calculation
        estimated_monthly_income=estimated_income,
    )

    return RecommendationEngine.generate_recommendations(context)
