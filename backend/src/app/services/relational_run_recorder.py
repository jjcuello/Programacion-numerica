from __future__ import annotations

from dataclasses import dataclass

from src.analysis.benchmarking.comparator import ComparisonSummary
from src.app.services.academic_service import AcademicWorkflowService
from src.app.services.auth_service import AuthenticatedUser
from src.core.models.problem import ProblemDefinition
from src.core.results.method_result import MethodResult


@dataclass(slots=True)
class RelationalRunRecorder:
    academic_service: AcademicWorkflowService
    actor: AuthenticatedUser | None = None

    def save_run(self, problem: ProblemDefinition, result: MethodResult) -> dict[str, object] | None:
        assignment_id = problem.metadata.get("assignment_id")
        if not isinstance(assignment_id, str) or not assignment_id.strip() or self.actor is None:
            return None
        recorded = self.academic_service.record_attempt(
            actor=self.actor,
            assignment_id=assignment_id.strip(),
            problem=problem,
            result=result,
        )
        return {
            "submission_id": recorded.submission_id,
            "attempt_id": recorded.attempt_id,
            "attempt_number": recorded.attempt_number,
        }

    def save_comparison(self, problem: ProblemDefinition, summary: ComparisonSummary) -> list[dict[str, object] | None]:
        outputs = []
        for result in summary.results:
            outputs.append(self.save_run(problem, result))
        return outputs
