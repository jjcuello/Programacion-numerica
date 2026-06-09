# Matriz de analisis de respuestas docentes

Fecha de emision: 2026-06-09
Fase: 02_Analisis
Objetivo: consolidar entrevistas, detectar patrones y convertir hallazgos en backlog priorizado.

## 1. Consolidador por entrevista

| Codigo | Materia | Semestre | Dolor principal | Funcionalidad clave sugerida | Barrera de adopcion | Prioridad calculada | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ENT-001 |  |  |  |  |  |  |  |
| ENT-002 |  |  |  |  |  |  |  |
| ENT-003 |  |  |  |  |  |  |  |
| ENT-004 |  |  |  |  |  |  |  |
| ENT-005 |  |  |  |  |  |  |  |
| ENT-006 |  |  |  |  |  |  |  |

Decision sugerida:
- Inmediata (>= 4.0)
- Corto plazo (3.0 a 3.9)
- Diferido (< 3.0)

## 2. Frecuencia de problemas docentes detectados

| Problema detectado | Frecuencia (n) | Impacto percibido (Alto/Medio/Bajo) | Evidencia breve |
| --- | --- | --- | --- |
| Falta de trazabilidad por estudiante |  |  |  |
| Dificultad para comparar metodos en clase |  |  |  |
| Escasez de reportes para evaluacion |  |  |  |
| Dificultad para explicar convergencia/error |  |  |  |
| Exceso de tiempo en tareas manuales |  |  |  |

## 3. Matriz problema -> funcionalidad -> modulo tecnico

| Problema docente | Funcionalidad propuesta | Modulo tecnico impactado | Esfuerzo estimado (Bajo/Medio/Alto) | Prioridad |
| --- | --- | --- | --- | --- |
| Falta de comparacion clara de metodos | Comparador de metodos | src/analysis |  |  |
| Falta de evidencia de proceso | Historial de sesiones | src/infrastructure/storage |  |  |
| Dificultad para evaluacion docente | Reporte exportable CSV/JSON | src/infrastructure/exporters |  |  |
| Errores de parametrizacion no detectados | Alertas de convergencia | src/methods + src/core |  |  |
| Necesidad de apoyo visual | Graficas 2D/3D | metodos + futura web |  |  |

## 4. Priorizacion MoSCoW resultante

### Must
- 
- 
- 

### Should
- 
- 

### Could
- 
- 

### Won't (por ahora)
- 
- 

## 5. Criterios de aceptacion preliminares

| Item priorizado | Criterio de aceptacion funcional | Evidencia de validacion |
| --- | --- | --- |
| Comparador de metodos | Permite ejecutar al menos 2 metodos sobre el mismo problema y mostrar tabla comparativa |  |
| Historial de sesiones | Guarda y recupera ejecuciones con fecha, metodo y resultado |  |
| Exportacion CSV/JSON | Genera archivo legible por herramientas externas |  |
| Alertas de convergencia | Notifica divergia/oscilacion/parametros invalidos |  |

## 6. Riesgos de adopcion y mitigacion

| Riesgo | Probabilidad | Impacto | Mitigacion | Responsable |
| --- | --- | --- | --- | --- |
| Resistencia docente por curva de aprendizaje |  |  | Capacitacion breve + guia practica |  |
| Limitaciones de infraestructura en laboratorio |  |  | Version ligera y pruebas en equipos reales |  |
| Desconfianza en resultados numericos |  |  | Casos de validacion y trazabilidad de calculo |  |

## 7. Decision de salida de Analisis_02

- Estado de cierre: Pendiente / Aprobado
- Fecha de cierre: ____ / ____ / ______
- Condiciones para pasar a Diseno (03):
  1. ______________________________
  2. ______________________________
  3. ______________________________

Aprobado por:
- Responsable tecnico: ______________________________
- Responsable pedagogico: ______________________________
- Coordinacion academica: ______________________________
