"""Initial schema — 11 core tables (spec §5.1–5.11).

Revision ID: 001_initial_schema
Revises:
Create Date: 2026-06-03

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "001_initial_schema"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('CREATE EXTENSION IF NOT EXISTS "pgcrypto"')

    op.create_table(
        "users",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("username", sa.String(length=100), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("full_name", sa.String(length=255), nullable=True),
        sa.Column("avatar_url", sa.String(length=500), nullable=True),
        sa.Column("pytorch_level", sa.String(length=20), server_default="beginner"),
        sa.Column("daily_goal", sa.Integer(), server_default="5"),
        sa.Column("streak_count", sa.Integer(), server_default="0"),
        sa.Column("longest_streak", sa.Integer(), server_default="0"),
        sa.Column("last_active_date", sa.Date(), nullable=True),
        sa.Column("total_xp", sa.Integer(), server_default="0"),
        sa.Column("is_active", sa.Boolean(), server_default="true"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("username"),
    )

    op.create_table(
        "topics",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("slug", sa.String(length=200), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("icon", sa.String(length=100), nullable=True),
        sa.Column("color", sa.String(length=20), nullable=True),
        sa.Column("order_index", sa.Integer(), nullable=False),
        sa.Column("module_number", sa.Integer(), nullable=False),
        sa.Column("total_questions", sa.Integer(), server_default="0"),
        sa.Column("is_active", sa.Boolean(), server_default="true"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("slug"),
    )

    op.create_table(
        "questions",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("topic_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=500), nullable=False),
        sa.Column("slug", sa.String(length=500), nullable=False),
        sa.Column("difficulty", sa.String(length=20), nullable=False),
        sa.Column("question_type", sa.String(length=50), nullable=False),
        sa.Column("problem_statement", sa.Text(), nullable=False),
        sa.Column("constraints", sa.Text(), nullable=True),
        sa.Column("starter_code", sa.Text(), nullable=True),
        sa.Column("expected_output", sa.Text(), nullable=True),
        sa.Column("expected_output_shape", sa.String(length=200), nullable=True),
        sa.Column("pytorch_version", sa.String(length=20), server_default="2.x"),
        sa.Column("gpu_required", sa.Boolean(), server_default="false"),
        sa.Column("colab_link", sa.String(length=1000), nullable=True),
        sa.Column("tags", postgresql.ARRAY(sa.Text()), nullable=True),
        sa.Column("xp_reward", sa.Integer(), server_default="10"),
        sa.Column("time_estimate_mins", sa.Integer(), server_default="15"),
        sa.Column("is_published", sa.Boolean(), server_default="true"),
        sa.Column("source", sa.String(length=100), server_default="internal"),
        sa.Column("source_url", sa.String(length=500), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
        ),
        sa.CheckConstraint(
            "difficulty IN ('basic', 'intermediate', 'advanced')",
            name="ck_questions_difficulty",
        ),
        sa.ForeignKeyConstraint(["topic_id"], ["topics.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("slug"),
    )
    op.create_index(
        "idx_questions_topic_difficulty",
        "questions",
        ["topic_id", "difficulty"],
    )
    op.create_index(
        "idx_questions_tags",
        "questions",
        ["tags"],
        postgresql_using="gin",
    )

    op.create_table(
        "solutions",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("question_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("code", sa.Text(), nullable=False),
        sa.Column("language", sa.String(length=20), server_default="python"),
        sa.Column("explanation", sa.Text(), nullable=True),
        sa.Column("time_complexity", sa.String(length=100), nullable=True),
        sa.Column("space_complexity", sa.String(length=100), nullable=True),
        sa.Column("is_optimal", sa.Boolean(), server_default="false"),
        sa.Column("order_index", sa.Integer(), server_default="1"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
        ),
        sa.ForeignKeyConstraint(["question_id"], ["questions.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "test_cases",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("question_id", sa.Integer(), nullable=False),
        sa.Column("input_data", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column(
            "expected_output",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
        ),
        sa.Column("explanation", sa.Text(), nullable=True),
        sa.Column("is_hidden", sa.Boolean(), server_default="false"),
        sa.Column("order_index", sa.Integer(), server_default="1"),
        sa.ForeignKeyConstraint(["question_id"], ["questions.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "user_attempts",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("question_id", sa.Integer(), nullable=False),
        sa.Column("submitted_code", sa.Text(), nullable=True),
        sa.Column("result", sa.String(length=20), nullable=True),
        sa.Column("runtime_ms", sa.Integer(), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("hints_used", sa.Integer(), server_default="0"),
        sa.Column("time_spent_secs", sa.Integer(), server_default="0"),
        sa.Column("attempt_number", sa.Integer(), server_default="1"),
        sa.Column(
            "attempted_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
        ),
        sa.CheckConstraint(
            "result IN ('correct', 'incorrect', 'partial', 'skipped')",
            name="ck_user_attempts_result",
        ),
        sa.ForeignKeyConstraint(["question_id"], ["questions.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "idx_attempts_user_question",
        "user_attempts",
        ["user_id", "question_id"],
    )
    op.create_index(
        "idx_attempts_user_date",
        "user_attempts",
        ["user_id", "attempted_at"],
    )

    op.create_table(
        "user_progress",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("topic_id", sa.Integer(), nullable=False),
        sa.Column("questions_attempted", sa.Integer(), server_default="0"),
        sa.Column("questions_solved", sa.Integer(), server_default="0"),
        sa.Column("basic_solved", sa.Integer(), server_default="0"),
        sa.Column("intermediate_solved", sa.Integer(), server_default="0"),
        sa.Column("advanced_solved", sa.Integer(), server_default="0"),
        sa.Column("total_time_spent_secs", sa.Integer(), server_default="0"),
        sa.Column(
            "completion_pct",
            sa.Numeric(precision=5, scale=2),
            server_default="0.00",
        ),
        sa.Column("last_attempted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["topic_id"], ["topics.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "topic_id"),
    )

    op.create_table(
        "daily_activity",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("activity_date", sa.Date(), nullable=False),
        sa.Column("exercises_done", sa.Integer(), server_default="0"),
        sa.Column("exercises_correct", sa.Integer(), server_default="0"),
        sa.Column("time_spent_secs", sa.Integer(), server_default="0"),
        sa.Column("xp_earned", sa.Integer(), server_default="0"),
        sa.Column("modules_touched", postgresql.ARRAY(sa.Text()), nullable=True),
        sa.Column("streak_day", sa.Integer(), server_default="0"),
        sa.Column("goal_met", sa.Boolean(), server_default="false"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "activity_date"),
    )
    op.create_index(
        "idx_daily_activity_user_date",
        "daily_activity",
        ["user_id", sa.text("activity_date DESC")],
    )

    op.create_table(
        "revision_queue",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("question_id", sa.Integer(), nullable=False),
        sa.Column(
            "ease_factor",
            sa.Numeric(precision=4, scale=2),
            server_default="2.50",
        ),
        sa.Column("interval_days", sa.Integer(), server_default="1"),
        sa.Column("repetition_count", sa.Integer(), server_default="0"),
        sa.Column("next_review_date", sa.Date(), nullable=False),
        sa.Column("last_reviewed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_result", sa.String(length=20), nullable=True),
        sa.ForeignKeyConstraint(["question_id"], ["questions.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "question_id"),
    )
    op.create_index(
        "idx_revision_due",
        "revision_queue",
        ["user_id", "next_review_date"],
    )

    op.create_table(
        "user_notes",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("question_id", sa.Integer(), nullable=True),
        sa.Column("topic_id", sa.Integer(), nullable=True),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("note_type", sa.String(length=20), server_default="personal"),
        sa.Column("tags", postgresql.ARRAY(sa.Text()), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
        ),
        sa.ForeignKeyConstraint(["question_id"], ["questions.id"]),
        sa.ForeignKeyConstraint(["topic_id"], ["topics.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "custom_questions",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("topic_id", sa.Integer(), nullable=True),
        sa.Column("title", sa.String(length=500), nullable=False),
        sa.Column("difficulty", sa.String(length=20), nullable=True),
        sa.Column("problem_statement", sa.Text(), nullable=False),
        sa.Column("solution_code", sa.Text(), nullable=True),
        sa.Column("colab_link", sa.String(length=1000), nullable=True),
        sa.Column("tags", postgresql.ARRAY(sa.Text()), nullable=True),
        sa.Column("is_shared", sa.Boolean(), server_default="false"),
        sa.Column("import_source", sa.String(length=200), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
        ),
        sa.ForeignKeyConstraint(["topic_id"], ["topics.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("custom_questions")
    op.drop_table("user_notes")
    op.drop_index("idx_revision_due", table_name="revision_queue")
    op.drop_table("revision_queue")
    op.drop_index("idx_daily_activity_user_date", table_name="daily_activity")
    op.drop_table("daily_activity")
    op.drop_table("user_progress")
    op.drop_index("idx_attempts_user_date", table_name="user_attempts")
    op.drop_index("idx_attempts_user_question", table_name="user_attempts")
    op.drop_table("user_attempts")
    op.drop_table("test_cases")
    op.drop_table("solutions")
    op.drop_index("idx_questions_tags", table_name="questions")
    op.drop_index("idx_questions_topic_difficulty", table_name="questions")
    op.drop_table("questions")
    op.drop_table("topics")
    op.drop_table("users")
