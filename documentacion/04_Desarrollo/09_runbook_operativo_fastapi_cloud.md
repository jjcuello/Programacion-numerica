# Runbook Operativo FastAPI Cloud

## Objetivo

Este runbook sirve para ejecutar el primer despliegue real del backend en FastAPI Cloud con la menor cantidad posible de incertidumbre. Usa payloads reales que ya existen en las pruebas del repositorio.

## Antes de empezar

Debes tener listos estos insumos:

- repositorio actualizado;
- acceso a FastAPI Cloud;
- una base PostgreSQL creada;
- una cadena `DATABASE_URL` valida;
- un secreto largo para `AUTH_TOKEN_SECRET`.

## Paso 1. Verificacion local minima

Desde `backend/`:

```bash
pip install -r requirements.txt
fastapi --help
python run_web.py
```

En otra terminal:

```bash
curl http://127.0.0.1:8000/api/health
```

Respuesta esperada aproximada:

```json
{"status":"ok","storage_backend":"sqlite"}
```

Si `fastapi --help` falla indicando que debes instalar `fastapi[standard]`, vuelve a instalar dependencias con:

```bash
pip install -r requirements.txt
```

## Paso 2. Variables de entorno de produccion

Usa como base `backend/.env.example`.

Valores minimos recomendados:

```text
APP_ENV=production
WEB_ADAPTER=fastapi
DATABASE_URL=postgresql+psycopg://usuario:clave@host:5432/programacion_numerica
DATABASE_ECHO=false
AUTO_CREATE_SCHEMA=false
AUTH_TOKEN_SECRET=un-secreto-largo-y-unico-de-produccion
CORS_ALLOW_ORIGINS=https://tu-frontend.example.com
CORS_ALLOW_CREDENTIALS=false
```

## Paso 3. Desplegar el backend

Desde `backend/`:

```bash
fastapi deploy
```

Si FastAPI Cloud no detecta la aplicacion automaticamente, el punto de entrada correcto de esta app es:

```bash
uvicorn src.interfaces.web.app:create_fastapi_app --factory --host 0.0.0.0 --port 8000
```

## Paso 4. Aplicar migraciones

Una vez creado el servicio y configuradas las variables:

```bash
alembic upgrade head
```

La forma exacta de ejecutar este paso dependera de como FastAPI Cloud exponga consola, release commands o shell remota. Si esa ejecucion no esta disponible desde el servicio, debes aplicarlas desde un entorno que apunte a la misma `DATABASE_URL`.

## Paso 5. Prueba de humo de la API publicada

Exporta la URL real del backend publicado:

```bash
export BACKEND_URL="https://tu-backend.fastapicloud.dev"
```

Prueba salud:

```bash
curl "$BACKEND_URL/api/health"
```

Registrar profesor:

```bash
curl -X POST "$BACKEND_URL/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "teacher-fastapi@example.com",
    "password": "teacher-pass-123",
    "full_name": "Teacher FastAPI",
    "roles": ["teacher"]
  }'
```

Registrar estudiante:

```bash
curl -X POST "$BACKEND_URL/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "student-fastapi@example.com",
    "password": "student-pass-123",
    "full_name": "Student FastAPI",
    "roles": ["student"]
  }'
```

Login de profesor:

```bash
curl -X POST "$BACKEND_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "teacher-fastapi@example.com",
    "password": "teacher-pass-123"
  }'
```

## Paso 6. Smoke test automatizable

El repositorio incluye un script listo para validar el backend desplegado:

```bash
cd backend
chmod +x smoke_test_api.sh
BACKEND_URL="https://tu-backend.fastapicloud.dev" ./smoke_test_api.sh
```

Ese script ejecuta:

- `GET /api/health`
- registro de profesor;
- registro de estudiante;
- login de profesor;
- creacion de seccion.

## Paso 7. Validar una resolucion numerica real

Con un token de estudiante valido:

```bash
curl -X POST "$BACKEND_URL/api/roots/solve" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TU_TOKEN_ESTUDIANTE" \
  -d '{
    "method": "newton",
    "expression": "x**3 - x - 2",
    "x0": 1.5,
    "tolerance": 0.000001,
    "max_iterations": 50
  }'
```

Respuesta esperada:

- `status` igual a `success`;
- una raiz cercana a `1.5213797`;
- iteraciones serializadas.

## Paso 8. Conectar el frontend

Antes de cargar `platform-api.js`, define:

```html
<script>
  window.NUMERICAL_API_BASE_URL = "https://tu-backend.fastapicloud.dev";
</script>
```

Alternativamente, toma como referencia `frontend/assets/js/platform-config.example.js`.

## Paso 9. Errores tipicos

### `401` o autenticacion inconsistente

Revisar:

- `AUTH_TOKEN_SECRET`;
- token copiado correctamente;
- cabecera `Authorization: Bearer ...`.

### `500` al guardar datos

Revisar:

- `DATABASE_URL`;
- migraciones ejecutadas;
- permisos del usuario PostgreSQL.

### Frontend sin acceso a la API

Revisar:

- `CORS_ALLOW_ORIGINS`;
- URL real del frontend publicada;
- valor de `window.NUMERICAL_API_BASE_URL`.

## Paso 10. Criterio de exito para presentar

Puedes considerar exitoso el despliegue inicial si logras demostrar estos cinco puntos:

1. `GET /api/health` publico respondiendo correctamente.
2. Registro o login real contra la URL publica.
3. Resolucion numerica remota por `POST /api/roots/solve`.
4. Creacion de seccion y asignacion docente.
5. Integracion del frontend con la URL desplegada.

Ese conjunto ya justifica tecnicamente que el proyecto es desplegable como plataforma web educativa basada en FastAPI.