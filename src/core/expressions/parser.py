from __future__ import annotations

from collections.abc import Callable

from sympy import E, lambdify, pi, symbols
from sympy.parsing.sympy_parser import (
    convert_xor,
    implicit_multiplication_application,
    parse_expr,
    standard_transformations,
)


def build_scalar_function(expression: str, variable_name: str = "x") -> Callable[[float], float]:
    variable = symbols(variable_name)
    transformations = standard_transformations + (
        implicit_multiplication_application,
        convert_xor,
    )

    symbolic_expression = parse_expr(
        expression,
        local_dict={variable_name: variable, "pi": pi, "e": E},
        transformations=transformations,
    )

    if symbolic_expression.free_symbols - {variable}:
        raise ValueError(f"Solo se permite la variable {variable_name} en la expresion.")

    raw_function = lambdify(variable, symbolic_expression, modules=["math"])

    def evaluate(value: float) -> float:
        return float(raw_function(float(value)))

    return evaluate


def build_scalar_function_with_derivative(
    expression: str,
    variable_name: str = "x",
) -> tuple[Callable[[float], float], Callable[[float], float]]:
    variable = symbols(variable_name)
    transformations = standard_transformations + (
        implicit_multiplication_application,
        convert_xor,
    )

    symbolic_expression = parse_expr(
        expression,
        local_dict={variable_name: variable, "pi": pi, "e": E},
        transformations=transformations,
    )

    if symbolic_expression.free_symbols - {variable}:
        raise ValueError(f"Solo se permite la variable {variable_name} en la expresion.")

    derivative_expression = symbolic_expression.diff(variable)
    raw_function = lambdify(variable, symbolic_expression, modules=["math"])
    raw_derivative = lambdify(variable, derivative_expression, modules=["math"])

    def evaluate(value: float) -> float:
        return float(raw_function(float(value)))

    def evaluate_derivative(value: float) -> float:
        return float(raw_derivative(float(value)))

    return evaluate, evaluate_derivative