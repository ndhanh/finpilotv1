"""
Service layer for financial projection management and orchestration.

Handles projection calculation orchestration, caching, and result persistence.
"""

import hashlib
import json
from typing import Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..models.audit import CalculationAudit, ProjectionResult as ProjectionResultModel
from ..models.goal import Goal
from ..calculations.projection import (
    ProjectionCalculator,
    ProjectionInputs,
    ProjectionResult,
)
from ..schemas.projection import ProjectionInput
from ..utils.errors import NotFoundError, ValidationError


class ProjectionService:
    """Service for managing financial projections and calculations."""

    CALCULATION_VERSION = "1.0"  # Version of calculation logic for audit trail

    def __init__(self, db: AsyncSession):
        """Initialize projection service with database session.

        Args:
            db: AsyncSession for database operations
        """
        self.db = db

    async def calculate_projection(
        self,
        goal_id: int,
        user_id: int,
        projection_input: ProjectionInput,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> ProjectionResult:
        """Calculate financial projection for a goal.

        This method:
        1. Validates the projection inputs
        2. Runs the deterministic calculation
        3. Creates an audit trail of the calculation
        4. Stores the result in the database

        Args:
            goal_id: ID of the goal for this projection
            user_id: ID of the user requesting the calculation
            projection_input: Projection input parameters
            ip_address: Optional IP address of the requester
            user_agent: Optional user agent of the requester

        Returns:
            ProjectionResult with complete calculation details

        Raises:
            NotFoundError: If goal not found
            ValidationError: If calculation fails
        """
        # Verify goal exists
        goal_result = await self.db.execute(
            select(Goal).where(Goal.id == goal_id).where(Goal.user_id == user_id)
        )
        goal = goal_result.scalar_one_or_none()

        if not goal:
            raise NotFoundError(f"Goal with ID {goal_id} not found")

        try:
            # Prepare calculation inputs
            calc_inputs = ProjectionInputs(
                target_amount=projection_input.target_amount,
                timeline_years=projection_input.timeline_years,
                monthly_savings=projection_input.monthly_contribution,
                current_savings=projection_input.current_savings,
                current_debt=projection_input.current_debt,
                expected_return_rate=projection_input.expected_return_rate,
                inflation_rate=projection_input.inflation_rate,
                debt_interest_rate=projection_input.debt_interest_rate,
                start_date=projection_input.start_date,
            )

            # Run calculation
            start_time = datetime.now()
            projection_result = ProjectionCalculator.calculate_projection(calc_inputs)
            calculation_time_ms = (datetime.now() - start_time).total_seconds() * 1000

            # Create audit trail
            input_hash = self._hash_input(projection_input)

            # Prepare audit data
            input_data = projection_input.model_dump()
            output_data = {
                "is_achievable": projection_result.is_achievable,
                "total_months": projection_result.total_months,
                "final_savings": projection_result.final_savings,
                "final_debt": projection_result.final_debt,
                "final_net_worth": projection_result.final_net_worth,
                "total_contributions": projection_result.total_contributions,
                "total_investment_growth": projection_result.total_investment_growth,
                "shortfall_amount": projection_result.shortfall_amount,
                "recommended_monthly_increase": projection_result.recommended_monthly_increase,
                "break_even_month": projection_result.break_even_month,
            }

            # Create audit record
            audit = CalculationAudit(
                goal_id=goal_id,
                calculation_type="projection",
                calculation_version=self.CALCULATION_VERSION,
                input_hash=input_hash,
                input_data=input_data,
                output_data=output_data,
                calculation_time_ms=calculation_time_ms,
                user_id=user_id,
                ip_address=ip_address,
                user_agent=user_agent,
            )

            self.db.add(audit)
            await self.db.flush()
            await self.db.refresh(audit)

            # Store projection result
            projection_result_model = ProjectionResultModel(
                goal_id=goal_id,
                audit_id=audit.id,
                is_achievable=projection_result.is_achievable,
                total_months=projection_result.total_months,
                final_savings=projection_result.final_savings,
                final_debt=projection_result.final_debt,
                final_net_worth=projection_result.final_net_worth,
                total_contributions=projection_result.total_contributions,
                total_investment_growth=projection_result.total_investment_growth,
                shortfall_amount=projection_result.shortfall_amount,
                recommended_monthly_increase=projection_result.recommended_monthly_increase,
                break_even_month=projection_result.break_even_month,
                monthly_projections=[
                    {
                        "month": mp.month,
                        "year": mp.year,
                        "savings_balance": mp.savings_balance,
                        "debt_balance": mp.debt_balance,
                        "net_worth": mp.net_worth,
                        "monthly_contribution": mp.monthly_contribution,
                        "investment_growth": mp.investment_growth,
                        "debt_payment": mp.debt_payment,
                        "cumulative_savings": mp.cumulative_savings,
                        "cumulative_investments": mp.cumulative_investments,
                    }
                    for mp in projection_result.monthly_projections
                ],
            )

            self.db.add(projection_result_model)
            await self.db.flush()

            return projection_result

        except ValueError as e:
            raise ValidationError(f"Projection calculation failed: {str(e)}")
        except Exception as e:
            raise ValidationError(f"Unexpected error during projection: {str(e)}")

    async def get_projection_result(
        self, goal_id: int, user_id: int
    ) -> Optional[ProjectionResultModel]:
        """Get the most recent projection result for a goal.

        Args:
            goal_id: ID of the goal
            user_id: ID of the user (for authorization)

        Returns:
            Most recent ProjectionResult or None if no projections exist

        Raises:
            NotFoundError: If goal not found or doesn't belong to user
        """
        # Verify goal ownership
        goal_result = await self.db.execute(
            select(Goal).where(Goal.id == goal_id).where(Goal.user_id == user_id)
        )
        if not goal_result.scalar_one_or_none():
            raise NotFoundError(f"Goal with ID {goal_id} not found")

        # Get latest projection
        query = (
            select(ProjectionResultModel)
            .where(ProjectionResultModel.goal_id == goal_id)
            .order_by(ProjectionResultModel.created_at.desc())
            .limit(1)
        )

        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_audit_log(self, goal_id: int, user_id: int) -> list:
        """Get calculation audit log for a goal.

        Args:
            goal_id: ID of the goal
            user_id: ID of the user (for authorization)

        Returns:
            List of audit records for the goal

        Raises:
            NotFoundError: If goal not found or doesn't belong to user
        """
        # Verify goal ownership
        goal_result = await self.db.execute(
            select(Goal).where(Goal.id == goal_id).where(Goal.user_id == user_id)
        )
        if not goal_result.scalar_one_or_none():
            raise NotFoundError(f"Goal with ID {goal_id} not found")

        # Get all audit records
        query = (
            select(CalculationAudit)
            .where(CalculationAudit.goal_id == goal_id)
            .order_by(CalculationAudit.created_at.desc())
        )

        result = await self.db.execute(query)
        return result.scalars().all()

    def _hash_input(self, projection_input: ProjectionInput) -> str:
        """Create a deterministic hash of input parameters for caching.

        Args:
            projection_input: Projection input to hash

        Returns:
            Hex hash of the input
        """
        # Convert input to JSON string for hashing
        input_dict = projection_input.model_dump()
        input_json = json.dumps(input_dict, sort_keys=True, default=str)

        # Create SHA-256 hash
        return hashlib.sha256(input_json.encode()).hexdigest()

    async def commit(self) -> None:
        """Commit the current transaction."""
        await self.db.commit()

    async def rollback(self) -> None:
        """Rollback the current transaction."""
        await self.db.rollback()
