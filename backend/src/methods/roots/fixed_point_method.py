from __future__ import annotations

import math
import time

from src.core.expressions.parser import build_scalar_function
from src.core.models.problem import ProblemDefinition, ProblemKind
from src.core.results.iteration import IterationRecord
from src.core.results.method_result import ExecutionStatus, MethodResult
from src.methods.base import NumericalMethod


class FixedPointMethod(NumericalMethod):
    @property
    def name(self) -> str:
        return "fixedpoint"

    def supports(self, problem: ProblemDefinition) -> bool:
        return (
            problem.kind == ProblemKind.SCALAR_ROOT
            and len(problem.initial_guess) >= 1
            and isinstance(problem.metadata.get("g_expression"), str)
            and problem.metadata.get("g_expression", "").strip() != ""
        )

    def solve(self, problem: ProblemDefinition) -> MethodResult:
        started_at = time.perf_counter()

        if not self.supports(problem):
            return MethodResult(
                method_name=self.name,
                problem_kind=problem.kind,
                status=ExecutionStatus.UNSUPPORTED,
                elapsed_seconds=time.perf_counter() - started_at,
                message="Punto fijo requiere x0 y una expresion g(x).",
                metadata={"ui_status": "unsupported"},
            )

        g_expression = str(problem.metadata.get("g_expression", "")).strip()

        try:
            function_g = build_scalar_function(g_expression)
            function_f = build_scalar_function(problem.expression or "") if problem.expression else None
        except Exception as error:
            return MethodResult(
                method_name=self.name,
                problem_kind=problem.kind,
                status=ExecutionStatus.FAILED,
                elapsed_seconds=time.perf_counter() - started_at,
                message=f"No se pudo construir la funcion de punto fijo: {error}",
                metadata={"ui_status": "singularidad"},
            )

        current = float(problem.initial_guess[0])
        records: list[IterationRecord] = []
        residual = None

        for iteration in range(1, problem.max_iterations + 1):
            try:
                next_value = function_g(current)
                residual = function_f(current) if function_f is not None else current - next_value
            except Exception as error:
                return MethodResult(
                    method_name=self.name,
                    problem_kind=problem.kind,
                    status=ExecutionStatus.FAILED,
                    solution=current,
                    residual=residual,
                    iteration_count=iteration - 1,
                    elapsed_seconds=time.perf_counter() - started_at,
                    records=records,
                    message=f"No se pudo evaluar la iteracion de punto fijo: {error}",
                    metadata={"ui_status": "singularidad"},
                )

            if not math.isfinite(next_value) or not math.isfinite(residual):
                return MethodResult(
                    method_name=self.name,
                    problem_kind=problem.kind,
                    status=ExecutionStatus.FAILED,
                    solution=current,
                    residual=residual,
                    iteration_count=iteration - 1,
                    elapsed_seconds=time.perf_counter() - started_at,
                    records=records,
                    message="Se obtuvo un valor no finito durante la iteracion.",
                    metadata={"ui_status": "singularidad"},
                )

            delta = abs(next_value - current)
            relative_error = delta / abs(next_value) if next_value != 0 else 0.0
            records.append(
                IterationRecord(
                    iteration=iteration,
                    estimate=next_value,
                    residual=residual,
                    absolute_error=abs(residual),
                    relative_error=relative_error,
                    delta=delta,
                    metadata={"x(i)": current},
                )
            )

            if delta < problem.tolerance or abs(residual) < problem.tolerance:
                final_residual = function_f(next_value) if function_f is not None else next_value - function_g(next_value)
                return MethodResult(
                    method_name=self.name,
                    problem_kind=problem.kind,
                    status=ExecutionStatus.SUCCESS,
                    solution=next_value,
                    residual=final_residual,
                    iteration_count=iteration,
                    elapsed_seconds=time.perf_counter() - started_at,
                    records=records,
                    message="Metodo de punto fijo convergio correctamente.",
                    metadata={"ui_status": "success", "g_expression": g_expression},
                )

            current = next_value

        return MethodResult(
            method_name=self.name,
            problem_kind=problem.kind,
            status=ExecutionStatus.DID_NOT_CONVERGE,
            solution=current,
            residual=residual,
            iteration_count=problem.max_iterations,
            elapsed_seconds=time.perf_counter() - started_at,
            records=records,
            message="Se alcanzo el maximo de iteraciones sin converger.",
            metadata={"ui_status": "max_iter", "g_expression": g_expression},
        )