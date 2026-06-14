from __future__ import annotations

import math
import time

from src.core.expressions.parser import build_scalar_function
from src.core.models.problem import ProblemDefinition, ProblemKind
from src.core.results.iteration import IterationRecord
from src.core.results.method_result import ExecutionStatus, MethodResult
from src.methods.base import NumericalMethod


class BisectionMethod(NumericalMethod):
    @property
    def name(self) -> str:
        return "bisection"

    def supports(self, problem: ProblemDefinition) -> bool:
        return (
            problem.kind == ProblemKind.SCALAR_ROOT
            and problem.expression is not None
            and problem.interval is not None
        )

    def solve(self, problem: ProblemDefinition) -> MethodResult:
        started_at = time.perf_counter()

        if not self.supports(problem):
            return MethodResult(
                method_name=self.name,
                problem_kind=problem.kind,
                status=ExecutionStatus.UNSUPPORTED,
                message="Biseccion requiere una expresion escalar y un intervalo [a, b].",
            )

        function = build_scalar_function(problem.expression or "")
        left, right = problem.interval or (0.0, 0.0)

        try:
            f_left = function(left)
            f_right = function(right)
        except Exception as error:
            return MethodResult(
                method_name=self.name,
                problem_kind=problem.kind,
                status=ExecutionStatus.FAILED,
                elapsed_seconds=time.perf_counter() - started_at,
                message=f"No se pudo evaluar el intervalo inicial: {error}",
            )

        if f_left * f_right >= 0:
            return MethodResult(
                method_name=self.name,
                problem_kind=problem.kind,
                status=ExecutionStatus.FAILED,
                elapsed_seconds=time.perf_counter() - started_at,
                message="El intervalo [a, b] no presenta cambio de signo.",
                metadata={"interval": (left, right), "f(a)": f_left, "f(b)": f_right},
            )

        records: list[IterationRecord] = []
        midpoint = left
        residual = f_left

        for iteration in range(1, problem.max_iterations + 1):
            midpoint = (left + right) / 2.0
            residual = function(midpoint)
            delta = abs(right - left) / 2.0

            records.append(
                IterationRecord(
                    iteration=iteration,
                    estimate=midpoint,
                    residual=residual,
                    absolute_error=abs(residual),
                    delta=delta,
                    metadata={"a": left, "b": right},
                )
            )

            if abs(residual) < problem.tolerance or delta < problem.tolerance:
                return MethodResult(
                    method_name=self.name,
                    problem_kind=problem.kind,
                    status=ExecutionStatus.SUCCESS,
                    solution=midpoint,
                    residual=residual,
                    iteration_count=iteration,
                    elapsed_seconds=time.perf_counter() - started_at,
                    records=records,
                    message="Metodo de biseccion convergio correctamente.",
                    metadata={"interval": (problem.interval or (left, right))},
                )

            if f_left * residual < 0:
                right = midpoint
                f_right = residual
            else:
                left = midpoint
                f_left = residual

            if not math.isfinite(residual):
                return MethodResult(
                    method_name=self.name,
                    problem_kind=problem.kind,
                    status=ExecutionStatus.FAILED,
                    solution=midpoint,
                    residual=residual,
                    iteration_count=iteration,
                    elapsed_seconds=time.perf_counter() - started_at,
                    records=records,
                    message="Se encontro un valor no finito durante la iteracion.",
                )

        return MethodResult(
            method_name=self.name,
            problem_kind=problem.kind,
            status=ExecutionStatus.DID_NOT_CONVERGE,
            solution=midpoint,
            residual=residual,
            iteration_count=problem.max_iterations,
            elapsed_seconds=time.perf_counter() - started_at,
            records=records,
            message="Se alcanzo el maximo de iteraciones sin converger.",
        )