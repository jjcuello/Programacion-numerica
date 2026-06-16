# Propuesta de entrevistas a docentes de matematicas y ajuste de producto

Fecha de emision: 2026-06-09
Fase: 02_Analisis
Proposito: validar, desde la optica docente, que tan util es la plataforma para clase real y traducir hallazgos en decisiones concretas de desarrollo.

## 1. Enfoque recomendado para esta fase

La entrevista no debe quedarse en opiniones generales. Debe producir evidencia util para priorizar backlog.

Resultados esperados por entrevista:
- Problemas docentes concretos (situacion actual).
- Impacto pedagogico esperado (que debe mejorar en aprendizaje).
- Condiciones operativas reales (tiempo, infraestructura, tipo de clases).
- Nivel de ajuste del proyecto actual frente a esas necesidades.
- Recomendaciones priorizadas convertibles a tareas de desarrollo.

## 2. Perfil de muestra y alcance minimo

Muestra sugerida:
- 6 a 10 docentes de matematicas.
- Incluir al menos:
  - 2 de calculo diferencial/integral.
  - 2 de algebra lineal/metodos numericos.
  - 1 de estadistica (si aplica al pensum).
  - 1 coordinador o jefe de catedra.

Criterios de cobertura:
- Distintos semestres.
- Distinto dominio tecnologico (alto, medio, bajo).
- Distinta modalidad de clase (teorica, practica, laboratorio).

## 3. Guion de entrevista propuesto (version simplificada y directa)

Duracion sugerida: 20 a 25 minutos.
Formato: entrevista semiestructurada, con foco en decisiones de producto y no en contexto general.

Principios de uso:
- Evitar preguntas de contexto que no cambien una decision.
- Priorizar dolores, evidencias, adopcion y funcionalidades minimas.
- Profundizar solo cuando la respuesta abra una necesidad concreta.

### Bloque A: Problema docente actual (4 preguntas)

1. Cual es hoy la mayor dificultad para ensenar metodos numericos en clase?
2. Que errores o confusiones se repiten mas en los estudiantes?
3. Que informacion o evidencia le falta para saber si el estudiante realmente entendio?
4. Que parte de su trabajo docente le consume tiempo y aporta poco valor?

### Bloque B: Validacion de la solucion (5 preguntas)

5. Le aportaria valor una herramienta que muestre iteraciones paso a paso y compare metodos? Por que?
6. Que salida le resulta mas util para clase: tabla, grafica, comparacion o reporte? Cual no le aporta?
7. Si la herramienta existiera hoy, en que momento de la clase la usaria primero?
8. Que alertas o recomendaciones automaticas si le ayudarian de verdad?
9. Cual es la funcionalidad minima que deberia existir para que valga la pena probarla?

### Bloque C: Adopcion y prioridad (3 preguntas)

10. Cual es la principal barrera para adoptarla en su catedra?
11. Que condiciones minimas deben cumplirse para usarla en clase con confianza?
12. Si solo pudieramos construir 3 capacidades para un piloto, cuales elegiria primero?

Resultados esperados del guion:
- 1 dolor principal claro.
- 1 evidencia que hoy falta.
- 1 escenario de uso inmediato.
- 3 prioridades para piloto.
- 1 barrera de adopcion a mitigar.

## 4. Instrumento de medicion cuantitativa

Al cierre de cada entrevista, puntuar cada capacidad de 1 a 5 en:
- Utilidad pedagogica.
- Frecuencia de uso esperada.
- Factibilidad operativa.
- Urgencia academica.

Formula sugerida de prioridad:
Prioridad = (0.4 * Utilidad) + (0.25 * Frecuencia) + (0.2 * Urgencia) + (0.15 * Factibilidad)

Escala de decision:
- >= 4.0: entra a fase inmediata.
- 3.0 a 3.9: backlog de corto plazo.
- < 3.0: diferido o redisenado.

## 5. Criterios de conduccion

- Iniciar directo por el problema principal, no por datos de contexto amplios.
- Si una respuesta ya cubre otra pregunta, no repetirla.
- Pedir ejemplos concretos de clase en lugar de opiniones generales.
- Cerrar siempre con una priorizacion corta y forzada.
- Si el tiempo cae, conservar solo las preguntas 1, 3, 5, 9, 10 y 12.

## 6. Entregables de Analisis_02

1. Matriz de hallazgos por docente (dolor, evidencia, impacto).
2. Mapa de problemas recurrentes (top 10) con frecuencia.
3. Matriz problema -> funcionalidad -> modulo tecnico.
4. Priorizacion MoSCoW de funcionalidades para siguiente fase.
5. Criterios de aceptacion funcional por cada item priorizado.
6. Riesgos de adopcion y plan de mitigacion.

## 7. Traduccion a desarrollo

Must (MVP docente):
- Comparador de metodos con salida estandarizada.
- Historial de ejecuciones por sesion.
- Exportacion CSV/JSON.
- Alertas de convergencia y parametros invalidos.

Should:
- Vista docente resumida por tema/metodo.
- Reporte academico con tabla de iteraciones y conclusiones.

Could:
- Recomendador didactico inicial por tipo de problema.
- Banco de preguntas ligado a errores comunes.

Won't (por ahora):
- Dashboard institucional avanzado.
- Integraciones externas complejas.

## 8. Plan de ejecucion resumido

Semana 1:
- Ejecutar entrevistas (6 a 10).
- Consolidar notas con formato unico.
- Generar ranking de necesidades.

Semana 2:
- Taller interno desarrollo + docentes (60 a 90 min).
- Validar ranking y criterios de aceptacion.
- Cerrar backlog de entrada a la siguiente fase.

## 9. Cierre

Para este proyecto, la entrevista debe orientarse a una pregunta central:
"Que necesita el docente para ensenar mejor metodos numericos con evidencia, en menos tiempo y con mayor claridad para el estudiante?"

La propuesta anterior permite responder esa pregunta con datos accionables, no solo percepciones.
Con ello, la fase 02_Analisis queda conectada directamente con decisiones de arquitectura, casos de uso y prioridades reales del producto.

## 10. Artefactos asociados

- Plantilla de levantamiento en campo: `documentacion/02_Analisis/plantilla_operativa_entrevista_docentes.md`
- Matriz para consolidacion y priorizacion: `documentacion/02_Analisis/matriz_analisis_respuestas_docentes.md`
