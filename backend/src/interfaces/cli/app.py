from __future__ import annotations

import argparse
from pathlib import Path

from src.analysis.benchmarking.comparator import MethodComparator
from src.app.use_cases.solve_problem import CompareMethodsUseCase, SolveProblemUseCase
from src.core.models.problem import ProblemDefinition, ProblemKind
from src.infrastructure.storage.session_repository import JsonSessionRepository
from src.methods.roots.bisection_method import BisectionMethod
from src.methods.roots.newton_method import NewtonMethod


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="CLI experimental para la arquitectura v0.2")
    subparsers = parser.add_subparsers(dest="command", required=True)

    solve_parser = subparsers.add_parser("solve", help="Resolver un problema con un metodo")
    solve_parser.add_argument("--method", choices=["bisection", "newton"], required=True)
    solve_parser.add_argument("--expression", required=True)
    solve_parser.add_argument("--name", default="problema_cli")
    solve_parser.add_argument("--tolerance", type=float, default=1e-6)
    solve_parser.add_argument("--max-iterations", type=int, default=100)
    solve_parser.add_argument("--interval", nargs=2, type=float)
    solve_parser.add_argument("--x0", type=float)
    solve_parser.add_argument("--save-session", action="store_true")
    solve_parser.add_argument("--session-dir", default="sessions")

    compare_parser = subparsers.add_parser("compare", help="Comparar metodos sobre un mismo problema")
    compare_parser.add_argument("--expression", required=True)
    compare_parser.add_argument("--name", default="comparacion_cli")
    compare_parser.add_argument("--tolerance", type=float, default=1e-6)
    compare_parser.add_argument("--max-iterations", type=int, default=100)
    compare_parser.add_argument("--interval", nargs=2, type=float)
    compare_parser.add_argument("--x0", type=float)
    compare_parser.add_argument("--save-session", action="store_true")
    compare_parser.add_argument("--session-dir", default="sessions")

    sessions_parser = subparsers.add_parser("sessions", help="Listar sesiones guardadas")
    sessions_parser.add_argument("--session-dir", default="sessions")

    return parser


def run(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "sessions":
        repository = JsonSessionRepository(Path(args.session_dir))
        for session_file in repository.list_sessions():
            print(session_file)
        return 0

    repository = JsonSessionRepository(Path(args.session_dir)) if args.save_session else None

    if args.command == "solve":
        method = _build_method(args.method)
        problem = _build_problem_from_args(args)
        result = SolveProblemUseCase(session_repository=repository).execute(method, problem)
        _print_method_result(result)
        return 0 if result.converged else 1

    if args.command == "compare":
        problem = _build_problem_from_args(args)
        methods = [BisectionMethod(), NewtonMethod()]
        summary = CompareMethodsUseCase(
            comparator=MethodComparator(methods),
            session_repository=repository,
        ).execute(problem)
        _print_comparison(summary)
        return 0

    parser.error("Comando no soportado.")
    return 2


def _build_method(method_name: str):
    if method_name == "bisection":
        return BisectionMethod()
    if method_name == "newton":
        return NewtonMethod()
    raise ValueError(f"Metodo no soportado: {method_name}")


def _build_problem_from_args(args: argparse.Namespace) -> ProblemDefinition:
    interval = tuple(args.interval) if args.interval else None
    initial_guess = (args.x0,) if args.x0 is not None else ()
    return ProblemDefinition(
        name=args.name,
        kind=ProblemKind.SCALAR_ROOT,
        expression=args.expression,
        interval=interval,
        initial_guess=initial_guess,
        tolerance=args.tolerance,
        max_iterations=args.max_iterations,
        metadata={"source": "cli_v0_2"},
    )


def _print_method_result(result) -> None:
    print(f"Metodo: {result.method_name}")
    print(f"Estado: {result.status.value}")
    print(f"Solucion: {result.solution}")
    print(f"Residual: {result.residual}")
    print(f"Iteraciones: {result.iteration_count}")
    print(f"Tiempo: {result.elapsed_seconds:.6f} s")
    print(f"Mensaje: {result.message}")


def _print_comparison(summary) -> None:
    print(f"Problema: {summary.problem_name}")
    for result in summary.results:
        print("-" * 40)
        _print_method_result(result)

    best = summary.best_result()
    if best is not None:
        print("=" * 40)
        print(f"Mejor resultado: {best.method_name}")


if __name__ == "__main__":
    raise SystemExit(run())