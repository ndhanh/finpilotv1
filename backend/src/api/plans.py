"""
API endpoints for financial plans management.

Provides CRUD endpoints for creating, reading, updating, and deleting financial plans.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..services.plan_service import PlanService
from ..schemas.plan import PlanCreate, PlanUpdate, PlanResponse
from ..utils.errors import NotFoundError, ValidationError

router = APIRouter()


@router.post("/", response_model=PlanResponse, status_code=201)
async def create_plan(
    user_id: int,
    plan_data: PlanCreate,
    db: AsyncSession = Depends(get_db),
) -> PlanResponse:
    """Create a new financial plan.

    A plan is a container for organizing multiple financial goals together.
    For example, a user might create a "House and Car" plan that groups both
    a house purchase goal and a car purchase goal.

    Args:
        user_id: ID of the user creating the plan
        plan_data: Plan creation data (name, optional description)
        db: Database session

    Returns:
        Created plan with details

    Raises:
        HTTPException 422: If plan data is invalid
    """
    try:
        service = PlanService(db)
        plan = await service.create_plan(user_id, plan_data)
        await service.commit()

        return PlanResponse(
            id=plan.id,
            user_id=plan.user_id,
            name=plan.name,
            description=plan.description,
            created_at=plan.created_at,
            updated_at=plan.updated_at,
            goals=[],
        )

    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )


@router.get("/{plan_id}", response_model=PlanResponse)
async def get_plan(
    plan_id: int,
    user_id: int,
    db: AsyncSession = Depends(get_db),
) -> PlanResponse:
    """Retrieve a plan by ID with all its goals.

    Args:
        plan_id: ID of the plan to retrieve
        user_id: ID of the user (for authorization)
        db: Database session

    Returns:
        Plan details with associated goals

    Raises:
        HTTPException 404: If plan not found or doesn't belong to user
    """
    try:
        service = PlanService(db)
        plan = await service.get_plan(plan_id, user_id)

        # Convert goals to response format
        goals = [
            {"id": g.id, "name": g.name, "type": g.goal_type.value} for g in plan.goals
        ]

        return PlanResponse(
            id=plan.id,
            user_id=plan.user_id,
            name=plan.name,
            description=plan.description,
            created_at=plan.created_at,
            updated_at=plan.updated_at,
            goals=goals,
        )

    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.get("/", response_model=List[PlanResponse])
async def list_user_plans(
    user_id: int,
    db: AsyncSession = Depends(get_db),
) -> List[PlanResponse]:
    """List all plans for a user.

    Args:
        user_id: ID of the user
        db: Database session

    Returns:
        List of plans with their goals
    """
    service = PlanService(db)
    plans = await service.get_user_plans(user_id)

    results = []
    for plan in plans:
        goals = [
            {"id": g.id, "name": g.name, "type": g.goal_type.value} for g in plan.goals
        ]

        results.append(
            PlanResponse(
                id=plan.id,
                user_id=plan.user_id,
                name=plan.name,
                description=plan.description,
                created_at=plan.created_at,
                updated_at=plan.updated_at,
                goals=goals,
            )
        )

    return results


@router.put("/{plan_id}", response_model=PlanResponse)
async def update_plan(
    plan_id: int,
    user_id: int,
    plan_data: PlanUpdate,
    db: AsyncSession = Depends(get_db),
) -> PlanResponse:
    """Update a plan.

    Args:
        plan_id: ID of the plan to update
        user_id: ID of the user (for authorization)
        plan_data: Plan update data (partial)
        db: Database session

    Returns:
        Updated plan

    Raises:
        HTTPException 404: If plan not found
        HTTPException 422: If update data is invalid
    """
    try:
        service = PlanService(db)
        plan = await service.update_plan(plan_id, user_id, plan_data)
        await service.commit()

        goals = [
            {"id": g.id, "name": g.name, "type": g.goal_type.value} for g in plan.goals
        ]

        return PlanResponse(
            id=plan.id,
            user_id=plan.user_id,
            name=plan.name,
            description=plan.description,
            created_at=plan.created_at,
            updated_at=plan.updated_at,
            goals=goals,
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


@router.delete("/{plan_id}", status_code=204)
async def delete_plan(
    plan_id: int,
    user_id: int,
    db: AsyncSession = Depends(get_db),
) -> None:
    """Delete a plan and all associated goals.

    Args:
        plan_id: ID of the plan to delete
        user_id: ID of the user (for authorization)
        db: Database session

    Raises:
        HTTPException 404: If plan not found
    """
    try:
        service = PlanService(db)
        await service.delete_plan(plan_id, user_id)
        await service.commit()

    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.post("/{plan_id}/goals/{goal_id}", status_code=204)
async def add_goal_to_plan(
    plan_id: int,
    goal_id: int,
    user_id: int,
    db: AsyncSession = Depends(get_db),
) -> None:
    """Add a goal to a plan.

    Args:
        plan_id: ID of the plan
        goal_id: ID of the goal to add
        user_id: ID of the user (for authorization)
        db: Database session

    Raises:
        HTTPException 404: If plan or goal not found
    """
    try:
        service = PlanService(db)
        # Verify ownership by getting the plan
        await service.get_plan(plan_id, user_id)

        await service.add_goal_to_plan(plan_id, goal_id)
        await service.commit()

    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.delete("/{plan_id}/goals/{goal_id}", status_code=204)
async def remove_goal_from_plan(
    plan_id: int,
    goal_id: int,
    user_id: int,
    db: AsyncSession = Depends(get_db),
) -> None:
    """Remove a goal from a plan.

    Args:
        plan_id: ID of the plan
        goal_id: ID of the goal to remove
        user_id: ID of the user (for authorization)
        db: Database session

    Raises:
        HTTPException 404: If goal not found
    """
    try:
        service = PlanService(db)
        await service.remove_goal_from_plan(goal_id)
        await service.commit()

    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
