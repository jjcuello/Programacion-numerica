# Checklist tecnico de revision de contratos (v0.2)

Fecha de uso: semana de Diseno
Estado sugerido: [ ] Pendiente, [~] En revision, [x] Cumplido, [!] Hallazgo

## A) ProblemDefinition

| Item | Estado | Observaciones |
| --- | --- | --- |
| El campo kind usa valores del enum ProblemKind | [ ] | |
| expression y expressions no generan ambiguedad de uso | [ ] | |
| interval y initial_guess cubren biseccion y Newton | [ ] | |
| tolerance y max_iterations tienen defaults coherentes | [ ] | |
| to_dict serializa tipos sin perder informacion relevante | [ ] | |
| metadata conserva contexto de ejecucion sin acoplar UI | [ ] | |

## B) IterationRecord

| Item | Estado | Observaciones |
| --- | --- | --- |
| iteration siempre se registra en orden creciente | [ ] | |
| estimate soporta escalar y sistema cuando aplique | [ ] | |
| residual se usa con criterio consistente por metodo | [ ] | |
| absolute_error y relative_error no se contradicen | [ ] | |
| delta representa cambio iterativo con definicion clara | [ ] | |
| metadata incluye solo datos de valor tecnico | [ ] | |

## C) MethodResult

| Item | Estado | Observaciones |
| --- | --- | --- |
| status usa ExecutionStatus sin valores ad hoc | [ ] | |
| converged refleja correctamente status SUCCESS | [ ] | |
| iteration_count coincide con records cuando aplica | [ ] | |
| elapsed_seconds se registra en segundos | [ ] | |
| message describe causa de exito/fallo con claridad | [ ] | |
| metadata permite trazabilidad sin duplicaciones | [ ] | |

## D) Interfaz NumericalMethod

| Item | Estado | Observaciones |
| --- | --- | --- |
| name identifica de forma estable el metodo | [ ] | |
| supports filtra tipo de problema antes de solve | [ ] | |
| solve nunca depende de input() ni print() | [ ] | |
| solve devuelve siempre MethodResult | [ ] | |
| Errores de soporte se reflejan con status adecuado | [ ] | |

## E) Pruebas y consistencia

| Item | Estado | Observaciones |
| --- | --- | --- |
| tests/test_v0_2_contracts.py pasa completo | [ ] | |
| Casos de exito y falla cubiertos en metodos piloto | [ ] | |
| Comparator marca UNSUPPORTED correctamente | [ ] | |
| Campos serializados se validan en pruebas | [ ] | |
| No hay regresiones de API entre modulos v0.2 | [ ] | |

## F) Decisiones de revision

- Hallazgos criticos:
- Hallazgos no criticos:
- Decisiones aprobadas:
- Acciones para semana siguiente:

## G) Aprobacion tecnica

- Responsable 1: ____________________
- Responsable 2: ____________________
- Fecha: ____________________
- Estado final: [ ] Aprobado [ ] Aprobado con acciones [ ] Rechazado
