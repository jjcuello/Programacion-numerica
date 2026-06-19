# Matriz de analisis de respuestas docentes

Fecha de emision: 2026-06-09
Fase: 02_Analisis
Proposito: consolidar entrevistas, detectar patrones y convertir hallazgos en backlog priorizado.

## 1. Consolidador por entrevista

| Codigo | Materia | Dolor principal | Evidencia que falta hoy | Prioridad para piloto | Barrera principal | Decision |
| --- | --- | --- | --- | --- | --- | --- |
| ENT-001 | Matematicas | Debilidad en comprension de analisis numerico e interpretacion de problemas | Evidencia de razonamiento, analisis escrito y resumen por estudiante | Reportes individuales/grupales con filtros + apoyo a correccion de examenes | Requiere carga simple y vista clara para uso real en clase | Inmediata |
| ENT-002 | Arquitectura | Los estudiantes entienden resultados, pero no procesos | Seguimiento del rendimiento, uso de la plataforma y progreso del equipo | Seguimiento docente + interfaz intuitiva + orientacion de uso | Riesgo de mala adopcion si la herramienta no es intuitiva o si la IA redacta por el estudiante | Corto plazo |
| ENT-003 | Matematicas | Errores en convergencia, algebra y comprension de margen de error | Trazabilidad paso a paso, metricas de uso y evidencia del avance del alumno | Soluciones paso a paso + alertas de convergencia + reportes de seguimiento | Necesita arquitectura abierta, estabilidad y confianza en los resultados | Inmediata |

Nota de uso:
- Registrar una sola idea por celda.
- Sintetizar cada entrevista en 5 hallazgos clave, no en notas extensas.
- Escribir la prioridad para piloto como capacidad concreta, no como categoria general.

Escala de decision sugerida:
- Inmediata (>= 4.0)
- Corto plazo (3.0 a 3.9)
- Diferido (< 3.0)

## 2. Frecuencia de problemas detectados

| Problema detectado | Frecuencia (n) | Impacto percibido (Alto/Medio/Bajo) | Evidencia breve |
| --- | --- | --- | --- |
| Falta de trazabilidad por estudiante | 3 | Alto | Se pide seguimiento por estudiante, evidencia del proceso, tiempo de uso y progreso del equipo. |
| Dificultad para comparar metodos en clase | 2 | Medio | Se valora mostrar procedimientos, soluciones paso a paso y apoyo visual para explicar el metodo. |
| Escasez de reportes para evaluacion | 2 | Alto | Se solicitan resumentes, reportes individuales/grupales y evidencia para revisar examenes. |
| Dificultad para explicar convergencia/error | 2 | Alto | Aparecen problemas de convergencia, margen de error, algebra y comprension del proceso numerico. |
| Exceso de tiempo en tareas manuales | 2 | Medio | Se menciona correccion de examenes, revision de trabajos y necesidad de automatizacion docente. |

Nota de uso:
- Consolidar solo problemas repetidos en 2 o mas entrevistas.
- Si un problema aparece una sola vez pero es critico, moverlo a riesgos o backlog, no inflar esta tabla.

## 3. Relacion problema -> funcionalidad -> modulo tecnico

| Problema docente | Evidencia faltante asociada | Funcionalidad propuesta | Modulo tecnico impactado | Prioridad |
| --- | --- | --- | --- | --- |
| Falta de comparacion clara de metodos | El docente necesita mostrar procedimiento, razonamiento y resultados en una sola secuencia | Comparador de metodos con vista paso a paso | src/analysis | Should |
| Falta de evidencia de proceso | No existe registro claro de iteraciones, uso y avance por estudiante | Historial de sesiones y seguimiento por estudiante | src/infrastructure/storage | Must |
| Dificultad para evaluacion docente | No hay salida util para revisar examenes o consolidar resultados por grupo | Reporte exportable CSV/JSON + resumen docente | src/infrastructure/exporters | Must |
| Errores de parametrizacion no detectados | El estudiante falla sin entender por que diverge, oscila o acumula error | Alertas de convergencia y validacion de parametros | src/methods + src/core | Must |
| Necesidad de apoyo visual | La explicacion pierde claridad sin apoyo grafico inmediato y sin control didactico | Graficas 2D/3D con lectura pedagogica | metodos + futura web | Should |

## 4. Priorizacion MoSCoW resultante

### Must
- Historial de sesiones y seguimiento por estudiante.
- Reportes exportables y resumen docente para evaluacion.
- Alertas de convergencia, oscilacion y parametros invalidos.

### Should
- Comparador de metodos con salida paso a paso.
- Graficas 2D/3D faciles de leer para apoyar la explicacion en clase.

### Could
- Deteccion de plagio o similitud entre respuestas.
- Recomendaciones didacticas y desbloqueo secuencial de herramientas.

### Won't (por ahora)
- Integraciones institucionales avanzadas.
- Automatizacion total de redaccion o resolucion por IA.

## 5. Criterios de aceptacion preliminares

| Item priorizado | Criterio de aceptacion funcional | Evidencia de validacion |
| --- | --- | --- |
| Comparador de metodos | Permite ejecutar al menos 2 metodos sobre el mismo problema y mostrar procedimiento, resultado y diferencias en una sola vista | Demo con un ejercicio comun de clase y comparacion visible para el docente |
| Historial de sesiones | Guarda y recupera ejecuciones con fecha, metodo, parametros, resultado y estudiante asociado | Consulta de sesiones previas en prueba corta con al menos 3 registros |
| Exportacion CSV/JSON | Genera archivo legible con datos suficientes para revision docente individual y grupal | Exportacion abierta en hoja de calculo o lector JSON sin perdida de campos clave |
| Alertas de convergencia | Notifica divergia, oscilacion, parametros invalidos o falta de convergencia con mensaje comprensible | Caso de prueba con entrada invalida y otro caso con convergencia correcta |

Regla de uso:
- Mantener solo criterios validables en una demo o prueba corta.
- Si un criterio no puede mostrarse o verificarse rapido, reescribirlo.

## 6. Riesgos de adopcion y mitigacion

| Riesgo | Probabilidad | Impacto | Mitigacion | Responsable |
| --- | --- | --- | --- | --- |
| Resistencia docente por curva de aprendizaje | Media | Alta | Capacitacion breve, guia practica y flujo inicial intuitivo | Equipo de producto |
| Limitaciones de infraestructura en laboratorio | Media | Media | Version ligera, soporte offline parcial y pruebas en equipos reales | Equipo tecnico |
| Desconfianza en resultados numericos | Alta | Alta | Casos de validacion, trazabilidad de calculo y soluciones paso a paso | Equipo tecnico y docente validador |

Nota de control:
- No abrir mas de 3 riesgos principales en esta fase.
- Si aparece un riesgo nuevo, reemplazar uno menor en vez de expandir la tabla.

## 7. Decision de salida de Analisis_02

- Estado de cierre: Pendiente
- Fecha de cierre: 19 / 06 / 2026
- Condiciones para pasar a Diseno (03):
  1. Validar esta matriz con al menos un docente adicional o con el docente responsable de la catedra.
  2. Convertir los items Must en backlog tecnico con criterio de aceptacion y modulo responsable.
  3. Confirmar el alcance del piloto y las restricciones operativas de uso en clase.

Aprobado por:
- Responsable tecnico: Pendiente
- Responsable pedagogico: Pendiente
- Coordinacion academica: Pendiente
