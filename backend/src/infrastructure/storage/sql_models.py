from __future__ import annotations

from datetime import date, datetime, timezone
from uuid import uuid4

from sqlalchemy import JSON, Boolean, CheckConstraint, Date, DateTime, ForeignKey, Integer, Numeric, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


JSON_VARIANT = JSON().with_variant(JSONB, "postgresql")


class Base(DeclarativeBase):
    pass


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="active")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utcnow, onupdate=utcnow)

    profile: Mapped["ProfileModel | None"] = relationship(back_populates="user", uselist=False)

    __table_args__ = (
        CheckConstraint("status IN ('active', 'inactive', 'blocked')", name="ck_users_status"),
    )


class RoleModel(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)


class UserRoleModel(Base):
    __tablename__ = "user_roles"

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id", ondelete="RESTRICT"), primary_key=True)
    assigned_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utcnow)


class ProfileModel(Base):
    __tablename__ = "profiles"

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    full_name: Mapped[str] = mapped_column(String(180), nullable=False)
    institutional_code: Mapped[str | None] = mapped_column(String(80))
    metadata_json: Mapped[dict] = mapped_column("metadata", JSON_VARIANT, nullable=False, default=dict)

    user: Mapped[UserModel] = relationship(back_populates="profile")


class AcademicTermModel(Base):
    __tablename__ = "academic_terms"

    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    starts_on: Mapped[date] = mapped_column(Date, nullable=False)
    ends_on: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="planned")

    __table_args__ = (
        CheckConstraint("ends_on >= starts_on", name="ck_terms_date_order"),
        CheckConstraint("status IN ('planned', 'active', 'closed')", name="ck_terms_status"),
    )


class CourseModel(Base):
    __tablename__ = "courses"

    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))
    code: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(180), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)


class CourseSectionModel(Base):
    __tablename__ = "course_sections"

    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))
    course_id: Mapped[str] = mapped_column(ForeignKey("courses.id", ondelete="RESTRICT"), nullable=False)
    academic_term_id: Mapped[str] = mapped_column(ForeignKey("academic_terms.id", ondelete="RESTRICT"), nullable=False)
    teacher_user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    section_name: Mapped[str] = mapped_column(String(80), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="draft")

    __table_args__ = (
        CheckConstraint("status IN ('draft', 'active', 'closed')", name="ck_sections_status"),
    )


class EnrollmentModel(Base):
    __tablename__ = "enrollments"

    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))
    section_id: Mapped[str] = mapped_column(ForeignKey("course_sections.id", ondelete="CASCADE"), nullable=False)
    student_user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="active")
    enrolled_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utcnow)

    __table_args__ = (
        UniqueConstraint("section_id", "student_user_id", name="uq_enrollments_section_student"),
        CheckConstraint("status IN ('active', 'dropped', 'completed')", name="ck_enrollments_status"),
    )


class TopicModel(Base):
    __tablename__ = "topics"

    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    area: Mapped[str | None] = mapped_column(String(120))


class LearningUnitModel(Base):
    __tablename__ = "learning_units"

    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))
    topic_id: Mapped[str] = mapped_column(ForeignKey("topics.id", ondelete="RESTRICT"), nullable=False)
    title: Mapped[str] = mapped_column(String(180), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)


class ActivityModel(Base):
    __tablename__ = "activities"

    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))
    learning_unit_id: Mapped[str] = mapped_column(ForeignKey("learning_units.id", ondelete="RESTRICT"), nullable=False)
    activity_type: Mapped[str] = mapped_column(String(40), nullable=False)
    title: Mapped[str] = mapped_column(String(180), nullable=False)
    created_by_user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    __table_args__ = (
        CheckConstraint(
            "activity_type IN ('simulation', 'quiz', 'guide', 'practice', 'evaluation')",
            name="ck_activities_type",
        ),
    )


class ActivityVersionModel(Base):
    __tablename__ = "activity_versions"

    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))
    activity_id: Mapped[str] = mapped_column(ForeignKey("activities.id", ondelete="CASCADE"), nullable=False)
    version_number: Mapped[int] = mapped_column(Integer, nullable=False)
    definition: Mapped[dict] = mapped_column(JSON_VARIANT, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utcnow)

    __table_args__ = (
        UniqueConstraint("activity_id", "version_number", name="uq_activity_versions_activity_version"),
        CheckConstraint("version_number > 0", name="ck_activity_versions_version_positive"),
    )


class AssignmentModel(Base):
    __tablename__ = "assignments"

    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))
    activity_version_id: Mapped[str] = mapped_column(ForeignKey("activity_versions.id", ondelete="RESTRICT"), nullable=False)
    section_id: Mapped[str] = mapped_column(ForeignKey("course_sections.id", ondelete="CASCADE"), nullable=False)
    created_by_user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    title: Mapped[str] = mapped_column(String(180), nullable=False)
    instructions: Mapped[str | None] = mapped_column(Text)
    opens_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    due_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="draft")

    __table_args__ = (
        CheckConstraint("status IN ('draft', 'published', 'closed', 'archived')", name="ck_assignments_status"),
        CheckConstraint(
            "due_at IS NULL OR opens_at IS NULL OR due_at >= opens_at",
            name="ck_assignments_date_order",
        ),
    )


class SubmissionModel(Base):
    __tablename__ = "submissions"

    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))
    assignment_id: Mapped[str] = mapped_column(ForeignKey("assignments.id", ondelete="CASCADE"), nullable=False)
    student_user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="pending")
    score: Mapped[float | None] = mapped_column(Numeric(5, 2))
    submitted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    last_attempt_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    __table_args__ = (
        UniqueConstraint("assignment_id", "student_user_id", name="uq_submissions_assignment_student"),
        CheckConstraint("status IN ('pending', 'in_progress', 'submitted', 'reviewed')", name="ck_submissions_status"),
        CheckConstraint("score IS NULL OR (score >= 0 AND score <= 100)", name="ck_submissions_score_range"),
    )


class AttemptModel(Base):
    __tablename__ = "attempts"

    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))
    submission_id: Mapped[str] = mapped_column(ForeignKey("submissions.id", ondelete="CASCADE"), nullable=False)
    attempt_number: Mapped[int] = mapped_column(Integer, nullable=False)
    method_name: Mapped[str] = mapped_column(String(50), nullable=False)
    outcome_status: Mapped[str] = mapped_column(String(40), nullable=False)
    execution_time_ms: Mapped[float | None] = mapped_column(Numeric(12, 3))
    input_payload: Mapped[dict] = mapped_column(JSON_VARIANT, nullable=False)
    result_payload: Mapped[dict] = mapped_column(JSON_VARIANT, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utcnow)

    __table_args__ = (
        UniqueConstraint("submission_id", "attempt_number", name="uq_attempts_submission_number"),
        CheckConstraint("attempt_number > 0", name="ck_attempts_number_positive"),
    )


class FeedbackModel(Base):
    __tablename__ = "feedback"

    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))
    submission_id: Mapped[str] = mapped_column(ForeignKey("submissions.id", ondelete="CASCADE"), nullable=False)
    author_user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    feedback_type: Mapped[str] = mapped_column(String(40), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utcnow)

    __table_args__ = (
        CheckConstraint(
            "feedback_type IN ('teacher_comment', 'system_hint', 'grade_note')",
            name="ck_feedback_type",
        ),
    )
