"""create tasks and task_audit tables

Revision ID: 0001_create_tasks_and_task_audit
Revises: None
Create Date: 2026-04-29
"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "0001_create_tasks_and_task_audit"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "tasks",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("completed", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("priority", sa.SmallInteger(), nullable=False, server_default=sa.text("3")),
        sa.Column("due_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("timezone('utc', now())"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("timezone('utc', now())"),
        ),
    )
    op.create_index("idx_tasks_completed", "tasks", ["completed"], unique=False)
    op.create_index("idx_tasks_priority", "tasks", ["priority"], unique=False)
    op.create_index("idx_tasks_due_date", "tasks", ["due_date"], unique=False)
    op.create_index("idx_tasks_created_at", "tasks", ["created_at"], unique=False)

    op.create_table(
        "task_audit",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column(
            "task_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("tasks.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("action", sa.String(length=50), nullable=False),
        sa.Column("before_state", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("after_state", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("timezone('utc', now())"),
        ),
    )
    op.create_index("idx_task_audit_task_id", "task_audit", ["task_id"], unique=False)


def downgrade() -> None:
    op.drop_index("idx_task_audit_task_id", table_name="task_audit")
    op.drop_table("task_audit")

    op.drop_index("idx_tasks_created_at", table_name="tasks")
    op.drop_index("idx_tasks_due_date", table_name="tasks")
    op.drop_index("idx_tasks_priority", table_name="tasks")
    op.drop_index("idx_tasks_completed", table_name="tasks")
    op.drop_table("tasks")
