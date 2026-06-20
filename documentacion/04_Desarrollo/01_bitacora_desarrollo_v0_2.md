# Bitacora de Desarrollo v0.2

## Objetivo

Este documento resume, en orden cronologico, como ha evolucionado la aplicacion desde una base de consola y frontend estatico hacia un sistema web con backend numerico desacoplado, API HTTP, persistencia relacional y flujo academico inicial.

## Hito 1. Consolidacion del repositorio de trabajo

El punto de partida de esta fase fue sincronizar la carpeta local de trabajo con el repositorio remoto para asegurar que el desarrollo posterior ocurriera sobre una base actualizada y consistente.

Resultado de este hito:

- repositorio local alineado con `origin/main`;
- confirmacion del estado funcional previo del proyecto;
- establecimiento del backend v0.2 como base tecnica para continuar.

## Hito 2. Analisis de arquitectura frontend-backend

Se realizo una revision profunda de dos superficies:

- frontend estatico en HTML, CSS y JavaScript;
- backend Python modular en `backend/src/`.

El hallazgo principal fue que el frontend resolvia metodos numericos con logica propia en JavaScript, mientras que el backend ya contaba con un motor desacoplado que podia crecer como fuente unica de calculo.

Decision tomada:

- no ejecutar Python dentro del navegador;
- integrar frontend y backend mediante HTTP.

## Hito 3. Primera API HTTP para metodos de raices

Se implemento una interfaz web inicial en Python para exponer el motor numerico del backend. El objetivo fue mover primero el dominio de raices, porque ya existia una UI madura en frontend y el backend estaba mas cerca de soportar ese caso.

Capacidades agregadas:

- `GET /api/health`
- `POST /api/roots/solve`
- `POST /api/roots/compare`

Este hito tambien requirio ajustar la serializacion del backend para que el frontend pudiera seguir trabajando con la forma de datos que ya esperaba: raiz, iteraciones, estado y tiempo.

## Hito 4. Integracion de metodos faltantes en backend v0.2

La arquitectura v0.2 ya soportaba biseccion y Newton, pero para que el comparador docente y la experiencia del estudiante mantuvieran paridad con el frontend historico se integraron ademas:

- metodo de la secante;
- metodo de punto fijo.

Tambien se anadieron estados de interfaz (`ui_status`) para mapear correctamente singularidades, violaciones de Bolzano, raices en extremos y limites de iteracion.

## Hito 5. Migracion del frontend numerico al backend

Una vez operativa la API HTTP, el frontend dejo de resolver metodos de raices localmente para pasar a consumir el backend Python.

Resultado funcional:

- el estudiante sigue viendo la misma UI de metricas, tabla y grafica;
- el profesor sigue viendo la tabla comparativa y la grafica conjunta;
- el calculo numerico ya no depende del navegador, sino del backend desacoplado.

La evaluacion local de funciones se mantuvo solo donde sigue siendo util para graficas y validaciones didacticas del lado cliente.

## Hito 6. Modelado de datos y decision de persistencia

Se conceptualizo la base de datos de la plataforma pensando en crecimiento real del producto: seguimiento de estudiantes, asignaciones docentes, intentos, versionado de actividades y trazabilidad academica.

Se definio como decision tecnica principal:

- PostgreSQL como base objetivo para despliegue web multiusuario;
- SQLite como soporte pragmatica para desarrollo local y pruebas ligeras.

Tambien se documento un modelo entidad-relacion conceptual y un esquema MVP inicial.

## Hito 7. Implementacion de persistencia relacional MVP

Sobre esa definicion conceptual se implemento una capa relacional inicial en backend con:

- SQLAlchemy;
- Alembic;
- Psycopg;
- modelos ORM para el MVP academico;
- repositorios iniciales para usuarios, asignaciones, entregas e intentos.

La persistencia JSON existente no se elimino. Se mantuvo como soporte de sesiones locales y trazas de laboratorio, mientras la persistencia relacional quedo preparada para la evolucion web real.

## Hito 8. Flujo academico basico en backend

Se agregaron capacidades minimas para soportar un uso real profesor-estudiante:

- registro de usuario;
- login;
- creacion de secciones;
- matriculas;
- creacion de asignaciones;
- registro automatico de intentos cuando una resolucion viene asociada a una asignacion.

Este hito marca el paso de un laboratorio numerico hacia una plataforma academica trazable.

## Hito 9. Migracion de autenticacion a JWT estandar

La autenticacion inicial basada en token firmado ad hoc se migro a JWT estandar usando `PyJWT`.

Beneficios de este cambio:

- formato reconocido y portable;
- mejor interoperabilidad con FastAPI y clientes futuros;
- base mas limpia para evolucionar a seguridad mas formal.

## Hito 10. Adaptador FastAPI

Aunque ya existia un adaptador web funcional basado en `http.server`, se agrego un adaptador `FastAPI` como camino recomendado de evolucion.

Decision de implementacion:

- mantener disponible el adaptador `stdlib` para compatibilidad;
- usar `FastAPI` como adaptador principal mediante la variable `WEB_ADAPTER`.

## Hito 11. Integracion del frontend academico real

El frontend dejo de depender de credenciales mock y de una sesion meramente local. Se agrego un cliente compartido (`platform-api.js`) y se conectaron las siguientes piezas:

- login del frontend contra backend real;
- sesion persistida con token JWT;
- generacion de codigo de clase por el profesor;
- carga de asignacion y matricula por el estudiante;
- registro de intentos del estudiante al resolver una asignacion real.

El codigo de clase actual tiene el formato:

- `CLS:<section_id>:<assignment_id>`

## Hito 12. Estado alcanzado al cierre actual

La aplicacion ya cuenta con una cadena funcional coherente:

1. el profesor inicia sesion;
2. crea una seccion;
3. crea una asignacion ligada a una expresion y metodos permitidos;
4. obtiene un codigo de clase;
5. el estudiante inicia sesion;
6. carga el codigo de clase;
7. queda matriculado y recibe la asignacion;
8. resuelve el problema numerico;
9. el backend registra el intento.

Este estado no cierra el producto, pero si constituye una base v0.2 tecnicamente coherente y suficientemente trazable para seguir desarrollando.