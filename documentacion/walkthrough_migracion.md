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
- **Botón "Forzar Singularidad"**: Se añadió un botón `#force-singularity-btn` ("Forzar Sing.") junto al botón "Sugerir Valores" con el tooltip `"demostración de manejo de error didactico"`.
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
8. **Manejo Didáctico de Singularidades (Forzar Sing.)**: Al presionar "Forzar Sing.", el simulador configura automáticamente $f(x)=x^3-3x$, Newton-Raphson, y $x_0=-0.80648$. En la primera iteración calcula con éxito el paso tangente hasta $x_1 \approx 1.0$, y en la segunda iteración detecta la derivada cero ($f'(1.0)=0$). Se verificó que:
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
   - Se ejecutó el escenario de singularidad ( Newton con $x_0 = -0.80648$), fallando en el segundo paso. Se cargó de nuevo Bisección y se verificó que la tabla y el gráfico se reiniciaron de inmediato mostrando la curva azul limpia.
   - Se presionó "Sugerir" sobre la función de singularidad $x^3 - 3x$ y se comprobó que cargó los parámetros correctos ($x_0 = 2.0$ para Newton y $[1, 2.5]$ para Bisección) con el banner verde de validez.
   - Se presionó "Sugerir" en una expresión desconocida y se verificó la visualización del banner azul informativo con parámetros genéricos, aclarando que no han sido validados para esa expresión.
11. **Prueba del Historial**:
    - Se comprobó que el historial muestra correctamente etiquetas como "Secante" y "Punto Fijo" con el color correspondiente (rojo para singularidades, verde para éxitos), y que hacer clic en los elementos limpia y carga los datos correctamente.

