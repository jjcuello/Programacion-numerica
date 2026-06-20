from __future__ import annotations

import math
import time

from src.core.expressions.parser import build_scalar_function
from src.core.models.problem import ProblemDefinition, ProblemKind
from src.core.results.iteration import IterationRecord
from src.core.results.method_result import ExecutionStatus, MethodResult
from src.methods.base import NumericalMethod


class SecantMethod(NumericalMethod):
    @property
    def name(self) -> str:
        return "secant"

    def supports(self, problem: ProblemDefinition) -> bool:
        return (
            problem.kind == ProblemKind.SCALAR_ROOT
            and problem.expression is not None
            and len(problem.initial_guess) >= 2
        )

    def solve(self, problem: ProblemDefinition) -> MethodResult:
        started_at = time.perf_counter()

        if not self.supports(problem):
            return MethodResult(
                method_name=self.name,
                problem_kind=problem.kind,
                status=ExecutionStatus.UNSUPPORTED,
                elapsed_seconds=time.perf_counter() - started_at,
                message="Secante requiere una expresion escalar y dos valores iniciales x0, x1.",
                metadata={"ui_status": "unsupported"},
            )

        try:
            function = build_scalar_function(problem.expression or "")
        except Exception as error:
            return MethodResult(
                method_name=self.name,
                problem_kind=problem.kind,
                status=ExecutionStatus.FAILED,
                elapsed_seconds=time.perf_counter() - started_at,
                message=f"No se pudo construir la funcion escalar: {error}",
                metadata={"ui_status": "singularidad"},
            )

        previous = float(problem.initial_guess[0])
        current = float(problem.initial_guess[1])
        records: list[IterationRecord] = []
        residual = None

        for iteration in range(1, problem.max_iterations + 1):
            try:
                f_previous = function(previous)
                f_current = function(current)
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
                    message=f"No se pudo evaluar la funcion en la iteracion {iteration}: {error}",
                    metadata={"ui_status": "singularidad"},
                )

            denominator = f_current - f_previous
            if not math.isfinite(f_previous) or not math.isfinite(f_current) or abs(denominator) < 1e-12:
                return MethodResult(
                    method_name=self.name,
                    problem_kind=problem.kind,
                    status=ExecutionStatus.FAILED,
                    solution=current,
                    residual=f_current,
                    iteration_count=iteration - 1,
                    elapsed_seconds=time.perf_counter() - started_at,
                    records=records,
                    message="La secante encontro un denominador nulo o valores no finitos.",
                    metadata={"ui_status": "singularidad"},
                )

            next_value = current - f_current * (current - previous) / denominator
            delta = abs(next_value - current)

            try:
                next_residual = function(next_value)
            except Exception as error:
                return MethodResult(
                    method_name=self.name,
                    problem_kind=problem.kind,
                    status=ExecutionStatus.FAILED,
                    solution=current,
                    residual=f_current,
                    iteration_count=iteration - 1,
                    elapsed_seconds=time.perf_counter() - started_at,
                    records=records,
                    message=f"No se pudo evaluar la siguiente aproximacion: {error}",
                    metadata={"ui_status": "singularidad"},
                )

            residual = next_residual
            records.append(
                IterationRecord(
                    iteration=iteration,
                    estimate=next_value,
                    residual=next_residual,
                    absolute_error=abs(next_residual),
                    delta=delta,
                    metadata={"x(i-1)": previous, "x(i)": current},
                )
            )

            if abs(next_residual) < problem.tolerance or delta < problem.tolerance:
                return MethodResult(
                    method_name=self.name,
                    problem_kind=problem.kind,
                    status=ExecutionStatus.SUCCESS,
                    solution=next_value,
                    residual=next_residual,
                    iteration_count=iteration,
                    elapsed_seconds=time.perf_counter() - started_at,
                    records=records,
                    message="Metodo de la secante convergio correctamente.",
                    metadata={"initial_guess": (problem.initial_guess[0], problem.initial_guess[1]), "ui_status": "success"},
                )

            previous = current
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
            metadata={"ui_status": "max_iter"},
        )