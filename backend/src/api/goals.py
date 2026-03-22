"""
API endpoints for financial goals management.

Provides CRUD endpoints for creating, reading, updating, and deleting financial goals.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..services.goal_service import GoalService
from ..schemas.goal import GoalCreate, GoalUpdate, GoalResponse
from ..utils.errors import NotFoundError, ValidationError

router = APIRouter()


@router.post("/", response_model=GoalResponse, status_code=201)
async def create_goal(
    user_id: int,
    goal_data: GoalCreate,
    db: AsyncSession = Depends(get_db),
) -> GoalResponse:
    """Create a new financial goal.

    Args:
        user_id: ID of the user creating the goal
        goal_data: Goal creation data
        db: Database session

    Returns:
        Created goal with full details

    Raises:
        HTTPException 422: If goal data is invalid
    """
    try:
        service = GoalService(db)
        goal = await service.create_goal(user_id, goal_data)

        # Calculate additional fields
        progress = await service.calculate_progress(goal.id)
        months_remaining = await service.calculate_months_remaining(goal.id)

        await service.commit()

        return GoalResponse(
            id=goal.id,
            user_id=goal.user_id,
            name=goal.name,
            description=goal.description,
            goal_type=goal.goal_type,
            target_amount=goal.target_amount,
            target_date=goal.target_date,
            current_savings=goal.current_savings,
            status=goal.status,
            assumptions=goal.assumptions,
            created_at=goal.created_at,
            updated_at=goal.updated_at,
            progress_percentage=progress,
            months_remaining=months_remaining,
        )

    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )


@router.get("/{goal_id}", response_model=GoalResponse)
async def get_goal(
    goal_id: int,
    user_id: int,
    db: AsyncSession = Depends(get_db),
) -> GoalResponse:
    """Retrieve a goal by ID.

    Args:
        goal_id: ID of the goal to retrieve
        user_id: ID of the user (for authorization)
        db: Database session

    Returns:
        Goal details with progress information

    Raises:
        HTTPException 404: If goal not found or doesn't belong to user
    """
    try:
        service = GoalService(db)
        goal = await service.get_goal(goal_id, user_id)

        # Calculate additional fields
        progress = await service.calculate_progress(goal.id)
        months_remaining = await service.calculate_months_remaining(goal.id)

        return GoalResponse(
            id=goal.id,
            user_id=goal.user_id,
            name=goal.name,
            description=goal.description,
            goal_type=goal.goal_type,
            target_amount=goal.target_amount,
            target_date=goal.target_date,
            current_savings=goal.current_savings,
            status=goal.status,
            assumptions=goal.assumptions,
            created_at=goal.created_at,
            updated_at=goal.updated_at,
            progress_percentage=progress,
            months_remaining=months_remaining,
        )

    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.get("/", response_model=List[GoalResponse])
async def list_user_goals(
    user_id: int,
    plan_id: int = None,
    db: AsyncSession = Depends(get_db),
) -> List[GoalResponse]:
    """List all goals for a user, optionally filtered by plan.

    Args:
        user_id: ID of the user
        plan_id: Optional plan ID to filter goals
        db: Database session

    Returns:
        List of goals
    """
    service = GoalService(db)
    goals = await service.get_user_goals(user_id, plan_id)

    results = []
    for goal in goals:
        progress = await service.calculate_progress(goal.id)
        months_remaining = await service.calculate_months_remaining(goal.id)

        results.append(
            GoalResponse(
                id=goal.id,
                user_id=goal.user_id,
                name=goal.name,
                description=goal.description,
                goal_type=goal.goal_type,
                target_amount=goal.target_amount,
                target_date=goal.target_date,
                current_savings=goal.current_savings,
                status=goal.status,
                assumptions=goal.assumptions,
                created_at=goal.created_at,
                updated_at=goal.updated_at,
                progress_percentage=progress,
                months_remaining=months_remaining,
            )
        )

    return results


@router.put("/{goal_id}", response_model=GoalResponse)
async def update_goal(
    goal_id: int,
    user_id: int,
    goal_data: GoalUpdate,
    db: AsyncSession = Depends(get_db),
) -> GoalResponse:
    """Update a goal.

    Args:
        goal_id: ID of the goal to update
        user_id: ID of the user (for authorization)
        goal_data: Goal update data (partial)
        db: Database session

    Returns:
        Updated goal

    Raises:
        HTTPException 404: If goal not found
        HTTPException 422: If update data is invalid
    """
    try:
        service = GoalService(db)
        goal = await service.update_goal(goal_id, user_id, goal_data)

        # Calculate additional fields
        progress = await service.calculate_progress(goal.id)
        months_remaining = await service.calculate_months_remaining(goal.id)

        await service.commit()

        return GoalResponse(
            id=goal.id,
            user_id=goal.user_id,
            name=goal.name,
            description=goal.description,
            goal_type=goal.goal_type,
            target_amount=goal.target_amount,
            target_date=goal.target_date,
            current_savings=goal.current_savings,
            status=goal.status,
            assumptions=goal.assumptions,
            created_at=goal.created_at,
            updated_at=goal.updated_at,
            progress_percentage=progress,
            months_remaining=months_remaining,
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


@router.delete("/{goal_id}", status_code=204)
async def delete_goal(
    goal_id: int,
    user_id: int,
    db: AsyncSession = Depends(get_db),
) -> None:
    """Delete a goal.

    Args:
        goal_id: ID of the goal to delete
        user_id: ID of the user (for authorization)
        db: Database session

    Raises:
        HTTPException 404: If goal not found
    """
    try:
        service = GoalService(db)
        await service.delete_goal(goal_id, user_id)
        await service.commit()

    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
