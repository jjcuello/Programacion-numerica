import json
import tempfile
import unittest
from pathlib import Path

from src.analysis.benchmarking.comparator import MethodComparator
from src.app.use_cases.solve_problem import CompareMethodsUseCase, SolveProblemUseCase
from src.core.models.problem import ProblemDefinition, ProblemKind
from src.infrastructure.storage.session_repository import JsonSessionRepository
from src.interfaces.cli.app import run
from src.methods.roots.bisection_method import BisectionMethod
from src.methods.roots.newton_method import NewtonMethod


class CliAndStorageTests(unittest.TestCase):
    def test_json_repository_saves_single_run(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            repository = JsonSessionRepository(temp_dir)
            problem = ProblemDefinition(
                name="ecuacion cubica",
                kind=ProblemKind.SCALAR_ROOT,
                expression="x**3 - x - 2",
                interval=(1.0, 2.0),
                tolerance=1e-6,
            )

            result = SolveProblemUseCase(session_repository=repository).execute(
                BisectionMethod(),
                problem,
            )

            sessions = repository.list_sessions()
            self.assertEqual(result.status.value, "success")
            self.assertEqual(len(sessions), 1)

            payload = json.loads(Path(sessions[0]).read_text(encoding="utf-8"))
            self.assertEqual(payload["type"], "single_run")
            self.assertEqual(payload["problem"]["name"], "ecuacion cubica")

    def test_compare_use_case_saves_comparison(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            repository = JsonSessionRepository(temp_dir)
            problem = ProblemDefinition(
                name="comparacion cubica",
                kind=ProblemKind.SCALAR_ROOT,
                expression="x**3 - x - 2",
                interval=(1.0, 2.0),
                initial_guess=(1.5,),
                tolerance=1e-6,
            )

            summary = CompareMethodsUseCase(
                comparator=MethodComparator([BisectionMethod(), NewtonMethod()]),
                session_repository=repository,
            ).execute(problem)

            sessions = repository.list_sessions()
            self.assertEqual(len(summary.results), 2)
            self.assertEqual(len(sessions), 1)

            payload = repository.load_session(sessions[0])
            self.assertEqual(payload["type"], "comparison")
            self.assertEqual(len(payload["results"]), 2)
            self.assertIsNotNone(payload["best_result"])

    def test_cli_solve_command_creates_session_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            exit_code = run(
                [
                    "solve",
                    "--method",
                    "newton",
                    "--expression",
                    "x**3 - x - 2",
                    "--x0",
                    "1.5",
                    "--save-session",
                    "--session-dir",
                    temp_dir,
                ]
            )

            self.assertEqual(exit_code, 0)
            saved_files = sorted(Path(temp_dir).glob("*.json"))
            self.assertEqual(len(saved_files), 1)


if __name__ == "__main__":
    unittest.main()