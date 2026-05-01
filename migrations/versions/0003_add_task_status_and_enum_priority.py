"""add task status and convert priority to enum-like values

Revision ID: 0003_task_status_priority
Revises: 0002_drop_audit_cascade
Create Date: 2026-05-01
"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0003_task_status_priority"
down_revision = "0002_drop_audit_cascade"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "tasks",
        sa.Column(
            "status",
            sa.String(length=20),
            nullable=False,
            server_default=sa.text("'queued'"),
        ),
    )
    op.execute("UPDATE tasks SET status = CASE WHEN completed THEN 'completed' ELSE 'queued' END")

    op.drop_index("idx_tasks_completed", table_name="tasks")
    op.drop_index("idx_tasks_priority", table_name="tasks")

    op.alter_column(
        "tasks",
        "priority",
        existing_type=sa.SmallInteger(),
        type_=sa.String(length=20),
        postgresql_using=(
            "CASE priority "
            "WHEN 1 THEN 'low' "
            "WHEN 2 THEN 'medium' "
            "WHEN 3 THEN 'high' "
            "ELSE 'urgent' "
            "END"
        ),
        existing_nullable=False,
        existing_server_default=sa.text("3"),
    )

    op.drop_column("tasks", "completed")

    op.alter_column(
        "tasks",
        "status",
        existing_type=sa.String(length=20),
        server_default=sa.text("'queued'"),
    )
    op.alter_column(
        "tasks",
        "priority",
        existing_type=sa.String(length=20),
        server_default=sa.text("'medium'"),
    )

    op.create_index("idx_tasks_status", "tasks", ["status"], unique=False)
    op.create_index("idx_tasks_priority", "tasks", ["priority"], unique=False)


def downgrade() -> None:
    op.drop_index("idx_tasks_priority", table_name="tasks")
    op.drop_index("idx_tasks_status", table_name="tasks")

    op.add_column(
        "tasks",
        sa.Column("completed", sa.Boolean(), nullable=False, server_default=sa.text("false")),
    )
    op.execute("UPDATE tasks SET completed = CASE WHEN status = 'completed' THEN true ELSE false END")

    op.alter_column(
        "tasks",
        "priority",
        existing_type=sa.String(length=20),
        type_=sa.SmallInteger(),
        postgresql_using=(
            "CASE priority "
            "WHEN 'low' THEN 1 "
            "WHEN 'medium' THEN 2 "
            "WHEN 'high' THEN 3 "
            "ELSE 4 "
            "END"
        ),
        existing_nullable=False,
        existing_server_default=sa.text("'medium'"),
    )

    op.drop_column("tasks", "status")

    op.alter_column(
        "tasks",
        "priority",
        existing_type=sa.SmallInteger(),
        server_default=sa.text("3"),
    )

    op.create_index("idx_tasks_completed", "tasks", ["completed"], unique=False)
    op.create_index("idx_tasks_priority", "tasks", ["priority"], unique=False)
