from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.analysis.benchmarking.comparator import ComparisonSummary
from src.core.models.problem import ProblemDefinition
from src.core.results.method_result import MethodResult


class JsonSessionRepository:
    def __init__(self, base_path: str | Path):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    def save_run(self, problem: ProblemDefinition, result: MethodResult) -> Path:
        payload = {
            "type": "single_run",
            "created_at": self._timestamp(),
            "problem": problem.to_dict(),
            "result": self._serialize_method_result(result),
        }
        return self._write_payload(problem.name, payload)

    def save_comparison(self, problem: ProblemDefinition, summary: ComparisonSummary) -> Path:
        payload = {
            "type": "comparison",
            "created_at": self._timestamp(),
            "problem": problem.to_dict(),
            "results": [self._serialize_method_result(result) for result in summary.results],
            "best_result": (
                self._serialize_method_result(summary.best_result())
                if summary.best_result() is not None
                else None
            ),
        }
        return self._write_payload(problem.name, payload)

    def list_sessions(self) -> list[Path]:
        return sorted(self.base_path.glob("*.json"))

    def load_session(self, session_path: str | Path) -> dict[str, Any]:
        return json.loads(Path(session_path).read_text(encoding="utf-8"))

    def _write_payload(self, problem_name: str, payload: dict[str, Any]) -> Path:
        safe_name = self._slugify(problem_name)
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        output_path = self.base_path / f"{timestamp}_{safe_name}.json"
        output_path.write_text(
            json.dumps(payload, indent=2, ensure_ascii=True),
            encoding="utf-8",
        )
        return output_path

    def _serialize_method_result(self, result: MethodResult | None) -> dict[str, Any] | None:
        if result is None:
            return None

        data = asdict(result) if is_dataclass(result) else dict(result)
        data["problem_kind"] = result.problem_kind.value
        data["status"] = result.status.value
        return data

    def _timestamp(self) -> str:
        return datetime.now(timezone.utc).isoformat()

    def _slugify(self, value: str) -> str:
        normalized = [character.lower() if character.isalnum() else "_" for character in value]
        compact = "".join(normalized).strip("_")
        while "__" in compact:
            compact = compact.replace("__", "_")
        return compact or "session"