from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import date, datetime
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any
from urllib.parse import urlparse

from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from src.analysis.benchmarking.comparator import MethodComparator
from src.app.services import AcademicWorkflowService, AuthService, CompositeRunRecorder, RelationalRunRecorder
from src.app.use_cases.solve_problem import CompareMethodsUseCase, SolveProblemUseCase
from src.core.models.problem import ProblemDefinition, ProblemKind
from src.core.results.iteration import IterationRecord
from src.core.results.method_result import ExecutionStatus, MethodResult
from src.infrastructure.storage import DatabaseSettings, create_engine_from_settings, create_session_factory, initialize_database
from src.methods.roots.bisection_method import BisectionMethod
from src.methods.roots.fixed_point_method import FixedPointMethod
from src.methods.roots.newton_method import NewtonMethod
from src.methods.roots.secant_method import SecantMethod


METHODS = {
    "bisection": BisectionMethod,
    "newton": NewtonMethod,
    "secant": SecantMethod,
    "fixedpoint": FixedPointMethod,
}


@dataclass(slots=True)
class ApiServices:
    auth_service: AuthService
    academic_service: AcademicWorkflowService
    storage_backend: str


class ApiServer(ThreadingHTTPServer):
    def __init__(self, server_address: tuple[str, int], services: ApiServices, engine: Any):
        super().__init__(server_address, NumericalApiHandler)
        self.api_services = services
        self.database_engine = engine

    def server_close(self) -> None:
        try:
            if getattr(self, "database_engine", None) is not None:
                self.database_engine.dispose()
        finally:
            super().server_close()


def create_server(host: str = "127.0.0.1", port: int = 8000) -> ThreadingHTTPServer:
    services, engine = _build_api_services()
    return ApiServer((host, port), services, engine)


def run(host: str = "127.0.0.1", port: int = 8000) -> None:
    server = create_server(host=host, port=port)
    print(f"Servidor HTTP escuchando en http://{host}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


class NumericalApiHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self) -> None:
        self.send_response(HTTPStatus.NO_CONTENT)
        self._send_cors_headers()
        self.end_headers()

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/api/health":
            self._send_json(HTTPStatus.OK, {"status": "ok", "storage_backend": self.server.api_services.storage_backend})
            return

        if parsed.path == "/api/academic/my-assignments":
            self._handle_my_assignments()
            return

        assignment_prefix = "/api/academic/assignments/"
        if parsed.path.startswith(assignment_prefix):
            assignment_id = parsed.path[len(assignment_prefix):].strip()
            self._handle_assignment_detail(assignment_id)
            return

        self._send_json(HTTPStatus.NOT_FOUND, {"error": "Ruta no encontrada."})

    def do_POST(self) -> None:
        try:
            payload = self._read_json_body()
        except ValueError as error:
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": str(error)})
            return

        if self.path == "/api/roots/solve":
            self._handle_solve(payload)
            return

        if self.path == "/api/roots/compare":
            self._handle_compare(payload)
            return

        if self.path == "/api/auth/register":
            self._handle_register(payload)
            return

        if self.path == "/api/auth/login":
            self._handle_login(payload)
            return

        if self.path == "/api/academic/sections":
            self._handle_create_section(payload)
            return

        if self.path == "/api/academic/enrollments":
            self._handle_enrollment(payload)
            return

        if self.path == "/api/academic/assignments":
            self._handle_create_assignment(payload)
            return

        self._send_json(HTTPStatus.NOT_FOUND, {"error": "Ruta no encontrada."})

    def log_message(self, format: str, *args: Any) -> None:
        return

    def _handle_solve(self, payload: dict[str, Any]) -> None:
        try:
            method_name = str(payload["method"])
            method = _build_method(method_name)
            actor = self._get_authenticated_user(required=False)
            problem = _build_problem_from_payload(payload, method_name, actor_user_id=actor.user_id if actor else None)
            session_repository = self._build_run_recorder(payload, actor)
        except (KeyError, TypeError, ValueError, PermissionError) as error:
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": str(error)})
            return

        try:
            result = SolveProblemUseCase(session_repository=session_repository).execute(method, problem)
        except ValueError as error:
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": str(error)})
            return

        response_payload = {"result": serialize_frontend_result(method_name, result)}
        self._send_json(HTTPStatus.OK, response_payload)

    def _handle_compare(self, payload: dict[str, Any]) -> None:
        methods_payload = payload.get("methods")
        if not isinstance(methods_payload, list) or not methods_payload:
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": "Debes indicar una lista no vacia de metodos."})
            return

        try:
            actor = self._get_authenticated_user(required=False)
            results = {}
            for raw_method_name in methods_payload:
                method_name = str(raw_method_name)
                method = _build_method(method_name)
                problem = _build_problem_from_payload(payload, method_name, actor_user_id=actor.user_id if actor else None)
                result = CompareMethodsUseCase(comparator=MethodComparator([method])).execute(problem).results[0]
                results[method_name] = serialize_frontend_result(method_name, result)
        except (TypeError, ValueError) as error:
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": str(error)})
            return

        self._send_json(HTTPStatus.OK, {"results": results})

    def _handle_register(self, payload: dict[str, Any]) -> None:
        try:
            full_name = str(payload["full_name"])
            email = str(payload["email"])
            password = str(payload["password"])
            roles = tuple(payload.get("roles") or ["student"])
            institutional_code = payload.get("institutional_code")
            response = self.server.api_services.auth_service.register_user(
                email=email,
                password=password,
                full_name=full_name,
                role_names=tuple(str(role) for role in roles),
                institutional_code=str(institutional_code) if institutional_code is not None else None,
            )
        except (KeyError, ValueError) as error:
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": str(error)})
            return

        self._send_json(HTTPStatus.CREATED, response)

    def _handle_login(self, payload: dict[str, Any]) -> None:
        try:
            response = self.server.api_services.auth_service.login(
                email=str(payload["email"]),
                password=str(payload["password"]),
            )
        except (KeyError, ValueError) as error:
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": str(error)})
            return

        self._send_json(HTTPStatus.OK, response)

    def _handle_create_section(self, payload: dict[str, Any]) -> None:
        try:
            actor = self._get_authenticated_user(required=True)
            response = self.server.api_services.academic_service.create_section(
                actor=actor,
                course_code=str(payload["course_code"]),
                course_name=str(payload["course_name"]),
                term_name=str(payload["term_name"]),
                term_starts_on=_parse_date(str(payload["term_starts_on"])),
                term_ends_on=_parse_date(str(payload["term_ends_on"])),
                section_name=str(payload["section_name"]),
            )
        except (KeyError, ValueError, PermissionError) as error:
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": str(error)})
            return

        self._send_json(HTTPStatus.CREATED, response)

    def _handle_enrollment(self, payload: dict[str, Any]) -> None:
        try:
            actor = self._get_authenticated_user(required=True)
            student_user_id = payload.get("student_user_id")
            response = self.server.api_services.academic_service.enroll_student(
                actor=actor,
                section_id=str(payload["section_id"]),
                student_user_id=str(student_user_id) if student_user_id is not None else None,
            )
        except (KeyError, ValueError, PermissionError) as error:
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": str(error)})
            return

        self._send_json(HTTPStatus.CREATED, response)

    def _handle_create_assignment(self, payload: dict[str, Any]) -> None:
        try:
            actor = self._get_authenticated_user(required=True)
            response = self.server.api_services.academic_service.create_assignment(
                actor=actor,
                section_id=str(payload["section_id"]),
                title=str(payload["title"]),
                instructions=str(payload.get("instructions") or ""),
                expression=str(payload["expression"]),
                allowed_methods=tuple(str(method) for method in payload.get("allowed_methods") or ["bisection", "newton"]),
                topic_name=str(payload.get("topic_name") or "Raices"),
                unit_title=str(payload.get("unit_title") or "Metodos de raices"),
                opens_at=_parse_datetime(payload.get("opens_at")),
                due_at=_parse_datetime(payload.get("due_at")),
            )
        except (KeyError, ValueError, PermissionError) as error:
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": str(error)})
            return

        self._send_json(HTTPStatus.CREATED, response)

    def _handle_assignment_detail(self, assignment_id: str) -> None:
        try:
            actor = self._get_authenticated_user(required=True)
            response = self.server.api_services.academic_service.get_assignment_detail(
                actor=actor,
                assignment_id=assignment_id,
            )
        except (ValueError, PermissionError) as error:
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": str(error)})
            return

        self._send_json(HTTPStatus.OK, response)

    def _handle_my_assignments(self) -> None:
        try:
            actor = self._get_authenticated_user(required=True)
            response = self.server.api_services.academic_service.list_assignments_for_student(actor=actor)
        except (ValueError, PermissionError) as error:
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": str(error)})
            return

        self._send_json(HTTPStatus.OK, response)

    def _read_json_body(self) -> dict[str, Any]:
        content_length = int(self.headers.get("Content-Length", "0"))
        raw_body = self.rfile.read(content_length) if content_length > 0 else b"{}"
        try:
            payload = json.loads(raw_body.decode("utf-8"))
        except json.JSONDecodeError as error:
            raise ValueError(f"JSON invalido: {error.msg}") from error

        if not isinstance(payload, dict):
            raise ValueError("El cuerpo debe ser un objeto JSON.")

        return payload

    def _send_json(self, status: HTTPStatus, payload: dict[str, Any]) -> None:
        body = json.dumps(payload, ensure_ascii=True).encode("utf-8")
        self.send_response(status)
        self._send_cors_headers()
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_cors_headers(self) -> None:
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")

    def _get_authenticated_user(self, *, required: bool) -> Any:
        authorization = self.headers.get("Authorization", "")
        if not authorization:
            if required:
                raise PermissionError("Se requiere autenticacion.")
            return None

        prefix = "Bearer "
        if not authorization.startswith(prefix):
            raise PermissionError("Cabecera Authorization invalida.")
        token = authorization[len(prefix):].strip()
        if not token:
            raise PermissionError("Token vacio.")
        return self.server.api_services.auth_service.authenticate(token)

    def _build_run_recorder(self, payload: dict[str, Any], actor: Any) -> CompositeRunRecorder | None:
        recorders = []
        assignment_id = payload.get("assignment_id")
        if assignment_id is not None:
            if actor is None:
                raise PermissionError("Se requiere autenticacion para registrar intentos academicos.")
            recorders.append(RelationalRunRecorder(self.server.api_services.academic_service, actor=actor))
        return CompositeRunRecorder(recorders) if recorders else None


def _build_api_services() -> tuple[ApiServices, Any]:
    settings = DatabaseSettings.from_env()
    engine = create_engine_from_settings(settings)
    if settings.auto_create_schema:
        initialize_database(engine)
    session_factory = create_session_factory(engine)
    if settings.url.startswith("sqlite+"):
        storage_backend = "sqlite"
    elif settings.url.startswith("postgresql+"):
        storage_backend = "postgresql"
    else:
        storage_backend = "custom"
    return (
        ApiServices(
            auth_service=AuthService(session_factory),
            academic_service=AcademicWorkflowService(session_factory),
            storage_backend=storage_backend,
        ),
        engine,
    )


def create_fastapi_app() -> FastAPI:
    services, _engine = _build_api_services()
    app = FastAPI(title="Metodos Numericos API", version="0.2")
    app.state.api_services = services
    cors_origins = _parse_cors_origins(os.getenv("CORS_ALLOW_ORIGINS", "*"))
    allow_credentials = os.getenv("CORS_ALLOW_CREDENTIALS", "false").strip().lower() == "true"

    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=allow_credentials,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    def _actor_from_header(authorization: str | None, required: bool = False):
        if not authorization:
            if required:
                raise HTTPException(status_code=401, detail="Se requiere autenticacion.")
            return None
        prefix = "Bearer "
        if not authorization.startswith(prefix):
            raise HTTPException(status_code=401, detail="Cabecera Authorization invalida.")
        token = authorization[len(prefix):].strip()
        try:
            return app.state.api_services.auth_service.authenticate(token)
        except ValueError as error:
            raise HTTPException(status_code=401, detail=str(error)) from error

    @app.get("/api/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "storage_backend": services.storage_backend}

    @app.post("/api/roots/solve")
    def solve(payload: dict[str, Any], authorization: str | None = Header(default=None)) -> JSONResponse:
        try:
            method_name = str(payload["method"])
            method = _build_method(method_name)
            actor = _actor_from_header(authorization, required=False)
            problem = _build_problem_from_payload(payload, method_name, actor_user_id=actor.user_id if actor else None)
            recorder = None
            if payload.get("assignment_id") is not None:
                if actor is None:
                    raise PermissionError("Se requiere autenticacion para registrar intentos academicos.")
                recorder = CompositeRunRecorder([RelationalRunRecorder(services.academic_service, actor)])
            result = SolveProblemUseCase(session_repository=recorder).execute(method, problem)
            return JSONResponse({"result": serialize_frontend_result(method_name, result)})
        except (KeyError, TypeError, ValueError, PermissionError) as error:
            raise HTTPException(status_code=400, detail=str(error)) from error

    @app.post("/api/roots/compare")
    def compare(payload: dict[str, Any], authorization: str | None = Header(default=None)) -> JSONResponse:
        methods_payload = payload.get("methods")
        if not isinstance(methods_payload, list) or not methods_payload:
            raise HTTPException(status_code=400, detail="Debes indicar una lista no vacia de metodos.")
        try:
            actor = _actor_from_header(authorization, required=False)
            results = {}
            for raw_method_name in methods_payload:
                method_name = str(raw_method_name)
                method = _build_method(method_name)
                problem = _build_problem_from_payload(payload, method_name, actor_user_id=actor.user_id if actor else None)
                result = CompareMethodsUseCase(comparator=MethodComparator([method])).execute(problem).results[0]
                results[method_name] = serialize_frontend_result(method_name, result)
            return JSONResponse({"results": results})
        except (TypeError, ValueError) as error:
            raise HTTPException(status_code=400, detail=str(error)) from error

    @app.post("/api/auth/register", status_code=201)
    def register(payload: dict[str, Any]) -> dict[str, object]:
        try:
            return services.auth_service.register_user(
                email=str(payload["email"]),
                password=str(payload["password"]),
                full_name=str(payload["full_name"]),
                role_names=tuple(str(role) for role in (payload.get("roles") or ["student"])),
                institutional_code=str(payload.get("institutional_code")) if payload.get("institutional_code") is not None else None,
            )
        except (KeyError, ValueError) as error:
            raise HTTPException(status_code=400, detail=str(error)) from error

    @app.post("/api/auth/login")
    def login(payload: dict[str, Any]) -> dict[str, object]:
        try:
            return services.auth_service.login(email=str(payload["email"]), password=str(payload["password"]))
        except (KeyError, ValueError) as error:
            raise HTTPException(status_code=400, detail=str(error)) from error

    @app.post("/api/academic/sections", status_code=201)
    def create_section(payload: dict[str, Any], authorization: str | None = Header(default=None)) -> dict[str, object]:
        actor = _actor_from_header(authorization, required=True)
        try:
            return services.academic_service.create_section(
                actor=actor,
                course_code=str(payload["course_code"]),
                course_name=str(payload["course_name"]),
                term_name=str(payload["term_name"]),
                term_starts_on=_parse_date(str(payload["term_starts_on"])),
                term_ends_on=_parse_date(str(payload["term_ends_on"])),
                section_name=str(payload["section_name"]),
            )
        except (KeyError, ValueError, PermissionError) as error:
            raise HTTPException(status_code=400, detail=str(error)) from error

    @app.post("/api/academic/enrollments", status_code=201)
    def enroll(payload: dict[str, Any], authorization: str | None = Header(default=None)) -> dict[str, object]:
        actor = _actor_from_header(authorization, required=True)
        try:
            student_user_id = payload.get("student_user_id")
            return services.academic_service.enroll_student(
                actor=actor,
                section_id=str(payload["section_id"]),
                student_user_id=str(student_user_id) if student_user_id is not None else None,
            )
        except (KeyError, ValueError, PermissionError) as error:
            raise HTTPException(status_code=400, detail=str(error)) from error

    @app.post("/api/academic/assignments", status_code=201)
    def create_assignment(payload: dict[str, Any], authorization: str | None = Header(default=None)) -> dict[str, object]:
        actor = _actor_from_header(authorization, required=True)
        try:
            return services.academic_service.create_assignment(
                actor=actor,
                section_id=str(payload["section_id"]),
                title=str(payload["title"]),
                instructions=str(payload.get("instructions") or ""),
                expression=str(payload["expression"]),
                allowed_methods=tuple(str(method) for method in payload.get("allowed_methods") or ["bisection", "newton"]),
                topic_name=str(payload.get("topic_name") or "Raices"),
                unit_title=str(payload.get("unit_title") or "Metodos de raices"),
                opens_at=_parse_datetime(payload.get("opens_at")),
                due_at=_parse_datetime(payload.get("due_at")),
            )
        except (KeyError, ValueError, PermissionError) as error:
            raise HTTPException(status_code=400, detail=str(error)) from error

    @app.get("/api/academic/my-assignments")
    def my_assignments(authorization: str | None = Header(default=None)) -> dict[str, object]:
        actor = _actor_from_header(authorization, required=True)
        try:
            return services.academic_service.list_assignments_for_student(actor=actor)
        except (ValueError, PermissionError) as error:
            raise HTTPException(status_code=400, detail=str(error)) from error

    @app.get("/api/academic/assignments/{assignment_id}")
    def assignment_detail(assignment_id: str, authorization: str | None = Header(default=None)) -> dict[str, object]:
        actor = _actor_from_header(authorization, required=True)
        try:
            return services.academic_service.get_assignment_detail(actor=actor, assignment_id=assignment_id)
        except (ValueError, PermissionError) as error:
            raise HTTPException(status_code=400, detail=str(error)) from error

    return app


def _build_method(method_name: str):
    normalized = method_name.strip().lower()
    method_class = METHODS.get(normalized)
    if method_class is None:
        raise ValueError(f"Metodo no soportado: {method_name}")
    return method_class()


def _parse_cors_origins(raw_origins: str) -> list[str]:
    origins = [origin.strip() for origin in raw_origins.split(",") if origin.strip()]
    return origins or ["*"]


def _build_problem_from_payload(payload: dict[str, Any], method_name: str, actor_user_id: str | None = None) -> ProblemDefinition:
    expression = payload.get("expression")
    if expression is not None and not isinstance(expression, str):
        raise ValueError("La expresion debe ser texto.")

    interval = None
    interval_payload = payload.get("interval")
    if interval_payload is not None:
        if not isinstance(interval_payload, (list, tuple)) or len(interval_payload) != 2:
            raise ValueError("El intervalo debe contener dos valores.")
        interval = (float(interval_payload[0]), float(interval_payload[1]))

    metadata = {"source": "web_api"}
    if actor_user_id is not None:
        metadata["actor_user_id"] = actor_user_id
    assignment_id = payload.get("assignment_id")
    if assignment_id is not None:
        metadata["assignment_id"] = str(assignment_id)
    if method_name == "fixedpoint":
        g_expression = payload.get("g_expression")
        if not isinstance(g_expression, str) or not g_expression.strip():
            raise ValueError("Punto fijo requiere g_expression.")
        metadata["g_expression"] = g_expression.strip()

    initial_guess = _resolve_initial_guess(payload, method_name, interval)

    return ProblemDefinition(
        name=str(payload.get("name") or "problema_web"),
        kind=ProblemKind.SCALAR_ROOT,
        expression=expression,
        interval=interval,
        initial_guess=initial_guess,
        tolerance=float(payload.get("tolerance", 1e-6)),
        max_iterations=int(payload.get("max_iterations", 100)),
        metadata=metadata,
    )


def _resolve_initial_guess(
    payload: dict[str, Any],
    method_name: str,
    interval: tuple[float, float] | None,
) -> tuple[float, ...]:
    if method_name == "newton":
        x0 = payload.get("x0")
        if x0 is None:
            raise ValueError("Newton requiere x0.")
        return (float(x0),)

    if method_name == "secant":
        x0 = payload.get("x0")
        x1 = payload.get("x1")
        if x0 is not None and x1 is not None:
            return (float(x0), float(x1))
        if interval is not None:
            return interval
        raise ValueError("Secante requiere x0 y x1, o bien un intervalo [x0, x1].")

    if method_name == "fixedpoint":
        x0 = payload.get("x0")
        if x0 is None:
            raise ValueError("Punto fijo requiere x0.")
        return (float(x0),)

    return ()


def serialize_frontend_result(method_name: str, result: MethodResult) -> dict[str, Any]:
    return {
        "root": result.solution if isinstance(result.solution, float) else None,
        "iterations": [serialize_frontend_iteration(method_name, record) for record in result.records],
        "status": map_status(method_name, result),
        "time": f"{result.elapsed_seconds:.6f}",
        "message": result.message,
    }


def serialize_frontend_iteration(method_name: str, record: IterationRecord) -> dict[str, Any]:
    if method_name == "bisection":
        return {
            "iter": record.iteration,
            "xi": record.metadata.get("a"),
            "sup": record.metadata.get("b"),
            "root": record.estimate,
            "error": "-" if record.iteration == 1 or record.delta is None else f"{record.delta:.8f}",
            "residual": record.residual,
        }

    if method_name == "secant":
        return {
            "iter": record.iteration,
            "xi": record.metadata.get("x(i-1)"),
            "sup": record.metadata.get("x(i)"),
            "root": record.estimate,
            "error": "-" if record.iteration == 1 or record.delta is None else f"{record.delta:.8f}",
            "residual": record.residual,
        }

    return {
        "iter": record.iteration,
        "xi": record.metadata.get("x(i)"),
        "sup": record.estimate,
        "root": record.estimate,
        "error": "-" if record.iteration == 1 or record.relative_error is None else f"{record.relative_error:.8f}",
        "residual": record.residual,
    }


def map_status(method_name: str, result: MethodResult) -> str:
    ui_status = result.metadata.get("ui_status")
    if isinstance(ui_status, str):
        return ui_status

    if result.status == ExecutionStatus.SUCCESS:
        return "success"
    if result.status == ExecutionStatus.DID_NOT_CONVERGE:
        return "max_iter"
    if result.status == ExecutionStatus.UNSUPPORTED:
        return "error"

    message = result.message.lower()
    if method_name == "bisection" and "cambio de signo" in message:
        return "bolzano_violation"
    if "derivada" in message or "denominador" in message or "no finito" in message:
        return "singularidad"
    return "error"


def _parse_date(value: str) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError as error:
        raise ValueError("La fecha debe usar formato ISO YYYY-MM-DD.") from error


def _parse_datetime(value: Any) -> datetime | None:
    if value in (None, ""):
        return None
    if not isinstance(value, str):
        raise ValueError("La fecha y hora debe ser texto ISO 8601.")
    normalized = value.replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(normalized)
    except ValueError as error:
        raise ValueError("La fecha y hora debe usar formato ISO 8601.") from error