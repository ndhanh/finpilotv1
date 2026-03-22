"""
API endpoints for financial projections.

Provides endpoints for calculating projections, retrieving results, and audit logs.
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..services.projection_service import ProjectionService
from ..schemas.projection import ProjectionInput, ProjectionResult
from ..utils.errors import NotFoundError, ValidationError

router = APIRouter()


@router.post("/calculate", response_model=ProjectionResult, status_code=201)
async def calculate_projection(
    goal_id: int,
    user_id: int,
    projection_input: ProjectionInput,
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> ProjectionResult:
    """Calculate financial projection for a goal.

    This endpoint calculates a deterministic financial projection based on:
    - Current financial position (savings, debt)
    - Monthly contribution amount
    - Target amount and timeline
    - Expected investment returns and inflation rates

    The calculation follows conservative financial planning principles with
    an audit trail for full transparency.

    Args:
        goal_id: ID of the goal to project
        user_id: ID of the user (for authorization)
        projection_input: Projection parameters (target, timeline, monthly savings, etc.)
        request: Request object for IP and user agent
        db: Database session

    Returns:
        ProjectionResult with:
        - is_achievable: Whether the goal is achievable
        - monthly_projections: Detailed monthly breakdown
        - shortfall_amount: If not achievable, amount needed
        - recommended_monthly_increase: If not achievable, suggested increase

    Raises:
        HTTPException 404: If goal not found
        HTTPException 422: If projection calculation fails
    """
    try:
        service = ProjectionService(db)

        # Extract client information
        ip_address = request.client.host if request.client else None
        user_agent = request.headers.get("user-agent")

        # Calculate projection
        result = await service.calculate_projection(
            goal_id=goal_id,
            user_id=user_id,
            projection_input=projection_input,
            ip_address=ip_address,
            user_agent=user_agent,
        )

        # Commit the audit trail and result
        await service.commit()

        # Convert result to response schema
        return ProjectionResult(
            is_achievable=result.is_achievable,
            total_months=result.total_months,
            final_savings=result.final_savings,
            final_debt=result.final_debt,
            final_net_worth=result.final_net_worth,
            total_contributions=result.total_contributions,
            total_investment_growth=result.total_investment_growth,
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
                for mp in result.monthly_projections
            ],
            shortfall_amount=result.shortfall_amount,
            recommended_monthly_increase=result.recommended_monthly_increase,
            break_even_month=result.break_even_month,
        )

    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}",
        )


@router.get("/{goal_id}/result", response_model=Optional[ProjectionResult])
async def get_latest_projection(
    goal_id: int,
    user_id: int,
    db: AsyncSession = Depends(get_db),
) -> Optional[ProjectionResult]:
    """Retrieve the most recent projection result for a goal.

    Args:
        goal_id: ID of the goal
        user_id: ID of the user (for authorization)
        db: Database session

    Returns:
        Most recent ProjectionResult or None if no projections exist

    Raises:
        HTTPException 404: If goal not found or doesn't belong to user
    """
    try:
        service = ProjectionService(db)
        result = await service.get_projection_result(goal_id, user_id)

        if not result:
            return None

        # Convert to response schema
        return ProjectionResult(
            is_achievable=result.is_achievable,
            total_months=result.total_months,
            final_savings=result.final_savings,
            final_debt=result.final_debt,
            final_net_worth=result.final_net_worth,
            total_contributions=result.total_contributions,
            total_investment_growth=result.total_investment_growth,
            monthly_projections=result.monthly_projections,
            shortfall_amount=result.shortfall_amount,
            recommended_monthly_increase=result.recommended_monthly_increase,
            break_even_month=result.break_even_month,
        )

    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
