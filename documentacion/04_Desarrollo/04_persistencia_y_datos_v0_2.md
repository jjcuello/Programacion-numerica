# Persistencia y Datos v0.2

## Objetivo de este documento

Explicar como se maneja actualmente la persistencia del proyecto, por que conviven distintos mecanismos de almacenamiento y como se organiza el modelo de datos para la fase actual.

## Situacion previa

Antes de la incorporacion de la base relacional, el proyecto contaba con persistencia basada en archivos JSON para sesiones de ejecucion y trazas de laboratorio.

Ese mecanismo sigue siendo util para:

- ejecucion local de la CLI;
- guardado simple de experimentos;
- exportes ligeros sin dependencias de base de datos.

## Persistencia actual: dos capas coexistentes

### 1. Persistencia JSON

Responsabilidad:

- sesiones locales del laboratorio;
- compatibilidad con el flujo CLI ya existente.

### 2. Persistencia relacional MVP

Responsabilidad:

- usuarios;
- roles;
- secciones;
- matriculas;
- actividades y versiones;
- asignaciones;
- entregas;
- intentos;
- feedback.

Esta capa es la que habilita el seguimiento academico real y la futura evolucion institucional del sistema.

## Stack tecnico de persistencia

- SQLAlchemy
- Alembic
- Psycopg

## Motores de base previstos

### Desarrollo y pruebas locales

- SQLite por defecto en entornos locales o de prueba.

### Despliegue web multiusuario

- PostgreSQL como opcion objetivo y recomendada.

## Razones de la decision SQLite/PostgreSQL

SQLite se usa por practicidad durante el desarrollo porque:

- reduce friccion de arranque;
- no obliga a provisionar una base externa;
- funciona bien para pruebas automatizadas y ciclos rapidos.

PostgreSQL se define como objetivo porque:

- el dominio es fuertemente relacional;
- se necesita consistencia historica;
- se requiere trazabilidad academica seria;
- soporta mejor crecimiento multiusuario;
- encaja mejor con el despliegue web futuro.

## Configuracion por entorno

Variables relevantes:

- `APP_ENV`
- `DATABASE_URL`
- `DATABASE_ECHO`
- `AUTO_CREATE_SCHEMA`
- `WEB_ADAPTER`

Comportamiento actual:

- en `development`, `dev`, `local` y `test`, si no existe `DATABASE_URL`, el backend favorece SQLite;
- en escenarios de despliegue, la ruta natural es definir `DATABASE_URL` apuntando a PostgreSQL.

## Modelo academico MVP implementado

La persistencia relacional actual no intenta cubrir toda la institucion. Se implemento un MVP con foco en flujo central:

1. un profesor crea una seccion;
2. un profesor crea una asignacion;
3. un estudiante se matricula;
4. un estudiante resuelve el ejercicio;
5. el sistema registra su intento.

Ese enfoque evita sobrecargar el sistema de datos antes de validar el flujo real del producto.

## Mecanismo actual de registro de intentos

Cuando el frontend envia una resolucion al backend con:

- autenticacion valida;
- `assignment_id`;

entonces el backend puede:

- crear o reutilizar una `submission` del estudiante;
- generar un nuevo `attempt` asociado;
- guardar entradas, resultado resumido, estado y tiempo.

## Migraciones

Se dejo preparada una base de migraciones con Alembic, incluyendo una migracion inicial del esquema relacional MVP.

Esto permite:

- versionar cambios de base de datos;
- reproducir estructura en distintos entornos;
- preparar crecimiento posterior sin cambios manuales desordenados.

## Estado actual de madurez

La capa de persistencia ya esta mas alla de una prueba conceptual, porque:

- tiene esquema inicial;
- tiene modelos ORM;
- tiene repositorios iniciales;
- tiene pruebas de migracion y CRUD;
- ya participa del flujo academico de asignaciones e intentos.

## Limites actuales

Aunque esta capa ya es util, todavia quedan extensiones naturales:

- consultas mas ricas para dashboards;
- repositorios adicionales para historial y seguimiento docente;
- feedback persistido desde interfaz;
- reportes por estudiante, seccion y cohorte;
- endurecimiento de seguridad para despliegue real.