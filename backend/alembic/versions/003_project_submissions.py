"""Project submissions table for end-of-module projects.

Revision ID: 003_project_submissions
Revises: 002_python_studio_extensions
Create Date: 2026-06-06
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "003_project_submissions"
down_revision: Union[str, None] = "002_python_studio_extensions"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "project_submissions",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("topic_id", sa.Integer(), nullable=False),
        sa.Column("code", sa.Text(), nullable=False),
        sa.Column("stdout", sa.Text(), nullable=True),
        sa.Column("stderr", sa.Text(), nullable=True),
        sa.Column("score", sa.Integer(), server_default="0"),
        sa.Column("is_passed", sa.Boolean(), server_default="false"),
        sa.Column("feedback", sa.Text(), nullable=True),
        sa.Column("pep8_score", sa.Integer(), nullable=True),
        sa.Column(
            "submitted_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
        ),
        sa.ForeignKeyConstraint(["topic_id"], ["topics.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "topic_id", name="uq_project_submission_user_topic"),
    )
    op.create_index(
        "idx_project_submissions_user",
        "project_submissions",
        ["user_id", sa.text("submitted_at DESC")],
    )


def downgrade() -> None:
    op.drop_index("idx_project_submissions_user", table_name="project_submissions")
    op.drop_table("project_submissions")
