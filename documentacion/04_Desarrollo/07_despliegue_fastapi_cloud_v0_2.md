# Despliegue en FastAPI Cloud v0.2

## Objetivo de este documento

Orientar el despliegue de este proyecto en FastAPI Cloud de una forma realista y compatible con el estado actual del repositorio.

## 1. Que significa FastAPI Cloud en este contexto

FastAPI Cloud es el servicio gestionado del ecosistema FastAPI para desplegar aplicaciones FastAPI con menos friccion operativa. Segun la documentacion publica de FastAPI, el flujo puede llegar a ser tan simple como ejecutar `fastapi deploy`, y la plataforma resuelve aspectos como HTTPS y parte de la operacion en la nube.

Para este proyecto, eso aplica principalmente al backend ubicado en `backend/`, no al frontend estatico en `frontend/`.

## 2. Decision recomendada para este repositorio

La recomendacion practica para esta fase es separar publicacion en dos piezas:

### Backend

- desplegar `backend/` en FastAPI Cloud.

### Frontend

- publicar `frontend/` como sitio estatico en otro servicio de hosting web;
- o, como alternativa futura, servirlo desde el propio backend si se decide integrar archivos estaticos en FastAPI.

Esta separacion es la mas limpia porque el frontend actual es estatico y el backend ya expone su API de forma independiente.

## 3. Punto de entrada correcto del backend

Este proyecto no define un objeto global `app` en un archivo `main.py`. En cambio, la aplicacion FastAPI se crea con una fabrica:

- `src.interfaces.web.app:create_fastapi_app`

Por eso, si FastAPI Cloud detecta automaticamente la aplicacion, perfecto. Si la deteccion automatica falla, el comando o entrypoint correcto debe usar esa fabrica.

Referencia tecnica interna:

- `backend/run_web.py`
- `backend/src/interfaces/web/app.py`

## 4. Variables de entorno recomendadas para produccion

### Minimas

- `APP_ENV=production`
- `WEB_ADAPTER=fastapi`
- `AUTH_TOKEN_SECRET=<secreto-largo-y-unico>`
- `DATABASE_URL=<cadena-de-postgresql>`
- `CORS_ALLOW_ORIGINS=https://tu-frontend.example.com`

### Opcionales utiles

- `DATABASE_ECHO=false`
- `AUTO_CREATE_SCHEMA=false`
- `CORS_ALLOW_CREDENTIALS=false`

Notas:

- `AUTH_TOKEN_SECRET` no debe ser corto ni reutilizado entre ambientes.
- para produccion, conviene apuntar `DATABASE_URL` a PostgreSQL.
- si el frontend y el backend viven en dominios distintos, `CORS_ALLOW_ORIGINS` debe contener el dominio real del frontend publicado.

## 5. Preparacion local antes de desplegar

Desde la carpeta `backend/`, el proyecto debe poder instalar dependencias y levantar su API sin errores.

Dependencias actuales registradas:

- `fastapi[standard]`
- `uvicorn`
- `sqlalchemy`
- `alembic`
- `psycopg[binary]`
- `PyJWT`

Comprobacion local minima:

```bash
cd backend
pip install -r requirements.txt
fastapi --help
python run_web.py
```

Y validar:

- `GET /api/health`
- login;
- una llamada a `POST /api/roots/solve`

## 6. Ruta simple con FastAPI Cloud

La documentacion publica de FastAPI indica que se puede desplegar con:

```bash
fastapi deploy
```

Recomendacion practica para este repositorio:

```bash
cd backend
fastapi deploy
```

Si el comando `fastapi` falla con un mensaje indicando que debes instalar `fastapi[standard]`, primero reinstala dependencias desde `backend/` con `pip install -r requirements.txt`.

Si el servicio detecta automaticamente la aplicacion, el backend deberia quedar publicado sin mas configuracion de entrada.

## 7. Si la deteccion automatica falla

Como esta aplicacion usa una fabrica `create_fastapi_app()`, el punto de entrada explicito que debes tener a mano es:

```bash
uvicorn src.interfaces.web.app:create_fastapi_app --factory --host 0.0.0.0 --port 8000
```

Eso no significa necesariamente que vayas a ejecutar exactamente ese comando a mano dentro de FastAPI Cloud, pero si te sirve como referencia correcta para:

- start command;
- app import string;
- diagnostico cuando el autodescubrimiento no encuentre la app.

## 8. Base de datos: que hacer en despliegue real

Para una evaluacion academica seria y un despliegue publico, la mejor opcion actual para este proyecto sigue siendo PostgreSQL.

No recomiendo desplegar esta fase productiva con SQLite si esperas:

- multiples usuarios;
- concurrencia;
- persistencia estable en nube;
- evolucion a reportes y seguimiento docente.

Secuencia recomendada:

1. provisionar una base PostgreSQL gestionada;
2. cargar `DATABASE_URL` en FastAPI Cloud;
3. ejecutar migraciones con Alembic;
4. recien despues publicar el frontend final apuntando a la URL publica del backend.

## 9. Migraciones en despliegue

Como el proyecto ya tiene Alembic configurado, la forma correcta de preparar la base es correr migraciones, no depender de creacion implicita de tablas en produccion.

Comando de referencia:

```bash
cd backend
alembic upgrade head
```

En una plataforma gestionada, esto puede ejecutarse como paso previo de build o release, segun lo que permita el servicio.

## 10. Frontend: que debes cambiar al publicarlo

El frontend no se despliega automaticamente junto con FastAPI Cloud. Debes revisar al menos dos cosas:

### URL base de API

El frontend tiene que apuntar a la URL publica del backend desplegado.

Como apoyo, el repositorio incluye:

- `frontend/assets/js/platform-config.example.js`

Ese archivo sirve como referencia para declarar `window.NUMERICAL_API_BASE_URL` antes de cargar `platform-api.js`.

### CORS

Si frontend y backend usan dominios distintos, el backend debe aceptar el origen del frontend. El proyecto ya queda preparado para eso mediante:

- `CORS_ALLOW_ORIGINS`

Ejemplo:

```text
CORS_ALLOW_ORIGINS=https://tu-frontend.netlify.app
```

## 11. Prueba de humo despues del despliegue

Despues de publicar, valida este orden:

1. `GET /api/health`
2. registro o login
3. `POST /api/roots/solve`
4. creacion de seccion
5. creacion de asignacion
6. carga de codigo de clase desde el frontend

Si falla el frontend pero la API responde bien por navegador o por cliente HTTP, el primer sospechoso debe ser CORS o la URL base de la API en JavaScript.

## 12. Riesgos probables en tu primer despliegue

### 1. El backend publica, pero el frontend no conecta

Causa habitual:

- URL de API incorrecta;
- origen del frontend no incluido en `CORS_ALLOW_ORIGINS`.

### 2. La app levanta pero no autentica

Causa habitual:

- `AUTH_TOKEN_SECRET` ausente o inconsistente.

### 3. La app responde, pero no persiste datos

Causa habitual:

- `DATABASE_URL` mal configurada;
- migraciones no ejecutadas;
- base publicada sin permisos correctos.

### 4. FastAPI Cloud no detecta la app automaticamente

Causa habitual:

- el proyecto usa fabrica de aplicacion y no un `app` global evidente.

Respuesta correcta:

- proporcionar el entrypoint basado en `src.interfaces.web.app:create_fastapi_app`.

## 13. Recomendacion final para tu caso

Si nunca has usado FastAPI Cloud, no empieces intentando publicar todo a la vez. Hazlo en este orden:

1. desplegar solo el backend;
2. probar `health`, `login` y `solve` con la URL publica;
3. conectar el frontend a esa URL;
4. validar el flujo profesor-estudiante;
5. recien despues ajustar aspectos visuales o de hosting del frontend.

Ese orden reduce mucho el ruido al depurar y te permite demostrar avance funcional al profesor con evidencia tecnica clara.