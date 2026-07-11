# Runbook de Implementacion en Supabase (MVP Backend v0.2)

## 1. Objetivo

Dejar la base de datos de Supabase lista para el flujo web profesor-estudiante del proyecto, usando el esquema relacional MVP ya definido en backend y documentando un proceso repetible para Leonardo y su agente.

## 2. Alcance de esta entrega

- Provision de la base PostgreSQL administrada en Supabase.
- Aplicacion del esquema con migraciones Alembic del backend.
- Seed minimo para catalogos base (roles, tema/unidad inicial).
- Verificacion tecnica por SQL y por API.
- Checklist de handoff para continuar desarrollo frontend y mejoras web.

No incluye en esta fase:

- politicas RLS por tabla;
- integracion con auth.users de Supabase;
- datos academicos reales en produccion.

## 3. Fuente de verdad del esquema

- Migracion inicial: backend/alembic/versions/20260619_0001_initial_relational_schema.py
- DDL de referencia humana: documentacion/03_Diseño/esquema_postgresql_mvp_v0_2.sql

Regla operativa: en ambientes reales usar siempre Alembic para crear/actualizar estructura.

## 4. Variables de entorno requeridas

Copiar base desde backend/.env.example y completar al menos:

- APP_ENV=production
- WEB_ADAPTER=fastapi
- AUTH_TOKEN_SECRET=<secreto-largo>
- DATABASE_URL=<url-postgresql-supabase-con-sslmode>
- AUTO_CREATE_SCHEMA=false
- DATABASE_ECHO=false
- CORS_ALLOW_ORIGINS=<dominio-frontend>

Formato recomendado para DATABASE_URL con SQLAlchemy + psycopg:

postgresql+psycopg://<usuario>:<password>@<host>:5432/postgres?sslmode=require

## 5. Paso a paso de ejecucion

### Paso 1: crear proyecto en Supabase

1. Crear proyecto en Supabase.
2. Esperar disponibilidad de la instancia PostgreSQL.
3. Copiar credenciales de conexion de Database settings.

### Paso 2: preparar backend local

1. Entrar a backend.
2. Instalar dependencias.
3. Definir variables de entorno (o archivo .env local no versionado).

Comandos sugeridos:

```bash
cd backend
pip install -r requirements.txt
```

### Paso 3: aplicar migraciones

```bash
cd backend
alembic upgrade head
```

Resultado esperado: esquema MVP creado en public con 16 tablas principales.

### Paso 4: aplicar seed minimo

Ejecutar en SQL Editor de Supabase:

- backend/scripts/sql/supabase_seed_mvp.sql

Resultado esperado:

- roles: student, teacher, admin
- topic: Raices
- learning unit: Metodos de raices

### Paso 5: validacion SQL

Ejecutar en SQL Editor de Supabase:

- backend/scripts/sql/supabase_smoke_checks.sql

Resultado esperado:

- aparecen todas las tablas del MVP;
- roles cargados;
- tema/unidad base cargados.

### Paso 6: validacion por API

1. Levantar backend apuntando a Supabase.
2. Validar endpoints minimos:

- GET /api/health
- POST /api/auth/register
- POST /api/auth/login
- POST /api/academic/sections (token teacher)
- POST /api/academic/assignments (token teacher)
- POST /api/academic/enrollments (token student o teacher)
- POST /api/roots/solve con assignment_id (token student)

Resultado esperado: creacion de submission y attempts en la base Supabase.

## 6. Hoja de ruta operativa (hoy -> siguiente iteracion)

### Fase A (hoy) - habilitacion de datos para web

- confirmar DATABASE_URL de Supabase en entorno de backend;
- correr alembic upgrade head;
- ejecutar seed minimo;
- correr smoke checks SQL;
- registrar evidencia (capturas o logs).

### Fase B (siguiente iteracion) - endurecimiento

- definir politicas RLS por rol y uso de service role en backend;
- separar esquema de app (por ejemplo app_public) si se requiere;
- agregar migracion para auditoria basica (tabla de eventos).

### Fase C (iteracion web de Leonardo)

- consumir endpoints academicos sobre base Supabase real;
- incorporar dashboards de profesor y alumno con datos persistidos;
- agregar seeds de datos demo para presentaciones docentes.

## 7. Checklist de cierre para handoff a Leonardo

- [ ] Supabase project creado y accesible.
- [ ] DATABASE_URL productiva definida con sslmode=require.
- [ ] Migraciones aplicadas (alembic head).
- [ ] Seed minimo aplicado.
- [ ] Smoke checks SQL sin errores.
- [ ] Flujo API register/login/section/assignment/solve validado.
- [ ] Evidencia documentada en bitacora de desarrollo.

Plan de validacion funcional de apoyo:

- documentacion/05_Pruebas/plan_validacion_supabase_mvp_2026-06-28.md

## 8. Riesgos y mitigaciones

- Riesgo: usar AUTO_CREATE_SCHEMA=true en produccion.
  Mitigacion: mantener false y usar solo Alembic.

- Riesgo: credenciales invalidas o host incorrecto en DATABASE_URL.
  Mitigacion: validar conexion con alembic current y health endpoint.

- Riesgo: frontend no conecta por CORS.
  Mitigacion: definir CORS_ALLOW_ORIGINS con dominio real publicado.

## 9. Nota para agentes futuros

Si se modifica el modelo ORM o se agregan tablas, primero crear nueva migracion Alembic y versionar el cambio; no editar manualmente tablas en Supabase sin migracion correspondiente.
