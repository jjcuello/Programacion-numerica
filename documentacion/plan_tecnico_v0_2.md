# Plan Tecnico v0.2

Este documento traduce la vision de v0.2 a entregables tecnicos concretos para una migracion progresiva desde la aplicacion actual basada en consola.

## Base estrategica del documento

Este plan tecnico no debe leerse como una lista aislada de archivos o tareas. Su funcion es conectar la vision academica del proyecto con decisiones de arquitectura, desarrollo, validacion y evolucion.

La idea central es esta:

- el proyecto debe crecer como plataforma didactica de metodos numericos,
- no como una suma desordenada de scripts,
- y cada fase tecnica debe sostener ese objetivo.

## Arbol de trabajo del proyecto

El trabajo del proyecto puede organizarse en ocho frentes complementarios.

1. Planificar
2. Analizar
3. Disenar
4. Desarrollar
5. Probar
6. Implementar
7. Mantener
8. Documentar

En este documento se desarrolla con mas profundidad la capa tecnica de los dos primeros frentes, porque son los que condicionan el resto del proyecto.

## 1. Planificar

Planificar significa decidir con rigor que tipo de sistema queremos construir, que valor debe aportar y cual es la ruta prioritaria de crecimiento.

### 1.1 Objetivo de planificacion

- Definir por que el proyecto debe escalar.
- Determinar a quien beneficia el escalado.
- Seleccionar la ruta principal de evolucion.
- Delimitar alcance y restricciones.
- Ordenar hitos antes de nuevas expansiones funcionales.

### 1.2 Utilidad esperada del escalado

#### Para estudiantes

- Reducir friccion de uso.
- Mejorar la comprension de convergencia, error y comportamiento iterativo.
- Permitir una futura experiencia visual mas accesible que la consola tradicional.

#### Para profesores

- Facilitar demostraciones en clase.
- Generar comparaciones claras entre metodos.
- Habilitar exportacion futura de tablas, resultados y reportes.

#### Para el equipo del proyecto

- Disminuir el costo de agregar nuevos metodos.
- Reutilizar el nucleo en CLI, web y reportes.
- Facilitar mantenimiento, pruebas y trazabilidad.

### 1.3 Ruta principal recomendada

La ruta principal del proyecto es:

- Nucleo desacoplado + comparador de metodos + persistencia de experimentos + reportes + futura interfaz web educativa.

Esta combinacion es la mas coherente con el valor didactico y con el potencial de tesis del proyecto.

### 1.4 Limites de planificacion

- No competir con herramientas cientificas industriales en rendimiento bruto.
- No priorizar complejidad tecnica por encima de accesibilidad academica.
- No incorporar modulos nuevos sin contratos y arquitectura comun.
- No saltar a interfaz web sin estabilizar nucleo, pruebas y persistencia.

### 1.5 Hitos estrategicos

1. Desacoplar logica matematica de la interfaz actual.
2. Migrar metodos principales al nuevo nucleo.
3. Consolidar comparacion, trazabilidad y sesiones.
4. Incorporar reportes exportables.
5. Integrar algebra lineal como siguiente bloque academico fuerte.
6. Construir interfaz web educativa.
7. Validar uso real en contexto academico.

## 2. Analizar

Analizar significa estudiar el proyecto tal como existe hoy para identificar fortalezas, debilidades, necesidades del usuario y condiciones reales de evolucion.

### 2.1 Objetivo del analisis

- Entender que utilidad real ofrece hoy el sistema.
- Detectar cuellos de botella para escalar.
- Reconocer necesidades de estudiantes y profesores.
- Traducir esas necesidades en requisitos tecnicos y funcionales.

### 2.2 Analisis del estado actual

El proyecto actual ofrece valor academico inmediato en estas areas:

- Metodos de raices para ecuaciones no lineales.
- Comparacion didactica entre metodos iterativos.
- Analisis de $e$ y $\pi$ desde enfoque numerico.
- Evaluacion segura con evasion de singularidades.
- Visualizacion 2D, 3D y animaciones.

Fortalezas detectadas:

- El proyecto ya tiene identidad didactica.
- La salida por iteraciones favorece comprension del proceso.
- Existen modulos con base util para refactorizar en vez de reescribir todo.
- El sistema ya permite argumentar valor academico y potencial de tesis.

Debilidades detectadas:

- Acoplamiento fuerte entre logica matematica e interfaz de consola.
- Salidas poco estandarizadas entre modulos.
- Ausencia de una capa comun de resultados, sesiones y metricas en la version original.
- Cobertura automatizada aun parcial respecto a todos los modulos existentes.
- La experiencia para usuario final sigue centrada en terminal.

### 2.3 Analisis por tipo de usuario

#### Estudiante

Necesidades principales:

- Entender mas que ejecutar.
- Ver tablas, errores y convergencia de forma clara.
- Tener menos friccion tecnica de entrada.
- Poder repetir experimentos y comparar resultados.

#### Profesor

Necesidades principales:

- Mostrar metodos en clase con apoyo visual.
- Contrastar algoritmos de forma rapida.
- Reutilizar ejemplos y resultados.
- Exportar evidencia didactica para evaluaciones, guias o presentaciones.

#### Equipo desarrollador

Necesidades principales:

- Arquitectura desacoplada.
- Contratos comunes para nuevos metodos.
- Persistencia y pruebas automatizadas.
- Evolucion ordenada hacia interfaz web y modulos adicionales.

### 2.4 Requisitos derivados del analisis

Del analisis del estado actual se desprenden estos requisitos prioritarios.

#### Requisitos funcionales

- Resolver problemas con metodos numericos usando una API comun.
- Comparar varios metodos sobre un mismo problema.
- Registrar iteraciones, tiempos, errores y metadatos.
- Guardar sesiones de ejecucion.
- Exportar resultados en formatos reutilizables.
- Presentar resultados en CLI y, a futuro, en interfaz web.

#### Requisitos no funcionales

- Modularidad.
- Reutilizacion.
- Testabilidad.
- Trazabilidad.
- Claridad pedagogica.
- Portabilidad entre entornos de desarrollo y ejecucion.

### 2.5 Riesgos detectados en el analisis

- Creer que agregar mas metodos equivale automaticamente a mejorar el proyecto.
- Construir interfaz nueva sobre una base no desacoplada.
- Perder consistencia entre modulos al migrar solo parcialmente.
- Documentar vision academica sin traducirla a contratos y casos de uso reales.
- No medir luego el impacto del sistema en aprendizaje.

### 2.6 Decisiones tecnicas justificadas por el analisis

El analisis sostiene estas decisiones tecnicas:

- Crear un nucleo comun de problemas, iteraciones y resultados.
- Implementar comparador de metodos como pieza central, no accesoria.
- Incorporar persistencia de sesiones desde etapas tempranas.
- Mantener la CLI como interfaz base de ingenieria.
- Reservar la interfaz web como siguiente salto de producto academico.

## Objetivo

Separar la logica numerica de la interfaz para que el proyecto pueda evolucionar hacia una plataforma reutilizable, medible y extensible para uso academico.

## Entregables por fase

### Fase 1. Nucleo y contratos comunes

Objetivo:

- Crear un lenguaje comun para describir problemas, iteraciones y resultados.

Archivos base:

- `src/core/models/problem.py`
- `src/core/results/iteration.py`
- `src/core/results/method_result.py`
- `src/methods/base.py`

Resultado esperado:

- Todos los metodos nuevos y refactorizados deben recibir un `ProblemDefinition` y devolver un `MethodResult`.

### Fase 2. Adaptacion de metodos existentes

Objetivo:

- Extraer la logica de `metodos/` y convertirla en componentes reutilizables.

Migraciones iniciales sugeridas:

- `metodos/biseccion.py` -> `src/methods/roots/bisection_method.py`
- `metodos/secante.py` -> `src/methods/roots/secant_method.py`
- `metodos/newton_raphson.py` -> `src/methods/roots/newton_method.py`
- `metodos/punto_fijo.py` -> `src/methods/roots/fixed_point_method.py`
- `metodos/evasion_singularidad.py` -> `src/methods/safe_eval/safe_evaluator.py`

Resultado esperado:

- La CLI actual podra seguir existiendo, pero actuando como adaptador sobre el nuevo nucleo.

### Fase 3. Comparacion, trazabilidad y reportes

Objetivo:

- Convertir ejecuciones sueltas en experimentos comparables.

Archivos sugeridos:

- `src/analysis/benchmarking/comparator.py`
- `src/analysis/convergence/metrics.py`
- `src/infrastructure/storage/session_repository.py`
- `src/infrastructure/exporters/json_exporter.py`

Resultado esperado:

- Comparar varios metodos sobre el mismo problema y persistir resultados.

### Fase 4. Capa didactica

Objetivo:

- Agregar explicacion, recomendacion y seguimiento pedagogico.

Archivos sugeridos:

- `src/tutoring/recommendations/rule_based_recommender.py`
- `src/tutoring/explanations/convergence_feedback.py`
- `src/tutoring/quizzes/question_bank.py`

Resultado esperado:

- La plataforma debe explicar por que un metodo fue adecuado o inadecuado.

### Fase 5. Interfaces y producto academico

Objetivo:

- Llevar el sistema a una experiencia mas fuerte que la consola tradicional.

Archivos sugeridos:

- `src/interfaces/cli/app.py`
- `src/interfaces/web/app.py`
- `src/app/use_cases/solve_problem.py`
- `src/app/use_cases/compare_methods.py`

Resultado esperado:

- CLI estable, interfaz web experimental y reportes exportables.

## Criterios de calidad para v0.2

- Cada metodo debe ser testeable sin `input()` ni `print()`.
- Cada ejecucion debe exponer historial de iteraciones y metadatos.
- Las comparaciones deben ser reproducibles con la misma entrada.
- La capa de interfaz no debe contener la logica matematica principal.
- La documentacion debe enlazar teoria, implementacion y salida esperada.

## Orden recomendado de implementacion

1. Contratos base.
2. Biseccion y Newton-Raphson como casos piloto.
3. Comparador de metodos.
4. Persistencia de sesiones.
5. Recomendador didactico.
6. Nueva CLI.
7. Interfaz web.