import unittest

from src.analysis.benchmarking.comparator import MethodComparator
from src.core.models.problem import ProblemDefinition, ProblemKind
from src.core.results.method_result import ExecutionStatus, MethodResult
from src.methods.base import NumericalMethod
from src.methods.roots.bisection_method import BisectionMethod
from src.methods.roots.newton_method import NewtonMethod


class SupportedMethod(NumericalMethod):
    @property
    def name(self) -> str:
        return "supported"

    def supports(self, problem: ProblemDefinition) -> bool:
        return problem.kind == ProblemKind.SCALAR_ROOT

    def solve(self, problem: ProblemDefinition) -> MethodResult:
        return MethodResult(
            method_name=self.name,
            problem_kind=problem.kind,
            status=ExecutionStatus.SUCCESS,
            solution=1.52138,
            residual=1e-8,
            iteration_count=7,
            elapsed_seconds=0.01,
            message=f"Problema resuelto: {problem.name}",
        )


class UnsupportedMethod(NumericalMethod):
    @property
    def name(self) -> str:
        return "unsupported"

    def supports(self, problem: ProblemDefinition) -> bool:
        return False

    def solve(self, problem: ProblemDefinition) -> MethodResult:
        raise AssertionError("solve() no debe ejecutarse para metodos no compatibles")


class MethodComparatorTests(unittest.TestCase):
    def test_problem_definition_serializes_expected_fields(self):
        problem = ProblemDefinition(
            name="ecuacion cubica",
            kind=ProblemKind.SCALAR_ROOT,
            expression="x**3 - x - 2",
            interval=(1.0, 2.0),
            initial_guess=(1.5,),
            metadata={"origin": "unit-test"},
        )

        serialized = problem.to_dict()

        self.assertEqual(serialized["name"], "ecuacion cubica")
        self.assertEqual(serialized["kind"], "scalar_root")
        self.assertEqual(serialized["interval"], (1.0, 2.0))
        self.assertEqual(serialized["initial_guess"], [1.5])

    def test_comparator_marks_unsupported_methods(self):
        problem = ProblemDefinition(name="demo", kind=ProblemKind.SCALAR_ROOT)
        comparator = MethodComparator([SupportedMethod(), UnsupportedMethod()])

        summary = comparator.compare(problem)

        self.assertEqual(len(summary.results), 2)
        self.assertEqual(summary.results[0].status, ExecutionStatus.SUCCESS)
        self.assertEqual(summary.results[1].status, ExecutionStatus.UNSUPPORTED)

    def test_best_result_returns_successful_method(self):
        problem = ProblemDefinition(name="demo", kind=ProblemKind.SCALAR_ROOT)
        comparator = MethodComparator([SupportedMethod()])

        summary = comparator.compare(problem)
        best = summary.best_result()

        self.assertIsNotNone(best)
        self.assertEqual(best.method_name, "supported")

    def test_bisection_method_solves_scalar_root_problem(self):
        problem = ProblemDefinition(
            name="ecuacion cubica",
            kind=ProblemKind.SCALAR_ROOT,
            expression="x**3 - x - 2",
            interval=(1.0, 2.0),
            tolerance=1e-6,
            max_iterations=100,
        )

        result = BisectionMethod().solve(problem)

        self.assertEqual(result.status, ExecutionStatus.SUCCESS)
        self.assertIsNotNone(result.solution)
        assert result.solution is not None
        self.assertAlmostEqual(result.solution, 1.52138, places=4)
        self.assertGreater(len(result.records), 0)

    def test_bisection_method_rejects_invalid_interval(self):
        problem = ProblemDefinition(
            name="intervalo invalido",
            kind=ProblemKind.SCALAR_ROOT,
            expression="x**2 + 1",
            interval=(-1.0, 1.0),
        )

        result = BisectionMethod().solve(problem)

        self.assertEqual(result.status, ExecutionStatus.FAILED)
        self.assertIn("cambio de signo", result.message)

    def test_newton_method_solves_scalar_root_problem(self):
        problem = ProblemDefinition(
            name="ecuacion cubica",
            kind=ProblemKind.SCALAR_ROOT,
            expression="x**3 - x - 2",
            initial_guess=(1.5,),
            tolerance=1e-6,
            max_iterations=100,
        )

        result = NewtonMethod().solve(problem)

        self.assertEqual(result.status, ExecutionStatus.SUCCESS)
        self.assertIsNotNone(result.solution)
        assert result.solution is not None
        self.assertAlmostEqual(result.solution, 1.52138, places=4)
        self.assertGreater(len(result.records), 0)

    def test_newton_method_fails_when_derivative_is_zero(self):
        problem = ProblemDefinition(
            name="derivada nula",
            kind=ProblemKind.SCALAR_ROOT,
            expression="x**2",
            initial_guess=(0.0,),
            tolerance=1e-6,
            max_iterations=10,
        )

        result = NewtonMethod().solve(problem)

        self.assertEqual(result.status, ExecutionStatus.FAILED)
        self.assertIn("derivada es cero", result.message)


if __name__ == "__main__":
    unittest.main()