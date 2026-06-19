# Paquete de Diseno - Semana 1

Fecha de inicio prevista: 2026-06-08
Fecha de corte prevista: 2026-06-14
Foco: contratos base y consistencia de resultados

## 1) Objetivo operativo de la semana

Cerrar el diseno tecnico minimo para que el nucleo numerico avance con contratos estables, salida uniforme y validacion reproducible en pruebas.

## 2) Alcance de esta semana

Incluye:

- Contrato base de problema en src/core/models/problem.py.
- Contrato base de iteracion en src/core/results/iteration.py.
- Contrato base de resultado de metodo en src/core/results/method_result.py.
- Interfaz comun de metodos en src/methods/base.py.
- Validacion de contratos con pruebas en tests/test_v0_2_contracts.py.

No incluye:

- Implementacion de interfaz web.
- Migracion completa de todos los metodos historicos.
- Capa didactica avanzada (recomendaciones/quizzes).

## 3) Entregables de salida de la semana

1. Especificacion v0.2 de contratos base aprobada por el equipo.
2. Criterios unificados de resultado por iteracion (error, residual, estado, metadata).
3. Checklist tecnico de revision ejecutado y firmado.
4. Lista de cambios priorizados para semana 2.

## 4) Definition of Done (DoD) de contratos base

Se considera terminado si se cumple todo:

1. El contrato ProblemDefinition cubre entradas requeridas por metodos piloto.
2. El contrato MethodResult define estado, solucion, trazabilidad y mensaje.
3. IterationRecord conserva informacion suficiente para analisis de convergencia.
4. NumericalMethod impone interfaz comun sin dependencias de CLI.
5. Las pruebas de contratos pasan sin regressions en tests/test_v0_2_contracts.py.
6. No se agrega logica de negocio en capa de interfaz.

## 5) Plan de trabajo por dia

| Fecha | Actividad | Responsable | Resultado esperado |
| --- | --- | --- | --- |
| 2026-06-08 | Revision de contratos actuales y gap analysis | Jose Javier Cuello | Lista de ajustes propuestos |
| 2026-06-09 | Ajuste de especificacion ProblemDefinition y MethodResult | Jose Javier Cuello | Contratos estables version 1 |
| 2026-06-10 | Estandar de IterationRecord y reglas de metadata | Jose Javier Cuello | Formato uniforme de iteraciones |
| 2026-06-11 | Revision tecnica cruzada con flujo UX academico | Leonardo Gonzalez | Comentarios de uso para salida didactica |
| 2026-06-12 | Ejecucion de checklist tecnico + cierre de hallazgos | Jose Javier Cuello y Leonardo Gonzalez | Checklist cerrado |
| 2026-06-14 | Cierre semanal y backlog priorizado de semana 2 | Jose Javier Cuello y Leonardo Gonzalez | Minuta y backlog actualizado |

## 6) Riesgos de ejecucion de esta semana

- Riesgo: cambiar contratos y romper metodos piloto.
  Mitigacion: correr pruebas de contratos en cada ajuste.

- Riesgo: sobre-diseno de modelos antes de validar casos reales.
  Mitigacion: limitar cambios a necesidades de biseccion y Newton.

- Riesgo: divergencia entre salida tecnica y necesidades docentes.
  Mitigacion: revision cruzada con criterios de lectura didactica.

## 7) Evidencia obligatoria al cierre

1. Checklist tecnico completo en documentacion/03_Diseño/checklist_tecnico_revision_contratos.md.
2. Resultado de pruebas de contratos en tests/test_v0_2_contracts.py.
3. Minuta de cierre semanal con decisiones de continuidad.

## 8) Backlog tecnico priorizado para semana 2

Fuente de entrada:
- Matriz consolidada de entrevistas docentes en documentacion/02_Analisis/matriz_analisis_respuestas_docentes.md.

Objetivo:
- Traducir las prioridades docentes del analisis en tareas tecnicas ejecutables, con modulo responsable, dependencia y criterio de salida verificable.

### Must

| ID | Item tecnico | Descripcion operativa | Modulos impactados | Dependencias | Criterio de salida |
| --- | --- | --- | --- | --- | --- |
| S2-M1 | Historial de sesiones por estudiante | Registrar ejecuciones con fecha, metodo, parametros, resultado y referencia de estudiante o sesion | src/infrastructure/storage, src/core/results, src/app/services | Contratos v0.2 estables y serializacion uniforme | Se pueden guardar y consultar al menos 3 ejecuciones distintas sin perder trazabilidad |
| S2-M2 | Reportes exportables para evaluacion | Exportar resultados individuales y grupales en formatos legibles para revision docente | src/infrastructure/exporters, src/app/use_cases, src/interfaces/cli | Historial de sesiones disponible y campos normalizados | Se genera un CSV o JSON con datos suficientes para revision docente y lectura externa |
| S2-M3 | Alertas de convergencia y parametros | Detectar divergia, oscilacion, parametros invalidos y falta de convergencia con mensajes claros | src/methods, src/core, src/analysis | IterationRecord y MethodResult con estado consistente | El sistema diferencia al menos un caso valido, uno divergente y uno invalido con mensajes comprensibles |

### Should

| ID | Item tecnico | Descripcion operativa | Modulos impactados | Dependencias | Criterio de salida |
| --- | --- | --- | --- | --- | --- |
| S2-S1 | Comparador de metodos paso a paso | Ejecutar 2 o mas metodos sobre un mismo problema y mostrar procedimiento, resultado y diferencias | src/analysis/benchmarking, src/app/use_cases, src/interfaces/cli | Contratos base cerrados y alertas consistentes | Existe una salida comparativa utilizable en demo docente |
| S2-S2 | Graficas didacticas de apoyo | Presentar visualizaciones 2D o 3D faciles de leer para explicar comportamiento y resultados | infrastructure/plotting, legacy/metodos como referencia, futura web | Datos de iteracion y salida normalizada | Se puede generar al menos una visualizacion interpretable para un caso piloto |

### Could

| ID | Item tecnico | Descripcion operativa | Modulos impactados | Dependencias | Criterio de salida |
| --- | --- | --- | --- | --- | --- |
| S2-C1 | Deteccion de similitud entre respuestas | Explorar reglas simples para identificar respuestas o procedimientos excesivamente parecidos | futura capa web, analisis academico posterior | Historial por estudiante y datos consistentes | Existe propuesta tecnica o prototipo exploratorio |
| S2-C2 | Recomendacion didactica inicial | Sugerir apoyos o desbloqueo secuencial segun error comun o fase del ejercicio | src/tutoring, src/analysis | Alertas, historial y clasificacion de errores | Se define una regla inicial validable con 2 o 3 casos |

### Orden recomendado de ejecucion

1. S2-M1 Historial de sesiones por estudiante.
2. S2-M3 Alertas de convergencia y parametros.
3. S2-M2 Reportes exportables para evaluacion.
4. S2-S1 Comparador de metodos paso a paso.
5. S2-S2 Graficas didacticas de apoyo.

### Nota de control

- No iniciar items Could mientras no esten validados todos los Must.
- Cada item debe convertirse en historia tecnica con prueba o demo verificable antes de darse por cerrado.
