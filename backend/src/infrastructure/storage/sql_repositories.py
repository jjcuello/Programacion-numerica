from __future__ import annotations

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.infrastructure.storage.sql_models import AssignmentModel, AttemptModel, SubmissionModel, UserModel


class SqlAlchemyUserRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, *, email: str, password_hash: str, status: str = "active") -> UserModel:
        user = UserModel(email=email, password_hash=password_hash, status=status)
        self.session.add(user)
        self.session.flush()
        return user

    def get(self, user_id: str) -> UserModel | None:
        return self.session.get(UserModel, user_id)

    def get_by_email(self, email: str) -> UserModel | None:
        statement = select(UserModel).where(UserModel.email == email)
        return self.session.execute(statement).scalar_one_or_none()


class SqlAlchemyAssignmentRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(
        self,
        *,
        activity_version_id: str,
        section_id: str,
        created_by_user_id: str,
        title: str,
        instructions: str | None = None,
        opens_at: datetime | None = None,
        due_at: datetime | None = None,
        status: str = "draft",
    ) -> AssignmentModel:
        assignment = AssignmentModel(
            activity_version_id=activity_version_id,
            section_id=section_id,
            created_by_user_id=created_by_user_id,
            title=title,
            instructions=instructions,
            opens_at=opens_at,
            due_at=due_at,
            status=status,
        )
        self.session.add(assignment)
        self.session.flush()
        return assignment

    def get(self, assignment_id: str) -> AssignmentModel | None:
        return self.session.get(AssignmentModel, assignment_id)

    def list_for_section(self, section_id: str) -> list[AssignmentModel]:
        statement = select(AssignmentModel).where(AssignmentModel.section_id == section_id).order_by(AssignmentModel.due_at)
        return list(self.session.execute(statement).scalars())


class SqlAlchemySubmissionRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(
        self,
        *,
        assignment_id: str,
        student_user_id: str,
        status: str = "pending",
        score: float | None = None,
        submitted_at: datetime | None = None,
        last_attempt_at: datetime | None = None,
    ) -> SubmissionModel:
        submission = SubmissionModel(
            assignment_id=assignment_id,
            student_user_id=student_user_id,
            status=status,
            score=score,
            submitted_at=submitted_at,
            last_attempt_at=last_attempt_at,
        )
        self.session.add(submission)
        self.session.flush()
        return submission

    def get(self, submission_id: str) -> SubmissionModel | None:
        return self.session.get(SubmissionModel, submission_id)

    def get_for_assignment_student(self, assignment_id: str, student_user_id: str) -> SubmissionModel | None:
        statement = select(SubmissionModel).where(
            SubmissionModel.assignment_id == assignment_id,
            SubmissionModel.student_user_id == student_user_id,
        )
        return self.session.execute(statement).scalar_one_or_none()


class SqlAlchemyAttemptRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(
        self,
        *,
        submission_id: str,
        attempt_number: int,
        method_name: str,
        outcome_status: str,
        input_payload: dict,
        result_payload: dict,
        execution_time_ms: float | None = None,
    ) -> AttemptModel:
        attempt = AttemptModel(
            submission_id=submission_id,
            attempt_number=attempt_number,
            method_name=method_name,
            outcome_status=outcome_status,
            input_payload=input_payload,
            result_payload=result_payload,
            execution_time_ms=execution_time_ms,
        )
        self.session.add(attempt)
        self.session.flush()
        return attempt

    def get(self, attempt_id: str) -> AttemptModel | None:
        return self.session.get(AttemptModel, attempt_id)

    def list_for_submission(self, submission_id: str) -> list[AttemptModel]:
        statement = select(AttemptModel).where(AttemptModel.submission_id == submission_id).order_by(AttemptModel.attempt_number)
        return list(self.session.execute(statement).scalars())
