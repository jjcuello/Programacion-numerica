# Propuesta de entrevistas a docentes de matematicas y ajuste de producto

Fecha: 2026-06-09
Fase: 02_Analisis
Objetivo: validar, desde la optica de quienes ensenan, que tan util es la plataforma para clase real y traducir hallazgos en decisiones concretas de desarrollo.

## 1. Enfoque recomendado para esta fase

La entrevista no debe quedarse en opiniones generales. Debe producir evidencia util para priorizar backlog.

Resultado esperado de cada entrevista:
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

Criterio de cobertura:
- Distintos semestres.
- Distinto dominio tecnologico (alto, medio, bajo).
- Distinta modalidad de clase (teorica, practica, laboratorio).

## 3. Guion de entrevista propuesto (version orientada a desarrollo)

Duracion sugerida: 35 a 50 minutos.
Formato: semiestructurada (preguntas base + profundizacion).

### Bloque A: Contexto de docencia (5 preguntas)

1. Que materias y que temas numericos imparte actualmente?
2. En que momentos del curso se le dificulta mas explicar convergencia, error y comportamiento iterativo?
3. Que herramientas usa hoy (pizarra, Excel, calculadora, software, scripts)?
4. Cuanto tiempo de clase dedica a demostracion vs practica guiada?
5. Cuales son los 3 errores mas repetidos de los estudiantes en metodos numericos?

### Bloque B: Problema real y dolor docente (6 preguntas)

6. Que parte del proceso de ensenanza le consume mas tiempo y no agrega valor directo?
7. Donde pierde trazabilidad del avance del estudiante?
8. En que casos no logra comparar metodos de forma clara en clase?
9. Que evidencia le cuesta recoger para evaluar (iteraciones, errores, procedimiento)?
10. Que tipo de salida considera inutil o confusa para estudiantes?
11. Si pudiera eliminar una friccion hoy, cual seria?

### Bloque C: Validacion del producto actual (10 preguntas)

12. Que valor ve en una herramienta que muestre iteraciones paso a paso?
13. Que tan importante es visualizar residual, error absoluto y error relativo en clase?
14. Le resultaria util comparar dos o mas metodos sobre el mismo problema en una sola vista?
15. Que nivel de detalle necesita en reportes (resumen, tabla completa, ambos)?
16. Prefiere comenzar con una CLI robusta o considera indispensable una interfaz web desde ya?
17. Cuales vistas docentes deberian existir primero (seguimiento por curso, por tema, por estudiante)?
18. Que alertas pedagogicas le gustaria ver (divergencia, oscilacion, mala parametrizacion)?
19. Que recomendaciones automaticas considera realmente utiles y cuales evitaria?
20. Que formato de exportacion necesita para trabajo academico (PDF, CSV, JSON)?
21. Con que frecuencia usaria esta herramienta durante el semestre?

### Bloque D: Criterios de adopcion institucional (6 preguntas)

22. Que condiciones minimas de uso debe cumplir para adoptarla en su catedra?
23. Que tan importante es que funcione en laboratorio con recursos limitados?
24. Que barreras de adopcion anticipa en docentes o estudiantes?
25. Que evidencias pediria para confiar en los resultados numericos?
26. Que capacitacion minima requeriria para su equipo docente?
27. Que riesgos academicos o eticos ve en el uso de una herramienta asi?

### Bloque E: Priorizacion forzada (4 preguntas)

Pedir al docente elegir Top 5 de valor inmediato:
- Comparador de metodos.
- Historial de sesiones.
- Reportes exportables.
- Visualizacion 2D/3D.
- Alertas de convergencia.
- Recomendador didactico.
- Banco de ejercicios.
- Dashboard docente.

28. Cuales 5 funcionalidades aportan mayor impacto en aprendizaje?
29. Cuales 2 dejaria para una fase posterior?
30. Que funcionalidad considera critica para piloto institucional?
31. Con que indicador mediria exito en 8 semanas?

## 4. Instrumento de medicion cuantitativa (para decidir backlog)

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

## 5. Entregables concretos de Analisis_02

1. Matriz de hallazgos por docente (dolor, evidencia, impacto).
2. Mapa de problemas recurrentes (top 10) con frecuencia.
3. Matriz problema -> funcionalidad -> modulo tecnico.
4. Priorizacion MoSCoW de funcionalidades para siguiente fase.
5. Criterios de aceptacion funcional por cada item priorizado.
6. Riesgos de adopcion y plan de mitigacion.

## 6. Traduccion directa a desarrollo (propuesta de backlog inicial)

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

## 7. Plan de ejecucion rapido (2 semanas)

Semana 1:
- Ejecutar entrevistas (6 a 10).
- Consolidar notas con formato unico.
- Generar ranking de necesidades.

Semana 2:
- Taller interno desarrollo + docentes (60 a 90 min).
- Validar ranking y criterios de aceptacion.
- Cerrar backlog de entrada a la siguiente fase.

## 8. Recomendacion final

Para este proyecto, la entrevista debe orientarse a una pregunta central:
"Que necesita el docente para ensenar mejor metodos numericos con evidencia, en menos tiempo y con mayor claridad para el estudiante?"

La propuesta anterior permite responder esa pregunta con datos accionables, no solo percepciones.
Con esto, la fase 02_Analisis quedaria conectada directamente con decisiones de arquitectura, casos de uso y prioridades reales del producto.

## 9. Artefactos operativos creados

- Plantilla de levantamiento en campo: `documentacion/02_Analisis/plantilla_operativa_entrevista_docentes.md`
- Matriz para consolidacion y priorizacion: `documentacion/02_Analisis/matriz_analisis_respuestas_docentes.md`
