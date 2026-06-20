# Checklist de Primer Despliegue en FastAPI Cloud

## Objetivo

Este checklist esta pensado para ejecutar la primera publicacion funcional del proyecto sin mezclar demasiadas variables al mismo tiempo. La idea es publicar primero el backend, validarlo y despues conectar el frontend.

## Fase 1. Preparar backend local

1. Entra a `backend/`.
2. Activa tu entorno virtual.
3. Instala dependencias con `pip install -r requirements.txt`.
4. Verifica que el backend levante localmente con `python run_web.py`.
5. Abre `http://127.0.0.1:8000/api/health` y confirma respuesta `status: ok`.

## Fase 2. Preparar base de datos de produccion

1. Crea una instancia PostgreSQL gestionada.
2. Guarda la cadena real de conexion `DATABASE_URL`.
3. Confirma que el usuario de base tenga permisos para crear y modificar tablas.

## Fase 3. Preparar configuracion del backend

1. Usa `backend/.env.example` como referencia.
2. Define estas variables en FastAPI Cloud:
   - `APP_ENV=production`
   - `WEB_ADAPTER=fastapi`
   - `DATABASE_URL=postgresql+psycopg://...`
   - `AUTH_TOKEN_SECRET=<secreto-largo-y-unico>`
   - `CORS_ALLOW_ORIGINS=https://tu-frontend.example.com`
3. Deja `AUTO_CREATE_SCHEMA=false`.
4. Deja `DATABASE_ECHO=false`.

## Fase 4. Publicar backend en FastAPI Cloud

1. Abre terminal en `backend/`.
2. Ejecuta `fastapi deploy`.
3. Si la deteccion automatica falla, usa como referencia el entrypoint:

```bash
uvicorn src.interfaces.web.app:create_fastapi_app --factory --host 0.0.0.0 --port 8000
```

4. Anota la URL publica entregada por FastAPI Cloud.

## Fase 5. Ejecutar migraciones

1. Corre `alembic upgrade head` en el entorno asociado al despliegue.
2. Verifica que las tablas principales existan.
3. Repite `GET /api/health` sobre la URL publica.

## Fase 6. Prueba de humo del backend publicado

1. Valida `GET /api/health`.
2. Valida `POST /api/auth/register`.
3. Valida `POST /api/auth/login`.
4. Valida `POST /api/roots/solve`.
5. Si estas cuatro pruebas fallan, no conectes aun el frontend.

## Fase 7. Preparar frontend para el backend publicado

1. Publica el frontend como sitio estatico.
2. Define la URL del backend antes de cargar `platform-api.js`.
3. Puedes hacerlo con un script inline o usando como referencia `frontend/assets/js/platform-config.example.js`.

Ejemplo:

```html
<script>
  window.NUMERICAL_API_BASE_URL = "https://tu-backend.fastapicloud.dev";
</script>
```

4. Si pruebas el frontend localmente, usa `python -m http.server 8080` desde `frontend/`.

## Fase 8. Conectar frontend y backend

1. Ajusta `CORS_ALLOW_ORIGINS` con el dominio real del frontend.
2. Publica o recarga el frontend.
3. Prueba login como `estudiante` y `profesor`.
4. Prueba crear seccion y asignacion desde el modulo docente.
5. Prueba cargar codigo de clase y resolver desde el modulo estudiante.

## Fase 9. Diagnostico rapido si algo falla

### Caso A. `health` responde pero login falla

Revisar:

- `AUTH_TOKEN_SECRET`
- estado de la base de datos
- migraciones aplicadas

### Caso B. Login funciona pero el frontend no conecta

Revisar:

- `window.NUMERICAL_API_BASE_URL`
- `CORS_ALLOW_ORIGINS`
- consola del navegador

### Caso C. El backend responde pero no guarda datos

Revisar:

- `DATABASE_URL`
- permisos del usuario PostgreSQL
- tablas creadas con Alembic

## Fase 10. Cierre minimo aceptable para presentar

Puedes considerar exitoso el primer despliegue si logras demostrar:

1. backend publico respondiendo `health`;
2. login real contra backend;
3. resolucion numerica remota;
4. flujo basico profesor-estudiante con asignacion e intento registrado.

Ese conjunto ya demuestra que el proyecto paso de maqueta local a plataforma web funcional con backend desplegable.