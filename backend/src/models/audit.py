"""
SQLAlchemy models for calculation audit trails.

Provides audit logging for all financial calculations to ensure
deterministic, explainable results.
"""

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
    JSON,
    Float,
    func,
)
from sqlalchemy.orm import relationship
from ..database import Base


class CalculationAudit(Base):
    """Audit trail for financial calculations."""

    __tablename__ = "calculation_audits"

    id = Column(Integer, primary_key=True, index=True)
    goal_id = Column(Integer, ForeignKey("goals.id"), nullable=False, index=True)

    # Calculation metadata
    calculation_type = Column(
        String(50), nullable=False
    )  # e.g., "projection", "recommendation"
    calculation_version = Column(
        String(20), nullable=False
    )  # Version of calculation logic
    input_hash = Column(
        String(64), nullable=False, index=True
    )  # Hash of inputs for deduplication

    # Input data (stored as JSON for audit purposes)
    input_data = Column(JSON, nullable=False)

    # Output data (stored as JSON)
    output_data = Column(JSON, nullable=False)

    # Performance metrics
    calculation_time_ms = Column(Float, nullable=True)  # Time taken for calculation

    # Metadata
    user_id = Column(
        Integer, ForeignKey("users.id"), nullable=True, index=True
    )  # For non-goal calculations
    ip_address = Column(String(45), nullable=True)  # IPv4/IPv6
    user_agent = Column(Text, nullable=True)

    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    goal = relationship("Goal", back_populates="audit_logs")
    user = relationship("User")

    def __repr__(self):
        return f"<CalculationAudit(id={self.id}, type='{self.calculation_type}', goal_id={self.goal_id})>"


class ProjectionResult(Base):
    """Stored projection calculation results."""

    __tablename__ = "projection_results"

    id = Column(Integer, primary_key=True, index=True)
    goal_id = Column(Integer, ForeignKey("goals.id"), nullable=False, index=True)
    audit_id = Column(Integer, ForeignKey("calculation_audits.id"), nullable=False)

    # Projection results
    is_achievable = Column(
        Integer, nullable=False
    )  # Using Integer for boolean (SQLite compatibility)
    total_months = Column(Integer, nullable=False)
    final_savings = Column(Integer, nullable=False)  # VND
    final_debt = Column(Integer, nullable=False)  # VND
    final_net_worth = Column(Integer, nullable=False)  # VND
    total_contributions = Column(Integer, nullable=False)  # VND
    total_investment_growth = Column(Integer, nullable=False)  # VND
    shortfall_amount = Column(Integer, nullable=False)  # VND
    recommended_monthly_increase = Column(Integer, nullable=False)  # VND
    break_even_month = Column(Integer, nullable=True)

    # Monthly data stored as JSON
    monthly_projections = Column(JSON, nullable=False)

    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    goal = relationship("Goal")
    audit = relationship("CalculationAudit")

    def __repr__(self):
        return f"<ProjectionResult(id={self.id}, goal_id={self.goal_id}, achievable={bool(self.is_achievable)})>"
