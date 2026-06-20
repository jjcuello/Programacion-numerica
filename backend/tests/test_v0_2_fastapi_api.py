from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path

from fastapi.testclient import TestClient

from src.interfaces.web.app import create_fastapi_app


class FastApiAdapterTests(unittest.TestCase):
    def test_fastapi_health_and_academic_flow(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            previous_env = {key: os.environ.get(key) for key in ["APP_ENV", "DATABASE_URL", "AUTO_CREATE_SCHEMA", "AUTH_TOKEN_SECRET"]}
            db_path = Path(temp_dir) / "fastapi.sqlite3"
            os.environ["APP_ENV"] = "test"
            os.environ["DATABASE_URL"] = f"sqlite+pysqlite:///{db_path}"
            os.environ["AUTO_CREATE_SCHEMA"] = "true"
            os.environ["AUTH_TOKEN_SECRET"] = "fastapi-secret-with-32-chars-minimum"

            try:
                client = TestClient(create_fastapi_app())

                health = client.get("/api/health")
                self.assertEqual(health.status_code, 200)
                self.assertEqual(health.json()["status"], "ok")

                teacher = client.post(
                    "/api/auth/register",
                    json={
                        "email": "teacher-fastapi@example.com",
                        "password": "teacher-pass-123",
                        "full_name": "Teacher FastAPI",
                        "roles": ["teacher"],
                    },
                )
                self.assertEqual(teacher.status_code, 201)
                teacher_token = teacher.json()["token"]

                student = client.post(
                    "/api/auth/register",
                    json={
                        "email": "student-fastapi@example.com",
                        "password": "student-pass-123",
                        "full_name": "Student FastAPI",
                        "roles": ["student"],
                    },
                )
                self.assertEqual(student.status_code, 201)
                student_payload = student.json()

                section = client.post(
                    "/api/academic/sections",
                    json={
                        "course_code": "PN-201",
                        "course_name": "Programacion Numerica II",
                        "term_name": "2026-II",
                        "term_starts_on": "2026-07-01",
                        "term_ends_on": "2026-12-01",
                        "section_name": "B",
                    },
                    headers={"Authorization": f"Bearer {teacher_token}"},
                )
                self.assertEqual(section.status_code, 201)
                section_id = section.json()["section"]["id"]

                enrollment = client.post(
                    "/api/academic/enrollments",
                    json={"section_id": section_id, "student_user_id": student_payload["user"]["id"]},
                    headers={"Authorization": f"Bearer {teacher_token}"},
                )
                self.assertEqual(enrollment.status_code, 201)

                assignment = client.post(
                    "/api/academic/assignments",
                    json={
                        "section_id": section_id,
                        "title": "Practica FastAPI",
                        "instructions": "Resolver por Newton.",
                        "expression": "x**3 - x - 2",
                        "allowed_methods": ["newton"],
                    },
                    headers={"Authorization": f"Bearer {teacher_token}"},
                )
                self.assertEqual(assignment.status_code, 201)
                assignment_id = assignment.json()["assignment"]["id"]

                student_token = student_payload["token"]
                mine = client.get("/api/academic/my-assignments", headers={"Authorization": f"Bearer {student_token}"})
                self.assertEqual(mine.status_code, 200)
                self.assertEqual(len(mine.json()["assignments"]), 1)

                detail = client.get(
                    f"/api/academic/assignments/{assignment_id}",
                    headers={"Authorization": f"Bearer {student_token}"},
                )
                self.assertEqual(detail.status_code, 200)
                self.assertEqual(detail.json()["assignment"]["definition"]["expression"], "x**3 - x - 2")
            finally:
                for key, value in previous_env.items():
                    if value is None:
                        os.environ.pop(key, None)
                    else:
                        os.environ[key] = value


if __name__ == "__main__":
    unittest.main()