# Informe de revision tecnica

Fecha: 2026-06-14  
Autor de revision: Equipo de integracion  
Rama revisada: origin/Leonardo_cambios  
Commit revisado: 789d97d  
Repositorio base: origin/main

## 1) Resumen ejecutivo
La rama aporta una reestructuracion de carpetas (backend, frontend, legacy) sin cambios de logica en metodos numericos. Sin embargo, en su estado actual no esta lista para merge a main porque rompe el flujo de pruebas desde la raiz del repositorio y deja documentacion operativa desactualizada.

Estado recomendado: **No aprobar aun**.

## 2) Alcance de la revision
Se valido:
- Historial y diff contra main.
- Estado de cambios funcionales vs movimientos de archivos.
- Ejecucion de pruebas automatizadas en dos contextos (raiz y backend).
- Consistencia operativa de documentacion/comandos.

## 3) Hallazgos y evidencia

### Hallazgo A (Critico): Pruebas fallan desde la raiz del repositorio
Descripcion:
- En la rama reestructurada, los tests importan modulos con prefijo `src`, pero el codigo ahora vive en `backend/src`.
- Resultado: error de importacion al correr pruebas desde la raiz.

Evidencia observada:
- En main: `10 passed`.
- En origin/Leonardo_cambios desde raiz: `ModuleNotFoundError: No module named 'src'`.
- En origin/Leonardo_cambios desde backend: `10 passed`.

Impacto:
- Riesgo alto de falla en CI/CD si el pipeline ejecuta pruebas desde la raiz (comportamiento comun).
- Cualquier colaborador que siga flujo tradicional desde raiz vera fallos.

Causa raiz:
- Cambio de estructura sin ajustar de forma completa el contrato de ejecucion del proyecto (working directory, PYTHONPATH, comandos oficiales, pipeline).

---

### Hallazgo B (Alto): Documentacion operativa no alineada con la nueva estructura
Descripcion:
- La documentacion principal mantiene comandos y arbol anterior (archivos en raiz), pero la rama los mueve a backend.

Impacto:
- Onboarding y ejecucion local inconsistentes.
- Aumenta friccion para validacion de PR y soporte.

Causa raiz:
- Reestructuracion de rutas sin cierre documental en el mismo cambio.

---

### Hallazgo C (Medio): Frontend agregado como placeholders vacios
Descripcion:
- Se agregaron archivos HTML en frontend con tamano 0 bytes.

Impacto:
- No rompe backend, pero agrega ruido en PR y no entrega valor funcional.

Causa raiz:
- Se creo estructura inicial sin contenido minimo util ni alcance definido en este PR.

## 4) Plan de correccion recomendado para Leonardo

### Opcion 1 (Recomendada): Definir backend como raiz tecnica explicita
Aplicar estos cambios:
1. Estandarizar que pruebas y ejecucion de v0.2 corren desde carpeta backend.
2. Actualizar README y guia operativa con comandos basados en backend.
3. Ajustar pipeline CI para `working-directory: backend`.
4. Mantener imports internos como `from src...` (siempre que src sea paquete dentro de backend y los comandos se ejecuten desde backend).
5. Agregar nota clara de compatibilidad para colaboradores:
   - "No ejecutar pytest desde raiz; ejecutar desde backend".

Ventaja:
- Cambio minimo sobre la reestructuracion actual.

Riesgo residual:
- Si alguien insiste en ejecutar desde raiz sin wrapper, volvera a fallar.

---

### Opcion 2: Mantener ejecucion desde raiz (contrato historico)
Aplicar estos cambios:
1. Crear wrappers en raiz para pruebas y CLI que redirijan a backend.
2. Configurar PYTHONPATH o paquete instalable editable para que `src` sea resoluble desde raiz.
3. Ajustar CI y documentacion para reflejar ese enfoque.

Ventaja:
- Menor ruptura para usuarios que ya trabajan desde raiz.

Riesgo:
- Mayor complejidad de configuracion.

## 5) Correcciones minimas obligatorias antes de aprobar
1. Definir y documentar un unico contrato de ejecucion (raiz o backend).
2. Hacer que la suite de pruebas pase en el contexto oficial declarado.
3. Alinear README, comandos de instalacion y ejecucion con esa decision.
4. Validar el pipeline de CI con esa misma convencion.

## 6) Checklist de validacion para re-entrega

### 6.1 Validacion funcional
- [ ] `pytest -q` pasa en el contexto oficial definido.
- [ ] El comando CLI oficial de v0.2 funciona segun documentacion.
- [ ] No hay imports rotos por movimiento de rutas.

### 6.2 Validacion documental
- [ ] README actualizado con arbol real.
- [ ] Comandos de instalacion y ejecucion corregidos.
- [ ] Instrucciones para colaboradores alineadas con CI.

### 6.3 Validacion de alcance
- [ ] Frontend: o se agrega contenido minimo util o se excluye de este PR.
- [ ] PR con descripcion clara de "breaking changes" de estructura.

## 7) Propuesta de mensaje para Leonardo
Hola Leonardo,

Gracias por la reestructuracion. La idea general esta bien y el cambio parece mayormente de organizacion (sin cambios de logica), pero no podemos aprobarlo aun porque rompe el flujo de pruebas desde la raiz del repo.

Puntos a corregir antes de merge:
1) Definir contrato de ejecucion unico (raiz o backend) y dejarlo explicito.
2) Alinear README y comandos con ese contrato.
3) Asegurar que `pytest -q` pase en el contexto oficial.
4) Ajustar CI para usar ese mismo contexto.
5) Revisar frontend placeholder (0 bytes): agregar minimo util o sacar de este PR.

Cuando tengas estos ajustes, revalidamos y avanzamos a aprobacion.

## 8) Criterio de aprobacion final
Se aprueba cuando:
- No hay regresiones de pruebas en el contexto oficial documentado.
- Documentacion y CI reflejan exactamente la estructura final del repo.
- El PR queda enfocado, coherente y ejecutable por cualquier colaborador siguiendo README.
