# Control de cierre de planificacion

Fecha de emision: 2026-06-07
Fase evaluada: Planificacion
Decision de avance: Aprobada para pasar a Diseno

## 1) Criterios de salida go/no-go

| Criterio | Estado | Evidencia |
| --- | --- | --- |
| Objetivo general y objetivos especificos definidos | GO | README.md |
| Alcance actual, alcance objetivo y fuera de alcance definidos | GO | README.md |
| Arquitectura actual y arquitectura objetivo documentadas | GO | README.md |
| Roadmap por fases y cronograma definidos | GO | README.md |
| Requisitos funcionales y no funcionales definidos | GO | documentacion/plan_tecnico_v0_2.md |
| Riesgos principales identificados y priorizados | GO | Seccion 2 de este documento |
| Responsables y fechas de corto plazo asignados | GO | Seccion 3 de este documento |
| Backlog de Diseno priorizado y con DoD minima | GO | Seccion 4 de este documento |
| Registro de aprobacion del equipo emitido | GO | Seccion 5 de este documento |

Resultado go/no-go: GO.

## 2) Matriz de riesgos priorizada

Escala usada:
- Probabilidad: Alta, Media, Baja.
- Impacto: Alto, Medio, Bajo.
- Prioridad: Critica, Alta, Media.

| ID | Riesgo | Probabilidad | Impacto | Prioridad | Mitigacion | Responsable |
| --- | --- | --- | --- | --- | --- | --- |
| R1 | Avanzar interfaz web sin estabilizar contratos del nucleo | Media | Alto | Critica | Bloquear tareas web que dependan de contratos no cerrados; revisar contratos en cada corte semanal | Jose Javier Cuello |
| R2 | Inconsistencia entre metodos migrados y metodos historicos | Alta | Alto | Critica | Definir pruebas de regresion por metodo piloto y validar salida estandarizada | Jose Javier Cuello |
| R3 | Cobertura de pruebas insuficiente al crecer modulos | Media | Alto | Alta | Exigir prueba minima por caso de uso nuevo y mantener ejecucion continua local | Jose Javier Cuello |
| R4 | Retraso en definicion de UX didactica para la fase web | Media | Medio | Media | Prototipo temprano de flujos estudiante/profesor y validacion interna | Leonardo Gonzalez |
| R5 | Deriva de alcance por agregar modulos no priorizados | Media | Medio | Media | Gate de priorizacion: solo backlog de fase vigente y cambios aprobados en corte | Jose Javier Cuello y Leonardo Gonzalez |

## 3) Asignacion operativa de entregables inmediatos

Ventana objetivo de esta asignacion: 2026-06-08 al 2026-06-14.

| Entregable inmediato | Responsable | Fecha compromiso | Criterio de aceptacion |
| --- | --- | --- | --- |
| Contrato base revisado de ProblemDefinition y MethodResult | Jose Javier Cuello | 2026-06-09 | Contratos vigentes y consistentes con metodos piloto |
| Estandar minimo de resultados de iteracion (error, residual, estado) | Jose Javier Cuello | 2026-06-10 | Estructura uniforme en metodos piloto |
| Backlog tecnico detallado de Diseno con prioridades | Jose Javier Cuello | 2026-06-09 | Lista priorizada con dependencia y DoD minima |
| Definicion de criterios UX para flujos didacticos base | Leonardo Gonzalez | 2026-06-11 | Documento con flujos de estudiante y profesor |
| Plantilla de reporte de comparacion para uso academico | Leonardo Gonzalez | 2026-06-12 | Plantilla revisable por docente y equipo |
| Revision conjunta de coherencia plan-tecnico-documental | Jose Javier Cuello y Leonardo Gonzalez | 2026-06-14 | Minuta de revision y ajustes aplicados |

## 4) Backlog de Diseno priorizado (Definition of Done minima)

### Prioridad alta

1. Disenar contratos estables para problemas, iteraciones y resultados.
   DoD minima:
   - Contratos versionados en src/core.
   - Ejemplos de uso documentados.
   - Compatibilidad validada con biseccion y Newton.

2. Definir interfaz comun para metodos numericos desacoplados.
   DoD minima:
   - Clase base acordada en src/methods/base.py.
   - Reglas de entrada/salida unificadas.
   - Prueba de contrato para cada metodo piloto.

3. Disenar esquema de persistencia de sesiones y ejecuciones.
   DoD minima:
   - Modelo de datos de sesion definido.
   - Operaciones guardar/cargar documentadas.
   - Caso de uso de trazabilidad validado.

### Prioridad media

1. Definir metrica comun para comparacion de metodos.
   DoD minima:
   - Metricas minimas (iteraciones, error, tiempo, residual).
   - Estructura de salida comparable.
   - Criterios de ordenamiento de resultados.

2. Disenar base de reportes exportables (JSON/CSV inicial).
   DoD minima:
   - Formato de exportacion base acordado.
   - Ejemplo de exportacion funcional.
   - Validacion de lectura por herramienta externa.

3. Definir guias de validacion de expresiones matematicas.
   DoD minima:
   - Reglas de entrada permitida y bloqueada.
   - Casos de prueba de seguridad minima.
   - Documentacion de errores esperados.

### Prioridad baja

1. Propuesta inicial de interfaz web educativa por roles.
   DoD minima:
   - Mapa de vistas por rol.
   - Flujo de navegacion preliminar.
   - Dependencias tecnicas identificadas.

2. Propuesta de capa didactica para recomendaciones y quizzes.
   DoD minima:
   - Reglas base del recomendador listadas.
   - Estructura inicial de banco de preguntas.
   - Criterios de evaluacion didactica inicial.

## 5) Registro de aprobacion de planificacion

Acta corta de aprobacion:

- Fecha: 2026-06-07
- Estado de planificacion: Aprobada con control formal completado.
- Decisiones:
  - Se autoriza el paso a la fase de Diseno.
  - Se mantiene control semanal de riesgos R1 y R2 por prioridad.
  - Se establece revision de avance contra entregables inmediatos el 2026-06-14.

Responsables que aprueban:

- Jose Javier Cuello - Aprobado.
- Leonardo Gonzalez - Aprobado.

## 6) Arranque de Diseno (artefactos asociados)

Para ejecutar el inicio de Diseno con trazabilidad, se definen los siguientes artefactos:

1. documentacion/02_Diseño/paquete_diseno_semana_1.md
2. documentacion/02_Diseño/checklist_tecnico_revision_contratos.md

Estos documentos operativizan los entregables inmediatos definidos en la Seccion 3.
