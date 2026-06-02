from __future__ import annotations

from dataclasses import dataclass

from src.core.models.problem import ProblemDefinition
from src.core.results.method_result import ExecutionStatus, MethodResult
from src.methods.base import NumericalMethod


@dataclass(slots=True)
class ComparisonSummary:
    problem_name: str
    results: list[MethodResult]

    def best_result(self) -> MethodResult | None:
        successful = [result for result in self.results if result.status == ExecutionStatus.SUCCESS]
        if not successful:
            return None

        return min(
            successful,
            key=lambda result: (
                float("inf") if result.residual is None else abs(result.residual),
                result.elapsed_seconds,
                result.iteration_count,
            ),
        )


class MethodComparator:
    def __init__(self, methods: list[NumericalMethod]):
        self.methods = methods

    def compare(self, problem: ProblemDefinition) -> ComparisonSummary:
        results: list[MethodResult] = []

        for method in self.methods:
            if not method.supports(problem):
                results.append(
                    MethodResult(
                        method_name=method.name,
                        problem_kind=problem.kind,
                        status=ExecutionStatus.UNSUPPORTED,
                        message="El metodo no soporta este tipo de problema.",
                    )
                )
                continue

            results.append(method.solve(problem))

        return ComparisonSummary(problem_name=problem.name, results=results)