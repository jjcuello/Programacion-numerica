from __future__ import annotations

import json
import os
import tempfile
import threading
import unittest
from pathlib import Path
from urllib import request

from src.infrastructure.storage import DatabaseSettings
from src.interfaces.web.app import create_server


class WebAcademicFlowTests(unittest.TestCase):
    def test_database_settings_defaults_to_sqlite_in_development(self):
        previous_app_env = os.environ.get("APP_ENV")
        previous_database_url = os.environ.get("DATABASE_URL")
        previous_auto_create_schema = os.environ.get("AUTO_CREATE_SCHEMA")
        try:
            os.environ["APP_ENV"] = "development"
            os.environ.pop("DATABASE_URL", None)
            os.environ.pop("AUTO_CREATE_SCHEMA", None)
            settings = DatabaseSettings.from_env()
            self.assertTrue(settings.url.startswith("sqlite+pysqlite:///"))
            self.assertTrue(settings.auto_create_schema)
        finally:
            if previous_app_env is None:
                os.environ.pop("APP_ENV", None)
            else:
                os.environ["APP_ENV"] = previous_app_env
            if previous_database_url is None:
                os.environ.pop("DATABASE_URL", None)
            else:
                os.environ["DATABASE_URL"] = previous_database_url
            if previous_auto_create_schema is None:
                os.environ.pop("AUTO_CREATE_SCHEMA", None)
            else:
                os.environ["AUTO_CREATE_SCHEMA"] = previous_auto_create_schema

    def test_auth_assignment_and_solve_flow_records_attempt(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            previous_env = {key: os.environ.get(key) for key in ["APP_ENV", "DATABASE_URL", "AUTO_CREATE_SCHEMA", "AUTH_TOKEN_SECRET"]}
            db_path = Path(temp_dir) / "academic.sqlite3"
            os.environ["APP_ENV"] = "test"
            os.environ["DATABASE_URL"] = f"sqlite+pysqlite:///{db_path}"
            os.environ["AUTO_CREATE_SCHEMA"] = "true"
            os.environ["AUTH_TOKEN_SECRET"] = "test-secret-with-32-chars-minimum-key"

            server = create_server(host="127.0.0.1", port=0)
            try:
                thread = threading.Thread(target=server.serve_forever, daemon=True)
                thread.start()
                base_url = f"http://127.0.0.1:{server.server_port}"

                teacher = self._post_json(
                    f"{base_url}/api/auth/register",
                    {
                        "email": "teacher@example.com",
                        "password": "teacher-pass-123",
                        "full_name": "Teacher User",
                        "roles": ["teacher"],
                    },
                    expected_status=201,
                )
                student = self._post_json(
                    f"{base_url}/api/auth/register",
                    {
                        "email": "student@example.com",
                        "password": "student-pass-123",
                        "full_name": "Student User",
                        "roles": ["student"],
                    },
                    expected_status=201,
                )

                teacher_token = teacher["token"]
                student_token = student["token"]

                section = self._post_json(
                    f"{base_url}/api/academic/sections",
                    {
                        "course_code": "PN-101",
                        "course_name": "Programacion Numerica",
                        "term_name": "2026-I",
                        "term_starts_on": "2026-01-10",
                        "term_ends_on": "2026-06-30",
                        "section_name": "A",
                    },
                    token=teacher_token,
                    expected_status=201,
                )
                section_id = section["section"]["id"]

                self._post_json(
                    f"{base_url}/api/academic/enrollments",
                    {"section_id": section_id, "student_user_id": student["user"]["id"]},
                    token=teacher_token,
                    expected_status=201,
                )

                assignment = self._post_json(
                    f"{base_url}/api/academic/assignments",
                    {
                        "section_id": section_id,
                        "title": "Practica de Newton",
                        "instructions": "Resolver la ecuacion usando Newton.",
                        "expression": "x**3 - x - 2",
                        "allowed_methods": ["newton"],
                    },
                    token=teacher_token,
                    expected_status=201,
                )
                assignment_id = assignment["assignment"]["id"]

                solve_response = self._post_json(
                    f"{base_url}/api/roots/solve",
                    {
                        "method": "newton",
                        "expression": "x**3 - x - 2",
                        "x0": 1.5,
                        "tolerance": 1e-6,
                        "max_iterations": 50,
                        "assignment_id": assignment_id,
                    },
                    token=student_token,
                    expected_status=200,
                )

                self.assertEqual(solve_response["result"]["status"], "success")

                login_response = self._post_json(
                    f"{base_url}/api/auth/login",
                    {"email": "student@example.com", "password": "student-pass-123"},
                    expected_status=200,
                )
                self.assertEqual(login_response["user"]["email"], "student@example.com")

                from sqlalchemy import create_engine, select
                from src.infrastructure.storage.sql_models import AttemptModel, SubmissionModel

                engine = create_engine(f"sqlite+pysqlite:///{db_path}")
                try:
                    with engine.connect() as connection:
                        attempts = connection.execute(select(AttemptModel)).all()
                        submissions = connection.execute(select(SubmissionModel)).all()
                    self.assertEqual(len(submissions), 1)
                    self.assertEqual(len(attempts), 1)
                finally:
                    engine.dispose()
            finally:
                server.shutdown()
                server.server_close()
                for key, value in previous_env.items():
                    if value is None:
                        os.environ.pop(key, None)
                    else:
                        os.environ[key] = value

    def _post_json(self, url: str, payload: dict[str, object], token: str | None = None, expected_status: int = 200) -> dict[str, object]:
        headers = {"Content-Type": "application/json"}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        response = request.urlopen(
            request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers=headers,
                method="POST",
            )
        )
        self.assertEqual(response.status, expected_status)
        return json.loads(response.read().decode("utf-8"))


if __name__ == "__main__":
    unittest.main()