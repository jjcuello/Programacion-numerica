# Hoja de ruta proxima iteracion

## Objetivo

Ordenar el trabajo inmediato posterior al despliegue para que la siguiente sesion pueda retomarse sin reexplorar el estado del proyecto.

## Prioridad 1. Cerrar el flujo publico extremo a extremo

### 1.1. Habilitar CORS para Cloudflare Pages

Accion:

- actualizar `CORS_ALLOW_ORIGINS` en FastAPI Cloud para incluir `https://programacion-numerica-frontend.pages.dev`.

Validacion esperada:

- la preflight `OPTIONS` deja de responder `Disallowed CORS origin`;
- login y registro funcionan desde el frontend ya publicado.

### 1.2. Validar frontend publico completo

Accion:

- probar `index.html`, login, `profesor.html` y `estudiante.html` directamente desde Cloudflare Pages.

Validacion esperada:

- login docente correcto;
- comparacion de algoritmos desde la UI publica;
- login estudiantil correcto;
- resolucion de simulacion y tabla de iteraciones desde la UI publica.

## Prioridad 2. Completar integracion funcional de la capa academica

### 2.1. Listado real de asignaciones e historial desde backend

Accion:

- reemplazar dependencias restantes de `localStorage` por consultas reales a asignaciones, submissions y attempts.

Resultado esperado:

- historial del estudiante sincronizado con base de datos real;
- menos divergencia entre estado visual y estado persistido.

### 2.2. Vista docente con datos reales de seguimiento

Accion:

- exponer y consumir reportes por seccion, asignacion y estudiante.

Resultado esperado:

- panel del profesor con informacion academica real, no solo simulacion visual.

### 2.3. Cerrar la vista administrativa

Accion:

- decidir si se deja como maqueta avanzada o si se conecta a endpoints minimos reales.

Resultado esperado:

- definicion clara del alcance de la vista admin para presentacion academica.

## Prioridad 3. Endurecimiento tecnico de produccion

### 3.1. Rotacion de secretos y limpieza operativa

Accion:

- rotar `AUTH_TOKEN_SECRET` y, si procede, la clave de base de datos si quedaron expuestas durante pruebas.

### 3.2. Revisar autorizacion por recurso

Accion:

- reforzar verificaciones de acceso en secciones, asignaciones y consultas por rol.

### 3.3. Ajustar observabilidad basica

Accion:

- definir logging minimo util para despliegue publico y errores de integracion.

## Prioridad 4. Pruebas y automatizacion

### 4.1. Consolidar smoke tests del entorno publico

Accion:

- ampliar `backend/smoke_test_api.sh` o crear un script complementario para validar tambien frontend publicado.

### 4.2. Pruebas E2E ligeras

Accion:

- formalizar al menos un flujo navegador docente y uno estudiantil usando herramientas similares a Playwright.

Resultado esperado:

- menos riesgo de regresion al seguir iterando en UI y API.

## Prioridad 5. Preparacion academica y de entrega

### 5.1. Consolidar narrativa de arquitectura publicada

Accion:

- mantener README y `documentacion/04_Desarrollo/` alineados con la topologia real: Cloudflare Pages + FastAPI Cloud + Supabase.

### 5.2. Preparar demo guiada

Accion:

- definir un recorrido corto para mostrar profesor, estudiante, API publica y persistencia real.

### 5.3. Identificar backlog posterior a la demostracion

Accion:

- separar claramente lo imprescindible para presentar de lo deseable para una v0.3.

## Secuencia sugerida de la siguiente sesion

1. corregir `CORS_ALLOW_ORIGINS` en FastAPI Cloud;
2. validar frontend publico completo en Cloudflare Pages;
3. registrar evidencia de pruebas publicas satisfactorias;
4. decidir el siguiente bloque funcional mas importante entre historial real, reportes docentes o vista admin.

## Criterio de exito inmediato

La siguiente sesion puede considerarse exitosa si se cumplen estos cuatro puntos:

1. el frontend publicado autentica contra el backend publicado;
2. profesor y estudiante pueden operar desde URLs publicas;
3. la documentacion refleja correctamente el estado final del despliegue;
4. el backlog inmediato queda reducido a funcionalidad y no a infraestructura base.