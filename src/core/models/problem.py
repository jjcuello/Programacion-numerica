from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class ProblemKind(str, Enum):
    SCALAR_ROOT = "scalar_root"
    NONLINEAR_SYSTEM = "nonlinear_system"
    CONSTANT_ANALYSIS = "constant_analysis"
    SAFE_EVALUATION = "safe_evaluation"


@dataclass(slots=True)
class ProblemDefinition:
    name: str
    kind: ProblemKind
    expression: str | None = None
    expressions: tuple[str, ...] = ()
    variable_names: tuple[str, ...] = ("x",)
    interval: tuple[float, float] | None = None
    initial_guess: tuple[float, ...] = ()
    tolerance: float = 1e-6
    max_iterations: int = 100
    precision: str = "float64"
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "kind": self.kind.value,
            "expression": self.expression,
            "expressions": list(self.expressions),
            "variable_names": list(self.variable_names),
            "interval": self.interval,
            "initial_guess": list(self.initial_guess),
            "tolerance": self.tolerance,
            "max_iterations": self.max_iterations,
            "precision": self.precision,
            "metadata": dict(self.metadata),
        }