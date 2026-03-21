"""
SQLAlchemy models for financial goals.

Defines Goal, GoalAssumptions, and related entities.
"""

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Float,
    Date,
    DateTime,
    ForeignKey,
    JSON,
    Enum,
    func,
)
from sqlalchemy.orm import relationship
import enum
from ..database import Base


class GoalType(str, enum.Enum):
    """Enumeration of supported goal types."""

    HOUSE_PURCHASE = "house_purchase"
    EMERGENCY_FUND = "emergency_fund"
    INVESTMENT = "investment"
    DEBT_PAYOFF = "debt_payoff"
    OTHER = "other"


class GoalStatus(str, enum.Enum):
    """Enumeration of goal statuses."""

    ACTIVE = "active"
    COMPLETED = "completed"
    PAUSED = "paused"
    CANCELLED = "cancelled"


class Goal(Base):
    """Financial goal model."""

    __tablename__ = "goals"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    plan_id = Column(Integer, ForeignKey("plans.id"), nullable=True, index=True)

    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    goal_type = Column(Enum(GoalType), nullable=False)
    target_amount = Column(Integer, nullable=False)  # VND
    target_date = Column(Date, nullable=False)
    current_savings = Column(Integer, default=0, nullable=False)  # VND
    status = Column(Enum(GoalStatus), default=GoalStatus.ACTIVE, nullable=False)
    assumptions = Column(
        JSON, default=dict, nullable=False
    )  # Goal-specific assumptions

    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relationships
    user = relationship("User", back_populates="goals")
    plan = relationship("Plan", back_populates="goals")
    snapshots = relationship(
        "FinancialSnapshot", back_populates="goal", cascade="all, delete-orphan"
    )
    audit_logs = relationship(
        "CalculationAudit", back_populates="goal", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Goal(id={self.id}, name='{self.name}', type='{self.goal_type.value}', target={self.target_amount})>"


class FinancialSnapshot(Base):
    """Snapshot of financial position at a point in time."""

    __tablename__ = "financial_snapshots"

    id = Column(Integer, primary_key=True, index=True)
    goal_id = Column(Integer, ForeignKey("goals.id"), nullable=False, index=True)

    # Financial data
    current_savings = Column(Integer, nullable=False)  # VND
    monthly_income = Column(Integer, nullable=True)  # VND
    monthly_expenses = Column(Integer, nullable=True)  # VND
    current_debt = Column(Integer, default=0, nullable=False)  # VND

    # Metadata
    snapshot_date = Column(Date, nullable=False)
    source = Column(String(50), nullable=False)  # e.g., "user_input", "calculation"
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    goal = relationship("Goal", back_populates="snapshots")

    def __repr__(self):
        return f"<FinancialSnapshot(id={self.id}, goal_id={self.goal_id}, date={self.snapshot_date})>"
