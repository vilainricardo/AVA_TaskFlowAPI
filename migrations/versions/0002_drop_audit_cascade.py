"""remove delete cascade from task_audit.task_id

Revision ID: 0002_drop_audit_cascade
Revises: 0001_create_tasks_and_task_audit
Create Date: 2026-05-01
"""
from __future__ import annotations

from alembic import op

# revision identifiers, used by Alembic.
revision = "0002_drop_audit_cascade"
down_revision = "0001_create_tasks_and_task_audit"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_constraint("task_audit_task_id_fkey", "task_audit", type_="foreignkey")


def downgrade() -> None:
    op.create_foreign_key(
        "task_audit_task_id_fkey",
        "task_audit",
        "tasks",
        ["task_id"],
        ["id"],
        ondelete="CASCADE",
    )
