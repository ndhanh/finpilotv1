"""
Service layer for goal management operations.

Handles CRUD operations for financial goals with validation and business logic.
"""

from typing import List, Optional
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload

from ..models.goal import Goal, FinancialSnapshot, GoalStatus
from ..schemas.goal import GoalCreate, GoalUpdate, GoalResponse
from ..utils.errors import NotFoundError, ValidationError


class GoalService:
    """Service for managing financial goals."""

    def __init__(self, db: AsyncSession):
        """Initialize goal service with database session.

        Args:
            db: AsyncSession for database operations
        """
        self.db = db

    async def create_goal(self, user_id: int, goal_data: GoalCreate) -> Goal:
        """Create a new financial goal.

        Args:
            user_id: ID of the user creating the goal
            goal_data: Goal creation schema with name, type, amounts, etc.

        Returns:
            Created Goal model instance

        Raises:
            ValidationError: If goal data is invalid
        """
        try:
            goal = Goal(
                user_id=user_id,
                name=goal_data.name,
                description=goal_data.description,
                goal_type=goal_data.goal_type,
                target_amount=goal_data.target_amount,
                target_date=goal_data.target_date,
                current_savings=goal_data.current_savings,
                assumptions=goal_data.assumptions or {},
            )
            self.db.add(goal)
            await self.db.flush()
            await self.db.refresh(goal)
            return goal
        except Exception as e:
            raise ValidationError(f"Failed to create goal: {str(e)}")

    async def get_goal(self, goal_id: int, user_id: Optional[int] = None) -> Goal:
        """Retrieve a goal by ID.

        Args:
            goal_id: ID of the goal to retrieve
            user_id: Optional user ID to verify ownership

        Returns:
            Goal model instance

        Raises:
            NotFoundError: If goal not found
        """
        query = select(Goal).where(Goal.id == goal_id)

        if user_id is not None:
            query = query.where(Goal.user_id == user_id)

        result = await self.db.execute(query)
        goal = result.scalar_one_or_none()

        if not goal:
            raise NotFoundError(f"Goal with ID {goal_id} not found")

        return goal

    async def get_user_goals(
        self, user_id: int, plan_id: Optional[int] = None
    ) -> List[Goal]:
        """Retrieve all goals for a user, optionally filtered by plan.

        Args:
            user_id: ID of the user
            plan_id: Optional plan ID to filter goals

        Returns:
            List of Goal model instances
        """
        query = select(Goal).where(Goal.user_id == user_id)

        if plan_id is not None:
            query = query.where(Goal.plan_id == plan_id)

        query = query.order_by(Goal.created_at.desc())
        result = await self.db.execute(query)
        return result.scalars().all()

    async def update_goal(
        self, goal_id: int, user_id: int, goal_data: GoalUpdate
    ) -> Goal:
        """Update an existing goal.

        Args:
            goal_id: ID of the goal to update
            user_id: ID of the user (for authorization)
            goal_data: Goal update schema with fields to update

        Returns:
            Updated Goal model instance

        Raises:
            NotFoundError: If goal not found
            ValidationError: If update data is invalid
        """
        goal = await self.get_goal(goal_id, user_id)

        update_data = goal_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(goal, field, value)

        try:
            self.db.add(goal)
            await self.db.flush()
            await self.db.refresh(goal)
            return goal
        except Exception as e:
            raise ValidationError(f"Failed to update goal: {str(e)}")

    async def delete_goal(self, goal_id: int, user_id: int) -> None:
        """Delete a goal.

        Args:
            goal_id: ID of the goal to delete
            user_id: ID of the user (for authorization)

        Raises:
            NotFoundError: If goal not found
        """
        goal = await self.get_goal(goal_id, user_id)
        await self.db.delete(goal)
        await self.db.flush()

    async def add_financial_snapshot(
        self,
        goal_id: int,
        user_id: int,
        current_savings: int,
        monthly_income: Optional[int] = None,
        monthly_expenses: Optional[int] = None,
        current_debt: int = 0,
        source: str = "user_input",
    ) -> FinancialSnapshot:
        """Add a financial snapshot for a goal.

        Args:
            goal_id: ID of the goal
            user_id: ID of the user (for authorization)
            current_savings: Current savings amount in VND
            monthly_income: Optional monthly income in VND
            monthly_expenses: Optional monthly expenses in VND
            current_debt: Current debt amount in VND
            source: Source of the snapshot (e.g., 'user_input', 'calculation')

        Returns:
            Created FinancialSnapshot model instance

        Raises:
            NotFoundError: If goal not found
        """
        goal = await self.get_goal(goal_id, user_id)

        snapshot = FinancialSnapshot(
            goal_id=goal_id,
            current_savings=current_savings,
            monthly_income=monthly_income,
            monthly_expenses=monthly_expenses,
            current_debt=current_debt,
            snapshot_date=date.today(),
            source=source,
        )

        self.db.add(snapshot)
        await self.db.flush()
        await self.db.refresh(snapshot)
        return snapshot

    async def get_latest_snapshot(self, goal_id: int) -> Optional[FinancialSnapshot]:
        """Get the most recent financial snapshot for a goal.

        Args:
            goal_id: ID of the goal

        Returns:
            Most recent FinancialSnapshot or None if no snapshots exist
        """
        query = (
            select(FinancialSnapshot)
            .where(FinancialSnapshot.goal_id == goal_id)
            .order_by(FinancialSnapshot.created_at.desc())
            .limit(1)
        )

        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def calculate_progress(self, goal_id: int) -> float:
        """Calculate progress percentage for a goal.

        Args:
            goal_id: ID of the goal

        Returns:
            Progress percentage (0-100)
        """
        goal = await self.db.execute(select(Goal).where(Goal.id == goal_id))
        goal = goal.scalar_one_or_none()

        if not goal:
            return 0.0

        if goal.target_amount <= 0:
            return 0.0

        progress = (goal.current_savings / goal.target_amount) * 100
        return min(progress, 100.0)

    async def calculate_months_remaining(self, goal_id: int) -> Optional[int]:
        """Calculate months remaining until target date for a goal.

        Args:
            goal_id: ID of the goal

        Returns:
            Number of months remaining or None if goal is past target date
        """
        goal = await self.db.execute(select(Goal).where(Goal.id == goal_id))
        goal = goal.scalar_one_or_none()

        if not goal:
            return None

        today = date.today()
        if goal.target_date <= today:
            return 0

        months = (goal.target_date.year - today.year) * 12 + (
            goal.target_date.month - today.month
        )
        return max(0, months)

    async def mark_completed(self, goal_id: int, user_id: int) -> Goal:
        """Mark a goal as completed.

        Args:
            goal_id: ID of the goal
            user_id: ID of the user (for authorization)

        Returns:
            Updated Goal model instance
        """
        goal = await self.get_goal(goal_id, user_id)
        goal.status = GoalStatus.COMPLETED
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
