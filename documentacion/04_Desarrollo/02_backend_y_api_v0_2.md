# Backend y API v0.2

## Objetivo de este documento

Explicar como esta construido actualmente el backend, que responsabilidades tiene cada capa y que interfaces web expone al dia de hoy.

## Estructura general del backend

El backend sigue una organizacion por capas dentro de `backend/src/`:

- `core/`: contratos del dominio, parser de expresiones y resultados.
- `methods/`: implementaciones de metodos numericos.
- `analysis/`: comparacion de metodos.
- `app/`: casos de uso y servicios de aplicacion.
- `infrastructure/`: persistencia, almacenamiento y detalles tecnicos.
- `interfaces/`: CLI y adaptadores web.
- `tutoring/`: espacio reservado para capacidades didacticas futuras.

## Motor numerico actual

El backend ya soporta al menos estos metodos de raices dentro de la arquitectura v0.2:

- biseccion;
- Newton-Raphson;
- secante;
- punto fijo.

Cada metodo opera sobre contratos comunes, lo que permite:

- comparar resultados;
- unificar iteraciones y estados;
- reutilizar la misma logica desde CLI, API y pruebas.

## Casos de uso principales

Los casos de uso activos mas importantes son:

- `SolveProblemUseCase`: ejecuta un metodo numerico sobre un problema;
- `CompareMethodsUseCase`: compara metodos sobre un mismo problema.

La evolucion reciente consistio en permitir que estos casos de uso trabajen no solo con persistencia JSON, sino tambien con recorders relacionales opcionales, lo que habilita registrar intentos academicos sin contaminar el dominio numerico.

## Adaptadores web disponibles

Actualmente existen dos adaptadores web:

### 1. Adaptador `stdlib`

Basado en `http.server`. Se mantiene por compatibilidad y como superficie simple de pruebas.

### 2. Adaptador `FastAPI`

Es el adaptador recomendado para seguir evolucionando la aplicacion web. Se activa por defecto desde `run_web.py`, salvo que se defina `WEB_ADAPTER=stdlib`.

## Endpoints numericos activos

### Salud y disponibilidad

- `GET /api/health`

### Resolucion y comparacion

- `POST /api/roots/solve`
- `POST /api/roots/compare`

## Endpoints academicos activos

### Autenticacion

- `POST /api/auth/register`
- `POST /api/auth/login`

### Gestion academica basica

- `POST /api/academic/sections`
- `POST /api/academic/enrollments`
- `POST /api/academic/assignments`

### Consulta de asignaciones

- `GET /api/academic/my-assignments`
- `GET /api/academic/assignments/{assignment_id}`

## Flujo actual de una resolucion academica

El flujo academico de resolucion ya no es solo numerico. Ahora opera asi:

1. el estudiante autentica su sesion;
2. el frontend envia el token JWT al backend;
3. el payload de resolucion puede incluir `assignment_id`;
4. el backend ejecuta el metodo numerico sobre el problema;
5. si existe contexto academico valido, se crea o reutiliza una `submission`;
6. se registra un `attempt` con entradas, resultado, tiempo y estado.

## Variables de entorno relevantes

- `APP_ENV`
- `DATABASE_URL`
- `DATABASE_ECHO`
- `AUTO_CREATE_SCHEMA`
- `AUTH_TOKEN_SECRET`
- `APP_HOST`
- `APP_PORT`
- `WEB_ADAPTER`

## Convivencia de componentes

Una caracteristica importante del estado actual es que el backend conserva compatibilidad con su historia tecnica:

- sigue existiendo la CLI;
- sigue existiendo el repositorio JSON de sesiones;
- se agrego persistencia relacional sin romper el motor numerico;
- se agrego FastAPI sin eliminar el adaptador web anterior.

Esto reduce riesgo de migracion y deja al proyecto en una posicion favorable para iterar sin reescrituras masivas.