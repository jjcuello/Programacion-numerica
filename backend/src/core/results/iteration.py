from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class IterationRecord:
    iteration: int
    estimate: float | tuple[float, ...] | None = None
    residual: float | None = None
    absolute_error: float | None = None
    relative_error: float | None = None
    delta: float | None = None
    metadata: dict[str, Any] = field(default_factory=dict)