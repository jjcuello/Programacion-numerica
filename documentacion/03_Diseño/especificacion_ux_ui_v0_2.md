# Especificación UX/UI y Diseño Frontend (v0.2)

**Proyecto:** Plataforma Web Interactiva para el Aprendizaje de Métodos Numéricos  
**Responsable de Frontend:** Leonardo González  
**Fase:** Diseño Técnico e Interfaz de Usuario  
**Fecha:** Junio 2026  

---

## 1. Visión General del Diseño Frontend
El objetivo principal de la interfaz es reducir la fricción técnica y priorizar la comprensión matemática. El sistema evoluciona de una consola de texto plano a un entorno gráfico interactivo, reactivo y guiado por un **"Tutor Didáctico"**.

La estética del diseño se basará en principios modernos de UI:
*   **Esquema de color:** Sleek Dark Mode (Fondo oscuro con gradientes suaves y colores de acento semánticos).
*   **Tipografía:** Fuentes modernas legibles (`Inter` u `Outfit`) integradas mediante Google Fonts.
*   **Interactividad:** Micro-animaciones en botones, estados de hover dinámicos y transiciones suaves en paneles desplegables.

---

## 2. Flujos de Usuario (User Journeys)

### 2.1. Rol: Estudiante
Enfocado en la simulación sin fricción y la autoevaluación.
*   **Dashboard:** Vista general del progreso del estudiante, últimos experimentos realizados y acceso rápido a prácticas recientes.
*   **Laboratorio Numérico (Simulador):** Espacio interactivo para configurar y ejecutar métodos sobre funciones $f(x)$ personalizadas, con soporte para sugerencias inteligentes.
*   **Visualización Didáctica:** Renderizado gráfico en tiempo real, tablas de iteraciones interactivas y conclusiones del Tutor.
*   **Tutor Didáctico (Retos):** Panel para configurar y realizar exámenes de práctica auto-generados para medir el entendimiento.
*   **Feedback Educativo:** Visualización paso a paso de los errores matemáticos cometidos y cómo corregirlos.

### 2.2. Rol: Profesor
Enfocado en las demostraciones en clase, la comparación algorítmica y la gestión de evaluaciones.
*   **Dashboard Docente:** Gestión de grupos, visualización de estadísticas de participación y rendimiento de los alumnos.
*   **Laboratorio de Comparación:** Ejecución simultánea de múltiples métodos sobre la misma función $f(x)$ para evaluar velocidad y eficiencia.
*   **Generador de Evaluaciones:** Herramienta interactiva para generar retos y exámenes basados en dificultad ponderada y temarios seleccionados.
*   **Monitoreo y Reportes:** Gráficos estadísticos del rendimiento grupal y exportación de reportes académicos (formatos JSON/CSV).

---

## 3. Componentes Visuales Core

### 3.1. Inputs del Simulador
*   **Caja de Input Matemático:** Renderizado en tiempo real de la fórmula ingresada utilizando MathJax o KaTeX. Incorpora validación sintáctica dinámica con bordes semánticos:
    *   🟢 **Verde:** Expresión matemática válida y parsed correctamente.
    *   🔴 **Rojo:** Error de sintaxis o caracteres no permitidos.
*   **Botón "✨ Sugerir Valores":** Acción inteligente que consulta al backend para analizar la función y autocompletar intervalos sugeridos $[a, b]$ o puntos iniciales $x_0$ viables.
*   **Configuración Avanzada:** Selector de tolerancia ($10^{-6}$ por defecto) y número máximo de iteraciones (100 por defecto) ocultos dentro de un acordeón colapsable para no abrumar al usuario.

### 3.2. Tabla Unificada de Iteraciones
Diseño minimalista con filas alternadas estilo cebra, cabecera fija (*sticky header*) y scroll interno para tolerar algoritmos con alto número de iteraciones sin romper el layout.

| Iteración | $x_i$ (Actual / Lím. Inf) | Siguiente Paso / Lím. Sup | Raíz Aprox. / Valor | Error Relativo | Residual $f(x)$ |
| :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | 1.500000 | 2.000000 | 1.750000 | - | -0.875000 |

### 3.3. Gráficas Interactivas (Plotly.js)
Las gráficas estáticas generadas por Matplotlib en el backend se reemplazan por un canvas dinámico del lado del cliente utilizando **Plotly.js**.
*   **Contrato de Datos (Backend ➡️ Frontend):**
    ```json
    {
      "graph_data": {
        "x_values": [1.0, 1.1, 1.2],
        "y_values": [-1.0, -0.6, 0.2],
        "roots": {"x": [1.15], "y": [0.0]},
        "interval": {"a": 1.0, "b": 2.0}
      }
    }
    ```
*   **Interacciones permitidas:** Zoom, paneo (*pan*), guardado de captura como imagen, y visualización de coordenadas en tooltips al pasar el cursor (*hover*).

---

## 4. Interceptación Didáctica de Singularidades (Manejo de Errores)
Cuando un algoritmo matemático entra en falla (por ejemplo, una división por cero en Newton-Raphson), la interfaz de usuario no se rompe, sino que se utiliza como un elemento pedagógico:
1.  **Banner de Alerta:** Fondo naranja/rojo llamativo advirtiendo: *"El algoritmo se detuvo: Singularidad matemática detectada en $x = 1.0$"*.
2.  **Marcador Gráfico:** Se dibuja una línea vertical roja punteada (Plotly trace) que representa la asíntota o el punto de singularidad sobre la gráfica.
3.  **Tooltip de Aprendizaje:** Ventana de ayuda explicando conceptualmente: *"La derivada de la función $f'(x)$ se hizo cero en este punto, haciendo imposible la proyección de la tangente"*.
4.  **Tabla Parcial:** Muestra las iteraciones realizadas con éxito hasta el momento del fallo, marcando la fila del error como `[ INDEFINIDO ]`.
5.  **Recomendación del Tutor:** Sugiere al usuario cambiar el valor del punto inicial $x_0$ o cambiar a un método cerrado (Bisección) que no dependa de derivadas.

---

## 5. Trazabilidad y Registro de Experimentos

### 5.1. Estructura de Datos Históricos
*   **Título:** Nombre identificador del experimento (generado automáticamente o editable por el estudiante).
*   **Método y Función $f(x)$:** Datos de sólo lectura formateados matemáticamente.
*   **Parámetros:** Chips visuales mostrando la tolerancia y el intervalo/punto inicial (ej. `x0=1`, `tol=1e-6`).
*   **Estado:** Píldora de estado de color:
    *   🟢 **Convergencia exitosa**
    *   🟡 **Límite de iteraciones alcanzado**
    *   🔴 **Fallo por singularidad**
*   **Apuntes Personales:** Campo de texto (*textarea*) para que el estudiante guarde sus propias observaciones o conclusiones de la práctica.

### 5.2. Interfaz de Historial
*   **Card View:** Tarjetas resumen ordenadas por fecha en el Dashboard del estudiante.
*   **Detail Modal:** Al hacer clic en una tarjeta, se abre un modal con el desglose de la tabla y la gráfica interactiva del experimento histórico.
*   **Botón "🔄 Volver a simular":** Acción clave en UX que inyecta automáticamente todos los parámetros del experimento histórico de vuelta en el simulador para repetir o modificar el ejercicio.

---

## 6. Panel del Tutor Didáctico (El Generador)

### 6.1. Configuración de Retos y Exámenes
*   **Interruptor de Modalidad:** Toggle visual para cambiar entre 📚 Examen Teórico (preguntas conceptuales) y 🧮 Examen Práctico (resolver simulaciones).
*   **Sliders Proporcionales de Dificultad:**
    *   Tres barras deslizadoras para ponderar la dificultad: Fácil (🟢), Medio (🟡) y Difícil (🔴).
    *   **Regla UX:** La suma de los tres porcentajes debe dar siempre exactamente **100%**. Al mover una barra, las otras dos se auto-ajustan de manera proporcional en tiempo real. Muestran además el número exacto de preguntas correspondientes al porcentaje.

### 6.2. Modo Enfoque (Ejecución del Reto)
*   **Barra superior fija (Sticky Header):** Muestra el porcentaje de progreso del examen y un cronómetro regresivo (el tiempo se tiñe de rojo parpadeante al entrar en los últimos 2 minutos).
*   **Tipografía matemática:** Visualización grande y clara de las ecuaciones a resolver.

### 6.3. Feedback y Resultados
*   **Tarjetas de Refuerzo (Insight Cards):** Tarjetas verdes que explican por qué las respuestas correctas fueron acertadas, reforzando la teoría.
*   **Tarjetas de Corrección:** Tarjetas naranjas con la explicación matemática del fallo y un botón directo: *"📚 Repasar Tema"* que redirige al simulador con un problema similar pre-cargado.
*   **Gráfico de Radar:** Un gráfico Plotly polar que muestra las fortalezas y debilidades del estudiante distribuidas por tema (ej. Raíces, Intervalos, Singularidades, Convergencia).
