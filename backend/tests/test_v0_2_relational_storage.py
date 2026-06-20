from __future__ import annotations

import tempfile
import unittest
from datetime import date, datetime, timezone
from pathlib import Path

from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, inspect

from src.infrastructure.storage.db import create_session_factory
from src.infrastructure.storage.sql_models import (
    AcademicTermModel,
    ActivityModel,
    ActivityVersionModel,
    CourseModel,
    CourseSectionModel,
    LearningUnitModel,
    SubmissionModel,
    TopicModel,
)
from src.infrastructure.storage.sql_repositories import (
    SqlAlchemyAssignmentRepository,
    SqlAlchemyAttemptRepository,
    SqlAlchemySubmissionRepository,
    SqlAlchemyUserRepository,
)


class RelationalStorageTests(unittest.TestCase):
    def test_alembic_upgrade_creates_mvp_tables(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = Path(temp_dir) / "mvp.sqlite3"
            config = Config("/home/jcuello/Python/backend/alembic.ini")
            config.set_main_option("script_location", "/home/jcuello/Python/backend/alembic")
            config.set_main_option("sqlalchemy.url", f"sqlite+pysqlite:///{db_path}")

            command.upgrade(config, "head")

            engine = create_engine(f"sqlite+pysqlite:///{db_path}")
            try:
                tables = set(inspect(engine).get_table_names())
                self.assertTrue({"users", "assignments", "submissions", "attempts"}.issubset(tables))
            finally:
                engine.dispose()

    def test_sqlalchemy_repositories_persist_assignment_submission_attempt_flow(self):
        engine = create_engine("sqlite+pysqlite:///:memory:")
        from src.infrastructure.storage.sql_models import Base

        Base.metadata.create_all(engine)
        session_factory = create_session_factory(engine)

        with session_factory() as session:
            user_repository = SqlAlchemyUserRepository(session)
            assignment_repository = SqlAlchemyAssignmentRepository(session)
            submission_repository = SqlAlchemySubmissionRepository(session)
            attempt_repository = SqlAlchemyAttemptRepository(session)

            teacher = user_repository.create(email="teacher@example.com", password_hash="hash-teacher")
            student = user_repository.create(email="student@example.com", password_hash="hash-student")

            topic = TopicModel(name="Raices", area="Metodos numericos")
            term = AcademicTermModel(name="2026-I", starts_on=date(2026, 1, 1), ends_on=date(2026, 6, 30), status="active")
            course = CourseModel(code="PN-101", name="Programacion Numerica")
            session.add_all([topic, term, course])
            session.flush()

            unit = LearningUnitModel(topic_id=topic.id, title="Metodos de raices")
            session.add(unit)
            session.flush()

            activity = ActivityModel(
                learning_unit_id=unit.id,
                activity_type="simulation",
                title="Resolver raiz de ecuacion cubica",
                created_by_user_id=teacher.id,
            )
            session.add(activity)
            session.flush()

            version = ActivityVersionModel(
                activity_id=activity.id,
                version_number=1,
                definition={"expression": "x**3 - x - 2", "allowed_methods": ["bisection", "newton"]},
            )
            session.add(version)
            session.flush()

            section = CourseSectionModel(
                course_id=course.id,
                academic_term_id=term.id,
                teacher_user_id=teacher.id,
                section_name="A",
                status="active",
            )
            session.add(section)
            session.flush()

            assignment = assignment_repository.create(
                activity_version_id=version.id,
                section_id=section.id,
                created_by_user_id=teacher.id,
                title="Practica 1",
                instructions="Resolver con Newton y justificar convergencia.",
                status="published",
                opens_at=datetime(2026, 6, 19, tzinfo=timezone.utc),
            )
            submission = submission_repository.create(
                assignment_id=assignment.id,
                student_user_id=student.id,
                status="in_progress",
            )
            attempt = attempt_repository.create(
                submission_id=submission.id,
                attempt_number=1,
                method_name="newton",
                outcome_status="success",
                input_payload={"x0": 1.5, "tolerance": 1e-6},
                result_payload={"root": 1.52138, "iterations": 4, "status": "success"},
                execution_time_ms=1.237,
            )

            session.commit()

        try:
            with session_factory() as session:
                assignment_repository = SqlAlchemyAssignmentRepository(session)
                submission_repository = SqlAlchemySubmissionRepository(session)
                attempt_repository = SqlAlchemyAttemptRepository(session)

                assignments = assignment_repository.list_for_section(section.id)
                saved_submission = submission_repository.get_for_assignment_student(assignment.id, student.id)
                attempts = attempt_repository.list_for_submission(submission.id)

                self.assertEqual(len(assignments), 1)
                self.assertEqual(saved_submission.status, "in_progress")
                self.assertEqual(len(attempts), 1)
                self.assertEqual(attempts[0].method_name, "newton")
                self.assertEqual(attempts[0].result_payload["status"], "success")
        finally:
            engine.dispose()


if __name__ == "__main__":
    unittest.main()