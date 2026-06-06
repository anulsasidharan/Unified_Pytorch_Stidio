"""Python Studio extensions — snippets, code_submissions, question new columns.

Revision ID: 002_python_studio_extensions
Revises: 001_initial_schema
Create Date: 2026-06-06

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "002_python_studio_extensions"
down_revision: Union[str, None] = "001_initial_schema"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ── snippets table ──────────────────────────────────────────────────────
    op.create_table(
        "snippets",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("slug", sa.String(length=200), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("code", sa.Text(), nullable=False),
        sa.Column("module_id", sa.Integer(), nullable=True),
        sa.Column("tags", postgresql.ARRAY(sa.Text()), nullable=True),
        sa.Column("difficulty", sa.String(length=20), nullable=True),
        sa.Column("is_featured", sa.Boolean(), server_default="false"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("slug"),
    )
    op.create_index("idx_snippets_module_id", "snippets", ["module_id"])
    op.create_index(
        "idx_snippets_tags", "snippets", ["tags"], postgresql_using="gin"
    )

    # ── code_submissions table ──────────────────────────────────────────────
    op.create_table(
        "code_submissions",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("question_id", sa.Integer(), nullable=True),
        sa.Column("code", sa.Text(), nullable=False),
        sa.Column("stdout", sa.Text(), nullable=True),
        sa.Column("stderr", sa.Text(), nullable=True),
        sa.Column("is_correct", sa.Boolean(), nullable=True),
        sa.Column("execution_time_ms", sa.Integer(), nullable=True),
        sa.Column("pep8_score", sa.Integer(), nullable=True),
        sa.Column(
            "submitted_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
        ),
        sa.ForeignKeyConstraint(["question_id"], ["questions.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "idx_code_submissions_user",
        "code_submissions",
        ["user_id", sa.text("submitted_at DESC")],
    )

    # ── Add new columns to questions ────────────────────────────────────────
    op.add_column(
        "questions",
        sa.Column("expected_output_type", sa.String(length=20), server_default="exact"),
    )
    op.add_column(
        "questions",
        sa.Column("run_in_browser", sa.Boolean(), server_default="true"),
    )
    op.add_column(
        "questions",
        sa.Column("pep8_required", sa.Boolean(), server_default="false"),
    )
    op.add_column(
        "questions",
        sa.Column("hints", postgresql.ARRAY(sa.Text()), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("questions", "hints")
    op.drop_column("questions", "pep8_required")
    op.drop_column("questions", "run_in_browser")
    op.drop_column("questions", "expected_output_type")
    op.drop_index("idx_code_submissions_user", table_name="code_submissions")
    op.drop_table("code_submissions")
    op.drop_index("idx_snippets_tags", table_name="snippets")
    op.drop_index("idx_snippets_module_id", table_name="snippets")
    op.drop_table("snippets")
