from __future__ import annotations

from dataclasses import dataclass

from src.analysis.benchmarking.comparator import ComparisonSummary, MethodComparator
from src.app.services.run_recorders import RunRecorder
from src.core.models.problem import ProblemDefinition
from src.core.results.method_result import MethodResult
from src.methods.base import NumericalMethod


@dataclass(slots=True)
class SolveProblemUseCase:
    session_repository: RunRecorder | None = None

    def execute(self, method: NumericalMethod, problem: ProblemDefinition) -> MethodResult:
        result = method.solve(problem)

        if self.session_repository is not None:
            self.session_repository.save_run(problem=problem, result=result)

        return result


@dataclass(slots=True)
class CompareMethodsUseCase:
    comparator: MethodComparator
    session_repository: RunRecorder | None = None

    def execute(self, problem: ProblemDefinition) -> ComparisonSummary:
        summary = self.comparator.compare(problem)

        if self.session_repository is not None:
            self.session_repository.save_comparison(problem=problem, summary=summary)

        return summary