"""remove delete cascade from task_audit.task_id

Revision ID: 0002_drop_audit_cascade
Revises: 0001_create_tasks_and_task_audit
Create Date: 2026-05-01
"""
from __future__ import annotations

from alembic import op
from sqlalchemy import inspect

# revision identifiers, used by Alembic.
revision = "0002_drop_audit_cascade"
down_revision = "0001_create_tasks_and_task_audit"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 0001 can leave task_audit without an FK (nome auto-gerado varia). Só remove se existir.
    bind = op.get_bind()
    inspector = inspect(bind)
    for fk in inspector.get_foreign_keys("task_audit"):
        if fk.get("referred_table") != "tasks":
            continue
        cols = fk.get("constrained_columns") or []
        if "task_id" not in cols:
            continue
        name = fk.get("name")
        if name:
            op.drop_constraint(name, "task_audit", type_="foreignkey")


def downgrade() -> None:
    op.create_foreign_key(
        "task_audit_task_id_fkey",
        "task_audit",
        "tasks",
        ["task_id"],
        ["id"],
        ondelete="CASCADE",
    )
