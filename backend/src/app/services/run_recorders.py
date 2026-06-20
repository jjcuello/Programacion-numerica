from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol

from src.analysis.benchmarking.comparator import ComparisonSummary
from src.core.models.problem import ProblemDefinition
from src.core.results.method_result import MethodResult


class RunRecorder(Protocol):
    def save_run(self, problem: ProblemDefinition, result: MethodResult) -> object:
        ...

    def save_comparison(self, problem: ProblemDefinition, summary: ComparisonSummary) -> object:
        ...


@dataclass(slots=True)
class CompositeRunRecorder:
    recorders: list[RunRecorder] = field(default_factory=list)

    def save_run(self, problem: ProblemDefinition, result: MethodResult) -> list[object]:
        outputs = []
        for recorder in self.recorders:
            outputs.append(recorder.save_run(problem, result))
        return outputs

    def save_comparison(self, problem: ProblemDefinition, summary: ComparisonSummary) -> list[object]:
        outputs = []
        for recorder in self.recorders:
            outputs.append(recorder.save_comparison(problem, summary))
        return outputs
