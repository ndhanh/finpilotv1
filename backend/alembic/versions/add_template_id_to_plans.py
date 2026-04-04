"""Add template_id to plans table.

Revision ID: add_template_id_to_plans
Revises: 823108182c7d
Create Date: 2026-04-04 00:00:00.000000

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "add_template_id_to_plans"
down_revision = "823108182c7d"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Upgrade database schema."""
    # Add template_id column as nullable first
    op.add_column(
        "plans",
        sa.Column(
            "template_id",
            sa.String(50),
            nullable=True,
            server_default="home_purchase",
        ),
    )

    # Backfill existing plans with home_purchase template
    op.execute(
        sa.text(
            "UPDATE plans SET template_id = 'home_purchase' WHERE template_id IS NULL"
        )
    )

    # Make template_id non-nullable after backfill
    op.alter_column("plans", "template_id", nullable=False, existing_nullable=True)

    # Add index on template_id for query performance
    op.create_index("ix_plans_template_id", "plans", ["template_id"])


def downgrade() -> None:
    """Downgrade database schema."""
    # Drop the index
    op.drop_index("ix_plans_template_id", table_name="plans")

    # Remove the template_id column
    op.drop_column("plans", "template_id")
