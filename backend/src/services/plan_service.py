"""
Service layer for financial plan management operations.

Handles CRUD operations for financial plans that group multiple goals together.
"""

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from ..models.plan import Plan
from ..models.goal import Goal
from ..schemas.plan import PlanCreate, PlanUpdate, PlanResponse
from ..utils.errors import NotFoundError, ValidationError


class PlanService:
    """Service for managing financial plans."""

    def __init__(self, db: AsyncSession):
        """Initialize plan service with database session.

        Args:
            db: AsyncSession for database operations
        """
        self.db = db

    async def create_plan(self, user_id: int, plan_data: PlanCreate) -> Plan:
        """Create a new financial plan.

        Args:
            user_id: ID of the user creating the plan
            plan_data: Plan creation schema with name and description

        Returns:
            Created Plan model instance

        Raises:
            ValidationError: If plan data is invalid
        """
        try:
            plan = Plan(
                user_id=user_id,
                name=plan_data.name,
                description=plan_data.description,
            )
            self.db.add(plan)
            await self.db.flush()
            await self.db.refresh(plan)
            return plan
        except Exception as e:
            raise ValidationError(f"Failed to create plan: {str(e)}")

    async def get_plan(self, plan_id: int, user_id: Optional[int] = None) -> Plan:
        """Retrieve a plan by ID.

        Args:
            plan_id: ID of the plan to retrieve
            user_id: Optional user ID to verify ownership

        Returns:
            Plan model instance with goals loaded

        Raises:
            NotFoundError: If plan not found
        """
        query = select(Plan).where(Plan.id == plan_id).options(selectinload(Plan.goals))

        if user_id is not None:
            query = query.where(Plan.user_id == user_id)

        result = await self.db.execute(query)
        plan = result.unique().scalar_one_or_none()

        if not plan:
            raise NotFoundError(f"Plan with ID {plan_id} not found")

        return plan

    async def get_user_plans(self, user_id: int) -> List[Plan]:
        """Retrieve all plans for a user.

        Args:
            user_id: ID of the user

        Returns:
            List of Plan model instances with goals loaded
        """
        query = (
            select(Plan)
            .where(Plan.user_id == user_id)
            .options(selectinload(Plan.goals))
            .order_by(Plan.created_at.desc())
        )

        result = await self.db.execute(query)
        return result.unique().scalars().all()

    async def get_latest_plan(self, user_id: int) -> Optional[Plan]:
        """Retrieve the most recently created plan for a user.

        Args:
            user_id: ID of the user

        Returns:
            Most recent Plan model instance or None if no plans exist
        """
        query = (
            select(Plan)
            .where(Plan.user_id == user_id)
            .options(selectinload(Plan.goals))
            .order_by(Plan.created_at.desc())
            .limit(1)
        )

        result = await self.db.execute(query)
        return result.unique().scalar_one_or_none()

    async def update_plan(
        self, plan_id: int, user_id: int, plan_data: PlanUpdate
    ) -> Plan:
        """Update an existing plan.

        Args:
            plan_id: ID of the plan to update
            user_id: ID of the user (for authorization)
            plan_data: Plan update schema with fields to update

        Returns:
            Updated Plan model instance

        Raises:
            NotFoundError: If plan not found
            ValidationError: If update data is invalid
        """
        plan = await self.get_plan(plan_id, user_id)

        update_data = plan_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(plan, field, value)

        try:
            self.db.add(plan)
            await self.db.flush()
            await self.db.refresh(plan)
            return plan
        except Exception as e:
            raise ValidationError(f"Failed to update plan: {str(e)}")

    async def delete_plan(self, plan_id: int, user_id: int) -> None:
        """Delete a plan and all associated goals.

        Args:
            plan_id: ID of the plan to delete
            user_id: ID of the user (for authorization)

        Raises:
            NotFoundError: If plan not found
        """
        plan = await self.get_plan(plan_id, user_id)
        await self.db.delete(plan)
        await self.db.flush()

    async def add_goal_to_plan(self, plan_id: int, goal_id: int) -> Goal:
        """Add a goal to a plan.

        Args:
            plan_id: ID of the plan
            goal_id: ID of the goal to add

        Returns:
            Updated Goal model instance

        Raises:
            NotFoundError: If plan or goal not found
        """
        plan = await self.db.execute(select(Plan).where(Plan.id == plan_id))
        plan = plan.scalar_one_or_none()

        if not plan:
            raise NotFoundError(f"Plan with ID {plan_id} not found")

        goal = await self.db.execute(select(Goal).where(Goal.id == goal_id))
        goal = goal.scalar_one_or_none()

        if not goal:
            raise NotFoundError(f"Goal with ID {goal_id} not found")

        goal.plan_id = plan_id
        self.db.add(goal)
        await self.db.flush()
        await self.db.refresh(goal)
        return goal

    async def remove_goal_from_plan(self, goal_id: int) -> Goal:
        """Remove a goal from a plan.

        Args:
            goal_id: ID of the goal to remove from plan

        Returns:
            Updated Goal model instance
        """
        goal = await self.db.execute(select(Goal).where(Goal.id == goal_id))
        goal = goal.scalar_one_or_none()

        if not goal:
            raise NotFoundError(f"Goal with ID {goal_id} not found")

        goal.plan_id = None
        self.db.add(goal)
        await self.db.flush()
        await self.db.refresh(goal)
        return goal

    async def commit(self) -> None:
        """Commit the current transaction."""
        await self.db.commit()

    async def rollback(self) -> None:
        """Rollback the current transaction."""
        await self.db.rollback()
