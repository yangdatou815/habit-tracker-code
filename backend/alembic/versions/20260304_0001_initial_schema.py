"""initial schema

Revision ID: 20260304_0001
Revises:
Create Date: 2026-03-04
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "20260304_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "habits",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=True),
        sa.Column(
            "is_active", sa.Boolean(), nullable=False, server_default=sa.text("1")
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
    )

    op.create_table(
        "habit_target_days",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "habit_id",
            sa.Integer(),
            sa.ForeignKey("habits.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("day_of_week", sa.String(length=3), nullable=False),
    )
    op.create_index("ix_habit_target_days_habit_id", "habit_target_days", ["habit_id"])

    op.create_table(
        "completions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "habit_id",
            sa.Integer(),
            sa.ForeignKey("habits.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("completed_date", sa.Date(), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.UniqueConstraint(
            "habit_id", "completed_date", name="uq_completions_habit_date"
        ),
    )
    op.create_index("ix_completions_habit_id", "completions", ["habit_id"])


def downgrade() -> None:
    op.drop_index("ix_completions_habit_id", table_name="completions")
    op.drop_table("completions")
    op.drop_index("ix_habit_target_days_habit_id", table_name="habit_target_days")
    op.drop_table("habit_target_days")
    op.drop_table("habits")
