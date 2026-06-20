from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, date, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker

from src.app.services.auth_service import AuthenticatedUser
from src.core.models.problem import ProblemDefinition
from src.core.results.method_result import MethodResult
from src.infrastructure.storage.sql_models import (
    AcademicTermModel,
    ActivityModel,
    ActivityVersionModel,
    AssignmentModel,
    AttemptModel,
    CourseModel,
    CourseSectionModel,
    EnrollmentModel,
    LearningUnitModel,
    SubmissionModel,
    TopicModel,
    UserModel,
)
from src.infrastructure.storage.sql_repositories import (
    SqlAlchemyAssignmentRepository,
    SqlAlchemyAttemptRepository,
    SqlAlchemySubmissionRepository,
)


@dataclass(frozen=True)
class RecordedAttempt:
    submission_id: str
    attempt_id: str
    attempt_number: int


class AcademicWorkflowService:
    def __init__(self, session_factory: sessionmaker[Session]):
        self.session_factory = session_factory

    def create_section(
        self,
        *,
        actor: AuthenticatedUser,
        course_code: str,
        course_name: str,
        term_name: str,
        term_starts_on: date,
        term_ends_on: date,
        section_name: str,
    ) -> dict[str, object]:
        self._require_role(actor, {"teacher", "admin"})
        with self.session_factory() as session:
            course = self._get_or_create_course(session, code=course_code, name=course_name)
            term = self._get_or_create_term(
                session,
                name=term_name,
                starts_on=term_starts_on,
                ends_on=term_ends_on,
            )
            section = CourseSectionModel(
                course_id=course.id,
                academic_term_id=term.id,
                teacher_user_id=actor.user_id,
                section_name=section_name.strip(),
                status="active",
            )
            session.add(section)
            session.commit()
            return {
                "section": {
                    "id": section.id,
                    "course_id": course.id,
                    "term_id": term.id,
                    "teacher_user_id": actor.user_id,
                    "section_name": section.section_name,
                    "status": section.status,
                }
            }

    def enroll_student(
        self,
        *,
        actor: AuthenticatedUser,
        section_id: str,
        student_user_id: str | None = None,
    ) -> dict[str, object]:
        if student_user_id is None:
            student_user_id = actor.user_id
        elif actor.user_id != student_user_id:
            self._require_role(actor, {"teacher", "admin"})

        with self.session_factory() as session:
            section = session.get(CourseSectionModel, section_id)
            if section is None:
                raise ValueError("La seccion no existe.")
            user = session.get(UserModel, student_user_id)
            if user is None:
                raise ValueError("El estudiante no existe.")
            existing = session.execute(
                select(EnrollmentModel).where(
                    EnrollmentModel.section_id == section_id,
                    EnrollmentModel.student_user_id == student_user_id,
                )
            ).scalar_one_or_none()
            if existing is not None:
                return {
                    "enrollment": {
                        "id": existing.id,
                        "section_id": existing.section_id,
                        "student_user_id": existing.student_user_id,
                        "status": existing.status,
                    }
                }
            enrollment = EnrollmentModel(section_id=section_id, student_user_id=student_user_id, status="active")
            session.add(enrollment)
            session.commit()
            return {
                "enrollment": {
                    "id": enrollment.id,
                    "section_id": enrollment.section_id,
                    "student_user_id": enrollment.student_user_id,
                    "status": enrollment.status,
                }
            }

    def create_assignment(
        self,
        *,
        actor: AuthenticatedUser,
        section_id: str,
        title: str,
        instructions: str,
        expression: str,
        allowed_methods: tuple[str, ...],
        topic_name: str = "Raices",
        unit_title: str = "Metodos de raices",
        opens_at: datetime | None = None,
        due_at: datetime | None = None,
    ) -> dict[str, object]:
        self._require_role(actor, {"teacher", "admin"})
        with self.session_factory() as session:
            section = session.get(CourseSectionModel, section_id)
            if section is None:
                raise ValueError("La seccion no existe.")

            topic = self._get_or_create_topic(session, topic_name)
            unit = self._get_or_create_learning_unit(session, topic.id, unit_title)
            activity = ActivityModel(
                learning_unit_id=unit.id,
                activity_type="simulation",
                title=title.strip(),
                created_by_user_id=actor.user_id,
                is_active=True,
            )
            session.add(activity)
            session.flush()

            activity_version = ActivityVersionModel(
                activity_id=activity.id,
                version_number=1,
                definition={
                    "expression": expression.strip(),
                    "allowed_methods": list(allowed_methods),
                    "instructions": instructions.strip(),
                },
            )
            session.add(activity_version)
            session.flush()

            assignment = SqlAlchemyAssignmentRepository(session).create(
                activity_version_id=activity_version.id,
                section_id=section_id,
                created_by_user_id=actor.user_id,
                title=title.strip(),
                instructions=instructions.strip(),
                opens_at=opens_at,
                due_at=due_at,
                status="published",
            )
            session.commit()
            return {
                "assignment": {
                    "id": assignment.id,
                    "section_id": assignment.section_id,
                    "activity_version_id": assignment.activity_version_id,
                    "title": assignment.title,
                    "status": assignment.status,
                }
            }

    def record_attempt(
        self,
        *,
        actor: AuthenticatedUser,
        assignment_id: str,
        problem: ProblemDefinition,
        result: MethodResult,
    ) -> RecordedAttempt:
        with self.session_factory() as session:
            assignment = session.get(AssignmentModel, assignment_id)
            if assignment is None:
                raise ValueError("La asignacion no existe.")

            enrollment = session.execute(
                select(EnrollmentModel).where(
                    EnrollmentModel.section_id == assignment.section_id,
                    EnrollmentModel.student_user_id == actor.user_id,
                    EnrollmentModel.status == "active",
                )
            ).scalar_one_or_none()
            if enrollment is None:
                raise ValueError("El estudiante no esta inscrito en la seccion de la asignacion.")

            submission_repository = SqlAlchemySubmissionRepository(session)
            attempt_repository = SqlAlchemyAttemptRepository(session)
            submission = submission_repository.get_for_assignment_student(assignment_id, actor.user_id)
            if submission is None:
                submission = submission_repository.create(
                    assignment_id=assignment_id,
                    student_user_id=actor.user_id,
                    status="in_progress",
                    last_attempt_at=datetime.now(UTC),
                )
            else:
                submission.last_attempt_at = datetime.now(UTC)
                if submission.status == "pending":
                    submission.status = "in_progress"

            previous_attempts = attempt_repository.list_for_submission(submission.id)
            attempt_number = len(previous_attempts) + 1
            attempt = attempt_repository.create(
                submission_id=submission.id,
                attempt_number=attempt_number,
                method_name=result.method_name,
                outcome_status=result.status.value,
                input_payload=problem.to_dict(),
                result_payload={
                    "status": result.status.value,
                    "solution": result.solution,
                    "message": result.message,
                    "iteration_count": result.iteration_count,
                    "elapsed_seconds": result.elapsed_seconds,
                },
                execution_time_ms=result.elapsed_seconds * 1000,
            )
            session.commit()
            return RecordedAttempt(submission_id=submission.id, attempt_id=attempt.id, attempt_number=attempt_number)

    def get_assignment_detail(self, *, actor: AuthenticatedUser, assignment_id: str) -> dict[str, object]:
        with self.session_factory() as session:
            assignment = session.get(AssignmentModel, assignment_id)
            if assignment is None:
                raise ValueError("La asignacion no existe.")

            version = session.get(ActivityVersionModel, assignment.activity_version_id)
            if version is None:
                raise ValueError("La version de actividad no existe.")

            if "student" in actor.roles:
                enrollment = session.execute(
                    select(EnrollmentModel).where(
                        EnrollmentModel.section_id == assignment.section_id,
                        EnrollmentModel.student_user_id == actor.user_id,
                        EnrollmentModel.status == "active",
                    )
                ).scalar_one_or_none()
                if enrollment is None:
                    raise PermissionError("No tienes acceso a esta asignacion.")

            return {
                "assignment": {
                    "id": assignment.id,
                    "section_id": assignment.section_id,
                    "title": assignment.title,
                    "instructions": assignment.instructions,
                    "status": assignment.status,
                    "opens_at": assignment.opens_at.isoformat() if assignment.opens_at else None,
                    "due_at": assignment.due_at.isoformat() if assignment.due_at else None,
                    "definition": dict(version.definition),
                }
            }

    def list_assignments_for_student(self, *, actor: AuthenticatedUser) -> dict[str, object]:
        self._require_role(actor, {"student", "teacher", "admin"})
        with self.session_factory() as session:
            if "student" in actor.roles and "teacher" not in actor.roles and "admin" not in actor.roles:
                statement = (
                    select(AssignmentModel, ActivityVersionModel)
                    .join(EnrollmentModel, EnrollmentModel.section_id == AssignmentModel.section_id)
                    .join(ActivityVersionModel, ActivityVersionModel.id == AssignmentModel.activity_version_id)
                    .where(EnrollmentModel.student_user_id == actor.user_id, EnrollmentModel.status == "active")
                    .order_by(AssignmentModel.due_at, AssignmentModel.title)
                )
            else:
                statement = (
                    select(AssignmentModel, ActivityVersionModel)
                    .join(ActivityVersionModel, ActivityVersionModel.id == AssignmentModel.activity_version_id)
                    .order_by(AssignmentModel.due_at, AssignmentModel.title)
                )

            assignments = []
            for assignment, version in session.execute(statement).all():
                assignments.append(
                    {
                        "id": assignment.id,
                        "section_id": assignment.section_id,
                        "title": assignment.title,
                        "instructions": assignment.instructions,
                        "status": assignment.status,
                        "definition": dict(version.definition),
                    }
                )
            return {"assignments": assignments}

    def _get_or_create_course(self, session: Session, *, code: str, name: str) -> CourseModel:
        statement = select(CourseModel).where(CourseModel.code == code.strip())
        course = session.execute(statement).scalar_one_or_none()
        if course is None:
            course = CourseModel(code=code.strip(), name=name.strip())
            session.add(course)
            session.flush()
        return course

    def _get_or_create_term(self, session: Session, *, name: str, starts_on: date, ends_on: date) -> AcademicTermModel:
        statement = select(AcademicTermModel).where(AcademicTermModel.name == name.strip())
        term = session.execute(statement).scalar_one_or_none()
        if term is None:
            term = AcademicTermModel(name=name.strip(), starts_on=starts_on, ends_on=ends_on, status="active")
            session.add(term)
            session.flush()
        return term

    def _get_or_create_topic(self, session: Session, name: str) -> TopicModel:
        statement = select(TopicModel).where(TopicModel.name == name.strip())
        topic = session.execute(statement).scalar_one_or_none()
        if topic is None:
            topic = TopicModel(name=name.strip(), area="Metodos numericos")
            session.add(topic)
            session.flush()
        return topic

    def _get_or_create_learning_unit(self, session: Session, topic_id: str, title: str) -> LearningUnitModel:
        statement = select(LearningUnitModel).where(
            LearningUnitModel.topic_id == topic_id,
            LearningUnitModel.title == title.strip(),
        )
        unit = session.execute(statement).scalar_one_or_none()
        if unit is None:
            unit = LearningUnitModel(topic_id=topic_id, title=title.strip())
            session.add(unit)
            session.flush()
        return unit

    def _require_role(self, actor: AuthenticatedUser, allowed_roles: set[str]) -> None:
        if not allowed_roles.intersection(actor.roles):
            raise PermissionError("No tienes permisos para realizar esta accion.")
