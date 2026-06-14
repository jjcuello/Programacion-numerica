from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from src.core.models.problem import ProblemKind
from src.core.results.iteration import IterationRecord


class ExecutionStatus(str, Enum):
    SUCCESS = "success"
    FAILED = "failed"
    DID_NOT_CONVERGE = "did_not_converge"
    UNSUPPORTED = "unsupported"


@dataclass(slots=True)
class MethodResult:
    method_name: str
    problem_kind: ProblemKind
    status: ExecutionStatus
    solution: float | tuple[float, ...] | None = None
    residual: float | None = None
    iteration_count: int = 0
    elapsed_seconds: float = 0.0
    records: list[IterationRecord] = field(default_factory=list)
    message: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def converged(self) -> bool:
        return self.status == ExecutionStatus.SUCCESS