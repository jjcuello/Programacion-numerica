# Plan de Validacion Supabase MVP (2026-06-28)

## Objetivo

Validar que el backend conectado a Supabase soporta el flujo academico base (profesor -> asignacion -> estudiante -> intento) sin errores de persistencia.

## Precondiciones

- Migraciones aplicadas con Alembic en Supabase.
- Seed minimo aplicado.
- Backend levantado con DATABASE_URL de Supabase.
- CORS configurado para el frontend de pruebas.

## Pruebas minimas obligatorias

### P1. Health del backend

- Request: GET /api/health
- Esperado: HTTP 200 y status=ok.

### P2. Registro de profesor

- Request: POST /api/auth/register
- Body sugerido:

```json
{
  "full_name": "Profesor Demo",
  "email": "profesor.demo@iupsm.local",
  "password": "DemoPass123!",
  "roles": ["teacher"]
}
```

- Esperado: HTTP 201 y token valido.

### P3. Registro de estudiante

- Request: POST /api/auth/register
- Body sugerido:

```json
{
  "full_name": "Estudiante Demo",
  "email": "estudiante.demo@iupsm.local",
  "password": "DemoPass123!",
  "roles": ["student"]
}
```

- Esperado: HTTP 201 y token valido.

### P4. Crear seccion con token teacher

- Request: POST /api/academic/sections
- Header: Authorization: Bearer <teacher_token>
- Body sugerido:

```json
{
  "course_code": "PN-101",
  "course_name": "Programacion Numerica",
  "term_name": "2026-2",
  "term_starts_on": "2026-07-01",
  "term_ends_on": "2026-12-01",
  "section_name": "Seccion A"
}
```

- Esperado: HTTP 201 y section.id.

### P5. Crear asignacion con token teacher

- Request: POST /api/academic/assignments
- Header: Authorization: Bearer <teacher_token>
- Body sugerido:

```json
{
  "section_id": "<section_id>",
  "title": "Raiz por biseccion",
  "instructions": "Resolver x^3-x-2 en [1,2]",
  "expression": "x**3 - x - 2",
  "allowed_methods": ["bisection", "newton"],
  "topic_name": "Raices",
  "unit_title": "Metodos de raices"
}
```

- Esperado: HTTP 201 y assignment.id.

### P6. Matricular estudiante

- Request: POST /api/academic/enrollments
- Header: Authorization: Bearer <teacher_token>
- Body sugerido:

```json
{
  "section_id": "<section_id>",
  "student_user_id": "<student_user_id>"
}
```

- Esperado: HTTP 201.

### P7. Resolver ejercicio con assignment_id

- Request: POST /api/roots/solve
- Header: Authorization: Bearer <student_token>
- Body sugerido:

```json
{
  "method": "bisection",
  "expression": "x**3 - x - 2",
  "a": 1,
  "b": 2,
  "tol": 0.0001,
  "max_iter": 100,
  "assignment_id": "<assignment_id>"
}
```

- Esperado: HTTP 200 y resultado numerico.
- Esperado en BD: se crea/actualiza submissions y se inserta fila en attempts.

## Verificacion SQL posterior

Ejecutar backend/scripts/sql/supabase_smoke_checks.sql y confirmar:

- users_count >= 2
- sections_count >= 1
- assignments_count >= 1
- attempts_count >= 1

## Criterio de salida

La validacion se considera aprobada si P1..P7 pasan y la verificacion SQL refleja datos persistidos coherentes.
