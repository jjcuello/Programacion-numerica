# 04_Desarrollo

## Proposito de esta carpeta

Esta carpeta consolida la fase de desarrollo de la aplicacion hasta el estado actual del proyecto. Su objetivo es dejar trazabilidad clara sobre que se construyo, como se construyo, por que decisiones tecnicas se llego al estado actual y que validaciones se ejecutaron.

La documentacion de esta carpeta esta pensada para:

- facilitar continuidad entre sesiones de trabajo;
- permitir que otros modelos o desarrolladores entiendan el estado real del sistema;
- separar el relato de implementacion de la fase de analisis y de la fase de diseño;
- registrar decisiones tecnicas y su impacto funcional.

## Documentos incluidos

### 1. Bitacora de desarrollo

Archivo: `01_bitacora_desarrollo_v0_2.md`

Resume cronologicamente los hitos principales del desarrollo realizado en el repositorio: sincronizacion, analisis de arquitectura, API HTTP, migracion del frontend, persistencia relacional, autenticacion y adaptador FastAPI.

### 2. Backend y API

Archivo: `02_backend_y_api_v0_2.md`

Explica la evolucion del backend Python, las capas activas, los endpoints disponibles y el flujo actual del motor numerico hacia la web.

### 3. Frontend e integracion

Archivo: `03_frontend_e_integracion_v0_2.md`

Describe como el frontend paso de logica local y autenticacion simulada a consumir el backend real, incluyendo login, comparacion docente, carga de asignaciones y registro de intentos.

### 4. Persistencia y datos

Archivo: `04_persistencia_y_datos_v0_2.md`

Documenta el estado actual de persistencia: JSON para sesiones, persistencia relacional MVP, variables de entorno, migraciones y decision de coexistencia entre SQLite y PostgreSQL.

### 5. Pruebas y estado actual

Archivo: `05_pruebas_y_estado_actual_v0_2.md`

Consolida las pruebas ejecutadas, los comandos de validacion relevantes, el estado operativo actual y los riesgos o puntos pendientes mas importantes.

### 6. Flujos operativos y diagramas

Archivo: `06_flujos_operativos_y_diagramas_v0_2.md`

Resume en diagramas Mermaid el flujo real profesor-estudiante-backend-base de datos, el recorrido de una resolucion numerica y la topologia web actual del sistema.

### 7. Despliegue en FastAPI Cloud

Archivo: `07_despliegue_fastapi_cloud_v0_2.md`

Explica como preparar y desplegar este backend en FastAPI Cloud, que variables de entorno se deben configurar y que decisiones practicas conviene tomar para publicar el frontend y el backend sin romper la integracion.

### 8. Checklist de primer despliegue

Archivo: `08_checklist_primer_despliegue_fastapi_cloud.md`

Lista paso a paso la primera publicacion recomendada del proyecto, desde la base de datos y variables de entorno hasta la conexion final del frontend con la URL publica del backend.

### 9. Runbook operativo de despliegue

Archivo: `09_runbook_operativo_fastapi_cloud.md`

Contiene una secuencia mas concreta con comandos listos para copiar, validaciones por `curl` y recomendaciones para depurar el primer despliegue real del backend.

### 10. Cierre de sesion de despliegue publico

Archivo: `10_cierre_sesion_despliegue_publico_2026_06_20.md`

Resume el cierre operativo de la sesion en la que se logro publicar el backend en FastAPI Cloud, el frontend en Cloudflare Pages, se validaron flujos reales y se identifico como pendiente principal la configuracion final de CORS.

### 11. Hoja de ruta proxima iteracion

Archivo: `11_hoja_ruta_proxima_iteracion.md`

Organiza el trabajo siguiente en bloques concretos: cierre del despliegue publico, integracion funcional restante, endurecimiento tecnico y preparacion academica para demostracion o defensa.

## Estado cubierto por esta fase

La fase de desarrollo documentada aqui cubre hasta el estado en el que:

- el backend resuelve metodos de raices por HTTP;
- el frontend ya consume el backend para resolucion numerica;
- existe persistencia relacional inicial para usuarios, secciones, asignaciones, entregas e intentos;
- la autenticacion del frontend y backend ya esta conectada;
- la aplicacion puede operar un flujo basico profesor-estudiante sobre una asignacion real.

## Relacion con carpetas anteriores

- `01_Planificacion/`: contiene control, cierre y seguimiento del planteamiento inicial.
- `02_Analisis/`: contiene necesidades, entrevistas, insumos docentes y justificacion del problema.
- `03_Diseño/`: contiene arquitectura objetivo, UX/UI, modelo de datos y decisiones tecnicas.
- `04_Desarrollo/`: registra lo efectivamente implementado hasta ahora.