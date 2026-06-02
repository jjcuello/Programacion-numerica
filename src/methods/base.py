from __future__ import annotations

from abc import ABC, abstractmethod

from src.core.models.problem import ProblemDefinition
from src.core.results.method_result import MethodResult


class NumericalMethod(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def supports(self, problem: ProblemDefinition) -> bool:
        raise NotImplementedError

    @abstractmethod
    def solve(self, problem: ProblemDefinition) -> MethodResult:
        raise NotImplementedError