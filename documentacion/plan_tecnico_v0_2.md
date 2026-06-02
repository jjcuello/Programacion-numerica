# Plan Tecnico v0.2

Este documento traduce la vision de v0.2 a entregables tecnicos concretos para una migracion progresiva desde la aplicacion actual basada en consola.

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