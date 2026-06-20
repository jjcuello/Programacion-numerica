# Frontend e Integracion v0.2

## Objetivo de este documento

Describir como ha evolucionado el frontend desde una experiencia parcialmente simulada y con calculo local hacia una interfaz conectada al backend real.

## Situacion inicial del frontend

El frontend ya tenia una base visual amplia:

- landing page institucional;
- panel del estudiante;
- panel del profesor;
- perfil de usuario;
- componentes de graficas, tablas y tutor didactico.

Sin embargo, dos partes clave seguian siendo locales:

- el calculo numerico en JavaScript;
- la autenticacion y sesion mediante usuarios mock en `localStorage`.

## Cambio 1. Resolucion numerica remota

La primera integracion real consistio en sustituir el calculo local de raices por llamadas HTTP al backend.

### Impacto en el estudiante

La pantalla del estudiante mantiene:

- vista previa matematica;
- metricas de estado;
- tabla de iteraciones;
- grafica interactiva;
- alertas didacticas.

Lo que cambio fue la fuente del calculo: ahora la resolucion viene del backend Python.

### Impacto en el profesor

El comparador docente mantiene su experiencia visual, pero ya consume la API del backend para ejecutar biseccion, Newton, secante y punto fijo.

## Cambio 2. Cliente compartido de plataforma

Se agrego `frontend/assets/js/platform-api.js` como cliente comun para encapsular:

- URL base de API;
- manejo de sesion;
- login y registro;
- creacion de secciones y asignaciones;
- matricula;
- consulta de asignaciones;
- resolucion y comparacion numerica.

Esto evita duplicar llamadas `fetch` y simplifica la continuidad del frontend.

## Cambio 3. Login real contra backend

La pantalla `login.html` ya no depende solo de un diccionario local de usuarios mock. Ahora:

- intenta autenticar contra backend real;
- si el usuario de prueba aun no existe, puede bootstrapearlo mediante registro automatico controlado;
- guarda una sesion real con token JWT;
- redirige al panel segun rol.

## Cambio 4. Navegacion y perfil con sesion real

Los componentes de navegacion y perfil se ajustaron para leer la sesion a traves del cliente compartido, no solo directamente desde `localStorage` sin estructura comun.

Esto mejora consistencia entre:

- login;
- dropdown de usuario;
- perfil;
- cierre de sesion.

## Cambio 5. Flujo docente real

La pantalla del profesor ya puede iniciar un flujo academico real usando el backend:

1. se autentica como profesor;
2. crea una seccion;
3. crea una asignacion ligada a la expresion del laboratorio docente;
4. genera un codigo de clase real con formato `CLS:<section_id>:<assignment_id>`.

El objetivo de ese codigo es encapsular la relacion entre grupo y asignacion, de forma simple para la experiencia actual.

## Cambio 6. Flujo estudiantil real

La pantalla del estudiante ahora puede:

1. iniciar sesion como estudiante;
2. ingresar el codigo de clase generado por el profesor;
3. matricularse en la seccion correspondiente;
4. cargar la asignacion real desde backend;
5. precargar la expresion y el metodo sugerido;
6. resolver la asignacion dejando el intento registrado.

## Persistencia de contexto en frontend

El frontend sigue usando `localStorage` para soporte de experiencia, pero ahora con roles mas claros:

- `user_session`: sesion actual con token y datos de usuario;
- `active_assignment_context`: asignacion activa cargada por codigo de clase;
- `simulations_history`: historial local de apoyo visual del estudiante.

Es importante notar que el historial local no reemplaza a la persistencia relacional del backend; solo complementa la experiencia actual.

## Estado funcional alcanzado

Con estos cambios, el frontend ya no es solamente una maqueta visual avanzada. Ahora opera como cliente de una plataforma academica en construccion.

Eso significa que:

- la autenticacion ya pasa por backend;
- las asignaciones ya pueden existir como objetos reales en la base;
- la resolucion numerica ya se ejecuta en Python;
- los intentos del estudiante ya pueden quedar trazados.

## Limitaciones actuales del frontend

Todavia quedan superficies por completar o refinar:

- la vista del profesor no lista aun todas sus asignaciones historicas;
- la vista del estudiante no reemplaza todavia todo su historial local por consultas reales a `submissions` y `attempts`;
- el flujo de administracion sigue menos conectado que los paneles de profesor y estudiante;
- faltan pruebas manuales de punta a punta en navegador para este nuevo flujo academico.