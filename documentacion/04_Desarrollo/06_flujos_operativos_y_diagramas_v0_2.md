# Flujos Operativos y Diagramas v0.2

## Objetivo de este documento

Traducir el estado actual del sistema a diagramas operativos simples para que cualquier desarrollador, evaluador o futuro modelo pueda entender rapidamente como fluye la aplicacion entre frontend, backend, autenticacion, persistencia y seguimiento academico.

## 1. Topologia web actual

```mermaid
flowchart LR
    A[Frontend estatico<br/>HTML CSS JS] -->|HTTP JSON| B[Backend FastAPI<br/>API numerica y academica]
    B --> C[Motor numerico Python<br/>metodos de raices]
    B --> D[Servicios de aplicacion<br/>auth y flujo academico]
    D --> E[(Base relacional<br/>SQLite o PostgreSQL)]
    C --> B
    B --> A
```

Lectura del diagrama:

- el frontend ya no calcula las raices localmente como camino principal;
- la API FastAPI centraliza autenticacion, asignaciones y resolucion numerica;
- el backend conserva separacion entre motor numerico y servicios academicos;
- la persistencia relacional soporta el seguimiento real de usuarios y actividades.

## 2. Flujo profesor-estudiante sobre una asignacion real

```mermaid
sequenceDiagram
    autonumber
    participant P as Profesor
    participant F as Frontend profesor
    participant API as Backend FastAPI
    participant DB as Base relacional
    participant E as Estudiante
    participant FE as Frontend estudiante

    P->>F: Inicia sesion
    F->>API: POST /api/auth/login
    API->>DB: Verifica usuario y roles
    DB-->>API: Usuario valido
    API-->>F: JWT + perfil

    P->>F: Crea seccion
    F->>API: POST /api/academic/sections
    API->>DB: Guarda seccion
    DB-->>API: section_id
    API-->>F: Seccion creada

    P->>F: Crea asignacion
    F->>API: POST /api/academic/assignments
    API->>DB: Guarda assignment
    DB-->>API: assignment_id
    API-->>F: Codigo CLS:<section_id>:<assignment_id>

    E->>FE: Inicia sesion
    FE->>API: POST /api/auth/login
    API->>DB: Verifica credenciales
    DB-->>API: Usuario valido
    API-->>FE: JWT + perfil

    E->>FE: Ingresa codigo de clase
    FE->>API: POST /api/academic/enrollments
    API->>DB: Registra matricula
    DB-->>API: Enrollment OK
    API-->>FE: Matricula confirmada

    FE->>API: GET /api/academic/assignments/{id}
    API->>DB: Consulta asignacion
    DB-->>API: Datos de assignment
    API-->>FE: Expresion + metodos permitidos
```

## 3. Flujo de una resolucion numerica con trazabilidad academica

```mermaid
sequenceDiagram
    autonumber
    participant FE as Frontend estudiante
    participant API as Backend FastAPI
    participant M as Metodo numerico
    participant S as Servicio academico
    participant DB as Base relacional

    FE->>API: POST /api/roots/solve + JWT + assignment_id
    API->>API: Autentica token
    API->>API: Construye ProblemDefinition
    API->>M: Ejecuta metodo seleccionado
    M-->>API: MethodResult
    API->>S: Registrar intento si hay assignment_id
    S->>DB: Crear o reutilizar submission
    S->>DB: Guardar attempt
    DB-->>S: Persistencia OK
    S-->>API: Registro OK
    API-->>FE: Resultados serializados para UI
```

Puntos importantes:

- la resolucion numerica sigue desacoplada del seguimiento academico;
- el registro de intentos es opcional y depende del contexto de asignacion;
- el frontend recibe una forma de datos compatible con sus tablas y graficas.

## 4. Topologia de despliegue recomendada para la fase actual

```mermaid
flowchart TB
    U[Usuario final] --> W[Frontend estatico publicado]
    W -->|fetch /api| X[Backend desplegado en FastAPI Cloud]
    X --> Y[(PostgreSQL recomendado en produccion)]
    X --> Z[Variables de entorno y JWT secret]
```

Interpretacion:

- el frontend y el backend pueden vivir en servicios distintos;
- si se publican en dominios separados, el backend debe permitir CORS para el dominio del frontend;
- en produccion conviene usar PostgreSQL y no SQLite.

## 5. Decision operativa actual

La forma mas coherente de publicar el proyecto hoy es:

1. desplegar el backend Python como aplicacion FastAPI;
2. publicar el frontend estatico en un hosting de archivos web;
3. conectar ambos mediante una URL base de API y CORS configurado por entorno.

Eso respeta la arquitectura ya implementada y evita rehacer el frontend para insertarlo artificialmente dentro del backend en esta etapa.