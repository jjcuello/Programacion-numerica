# Recorrido de la Migración de Métodos Legacy al Frontend Local

Se ha completado con éxito la migración de todos los módulos del script CLI de Python `legacy/run.py` al frontend local en [estudiante.html](../frontend/pages/estudiante.html). Todo el procesamiento matemático y gráfico se ejecuta directamente en el navegador de manera interactiva y fluida.

---

## Cambios Realizados

### 1. Interfaz de Pestañas (Tab Navigation)
- **HTML**: Se estructuró la página principal del Estudiante en 6 paneles/pestañas principales accesibles a través de un menú de botones en la parte superior. Se ajustó el sub-panel de Configuración Avanzada para apilar verticalmente los parámetros `a` y `b` (límite inferior y superior) en columnas dinámicas con placeholders claros (`a (Límite inferior / x₀)` / `b (Límite superior / x₁)`), previniendo el desbordamiento de las cajas en pantallas reducidas.
- **CSS**: Se estilizó la barra de navegación de pestañas con bordes degradados, estados interactivos y transiciones de animación suave (fade-in) al cambiar de pestaña.
- **JS**: Se implementó la lógica de selección de pestañas activa, controlando el redibujado automático de los gráficos Plotly en la pestaña activa para evitar desajustes visuales.


### 2. Nuevos Métodos de Raíces
- **Método de la Secante**: Implementado localmente en `runSecantLocal`. Calcula la convergencia a partir de dos puntos iniciales y grafica dinámicamente la recta secante didáctica.
- **Método de Punto Fijo**: Implementado localmente en `runFixedPointLocal`. Permite ingresar la ecuación de iteración $g(x)$ y opcionalmente $f(x)$ para comprobar el residual de la raíz.

### 3. Evasión de Singularidades
- Implementado el algoritmo del límite lateral en JS.
- Si la evaluación en el punto $x$ da un error (dominio, división por cero, o magnitud excesiva), el sistema aproxima los límites laterales reduciendo $\delta$ progresivamente ($20$ iteraciones desde $10^{-2}$).
- Clasifica automáticamente la singularidad como `removible` (como en $sin(x)/x$ en $x=0$) o `polo` (como en $1/x$ en $x=0$), trazando la asíntota vertical en rojo.

### 4. Aproximación de Constantes ($e$ y $\pi$)
- **Euler ($e$)**: Métodos de Taylor, Límite, Fracción Continua y Newton-Raphson.
- **Pi ($\pi$)**: Métodos de Leibniz, Nilakantha, Arquímedes, Ramanujan y Chudnovsky.
- **Visualización**: Muestra una tabla con el progreso de cada iteración, el error absoluto y el tiempo de cómputo, acompañada de un gráfico en escala logarítmica de la reducción del error.

### 5. Geometría 3D Interactiva
- Se implementaron mallas paramétricas 3D completas para representar las figuras de `graficas_3d.py`:
  - Recta en 3D
  - Esfera
  - Cilindro
  - Cono
  - Paraboloide Elíptico
- Permite configurar parámetros (radio, altura, vector, color) y rotar la figura interactivamente en 3D.
- Explica los conceptos de POO (Encapsulamiento, Herencia, Polimorfismo) ilustrados con estas figuras.

### 6. Ondas y Animaciones
- Tres animaciones en tiempo real usando `requestAnimationFrame`:
  1. *Onda Seno Dinámica*: Muestra variaciones dinámicas de la amplitud, frecuencia y fase de la función.
  2. *Interferencia*: Muestra la superposición de dos ondas viajeras y su resultante.
  3. *Superficie Trigonométrica 3D*: Renderiza y rota una superficie trigonométrica dinámica en 3D.
- Controles interactivos de reproducción (Play, Pause, Reset).

### 7. Tutor Didáctico y Segmentación de Retos
- **Interruptores de Modalidad**: Se incorporaron botones segmentados estilizados (`📚 Teo` / `🧮 Prac`) junto a cada slider de dificultad (Fácil, Medio, Difícil). Esto permite configurar un examen a medida mezclando preguntas teóricas y ejercicios prácticos en diferentes niveles.
- **Base de Preguntas Extendida**: Se diseñaron y agregaron nuevos problemas de carácter práctico (como cálculo del punto medio, proyecciones secantes y una iteración Newton-Raphson/Punto Fijo).
- **Filtrado Dinámico**: El motor de exámenes en `estudiante.js` filtra dinámicamente las preguntas basadas en la combinación Dificultad + Tipo seleccionada para cada slider, con un fallback seguro que evita errores de inicialización.

### 8. Descarga de Gráficas y Singularidades Didácticas
- **Descarga de Gráficas (PNG)**: Se agregó un botón `#download-plot-btn` ("Descargar PNG") en la cabecera de la tarjeta del gráfico Plotly. Este botón invoca de manera limpia y nativa `Plotly.downloadImage` para exportar la visualización activa a un archivo PNG sin requerir librerías de terceros.
- **Botón "Forzar Singularidad"**: Se añadió un botón `#force-singularity-btn` ("Forzar Sing.") junto al botón "Sugerir Valores" con el tooltip `"demostración de manejo de error didactico"`. Este botón ahora no altera el método seleccionado, sino que configura una singularidad pedagógica específica para el método activo:
  - **Bisección**: $f(x) = 1/(x-1.5)$ en $[1, 2]$ (falla en el punto medio $c=1.5$ por división entre cero).
  - **Secante**: $f(x) = x^2 - 2$ en $[1, -1]$ (falla en el primer paso por división entre cero al tener $f(x_1) - f(x_0) = 0$).
  - **Newton-Raphson**: $f(x) = x^3 - 3x$ con $x_0 = -0.80644$ (falla en el segundo paso por derivada igual a cero en $x = 1.0$).
  - **Punto Fijo**: $f(x) = x - 1/(x-1)$, $g(x) = 1/(x-1)$ con $x_0 = 1.5$ (falla en la tercera iteración por división entre cero al evaluar $g(1.0)$).
- **Manejo de Errores Didácticos**: Se refactorizaron los solucionadores numéricos locales (`runNewtonLocal`, `runSecantLocal`, `runBisectionLocal` y `runFixedPointLocal`) para capturar anomalías matemáticas (como derivadas iguales a cero o violaciones del intervalo de Bolzano) de manera interna sin lanzar excepciones destructivas. Esto permite que el simulador registre e imprima las iteraciones exitosas hasta el punto de error.
- **Gráfica con Asíntota de Fallo**: La función `plotFunctionGraph` fue modificada para recibir el estado del solucionador y, en caso de fallar por singularidad, dibujar la curva completa, los puntos e hilos de aproximación hasta el último paso válido, y una asíntota vertical punteada de color rojo (`#ef4444`) directamente en el punto de fallo.
- **Explicación de Sugerencias Válidas**: Al presionar el botón "Sugerir", el simulador ahora actualiza el banner didáctico `#didactic-alert` con un estilo de éxito verde (borde verde, fondo translúcido verde y un icono de checkmark verde) y muestra un mensaje explicativo detallando las razones matemáticas (ej. cumplimiento del Teorema de Bolzano o derivadas distintas de cero) por las cuales los parámetros sugeridos son adecuados para el método.
- **Resolución de Inconsistencias de Visualización**:
  - Se implementó la función `resetSimulationOutputs()` que se activa en cuanto el usuario altera cualquier parámetro (función, método, tolerancias, iteraciones o límites) o carga un elemento del historial. Esta función limpia inmediatamente las métricas, vacía la tabla y redibuja la curva limpia de la función en Plotly, eliminando aproximaciones y asíntotas de error obsoletas.
  - Se enriqueció la base de sugerencias para incluir la función del escenario de singularidad ($x^3 - 3x$) de forma diferenciada según el método activo.
  - Se diferencian visualmente las sugerencias: si están validadas en la base de datos se muestran en un banner **verde** ("Parámetros Sugeridos Válidos"), mientras que si son valores por defecto genéricos se muestran en un banner **azul** ("Parámetros Asignados (Por Defecto)") para no confundir al estudiante.
  - Se corrigió el historial de simulación para que traduzca correctamente los métodos ("Bisección", "Newton-Raphson", "Secante", "Punto Fijo") y muestre distintivos rojos (`badge-danger`) en caso de fallo por singularidad o violación de Bolzano.

---

## Resultados de Verificación

Se realizaron comprobaciones manuales en el entorno del frontend local:
1. **Secante**: Evaluada la función $x^3 - x - 2 = 0$ con valores iniciales $1$ y $2$. Convergió a la raíz exacta $1.521379$ en 5 iteraciones.
2. **Punto Fijo**: Evaluado con $g(x) = (x+2)^{1/3}$ y valor inicial $1.5$. Encontró la raíz a $1.521379$ con éxito.
3. **Evasión de Singularidad**:
   - $sin(x)/x$ en $0$: Evadió la división por cero y reportó límite aproximado de $1.000000$ (Removible).
   - $1/x$ en $0$: Detectó asíntota de polo y mostró error de no finito.
4. **Constantes**: El algoritmo de Chudnovsky convergió a $\pi = 3.141592653589793$ en solo 2 iteraciones con error absoluto menor a $10^{-16}$.
5. **Animaciones**: Verificado que los bucles de animación se inician y pausan correctamente, y se detienen automáticamente al cambiar de pestaña para liberar recursos del navegador.
6. **Tutor Didáctico (Retos)**: Se validó que al alternar entre Teórico y Práctico para los niveles de dificultad, el generador carga las preguntas correspondientes de forma correcta. Por ejemplo, al seleccionar `🟢 Fácil` + `🧮 Prac`, el examen inicia mostrando un ejercicio de cálculo del punto medio del método de bisección.
7. **Descarga de Gráficas**: Se comprobó que al hacer clic en "Descargar PNG" se exporta correctamente la gráfica de la función en un archivo de imagen.
8. **Manejo Didáctico de Singularidades (Forzar Sing.)**: Al presionar "Forzar Sing.", el simulador configura automáticamente $f(x)=x^3-3x$, Newton-Raphson, y $x_0=-0.80644$. En la primera iteración calcula con éxito el paso tangente hasta $x_1 \approx 1.0$, y en la segunda iteración detecta la derivada cero ($f'(1.0)=0$). Se verificó que:
   - La tabla muestra la primera iteración correcta y la segunda fila con el estado `[FALLO]`.
   - El gráfico Plotly renderiza la función en azul, la recta tangente naranja del primer paso correcto landing en $x_1 = 1.0$, y una línea vertical discontinua roja de fallo en $x = 1.0$.
   - El estado de la métrica de salida se actualiza a `singularidad` en rojo y el Tutor Didáctico muestra una recomendación específica detallando las causas matemáticas y las posibles soluciones en color rojo.
9. **Sugerencias y Alerta Didáctica de Éxito**: Al hacer clic en "Sugerir" con la función `x**3 - x - 2`, se verificó que:
   - Los inputs se ajustan a Bisección y el intervalo a `[1, 2]`.
   - Se muestra un banner verde con el título "Parámetros Sugeridos Válidos".
   - El banner explica que $f(1) = -2$ y $f(2) = 4$ tienen signos opuestos, por lo que el Teorema de Bolzano garantiza una raíz en ese rango.
   - Al ejecutar la simulación, el banner verde se oculta automáticamente, permitiendo visualizar los resultados de la simulación normal.
10. **Prueba de Inconsistencias y Reseteo**:
   - Se realizó una simulación con Bisección (exitosa), se modificó el intervalo y se confirmó que las métricas y la tabla se limpiaron y el gráfico eliminó los puntos de iteración verdes anteriores.
   - Se ejecutó el escenario de singularidad ( Newton con $x_0 = -0.80644$), fallando en el segundo paso. Se cargó de nuevo Bisección y se verificó que la tabla y el gráfico se reiniciaron de inmediato mostrando la curva azul limpia.
   - Se presionó "Sugerir" sobre la función de singularidad $x^3 - 3x$ y se comprobó que cargó los parámetros correctos ($x_0 = 2.0$ para Newton y $[1, 2.5]$ para Bisección) con el banner verde de validez.
   - Se presionó "Sugerir" en una expresión desconocida y se verificó la visualización del banner azul informativo con parámetros genéricos, aclarando que no han sido validados para esa expresión.
11. **Prueba del Historial**:
    - Se comprobó que el historial muestra correctamente etiquetas como "Secante" y "Punto Fijo" con el color correspondiente (rojo para singularidades, verde para éxitos), y que hacer clic en los elementos limpia y carga los datos correctamente.

---

## Actualización del Módulo del Profesor

Se ha completado la actualización estructural e interactiva de la vista de profesores en [profesor.html](../frontend/pages/profesor.html) y [profesor.js](../frontend/assets/js/profesor.js), logrando paridad de rendimiento, control estricto de restricciones matemáticas y una estética premium uniforme con el módulo estudiantil.

### Cambios Realizados

1. **Laboratorio de Comparación Docente Completo**:
   - **4 Métodos Simultáneos**: Bisección, Secante, Newton-Raphson y Punto Fijo. Se puede activar cualquier combinación de estos algoritmos mediante checkboxes estilizados.
   - **Métricas Comparativas Directas**: Una tabla consolidada que recopila el estado final del cálculo (Éxito, Límite Iter, Singularidad, Bolzano, etc.), la raíz exacta, número de iteraciones, último residual de la función $f(x)$ y tiempo de cómputo en segundos.
   - **Trazas de Convergencia Plotly**: Gráfico interactivo con hasta 4 trayectorias diferenciadas por color (Verde: Bisección, Cian: Secante, Naranja: Newton-Raphson, Morado: Punto Fijo) junto con la curva de la función principal.
   - **Ecuación $g(x)$ Dinámica**: El campo para ingresar $g(x)$ y su previsualización LaTeX KaTeX se muestran u ocultan de forma inteligente dependiendo de si el método de Punto Fijo está marcado.
   - **Alertas Didácticas**: Banner animado `#didactic-alert` que detecta e informa de divisiones por cero, derivadas nulas o violaciones de Bolzano durante el análisis comparativo, ofreciendo recomendaciones pedagógicas directas.
   - **Alineación Vertical del Intervalo**: Se apilaron verticalmente los inputs de `a` y `b` con placeholders descriptivos para evitar el desbordamiento horizontal en la columna de parámetros.

2. **Generador de Evaluaciones y Retos Estructurados**:
   - **Sliders de Dificultad Proporcionales**: Control de distribución de preguntas (Fácil, Medio, Difícil) sincronizados mediante la restricción de suma exacta del 100%.
   - **Modalidad Segmentada**: Botones interactivos segmentados por nivel de dificultad para configurar el tipo de preguntas (`📚 Teo` / `🧮 Prac` / `🔄 Mix`).
   - **Sincronización de Plantillas**: Selección de configuraciones preestablecidas de parciales que actualiza automáticamente las barras y etiquetas.
   - **Código de Clase Estructurado**: Generación de identificadores de curso estandarizados en base a la configuración activa (ej. `NUM-2026-E4T-M4P-D2M`).
   - **Exportación JSON completa**: Descarga local de un paquete de metadatos del examen en formato JSON con la distribución, código generado y marcas de tiempo.

### Resultados de Verificación (Módulo Profesor)

1. **Comparación Multitrayectoria**:
   - Se probó la función $x^3 - x - 2$ con Bisección en $[1, 2]$, Secante en $[1, 2]$, Newton en $x_0 = 1.5$ y Punto Fijo con $g(x) = (x+2)^{1/3}$ en $x_0 = 1.5$.
   - Los cuatro algoritmos convergieron exitosamente a la raíz $1.521379$. El gráfico consolidó las 4 trazas correctamente con sus colores predefinidos.
2. **Control de Restricciones en Sliders**:
   - Se modificó el slider "Fácil" a 50%. Los sliders "Medio" y "Difícil" se ajustaron automáticamente de forma proporcional para mantener el total en 100%.
   - Al cambiar el total de preguntas a 15, las etiquetas de cantidad se recalcularon instantáneamente (`🟢 Fácil: 50% (8 preguntas)`, `🟡 Medio: 30% (5 preguntas)`, etc.).
3. **Generación e Integración de Código de Clase**:
   - Se configuraron 10 preguntas con modalidad Teórica en Fácil, Práctica en Medio y Mixta en Difícil.
   - Al hacer clic en "Generar Código de Clase", se produjo el string exacto `NUM-2026-E4T-M4P-D2M` con una animación glow verde satisfactoria.
4. **Exportación de JSON**:
   - Se exportó la configuración del examen exitosamente, generando un archivo JSON válido que describe la plantilla seleccionada, la cantidad total de preguntas, la distribución exacta y el código de clase correspondiente.

## Validación de Ecuación de Iteración $g(x)$ (Módulos Estudiante y Profesor)

Para guiar pedagógicamente a los usuarios al resolver o comparar el método de Punto Fijo, se ha integrado un motor de validación matemática en tiempo real para la función de iteración $g(x)$ ingresada en relación a la función original $f(x)$ tanto en la vista del Estudiante como en la de Profesores.

### Cambios Realizados

1. **Validador Numérico Automático**:
   - Se implementó la función [checkGExpressionCompatibility](../frontend/assets/js/estudiante.js#L1044) en [estudiante.js](../frontend/assets/js/estudiante.js) y en [profesor.js](../frontend/assets/js/profesor.js#L667).
   - Esta función busca la raíz real $r$ de $f(x) = 0$ más cercana al punto inicial $x_0$ utilizando un resolvedor Newton-Raphson de alta precisión en segundo plano.
   - Si se encuentra una raíz, el sistema evalúa $g(r)$ y calcula la diferencia absoluta $|g(r) - r|$. Si esta diferencia supera la tolerancia ($0.005$), se considera que el despeje de $g(x)$ es matemáticamente incompatible o erróneo.

2. **Advertencia Didáctica Interactiva**:
   - **Módulo Estudiante**: Si se detecta incompatibilidad al simular, se dispara una alerta de advertencia en color naranja (`#f59e0b`) en el banner `#didactic-alert` con la discrepancia y recomendaciones.
   - **Módulo Profesor**: Al hacer clic en "Comparar Algoritmos", si el método de Punto Fijo está activo y $g(x)$ es incompatible, el comparador dispara el banner de incidencia didáctica detallando el error antes de mostrar los gráficos consolidados, permitiendo evidenciar pedagógicamente la divergencia.

### Resultados de Verificación

1. **Verificación de Entrada Correcta**:
   - Con $f(x) = x^3 - x - 2$ y $x_0 = 1.5$: se ingresó $g(x) = (x + 2)**(1/3)$. El validador determinó que es compatible, ejecutó la simulación con éxito en ambas vistas y no mostró ninguna alerta de advertencia.
2. **Verificación de Entrada Incorrecta (Detección y Alerta)**:
   - Con $f(x) = x^3 - x - 2$ y $x_0 = 1.5$: se ingresó un despeje erróneo $g(x) = x^2$.
   - Al simular en la vista de estudiantes o comparar en la vista de profesores, el motor detectó inmediatamente que en la raíz real $x \approx 1.521380$ se cumple $f(x) = 0$ pero $g(r) \approx 2.314597 \neq r$.
   - Se desplegó correctamente el banner de advertencia didáctica naranja advirtiendo de la incompatibilidad y detallando la discrepancia matemática.

---

## Cambio de Nombre e Identidad Visual (Métodos Numéricos)

Se actualizó la terminología de marca en toda la plataforma para utilizar el término académico estándar y descriptivo **Métodos Numéricos** en lugar del genérico "Programación Numérica".

### Cambios Realizados

1. **Ajuste de Cabecera Logo**: Se reemplazó el texto del logotipo en la barra de navegación superior de `Programación Numérica` a `Métodos Numéricos` en todas las páginas web de la plataforma:
   - [index.html](../index.html)
   - [estudiante.html](estudiante.html)
   - [profesor.html](profesor.html)
   - [admin.html](admin.html)
   - [dashboard.html](dashboard.html)
2. **Actualización de Textos e Identidad**: Se eliminó la mención a "Cátedra de" en subtítulos y pies de página de los archivos anteriores, quedando directamente configurado como "Métodos Numéricos" para simplificar y modernizar el pie de página de la plataforma.

---

## Representación Gráfica del Intervalo $[a, b]$ (Bisección)

Se identificó y resolvió un comportamiento visual confuso en el trazado de los límites del intervalo en el método de Bisección dentro del gráfico Plotly.

### Problema y Solución

* **Comportamiento Anterior**: El gráfico trazaba las líneas verticales discontinuas de los límites `a` y `b` basándose en los valores de la **última** iteración del cálculo (`successfulIt`). Dado que el intervalo se reduce a un tamaño menor a la tolerancia (ej. $10^{-6}$), los límites finalizaban prácticamente en el mismo punto exacto que la raíz, haciendo que ambas líneas se solaparan y parecieran una única vertical.
* **Solución Aplicada**: 
  - **Módulo Estudiante**: Refactoricé la lógica en [estudiante.js](../frontend/assets/js/estudiante.js#L1321) para tomar los límites del intervalo de la **primera** iteración (`iterations[0]`). Esto permite representar correctamente en la gráfica las líneas verticales del intervalo de búsqueda inicial $[a, b]$ seleccionado por el estudiante.
  - **Módulo Profesor**: Integre el trazado de los límites iniciales en [profesor.js](../frontend/assets/js/profesor.js#L822) para que las líneas verticales discontinuas del intervalo de búsqueda inicial $[a, b]$ se muestren translúcidas en el comparador de trayectorias, proporcionando una referencia visual clara del dominio elegido.

---

## Creación de Pull Request a `main`

Se realizó el commit, push y apertura del Pull Request oficial para consolidar todos los desarrollos interactivos y didácticos del proyecto:

* **Rama de origen (head)**: `Leonardo_cambios` (con todos los commits cargados y empujados).
* **Rama de destino (base)**: `main`.
* **Enlace del Pull Request**: [PR #2 en GitHub](https://github.com/jjcuello/Programacion-numerica/pull/2)
* **Contenido**: El cuerpo del PR detalla minuciosamente todos los cambios del Módulo de Profesor, la validación de correspondencia de $g(x)$, la corrección de límites de Bisección en gráficos y las actualizaciones terminológicas de marca ("Métodos Numéricos").

---

## Escaneo Dinámico de Intervalos de Búsqueda de Raíces

Para lograr una paridad del 100% con las herramientas heredadas del CLI (`legacy/run.py`), se ha implementado un motor de **escaneo dinámico de intervalos** en el frontend:

* **Problema Original**: La versión web sugería parámetros válidos basados únicamente en una base de datos estática para funciones predefinidas (ej. `x**3 - x - 2`). Si el estudiante ingresaba una función matemática personalizada, el sistema se limitaba a establecer parámetros por defecto genéricos (`[0, 2]` o `1.0`), perdiendo la capacidad del script de Python para explorar y sugerir intervalos que cumplan el Teorema de Bolzano.
* **Solución Implementada**:
  - **Función de Escaneo**: Se agregó la función `scanIntervalsForRoots(expr)` en [estudiante.js](../frontend/assets/js/estudiante.js). Esta función realiza una exploración matemática preliminar en el rango $[-10, 10]$ evaluando la expresión en $200$ puntos uniformes de forma segura.
  - **Identificación de Raíces**: Detecta cruces por cero directos ($f(x) = 0$) y cambios de signo de la función ($f(x_1) \cdot f(x_2) < 0$), aislando hasta 3 intervalos de raíces candidatas.
  - **Auto-Configuración Inteligente**: Si el estudiante hace clic en **Sugerir** para una función de usuario, el motor busca raíces reales dinámicamente. Al encontrarlas, configura de inmediato los campos de límites `a` y `b` (y el punto medio `x0` para métodos abiertos) y despliega el banner didáctico de éxito en color verde detallando la justificación del intervalo encontrado.
  - **Respaldo Seguro**: En caso de no detectarse raíces en el escaneo (como en `x**2 + 4`), el sistema asigna los valores por defecto genéricos y muestra un banner informativo azul con recomendaciones pedagógicas de exploración.

---

## Laboratorio Comparativo de Constantes ($e$ y $\pi$)

Para lograr paridad matemática y pedagógica con las herramientas heredadas del CLI (`legacy/run.py`), se ha implementado un **Laboratorio Comparativo Multimétodo** en la pestaña de Constantes de la vista del estudiante:

* **Problema Original**: La versión web anterior solo permitía simular un método a la vez para aproximar $e$ o $\pi$, impidiendo comparar el rendimiento de convergencia, las iteraciones necesarias y el error absoluto entre diferentes formulaciones en un mismo panel (tal como se hacía en consola en el código heredado).
* **Solución Implementada**:
  - **Switch Comparativo**: Se añadió el control interactivo **"Comparar todos los métodos"** en el panel de control del formulario de Constantes.
  - **Tabla Comparativa Consolidada**: Al activarlo y ejecutar, se calcula en paralelo la aproximación para todos los métodos correspondientes (4 métodos para $e$ y 5 métodos para $\pi$). La tabla consolidada reporta de manera unificada:
    - *Método*: Nombre del método evaluado.
    - *Aproximación*: Valor calculado con hasta 15 decimales.
    - *Iteraciones*: Número de pasos realizados hasta convergencia o límite seguro.
    - *Error Absoluto*: Discrepancia absoluta respecto al valor exacto del sistema (`Math.E` o `Math.PI`).
    - *Decimales Ok*: Cantidad exacta de cifras decimales correctas consecutivas tras la coma.
    - *Tiempo*: Duración exacta del cómputo en segundos.
  - **Gráfica de Convergencia Multitrayecto (Plotly Log-scale)**: Renderiza las curvas de error absoluto de todos los métodos en un solo gráfico interactivo utilizando una escala logarítmica en el eje Y. Esto permite contrastar visualmente la convergencia lineal y lenta (como Leibniz) con la convergencia cuadrática o exponencial ultra rápida (como Ramanujan o Chudnovsky). El error mínimo para el trazado se ha acotado a $10^{-16}$ (la precisión de máquina nativa de hardware para variables `float64`), optimizando la visualización de la curva y evitando distorsiones visuales por errores nulos.
  - **Observación Didáctica Directa**: Se muestra un banner explicativo dinámico (`#const-compare-alert`) con recomendaciones pedagógicas sobre la velocidad de convergencia (por ejemplo, destacando que la serie de Leibniz requiere 10,000 iteraciones para obtener apenas 3-4 decimales correctos debido a su naturaleza lineal, mientras que Chudnovsky y Ramanujan obtienen precisión total de hardware en 2-3 pasos).

---

## Simulación de Convergencia en Tiempo Real ("En Vivo") de Constantes

Para completar la paridad funcional del 100% con los scripts de consola heredados (`legacy/metodos/euler.py` y `legacy/metodos/pi.py`), se incorporó un motor de **simulación interactiva paso a paso en tiempo real** en la pestaña de Constantes:

* **Características**:
  - **Switch de Modo en Vivo**: Permite activar la simulación interactiva `#const-realtime-toggle` en modo individual.
  - **Ajustes Dinámicos**: Control deslizante de velocidad (`#const-realtime-speed`, entre $20\text{ ms}$ y $1000\text{ ms}$ de delay) y selector de tamaño de paso (`#const-realtime-step-slider`, entre $1$ y $500$ iteraciones por actualización) que se pueden cambiar en caliente durante la simulación.
  - **Controles de Reproducción**: Botones para **Pausar** (`#const-btn-pause`) y **Detener** (`#const-btn-stop`) la simulación en caliente.
  - **Trazado Dinámico**: La gráfica en Plotly y la tabla de iteraciones se van poblando dinámicamente de forma progresiva, animando visualmente la reducción del error absoluto y la precisión lograda paso a paso.
  - **Mitigación de Sobrecarga**: El algoritmo mantiene la optimización del muestreo para métodos de convergencia lenta (como Leibniz) previniendo fugas de memoria o congelamiento de la ventana del navegador.

---

## Auditoría de Frontend, Usabilidad y Control de Acceso (v0.4)

En esta fase se resolvieron incidencias de usabilidad, seguridad de acceso en el cliente y visualización dinámica en los paneles estudiantil, docente y administrativo.

### 1. Control de Acceso y Prevención de Parpadeo de Interfaz (FOUC)
- **Bloqueo Síncrono en Head**: Se movió la lógica de validación de sesión activa y redirección al `<head>` de [login.html](../frontend/pages/login.html) mediante una función autoejecutable. Esto redirige instantáneamente al usuario autenticado a su panel académico (`estudiante.html`, `profesor.html`, `admin.html`) antes de pintar el cuerpo de la página, eliminando el parpadeo de la pantalla de login.
- **Header Limpio y Dinámico**: Se vaciaron los enlaces de rol estáticos de la etiqueta `<nav class="main-nav">` de todos los archivos HTML (`index.html`, `estudiante.html`, `profesor.html`, `admin.html`). La renderización de los mismos ahora se realiza de forma 100% dinámica en [auth-ui.js](../frontend/assets/js/auth-ui.js), previniendo la exposición temporal de enlaces protegidos.
- **Accesos Integrados en Dropdown**: Se movieron los enlaces de acceso de rol al interior del menú desplegable del avatar del usuario (`user-profile-menu`), garantizando un diseño limpio y navegación ágil adaptada al rol actual.
- **Redirección de CTA en Inicio**: Los botones de acción principal (CTA) en [index.html](../frontend/index.html) redirigen al usuario a `pages/login.html` en caso de no tener una sesión activa.
- **Enlace de Perfil Corregido**: Se vinculó de forma correcta el script [auth-ui.js](../frontend/assets/js/auth-ui.js) al final de [perfil.html](../frontend/pages/perfil.html) para pintar la cabecera dinámica unificada en la vista de perfil de usuario.

### 2. Limpieza de Interfaz y Eliminación de Opciones Obsoletas
- **Remoción de Backend en Admin**: Se eliminó la sección "Modo de Ejecución del Backend" de [admin.html](../frontend/pages/admin.html), ya que todos los métodos numéricos y gráficos se ejecutan completamente del lado del cliente.
- **Remoción de Conceptos POO**: Se retiró la sección informativa sobre conceptos de Programación Orientada a Objetos (POO) del panel 3D en [estudiante.html](../frontend/pages/estudiante.html), adaptando la vista puramente a la simulación matemática.
- **Simplificación del Profesor**: Se eliminó el botón "Exportar JSON" de [profesor.html](../frontend/pages/profesor.html) y se protegió la vinculación del event listener en [profesor.js](../frontend/assets/js/profesor.js) con un chequeo de nulidad para evitar detenciones de ejecución del script.

### 3. Robustez de Simulación y Soporte de Fórmulas Didácticas
- **Detección de Raíces en Extremos (Bisección)**: En [estudiante.js](../frontend/assets/js/estudiante.js) y [profesor.js](../frontend/assets/js/profesor.js), el resolvedor de Bisección evalúa ahora de manera anticipada si alguno de los extremos de intervalo (`a` o `b`) ya representa una raíz exacta de la función (con tolerancia de $|f(x)| < 10^{-12}$). Si se cumple, el resolvedor responde con el estado `success_endpoint_root` y detiene el cómputo sin realizar iteraciones innecesarias.
- **Banner Didáctico de Éxito**: En la vista de estudiante, el estado `success_endpoint_root` despliega una alerta didáctica de éxito (`#didactic-alert`) de color verde que informa al estudiante sobre la coincidencia del límite y brinda consejos académicos para observar la tabla paso a paso.
- **Inicialización de Plots Protegida**: En [profesor.js](../frontend/assets/js/profesor.js), las inicializaciones de Plotly (`Plotly.newPlot` y `renderRadarChartClass`) se envolvieron en condicionales que comprueban la existencia del ID del contenedor, previniendo errores graves en páginas que no utilicen dichos elementos visuales.
- **Soporte para Multiplicación Implícita**: Se optimizó la función `evaluateFunction(expr, x)` en ambos archivos JS para pre-procesar expresiones algebraicas ingresadas de forma natural, insertando el operador `*` en patrones comunes:
  - Constantes seguidas de variables (ej. `2x` $\to$ `2*x`).
  - Constantes seguidas de constantes matemáticas (ej. `2pi` $\to$ `2*pi`, `2e` $\to$ `2*e`).
  - Constantes y variables al lado de paréntesis (ej. `2(x-1)` $\to$ `2*(x-1)`, `x(x-1)` $\to$ `x*(x-1)`).
  - Paréntesis consecutivos (ej. `(x+1)(x-2)` $\to$ `(x+1)*(x-2)`).

---

## Resultados de Verificación de Usabilidad y Auditoría (v0.4)

Se han realizado pruebas manuales en el navegador y análisis estáticos:
1. **Control de Acceso (FOUC)**: Verificado que al intentar acceder a `login.html` con una sesión activa, el script bloquea y redirige de forma imperceptible e inmediata al panel correspondiente sin mostrar el formulario de login.
2. **Navegación Dinámica**: Verificado que la barra de navegación superior no contiene enlaces estáticos, y tras iniciar sesión se carga de forma instantánea el dropdown del perfil que contiene los botones hacia el panel respectivo y la opción de cerrar sesión.
3. **Multiplicación Implícita**: Se simuló con éxito el método de Bisección y Newton-Raphson ingresando funciones con notación abreviada como `2x - 1` o `x(x-2)`, ejecutando la lógica matemática sin excepciones de sintaxis.
4. **Bisección en los Extremos**: Ingresando la función `x - 1` en el rango `[1, 2]` (donde $a=1$ es raíz exacta ya que $f(1)=0$), se comprobó que el solucionador responde de inmediato sin iterar y muestra el banner verde de éxito en el panel del estudiante.
5. **Robustez en la Vista de Profesor**: Se comprobó que al cargar la vista de profesor, no ocurren errores de Plotly y la visualización de comparación de métodos y radar se inicializa correctamente al contar con las comprobaciones de existencia de los contenedores en el DOM.
