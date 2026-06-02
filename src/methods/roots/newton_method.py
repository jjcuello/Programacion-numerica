from __future__ import annotations

import math
import time

from src.core.expressions.parser import build_scalar_function_with_derivative
from src.core.models.problem import ProblemDefinition, ProblemKind
from src.core.results.iteration import IterationRecord
from src.core.results.method_result import ExecutionStatus, MethodResult
from src.methods.base import NumericalMethod


class NewtonMethod(NumericalMethod):
    @property
    def name(self) -> str:
        return "newton_raphson"

    def supports(self, problem: ProblemDefinition) -> bool:
        return (
            problem.kind == ProblemKind.SCALAR_ROOT
            and problem.expression is not None
            and len(problem.initial_guess) >= 1
        )

    def solve(self, problem: ProblemDefinition) -> MethodResult:
        started_at = time.perf_counter()

        if not self.supports(problem):
            return MethodResult(
                method_name=self.name,
                problem_kind=problem.kind,
                status=ExecutionStatus.UNSUPPORTED,
                elapsed_seconds=time.perf_counter() - started_at,
                message="Newton-Raphson requiere una expresion escalar y un valor inicial x0.",
            )

        try:
            function, derivative = build_scalar_function_with_derivative(problem.expression or "")
        except Exception as error:
            return MethodResult(
                method_name=self.name,
                problem_kind=problem.kind,
                status=ExecutionStatus.FAILED,
                elapsed_seconds=time.perf_counter() - started_at,
                message=f"No se pudo construir la funcion derivable: {error}",
            )

        current = float(problem.initial_guess[0])
        records: list[IterationRecord] = []
        residual = None

        for iteration in range(1, problem.max_iterations + 1):
            try:
                fx = function(current)
                dfx = derivative(current)
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
                )

            if not math.isfinite(fx) or not math.isfinite(dfx):
                return MethodResult(
                    method_name=self.name,
                    problem_kind=problem.kind,
                    status=ExecutionStatus.FAILED,
                    solution=current,
                    residual=fx,
                    iteration_count=iteration - 1,
                    elapsed_seconds=time.perf_counter() - started_at,
                    records=records,
                    message="Se obtuvieron valores no finitos durante la iteracion.",
                )

            if dfx == 0:
                return MethodResult(
                    method_name=self.name,
                    problem_kind=problem.kind,
                    status=ExecutionStatus.FAILED,
                    solution=current,
                    residual=fx,
                    iteration_count=iteration - 1,
                    elapsed_seconds=time.perf_counter() - started_at,
                    records=records,
                    message="La derivada es cero en el punto actual.",
                )

            next_value = current - (fx / dfx)
            delta = abs(next_value - current)
            residual = fx
            records.append(
                IterationRecord(
                    iteration=iteration,
                    estimate=next_value,
                    residual=fx,
                    absolute_error=abs(fx),
                    delta=delta,
                    metadata={"x(i)": current, "f'(x)": dfx},
                )
            )

            if abs(fx) < problem.tolerance or delta < problem.tolerance:
                return MethodResult(
                    method_name=self.name,
                    problem_kind=problem.kind,
                    status=ExecutionStatus.SUCCESS,
                    solution=next_value,
                    residual=function(next_value),
                    iteration_count=iteration,
                    elapsed_seconds=time.perf_counter() - started_at,
                    records=records,
                    message="Metodo de Newton-Raphson convergio correctamente.",
                    metadata={"initial_guess": current},
                )

            current = next_value

        final_residual = function(current)
        return MethodResult(
            method_name=self.name,
            problem_kind=problem.kind,
            status=ExecutionStatus.DID_NOT_CONVERGE,
            solution=current,
            residual=final_residual,
            iteration_count=problem.max_iterations,
            elapsed_seconds=time.perf_counter() - started_at,
            records=records,
            message="Se alcanzo el maximo de iteraciones sin converger.",
        )