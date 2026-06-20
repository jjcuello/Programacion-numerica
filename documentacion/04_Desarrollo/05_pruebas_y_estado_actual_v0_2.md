# Pruebas y Estado Actual v0.2

## Objetivo de este documento

Concentrar las pruebas ejecutadas, el estado operativo actual y los puntos que siguen abiertos al cierre de esta fase de desarrollo.

## Estrategia de validacion usada hasta ahora

La validacion del proyecto se ha realizado por capas:

- pruebas unitarias y de contratos del backend;
- pruebas de CLI y persistencia JSON;
- pruebas HTTP sobre el adaptador web inicial;
- pruebas de persistencia relacional y migraciones;
- pruebas del flujo academico inicial;
- pruebas del adaptador FastAPI.

## Pruebas backend ejecutadas

### Contratos y metodos

- `tests/test_v0_2_contracts.py`

Valida contratos del dominio y metodos numericos integrados.

### CLI y almacenamiento local

- `tests/test_v0_2_cli_and_storage.py`

Valida la CLI modular y el guardado de sesiones en JSON.

### API HTTP numerica

- `tests/test_v0_2_web_api.py`

Valida endpoints de resolucion y comparacion numerica.

### Persistencia relacional

- `tests/test_v0_2_relational_storage.py`

Valida migracion inicial y persistencia CRUD minima del MVP academico.

### Flujo academico con servidor web

- `tests/test_v0_2_web_academic_flow.py`

Valida registro, login, seccion, matricula, asignacion y registro de intento.

### Adaptador FastAPI

- `tests/test_v0_2_fastapi_api.py`

Valida salud, autenticacion, asignaciones y consulta desde el adaptador FastAPI.

## Comando de regresion principal validado

```bash
cd backend
python -m unittest tests/test_v0_2_contracts.py tests/test_v0_2_cli_and_storage.py tests/test_v0_2_web_api.py tests/test_v0_2_relational_storage.py tests/test_v0_2_web_academic_flow.py tests/test_v0_2_fastapi_api.py
```

Resultado de referencia al cierre actual:

- `Ran 20 tests`
- `OK`

## Estado operativo actual

Al cierre de esta fase, la aplicacion puede:

- autenticar usuarios desde frontend y backend;
- operar profesor y estudiante sobre una sesion real;
- crear secciones y asignaciones;
- matricular estudiantes;
- resolver metodos de raices desde backend;
- comparar metodos desde el frontend del profesor;
- registrar intentos asociados a asignaciones.

## Riesgos y advertencias residuales

### 1. Warning de `fastapi.testclient`

Existe una advertencia deprecada relacionada con la compatibilidad entre `fastapi.testclient` y la version disponible de `httpx` en el entorno.

Estado:

- no rompe funcionalidad;
- no invalida las pruebas;
- conviene revisarlo en una fase de afinado de dependencias.

### 2. Historial local vs historial real

El estudiante sigue manteniendo parte de su experiencia historica en `localStorage`. Ya existe persistencia relacional para intentos, pero todavia no toda la UI consulta ese historial real desde backend.

### 3. Superficie administrativa incompleta

Los paneles de estudiante y profesor son los mas avanzados en integracion. La vista administrativa sigue menos conectada al backend real.

### 4. Seguridad pendiente para produccion

Aunque JWT y roles ya existen, aun faltan aspectos tipicos de endurecimiento para despliegue real:

- politicas mas fuertes de secretos;
- expiracion y renovacion de sesiones con mayor detalle;
- validaciones adicionales de autorizacion por recurso;
- observabilidad y auditoria mas formales.

## Proximo estado natural del proyecto

Los siguientes avances tecnicamente coherentes serian:

1. listar asignaciones reales en UI docente y estudiantil;
2. reemplazar historial local por consultas reales a `submissions` y `attempts`;
3. exponer reportes por estudiante y seccion;
4. formalizar despliegue con PostgreSQL real y variables de entorno endurecidas;
5. ampliar cobertura de pruebas hacia flujos manuales de navegador o pruebas E2E.

## Conclusión

El proyecto ya no se encuentra solo en etapa de concepto o maqueta visual. Actualmente tiene una base de desarrollo verificable, con componentes desacoplados, flujo web funcional, persistencia academica inicial y una ruta clara para continuar creciendo sin reescrituras estructurales.