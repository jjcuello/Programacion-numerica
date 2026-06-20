"""Initial relational schema for academic tracking MVP.

Revision ID: 20260619_0001
Revises:
Create Date: 2026-06-19 00:00:00
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "20260619_0001"
down_revision = None
branch_labels = None
depends_on = None


JSON_TYPE = sa.JSON().with_variant(postgresql.JSONB(astext_type=sa.Text()), "postgresql")


def upgrade() -> None:
    bind = op.get_bind()
    if bind.dialect.name == "postgresql":
        op.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto")

    op.create_table(
        "users",
        sa.Column("id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("status IN ('active', 'inactive', 'blocked')", name="ck_users_status"),
        sa.UniqueConstraint("email", name="uq_users_email"),
    )

    op.create_table(
        "roles",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.UniqueConstraint("name", name="uq_roles_name"),
    )

    op.create_table(
        "profiles",
        sa.Column("user_id", sa.String(length=36), sa.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True, nullable=False),
        sa.Column("full_name", sa.String(length=180), nullable=False),
        sa.Column("institutional_code", sa.String(length=80), nullable=True),
        sa.Column("metadata", JSON_TYPE, nullable=False),
    )

    op.create_table(
        "academic_terms",
        sa.Column("id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("starts_on", sa.Date(), nullable=False),
        sa.Column("ends_on", sa.Date(), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.CheckConstraint("ends_on >= starts_on", name="ck_terms_date_order"),
        sa.CheckConstraint("status IN ('planned', 'active', 'closed')", name="ck_terms_status"),
    )

    op.create_table(
        "courses",
        sa.Column("id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("code", sa.String(length=30), nullable=False),
        sa.Column("name", sa.String(length=180), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.UniqueConstraint("code", name="uq_courses_code"),
    )

    op.create_table(
        "topics",
        sa.Column("id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("area", sa.String(length=120), nullable=True),
        sa.UniqueConstraint("name", name="uq_topics_name"),
    )

    op.create_table(
        "user_roles",
        sa.Column("user_id", sa.String(length=36), sa.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True, nullable=False),
        sa.Column("role_id", sa.Integer(), sa.ForeignKey("roles.id", ondelete="RESTRICT"), primary_key=True, nullable=False),
        sa.Column("assigned_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        "course_sections",
        sa.Column("id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("course_id", sa.String(length=36), sa.ForeignKey("courses.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("academic_term_id", sa.String(length=36), sa.ForeignKey("academic_terms.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("teacher_user_id", sa.String(length=36), sa.ForeignKey("users.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("section_name", sa.String(length=80), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.CheckConstraint("status IN ('draft', 'active', 'closed')", name="ck_sections_status"),
    )

    op.create_table(
        "enrollments",
        sa.Column("id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("section_id", sa.String(length=36), sa.ForeignKey("course_sections.id", ondelete="CASCADE"), nullable=False),
        sa.Column("student_user_id", sa.String(length=36), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("enrolled_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("status IN ('active', 'dropped', 'completed')", name="ck_enrollments_status"),
        sa.UniqueConstraint("section_id", "student_user_id", name="uq_enrollments_section_student"),
    )

    op.create_table(
        "learning_units",
        sa.Column("id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("topic_id", sa.String(length=36), sa.ForeignKey("topics.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("title", sa.String(length=180), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
    )

    op.create_table(
        "activities",
        sa.Column("id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("learning_unit_id", sa.String(length=36), sa.ForeignKey("learning_units.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("activity_type", sa.String(length=40), nullable=False),
        sa.Column("title", sa.String(length=180), nullable=False),
        sa.Column("created_by_user_id", sa.String(length=36), sa.ForeignKey("users.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.CheckConstraint(
            "activity_type IN ('simulation', 'quiz', 'guide', 'practice', 'evaluation')",
            name="ck_activities_type",
        ),
    )

    op.create_table(
        "activity_versions",
        sa.Column("id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("activity_id", sa.String(length=36), sa.ForeignKey("activities.id", ondelete="CASCADE"), nullable=False),
        sa.Column("version_number", sa.Integer(), nullable=False),
        sa.Column("definition", JSON_TYPE, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("version_number > 0", name="ck_activity_versions_version_positive"),
        sa.UniqueConstraint("activity_id", "version_number", name="uq_activity_versions_activity_version"),
    )

    op.create_table(
        "assignments",
        sa.Column("id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("activity_version_id", sa.String(length=36), sa.ForeignKey("activity_versions.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("section_id", sa.String(length=36), sa.ForeignKey("course_sections.id", ondelete="CASCADE"), nullable=False),
        sa.Column("created_by_user_id", sa.String(length=36), sa.ForeignKey("users.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("title", sa.String(length=180), nullable=False),
        sa.Column("instructions", sa.Text(), nullable=True),
        sa.Column("opens_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("due_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.CheckConstraint("status IN ('draft', 'published', 'closed', 'archived')", name="ck_assignments_status"),
        sa.CheckConstraint("due_at IS NULL OR opens_at IS NULL OR due_at >= opens_at", name="ck_assignments_date_order"),
    )

    op.create_table(
        "submissions",
        sa.Column("id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("assignment_id", sa.String(length=36), sa.ForeignKey("assignments.id", ondelete="CASCADE"), nullable=False),
        sa.Column("student_user_id", sa.String(length=36), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("score", sa.Numeric(5, 2), nullable=True),
        sa.Column("submitted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_attempt_at", sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint("status IN ('pending', 'in_progress', 'submitted', 'reviewed')", name="ck_submissions_status"),
        sa.CheckConstraint("score IS NULL OR (score >= 0 AND score <= 100)", name="ck_submissions_score_range"),
        sa.UniqueConstraint("assignment_id", "student_user_id", name="uq_submissions_assignment_student"),
    )

    op.create_table(
        "attempts",
        sa.Column("id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("submission_id", sa.String(length=36), sa.ForeignKey("submissions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("attempt_number", sa.Integer(), nullable=False),
        sa.Column("method_name", sa.String(length=50), nullable=False),
        sa.Column("outcome_status", sa.String(length=40), nullable=False),
        sa.Column("execution_time_ms", sa.Numeric(12, 3), nullable=True),
        sa.Column("input_payload", JSON_TYPE, nullable=False),
        sa.Column("result_payload", JSON_TYPE, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("attempt_number > 0", name="ck_attempts_number_positive"),
        sa.UniqueConstraint("submission_id", "attempt_number", name="uq_attempts_submission_number"),
    )

    op.create_table(
        "feedback",
        sa.Column("id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("submission_id", sa.String(length=36), sa.ForeignKey("submissions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("author_user_id", sa.String(length=36), sa.ForeignKey("users.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("feedback_type", sa.String(length=40), nullable=False),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "feedback_type IN ('teacher_comment', 'system_hint', 'grade_note')",
            name="ck_feedback_type",
        ),
    )

    op.create_index("idx_users_email", "users", ["email"])
    op.create_index("idx_sections_teacher_term", "course_sections", ["teacher_user_id", "academic_term_id"])
    op.create_index("idx_enrollments_student", "enrollments", ["student_user_id"])
    op.create_index("idx_assignments_section_due_at", "assignments", ["section_id", "due_at"])
    op.create_index("idx_submissions_student_status", "submissions", ["student_user_id", "status"])
    op.create_index("idx_attempts_submission_created_at", "attempts", ["submission_id", "created_at"])
    op.create_index("idx_attempts_method_status", "attempts", ["method_name", "outcome_status"])


def downgrade() -> None:
    op.drop_index("idx_attempts_method_status", table_name="attempts")
    op.drop_index("idx_attempts_submission_created_at", table_name="attempts")
    op.drop_index("idx_submissions_student_status", table_name="submissions")
    op.drop_index("idx_assignments_section_due_at", table_name="assignments")
    op.drop_index("idx_enrollments_student", table_name="enrollments")
    op.drop_index("idx_sections_teacher_term", table_name="course_sections")
    op.drop_index("idx_users_email", table_name="users")

    op.drop_table("feedback")
    op.drop_table("attempts")
    op.drop_table("submissions")
    op.drop_table("assignments")
    op.drop_table("activity_versions")
    op.drop_table("activities")
    op.drop_table("learning_units")
    op.drop_table("enrollments")
    op.drop_table("course_sections")
    op.drop_table("user_roles")
    op.drop_table("topics")
    op.drop_table("courses")
    op.drop_table("academic_terms")
    op.drop_table("profiles")
    op.drop_table("roles")
    op.drop_table("users")
