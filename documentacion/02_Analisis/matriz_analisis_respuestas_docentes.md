# Matriz de analisis de respuestas docentes

Fecha de emision: 2026-06-09
Fase: 02_Analisis
Proposito: consolidar entrevistas, detectar patrones y convertir hallazgos en backlog priorizado.

## 1. Consolidador por entrevista

| Codigo | Materia | Dolor principal | Evidencia que falta hoy | Prioridad para piloto | Barrera principal | Decision |
| --- | --- | --- | --- | --- | --- | --- |
| ENT-001 |  |  |  |  |  |  |
| ENT-002 |  |  |  |  |  |  |
| ENT-003 |  |  |  |  |  |  |
| ENT-004 |  |  |  |  |  |  |
| ENT-005 |  |  |  |  |  |  |
| ENT-006 |  |  |  |  |  |  |

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
| Falta de trazabilidad por estudiante |  |  |  |
| Dificultad para comparar metodos en clase |  |  |  |
| Escasez de reportes para evaluacion |  |  |  |
| Dificultad para explicar convergencia/error |  |  |  |
| Exceso de tiempo en tareas manuales |  |  |  |

Nota de uso:
- Consolidar solo problemas repetidos en 2 o mas entrevistas.
- Si un problema aparece una sola vez pero es critico, moverlo a riesgos o backlog, no inflar esta tabla.

## 3. Relacion problema -> funcionalidad -> modulo tecnico

| Problema docente | Evidencia faltante asociada | Funcionalidad propuesta | Modulo tecnico impactado | Prioridad |
| --- | --- | --- | --- | --- |
| Falta de comparacion clara de metodos | El docente no puede contrastar procedimiento y resultado en una sola vista | Comparador de metodos | src/analysis |  |
| Falta de evidencia de proceso | No existe registro claro de iteraciones por estudiante | Historial de sesiones | src/infrastructure/storage |  |
| Dificultad para evaluacion docente | No hay salida util para revisar o exportar resultados | Reporte exportable CSV/JSON | src/infrastructure/exporters |  |
| Errores de parametrizacion no detectados | El estudiante falla sin entender por que diverge o no converge | Alertas de convergencia | src/methods + src/core |  |
| Necesidad de apoyo visual | La explicacion pierde claridad sin apoyo grafico inmediato | Graficas 2D/3D | metodos + futura web |  |

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

Regla de uso:
- Mantener solo criterios validables en una demo o prueba corta.
- Si un criterio no puede mostrarse o verificarse rapido, reescribirlo.

## 6. Riesgos de adopcion y mitigacion

| Riesgo | Probabilidad | Impacto | Mitigacion | Responsable |
| --- | --- | --- | --- | --- |
| Resistencia docente por curva de aprendizaje |  |  | Capacitacion breve + guia practica |  |
| Limitaciones de infraestructura en laboratorio |  |  | Version ligera y pruebas en equipos reales |  |
| Desconfianza en resultados numericos |  |  | Casos de validacion y trazabilidad de calculo |  |

Nota de control:
- No abrir mas de 3 riesgos principales en esta fase.
- Si aparece un riesgo nuevo, reemplazar uno menor en vez de expandir la tabla.

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
