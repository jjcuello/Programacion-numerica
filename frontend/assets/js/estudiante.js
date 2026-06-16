/* ==========================================================================
   LÓGICA INTERACTIVA DEL ESTUDIANTE - ESTUDIANTE.JS
   Responsable: Leonardo González
   Aesthetics: Rich user experience, KaTeX preview, Plotly plot, Sliders control
   ========================================================================== */

document.addEventListener("DOMContentLoaded", () => {
    // --- ESTADO GLOBAL DEL SIMULADOR Y TUTOR ---
    let history = JSON.parse(localStorage.getItem("simulations_history")) || [];
    let currentQuizQuestions = [];
    let currentQuestionIndex = 0;
    let quizTimerInterval = null;
    let quizTimeLeft = 600; // 10 minutos
    let userAnswers = [];
    let quizModes = {
        easy: "theoretical",
        medium: "theoretical",
        hard: "theoretical"
    };

    // --- ELEMENTOS DEL DOM ---
    const expressionInput = document.getElementById("expression-input");
    const mathPreview = document.getElementById("math-preview");
    const methodSelect = document.getElementById("method-select");
    const advancedToggle = document.getElementById("advanced-toggle");
    const advancedContent = document.getElementById("advanced-content");
    const advancedArrow = document.getElementById("advanced-arrow");
    const intervalGroup = document.getElementById("interval-group");
    const x0Group = document.getElementById("x0-group");
    const aInput = document.getElementById("a-input");
    const bInput = document.getElementById("b-input");
    const x0Input = document.getElementById("x0-input");
    const toleranceInput = document.getElementById("tolerance-input");
    const maxIterInput = document.getElementById("max-iter-input");
    const simulatorForm = document.getElementById("simulator-form");
    const suggestBtn = document.getElementById("suggest-btn");
    const downloadPlotBtn = document.getElementById("download-plot-btn");
    const forceSingularityBtn = document.getElementById("force-singularity-btn");
    
    // Resultados
    const didacticAlert = document.getElementById("didactic-alert");
    const alertTitle = document.getElementById("alert-title");
    const alertDescription = document.getElementById("alert-description");
    const alertRecommendation = document.getElementById("alert-recommendation");
    const metricStatus = document.getElementById("metric-status");
    const metricRoot = document.getElementById("metric-root");
    const metricIter = document.getElementById("metric-iter");
    const metricTime = document.getElementById("metric-time");
    const tableBody = document.getElementById("table-body");
    const historyList = document.getElementById("history-list");

    // Sliders de dificultad del Tutor
    const easySlider = document.getElementById("easy-slider");
    const mediumSlider = document.getElementById("medium-slider");
    const hardSlider = document.getElementById("hard-slider");
    const easyValueLabel = document.getElementById("easy-value");
    const mediumValueLabel = document.getElementById("medium-value");
    const hardValueLabel = document.getElementById("hard-value");
    const startQuizBtn = document.getElementById("start-quiz-btn");
    const tutorSetup = document.getElementById("tutor-setup");

    // Quiz Focus
    const quizFocusContainer = document.getElementById("quiz-focus-container");
    const quizQuestionCounter = document.getElementById("quiz-question-counter");
    const quizTimer = document.getElementById("quiz-timer");
    const timerText = document.getElementById("timer-text");
    const quizQuestionText = document.getElementById("quiz-question-text");
    const quizOptionsList = document.getElementById("quiz-options-list");
    const quizPrevBtn = document.getElementById("quiz-prev-btn");
    const quizNextBtn = document.getElementById("quiz-next-btn");
    const quizResultsContainer = document.getElementById("quiz-results-container");
    const scoreText = document.getElementById("score-text");
    const scoreComment = document.getElementById("score-comment");
    const resetQuizBtn = document.getElementById("reset-quiz-btn");
    const insightCardsContainer = document.getElementById("insight-cards-container");
    const quizTotalQuestionsInput = document.getElementById("quiz-total-questions");
    const quizTimeLimitInput = document.getElementById("quiz-time-limit");

    // --- NUEVOS SELECTORES PARA LAS PESTAÑAS (TABS) ---
    // Pestaña 2: Singularidades
    const singularityForm = document.getElementById("singularity-form");
    const singExprInput = document.getElementById("sing-expr-input");
    const singMathPreview = document.getElementById("sing-math-preview");
    const singXInput = document.getElementById("sing-x-input");
    const singTolInput = document.getElementById("sing-tol-input");
    const singMetricStatus = document.getElementById("sing-metric-status");
    const singMetricValue = document.getElementById("sing-metric-value");
    const singMetricMethod = document.getElementById("sing-metric-method");
    const singMetricError = document.getElementById("sing-metric-error");
    const singDetailMessage = document.getElementById("sing-detail-message");

    // Pestaña 3: Constantes
    const constantsForm = document.getElementById("constants-form");
    const constantSelect = document.getElementById("constant-select");
    const constMethodSelect = document.getElementById("const-method-select");
    const constTolInput = document.getElementById("const-tol-input");
    const constMaxIter = document.getElementById("const-max-iter");
    const constMetricIter = document.getElementById("const-metric-iter");
    const constMetricValue = document.getElementById("const-metric-value");
    const constMetricError = document.getElementById("const-metric-error");
    const constMetricTime = document.getElementById("const-metric-time");
    const constTableBody = document.getElementById("const-table-body");

    // Pestaña 4: Figuras 3D
    const shapes3DForm = document.getElementById("shapes-3d-form");
    const shapeSelect = document.getElementById("shape-select");
    const shapeColorSelect = document.getElementById("shape-color-select");

    // Pestaña 5: Ondas y Animaciones
    const animationsForm = document.getElementById("animations-form");
    const animationType = document.getElementById("animation-type");
    const animPlayBtn = document.getElementById("anim-play-btn");
    const animPauseBtn = document.getElementById("anim-pause-btn");
    const animResetBtn = document.getElementById("anim-reset-btn");
    const animDescription = document.getElementById("anim-description");

    // --- CONSTANTES Y ESTADO DE MÉTODOS Y ANIMACIONES ---
    const eulerMethods = [
        { value: "taylor", name: "Serie de Taylor (1/k!)" },
        { value: "limite", name: "Límite (1+1/n)^n" },
        { value: "fraccion", name: "Fracción Continua de Euler" },
        { value: "newton", name: "Newton-Raphson sobre ln(x)-1" }
    ];

    const piMethods = [
        { value: "leibniz", name: "Serie de Leibniz" },
        { value: "nilakantha", name: "Serie de Nilakantha" },
        { value: "archimedes", name: "Polígonos de Arquímedes" },
        { value: "ramanujan", name: "Fórmula de Ramanujan" },
        { value: "chudnovsky", name: "Algoritmo de Chudnovsky" }
    ];

    let animationFrameId = null;
    let animStartTime = 0;
    let animRunning = false;
    let animTimeOffset = 0;

    const animDescriptions = {
        sine: "Onda Seno Dinámica: Muestra cómo cambian la amplitud, frecuencia y desfase en una función senoidal pura a lo largo del tiempo. Ecuación: y = A sin(wx + phi).",
        interference: "Interferencia de Ondas: Superposición de dos ondas viajeras sinusoidales (azul y naranja) propagándose en sentidos opuestos, formando una onda resultante (roja).",
        surface3d: "Superficie Trigonométrica 3D: Animación tridimensional de la superficie oscilante de dos variables. Ecuación: z = sin(x + t) cos(y - 0.6t)."
    };

    // --- INITIALIZATION ---
    renderMathPreview();
    updateHistoryUI();
    renderEmptyPlot();
    initializeConstantsTab();
    initializeShapes3DTab();
    initializeAnimationsTab();
    updateSliderLabels();

    // --- EVENT LISTENERS ---

    // Lógica de navegación de pestañas (Tabs)
    const tabButtons = document.querySelectorAll(".tab-btn");
    const tabContents = document.querySelectorAll(".tab-content");

    tabButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            // Remover clase active y ocultar secciones
            tabButtons.forEach(b => b.classList.remove("active"));
            tabContents.forEach(c => c.style.display = "none");

            // Activar botón actual y mostrar su sección
            btn.classList.add("active");
            const targetId = btn.getAttribute("data-tab");
            document.getElementById(targetId).style.display = "block";

            // Detener bucles de animación si se sale de la pestaña de animaciones
            if (targetId !== "tab-animations") {
                stopAnimationLoop();
            }

            // Forzar a Plotly a recalcular el tamaño al cambiar de pestaña
            setTimeout(() => {
                if (targetId === "tab-roots") {
                    Plotly.Plots.resize('plot-container');
                } else if (targetId === "tab-singularities") {
                    Plotly.Plots.resize('plot-singularities');
                } else if (targetId === "tab-constants") {
                    Plotly.Plots.resize('plot-constants');
                } else if (targetId === "tab-3d") {
                    Plotly.Plots.resize('plot-3d');
                } else if (targetId === "tab-animations") {
                    Plotly.Plots.resize('plot-animations');
                }
            }, 50);
        });
    });
    
    // Input Matemático (KaTeX Preview)
    expressionInput.addEventListener("input", renderMathPreview);
    singExprInput.addEventListener("input", renderSingMathPreview);
    const gExprInput = document.getElementById("g-expression-input");
    gExprInput.addEventListener("input", renderGMathPreview);

    // Toggle de Acordeón
    advancedToggle.addEventListener("click", () => {
        advancedContent.classList.toggle("active");
        advancedArrow.classList.toggle("fa-chevron-down");
        advancedArrow.classList.toggle("fa-chevron-up");
    });

    // Selector de Método (Bisección / Secante / Newton / Punto Fijo)
    methodSelect.addEventListener("change", () => {
        const val = methodSelect.value;
        const exprLabel = document.getElementById("expr-label");
        const intervalLabel = document.getElementById("interval-label");
        const gExprGroup = document.getElementById("g-expression-group");

        // Reset
        gExprGroup.style.display = "none";
        gExprInput.required = false;
        exprLabel.textContent = "Función f(x)";

        if (val === "bisection") {
            intervalGroup.style.display = "block";
            x0Group.style.display = "none";
            intervalLabel.textContent = "Intervalo [a, b]";
        } else if (val === "secant") {
            intervalGroup.style.display = "block";
            x0Group.style.display = "none";
            intervalLabel.textContent = "Valores Iniciales [x₀, x₁]";
        } else if (val === "newton") {
            intervalGroup.style.display = "none";
            x0Group.style.display = "block";
        } else if (val === "fixedpoint") {
            intervalGroup.style.display = "none";
            x0Group.style.display = "block";
            gExprGroup.style.display = "block";
            gExprInput.required = true;
            exprLabel.textContent = "Función f(x) (para verificar)";
            
            // Auto-completar g(x) por defecto si la función es la predeterminada o está vacío
            if (!gExprInput.value.trim() || expressionInput.value.trim() === "x**3 - x - 2") {
                gExprInput.value = "(x + 2)**(1/3)";
                if (typeof renderGMathPreview === "function") {
                    renderGMathPreview();
                }
            }
        }
    });

    // Botón Sugerir Valores
    suggestBtn.addEventListener("click", suggestMathValues);

    // Descargar Gráfica como PNG
    if (downloadPlotBtn) {
        downloadPlotBtn.addEventListener("click", () => {
            Plotly.downloadImage('plot-container', { format: 'png', filename: 'grafica_funcion', width: 800, height: 500 });
        });
    }

    // Forzar Singularidad (Manejo de Error Didáctico)
    if (forceSingularityBtn) {
        forceSingularityBtn.addEventListener("click", () => {
            const method = methodSelect.value;
            
            if (method === "bisection") {
                expressionInput.value = "x - 1/x";
                renderMathPreview();
                
                aInput.value = "-0.5";
                bInput.value = "0.5";
                toleranceInput.value = "0.000001";
                maxIterInput.value = "100";
            } else if (method === "secant") {
                expressionInput.value = "x**2 - 2";
                renderMathPreview();
                
                aInput.value = "1.0";
                bInput.value = "-1.0";
                toleranceInput.value = "0.000001";
                maxIterInput.value = "100";
            } else if (method === "newton") {
                expressionInput.value = "x**3 - 3*x";
                renderMathPreview();
                
                x0Input.value = "-0.80644";
                toleranceInput.value = "0.000001";
                maxIterInput.value = "100";
            } else if (method === "fixedpoint") {
                expressionInput.value = "x - 1/(x - 1)";
                renderMathPreview();
                
                if (gExprInput) {
                    gExprInput.value = "1/(x - 1)";
                    renderGMathPreview();
                }
                x0Input.value = "1.5";
                toleranceInput.value = "0.000001";
                maxIterInput.value = "100";
            }
            
            runSimulation();
        });
    }

    // Formulario de Simulación
    simulatorForm.addEventListener("submit", (e) => {
        e.preventDefault();
        runSimulation();
    });

    // Restablecer salidas al modificar campos de entrada
    const inputsToWatch = [expressionInput, methodSelect, aInput, bInput, x0Input, toleranceInput, maxIterInput];
    inputsToWatch.forEach(input => {
        if (input) {
            input.addEventListener("input", () => {
                resetSimulationOutputs();
            });
            if (input === methodSelect) {
                input.addEventListener("change", () => {
                    resetSimulationOutputs();
                });
            }
        }
    });

    // Sliders Proporcionales (Regla de Suma de 100%)
    [easySlider, mediumSlider, hardSlider].forEach(slider => {
        slider.addEventListener("input", (event) => {
            adjustSlidersProportionally(event.target);
        });
    });

    // Quiz Event Listeners
    startQuizBtn.addEventListener("click", startQuiz);
    quizPrevBtn.addEventListener("click", () => navigateQuiz(-1));
    quizNextBtn.addEventListener("click", () => navigateQuiz(1));
    resetQuizBtn.addEventListener("click", resetQuiz);

    // Listener para cambios en la cantidad total de preguntas
    quizTotalQuestionsInput.addEventListener("input", updateSliderLabels);

    // Tutor Segmented Mode Buttons Listener
    const modeButtons = document.querySelectorAll(".mode-btn");
    modeButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            const difficulty = btn.getAttribute("data-difficulty");
            const mode = btn.getAttribute("data-mode");
            
            // Toggle active state in DOM for this difficulty group
            document.querySelectorAll(`.mode-btn[data-difficulty="${difficulty}"]`).forEach(b => b.classList.remove("active"));
            btn.classList.add("active");
            
            // Update state
            quizModes[difficulty] = mode;
        });
    });


    // --- FUNCIONES CORE ---

    // Restablecer salidas de simulación cuando cambian los parámetros
    function resetSimulationOutputs() {
        metricStatus.textContent = "-";
        metricStatus.className = "metric-card-value";
        metricRoot.textContent = "-";
        metricIter.textContent = "-";
        metricTime.textContent = "-";

        tableBody.innerHTML = `<tr><td colspan="6" style="text-align: center; color: var(--text-muted); padding: 1rem;">Configura los parámetros y haz clic en "Resolver Simulación".</td></tr>`;
        
        didacticAlert.style.display = "none";

        const expr = expressionInput.value.trim();
        if (expr) {
            try {
                // Graficar solo la curva limpia de la función
                plotFunctionGraph(expr, [], null, methodSelect.value, "idle");
            } catch (e) {
                renderEmptyPlot();
            }
        } else {
            renderEmptyPlot();
        }
    }

    // 1. Renderizar Vista Previa de Fórmulas Matemáticas
    function renderMathPreview() {
        let raw = expressionInput.value.trim();
        if (!raw) {
            mathPreview.innerHTML = "<span style='color: var(--text-muted);'>Esperando función...</span>";
            return;
        }
        
        // Traducir sintaxis simple de Python a LaTeX
        let parsed = raw
            .replace(/\*\*/g, "^")
            .replace(/\*/g, " \\cdot ")
            .replace(/sin/g, "\\sin")
            .replace(/cos/g, "\\cos")
            .replace(/tan/g, "\\tan")
            .replace(/exp/g, "e^")
            .replace(/log/g, "\\ln")
            .replace(/sqrt/g, "\\sqrt");
        
        try {
            katex.render("f(x) = " + parsed, mathPreview, {
                throwOnError: false,
                displayMode: true
            });
            expressionInput.style.borderColor = "var(--border-color)";
        } catch (err) {
            expressionInput.style.borderColor = "var(--danger)";
        }
    }

    // 2. Botón Sugerir Valores Inteligentes (Base de Datos Básica de f(x))
    function suggestMathValues() {
        const rawExpr = expressionInput.value.trim().toLowerCase();
        let method = methodSelect.value;
        
        // Diccionario de sugerencias específicas por función y método
        const suggestions = [
            // x^3 - x - 2
            { key: "x**3 - x - 2", method: "bisection", a: 1, b: 2, x0: 1.5, reason: "El intervalo [1.00, 2.00] es válido porque f(1) = -2 y f(2) = 4 tienen signos opuestos (f(a)·f(b) < 0), cumpliendo con el Teorema de Bolzano." },
            { key: "x**3 - x - 2", method: "newton", a: 1, b: 2, x0: 1.5, reason: "El punto inicial x₀ = 1.50 es válido para Newton-Raphson ya que la derivada f'(1.5) = 5.75 es segura y el punto está cerca de la raíz." },
            { key: "x**3 - x - 2", method: "secant", a: 1, b: 2, x0: 1.5, reason: "Los puntos iniciales [1.00, 2.00] son válidos para la Secante ya que f(1) y f(2) tienen valores con signos opuestos y no anulan el denominador." },
            { key: "x**3 - x - 2", method: "fixedpoint", a: 1, b: 2, x0: 1.5, g: "(x + 2)**(1/3)", reason: "El punto inicial x₀ = 1.50 es adecuado para Punto Fijo en la vecindad de la raíz." },
            
            // cos(x) - x
            { key: "cos(x) - x", method: "bisection", a: 0, b: 1, x0: 0.5, reason: "El intervalo [0.00, 1.00] cumple el Teorema de Bolzano (f(0) = 1.00 > 0 y f(1) ≈ -0.46 < 0). Además, la función es continua en todo el intervalo." },
            { key: "cos(x) - x", method: "newton", a: 0, b: 1, x0: 0.5, reason: "El punto inicial x₀ = 0.50 es seguro para Newton-Raphson puesto que la derivada f'(0.5) ≈ -1.48 es bastante lejana a cero." },
            { key: "cos(x) - x", method: "secant", a: 0, b: 1, x0: 0.5, reason: "Los valores iniciales [0.00, 1.00] son correctos para la Secante ya que f(0) = 1.00 y f(1) ≈ -0.46 son distintos." },
            { key: "cos(x) - x", method: "fixedpoint", a: 0, b: 1, x0: 0.5, g: "cos(x)", reason: "El punto inicial x₀ = 0.50 es adecuado para Punto Fijo." },

            // exp(-x) - x
            { key: "exp(-x) - x", method: "bisection", a: 0, b: 1, x0: 0.5, reason: "El intervalo [0.00, 1.00] es correcto para Bisección puesto que f(0) = 1.00 y f(1) ≈ -0.63 tienen signos contrarios." },
            { key: "exp(-x) - x", method: "newton", a: 0, b: 1, x0: 0.5, reason: "El punto inicial x₀ = 0.50 es óptimo para Newton puesto que f'(0.5) ≈ -1.61 no anula la derivada." },
            { key: "exp(-x) - x", method: "secant", a: 0, b: 1, x0: 0.5, reason: "Los puntos iniciales [0.00, 1.00] son válidos ya que f(0) y f(1) son distintos." },
            { key: "exp(-x) - x", method: "fixedpoint", a: 0, b: 1, x0: 0.5, g: "exp(-x)", reason: "El punto inicial x₀ = 0.50 es adecuado para Punto Fijo." },

            // x^2 + 2*x - 9
            { key: "x**2 + 2*x - 9", method: "bisection", a: 2, b: 3, x0: 2.2, reason: "La diferencia de signos en los extremos [2.00, 3.00] (f(2) = -1 y f(3) = 6) asegura que Bisección encerrará la raíz." },
            { key: "x**2 + 2*x - 9", method: "newton", a: 2, b: 3, x0: 2.2, reason: "El punto inicial x₀ = 2.20 es seguro para Newton ya que f'(2.2) = 6.40 es significativamente distinta de cero." },
            { key: "x**2 + 2*x - 9", method: "secant", a: 2, b: 3, x0: 2.2, reason: "Los valores iniciales [2.00, 3.00] son correctos para la Secante ya que f(2) = -1 y f(3) = 6 son distintos." },
            { key: "x**2 + 2*x - 9", method: "fixedpoint", a: 2, b: 3, x0: 2.2, g: "sqrt(9 - 2*x)", reason: "El punto inicial x₀ = 2.20 es adecuado para Punto Fijo." },

            // x^2 - 4
            { key: "x**2 - 4", method: "bisection", a: 1, b: 3, x0: 1.5, reason: "El intervalo [1.00, 3.00] cumple Bolzano puesto que f(1) = -3 y f(3) = 5 tienen signos opuestos." },
            { key: "x**2 - 4", method: "newton", a: 1, b: 3, x0: 1.5, reason: "El punto inicial x₀ = 1.50 es válido para Newton-Raphson porque la derivada f'(1.5) = 3.00 es lejana a cero." },
            { key: "x**2 - 4", method: "secant", a: 1, b: 3, x0: 1.5, reason: "Los puntos iniciales [1.00, 3.00] son correctos para la Secante puesto que f(1) y f(3) son diferentes." },
            { key: "x**2 - 4", method: "fixedpoint", a: 1, b: 3, x0: 1.5, g: "4/x", reason: "El punto inicial x₀ = 1.50 es adecuado para Punto Fijo." },

            // x^3 - 3*x (función de singularidad)
            { key: "x**3 - 3*x", method: "bisection", a: 1, b: 2.5, x0: 2.0, reason: "El intervalo [1.00, 2.50] cumple Bolzano (f(1) = -2 < 0 y f(2.5) ≈ 8.13 > 0) y evita el punto de derivada cero en x = 1." },
            { key: "x**3 - 3*x", method: "newton", a: 1, b: 2.5, x0: 2.0, reason: "El punto inicial x₀ = 2.00 es seguro para Newton puesto que f'(2) = 9.00 es distinta de cero y alejada de la singularidad en x = 1." },
            { key: "x**3 - 3*x", method: "secant", a: 1, b: 2.5, x0: 2.0, reason: "Los puntos [1.00, 2.50] son válidos para la Secante ya que f(1) = -2 y f(2.5) ≈ 8.13 son distintos." },
            { key: "x**3 - 3*x", method: "fixedpoint", a: 1, b: 2.5, x0: 2.0, g: "x**3 - 2*x", reason: "El punto inicial x₀ = 2.00 es seguro para Punto Fijo." },

            // x - 1/x (función de singularidad para Bisección)
            { key: "x - 1/x", method: "bisection", a: 0.5, b: 2.0, x0: 1.5, reason: "El intervalo [0.50, 2.00] es válido porque f(0.5) = -1.50 y f(2) = 1.50 tienen signos opuestos (cumple Bolzano) y evita el punto de singularidad (división por cero) en x = 0." },
            { key: "x - 1/x", method: "newton", a: 0.5, b: 2.0, x0: 1.5, reason: "El punto inicial x₀ = 1.50 evita la singularidad en x = 0 y la derivada f'(1.5) = 1.44 es segura (distinta de cero), convergiendo a la raíz x = 1.00." },
            { key: "x - 1/x", method: "secant", a: 0.5, b: 2.0, x0: 1.5, reason: "Los puntos iniciales [0.50, 2.00] evitan la singularidad en x = 0 y f(0.5) ≠ f(2), permitiendo calcular la secante correctamente hacia la raíz x = 1.00." },
            { key: "x - 1/x", method: "fixedpoint", a: 0.5, b: 2.0, x0: 1.5, g: "1/x", reason: "El punto inicial x₀ = 1.50 es adecuado para Punto Fijo." },

            // x^2 - 2 (función de singularidad para Secante)
            { key: "x**2 - 2", method: "bisection", a: 1.0, b: 2.0, x0: 1.5, reason: "El intervalo [1.00, 2.00] cumple Bolzano puesto que f(1) = -1 y f(2) = 2 tienen signos opuestos, conteniendo la raíz real √2 ≈ 1.414." },
            { key: "x**2 - 2", method: "newton", a: 1.0, b: 2.0, x0: 1.5, reason: "El punto inicial x₀ = 1.50 es válido para Newton-Raphson ya que la derivada f'(1.5) = 3.00 es lejana a cero." },
            { key: "x**2 - 2", method: "secant", a: 1.0, b: 2.0, x0: 1.5, reason: "Los puntos iniciales [1.00, 2.00] son válidos para la Secante ya que f(1) = -1 y f(2) = 2 tienen signos opuestos y no anulan el denominador." },
            { key: "x**2 - 2", method: "fixedpoint", a: 1.0, b: 2.0, x0: 1.5, g: "(x + 2/x)/2", reason: "El punto inicial x₀ = 1.50 con el método de Herón (g(x) = (x + 2/x)/2) converge de manera muy estable a la raíz √2." },

            // x - 1/(x - 1) (función de singularidad para Punto Fijo)
            { key: "x - 1/(x - 1)", method: "bisection", a: -0.8, b: 0.0, x0: -0.5, reason: "El intervalo [-0.80, 0.00] es válido porque f(-0.8) ≈ -0.24 y f(0) = 1.00 tienen signos opuestos (cumple Bolzano) y evita el punto de asíntota en x = 1." },
            { key: "x - 1/(x - 1)", method: "newton", a: -0.8, b: 0.0, x0: -0.5, reason: "El punto inicial x₀ = -0.50 es seguro para Newton puesto que f'(-0.5) = 1.44 no es cero y evita la singularidad en x = 1, convergiendo a la raíz negativa -0.618." },
            { key: "x - 1/(x - 1)", method: "secant", a: -0.8, b: 0.0, x0: -0.5, reason: "Los puntos iniciales [-0.80, 0.00] evitan la singularidad en x = 1 y f(-0.8) ≠ f(0), permitiendo iterar la secante hacia la raíz negativa -0.618." },
            { key: "x - 1/(x - 1)", method: "fixedpoint", a: -0.8, b: 0.0, x0: -0.5, g: "1/(x - 1)", reason: "El punto inicial x₀ = -0.50 converge de forma estable a la raíz negativa -0.618, ya que |g'(-0.618)| ≈ 0.38 < 1, cumpliendo el teorema de convergencia de Punto Fijo." }
        ];

        // Buscar coincidencia exacta de expresión y método
        let found = suggestions.find(s => s.key.replace(/\s+/g, "") === rawExpr.replace(/\s+/g, "") && s.method === method);
        
        // Si no se encuentra para el método actual, buscar cualquier método de esa función
        if (!found) {
            found = suggestions.find(s => s.key.replace(/\s+/g, "") === rawExpr.replace(/\s+/g, ""));
        }

        let reason = "";
        let isFallback = false;
        
        if (found) {
            // Si cambió de método, actualizar el select y disparar cambio
            if (methodSelect.value !== found.method) {
                methodSelect.value = found.method;
                methodSelect.dispatchEvent(new Event("change"));
            }
            aInput.value = found.a;
            bInput.value = found.b;
            x0Input.value = found.x0;
            if (found.method === "fixedpoint" && gExprInput && found.g) {
                gExprInput.value = found.g;
                if (typeof renderGMathPreview === "function") {
                    renderGMathPreview();
                }
            }
            reason = found.reason;
            
            // Efecto visual de brillo en sugerencia
            suggestBtn.style.boxShadow = "var(--shadow-glow)";
            setTimeout(() => suggestBtn.style.boxShadow = "none", 1000);
        } else {
            // Sugerencia genérica por defecto
            aInput.value = 0;
            bInput.value = 2;
            x0Input.value = 1.0;
            isFallback = true;
            
            if (method === "bisection" || method === "secant") {
                reason = "Se han establecido límites genéricos [0.00, 2.00] por defecto. Por favor, verifica de forma independiente que f(a)·f(b) < 0 antes de simular.";
            } else {
                reason = "Se ha establecido el punto inicial genérico x₀ = 1.00 por defecto. Por favor, verifica que f'(x₀) ≠ 0 antes de simular.";
            }
        }

        // Mostrar banner didáctico
        if (didacticAlert) {
            const alertIconSpan = didacticAlert.querySelector(".didactic-alert-icon");
            
            if (isFallback) {
                // Banner azul de información genérica
                didacticAlert.style.backgroundColor = "rgba(59, 130, 246, 0.1)";
                didacticAlert.style.borderColor = "var(--primary)";
                if (alertIconSpan) {
                    alertIconSpan.innerHTML = `<i class="fa-solid fa-circle-info" style="color: var(--primary);"></i>`;
                }
                alertTitle.textContent = "Parámetros Asignados (Por Defecto)";
                alertDescription.textContent = reason;
                alertRecommendation.textContent = "Consejo del Tutor: Revisa matemáticamente la función para ingresar límites o puntos iniciales adecuados.";
            } else {
                // Banner verde de éxito para sugerencia validada
                didacticAlert.style.backgroundColor = "var(--success-bg)";
                didacticAlert.style.borderColor = "var(--success)";
                if (alertIconSpan) {
                    alertIconSpan.innerHTML = `<i class="fa-solid fa-circle-check" style="color: var(--success);"></i>`;
                }
                alertTitle.textContent = "Parámetros Sugeridos Válidos";
                alertDescription.textContent = reason;
                alertRecommendation.textContent = "Consejo del Tutor: Ejecuta la simulación para visualizar cómo converge el algoritmo paso a paso.";
            }
            didacticAlert.style.display = "flex";
        }
    }

    // 3. Sliders de Dificultad Proporcionales que suman 100%
    function adjustSlidersProportionally(changedSlider) {
        let vEasy = parseInt(easySlider.value);
        let vMed = parseInt(mediumSlider.value);
        let vHard = parseInt(hardSlider.value);

        let total = vEasy + vMed + vHard;
        let diff = 100 - total;

        if (diff !== 0) {
            let activeSliders = [];
            if (easySlider !== changedSlider) activeSliders.push(easySlider);
            if (mediumSlider !== changedSlider) activeSliders.push(mediumSlider);
            if (hardSlider !== changedSlider) activeSliders.push(hardSlider);

            // Si hay sliders activos, repartimos la diferencia entre ellos de manera proporcional
            if (activeSliders.length > 0) {
                let sumActives = activeSliders.reduce((sum, s) => sum + parseInt(s.value), 0);
                
                if (sumActives === 0) {
                    // Si todos los otros son cero, asignamos la diferencia al primero activo
                    let val = parseInt(activeSliders[0].value) + diff;
                    activeSliders[0].value = Math.max(0, Math.min(100, val));
                } else {
                    activeSliders.forEach(s => {
                        let proportion = parseInt(s.value) / sumActives;
                        let val = Math.round(parseInt(s.value) + (diff * proportion));
                        s.value = Math.max(0, Math.min(100, val));
                    });
                }
            }
        }

        // Reajustar por si acaso el redondeo no sumó exactamente 100
        vEasy = parseInt(easySlider.value);
        vMed = parseInt(mediumSlider.value);
        vHard = parseInt(hardSlider.value);
        let currentTotal = vEasy + vMed + vHard;
        
        if (currentTotal !== 100) {
            let error = 100 - currentTotal;
            if (easySlider !== changedSlider) {
                easySlider.value = parseInt(easySlider.value) + error;
            } else {
                mediumSlider.value = parseInt(mediumSlider.value) + error;
            }
        }

        // Actualizar etiquetas visuales
        updateSliderLabels();
    }

    function updateSliderLabels() {
        const qTotal = parseInt(quizTotalQuestionsInput.value) || 10;
        
        let nEasy = Math.round((parseInt(easySlider.value) * qTotal) / 100);
        let nMed = Math.round((parseInt(mediumSlider.value) * qTotal) / 100);
        let nHard = qTotal - (nEasy + nMed);
        
        if (nHard < 0) {
            nHard = 0;
            nEasy = qTotal - nMed;
        }
        
        easyValueLabel.textContent = `${easySlider.value}% (${nEasy} preguntas)`;
        mediumValueLabel.textContent = `${mediumSlider.value}% (${nMed} preguntas)`;
        hardValueLabel.textContent = `${hardSlider.value}% (${nHard} preguntas)`;
    }

    // --- MOCK SIMULATOR RUNNER (OFFLINE MODE) ---
    
    // Función de evaluación matemática segura y básica para polinomios y trigonométricas sencillas
    function evaluateFunction(expr, x) {
        // Sanitizar y parsear términos habituales
        let formatted = expr.toLowerCase()
            .replace(/\s+/g, "")
            .replace(/sin\(/g, "Math.sin(")
            .replace(/cos\(/g, "Math.cos(")
            .replace(/tan\(/g, "Math.tan(")
            .replace(/exp\(/g, "Math.exp(")
            .replace(/log\(/g, "Math.log(")
            .replace(/sqrt\(/g, "Math.sqrt(")
            .replace(/\bpi\b/g, "Math.PI")
            .replace(/\be\b/g, "Math.E")
            .replace(/\^/g, "**");

        // Reemplazar la variable x con su valor numérico
        let evaluatedExpression = formatted.replace(/\bx\b/g, `(${x})`);
        
        try {
            // Evaluamos de manera controlada
            let result = new Function(`return ${evaluatedExpression}`)();
            if (isNaN(result) || !isFinite(result)) {
                throw new Error("indefinido");
            }
            return result;
        } catch (e) {
            throw new Error("singularidad");
        }
    }

    // Derivada numérica básica (Diferencia central) para Newton-Raphson
    function evaluateDerivative(expr, x) {
        const h = 1e-6;
        let fPlus = evaluateFunction(expr, x + h);
        let fMinus = evaluateFunction(expr, x - h);
        return (fPlus - fMinus) / (2 * h);
    }

    // 4. Correr Simulación Numérica
    function runSimulation() {
        const expression = expressionInput.value.trim();
        const method = methodSelect.value;
        const tol = parseFloat(toleranceInput.value);
        const maxIter = parseInt(maxIterInput.value);
        
        didacticAlert.style.display = "none";
        metricStatus.textContent = "Ejecutando...";
        metricStatus.className = "metric-card-value";

        const startTime = performance.now();
        let result = null;

        try {
            if (method === "bisection") {
                const a = parseFloat(aInput.value);
                const b = parseFloat(bInput.value);
                result = runBisectionLocal(expression, a, b, tol, maxIter);
            } else if (method === "secant") {
                const x0 = parseFloat(aInput.value);
                const x1 = parseFloat(bInput.value);
                result = runSecantLocal(expression, x0, x1, tol, maxIter);
            } else if (method === "newton") {
                const x0 = parseFloat(x0Input.value);
                result = runNewtonLocal(expression, x0, tol, maxIter);
            } else if (method === "fixedpoint") {
                const x0 = parseFloat(x0Input.value);
                const exprG = document.getElementById("g-expression-input").value.trim();
                
                // Verificar compatibilidad didáctica de g(x)
                try {
                    const compResult = checkGExpressionCompatibility(expression, exprG, x0);
                    if (!compResult.compatible) {
                        didacticAlert.style.backgroundColor = "rgba(245, 158, 11, 0.15)";
                        didacticAlert.style.borderColor = "#f59e0b";
                        const alertIconSpan = didacticAlert.querySelector(".didactic-alert-icon");
                        if (alertIconSpan) {
                            alertIconSpan.innerHTML = `<i class="fa-solid fa-triangle-exclamation" style="color: #f59e0b;"></i>`;
                        }
                        alertTitle.textContent = "¡Advertencia: g(x) Incompatible!";
                        let rootText = compResult.root.toFixed(6);
                        let gValText = compResult.gVal !== null ? compResult.gVal.toFixed(6) : "indefinido/error";
                        alertDescription.textContent = `La función de iteración g(x) = ${exprG} no parece ser un despeje matemáticamente compatible con f(x) = 0. En la raíz real de f(x) cercana (x ≈ ${rootText}), evaluar g(x) resulta en ${gValText}, lo cual viola la condición fundamental de Punto Fijo g(r) = r (diferencia de ${(compResult.discrepancy !== null ? compResult.discrepancy.toFixed(4) : "N/A")}).`;
                        alertRecommendation.textContent = "Consejo del Tutor: Asegúrate de despejar la variable 'x' de forma válida a partir de f(x) = 0. Por ejemplo, para x³ - x - 2 = 0, despejes correctos incluyen g(x) = (x + 2)**(1/3) o g(x) = x³ - 2. Recuerda que las potencias se ingresan con '**'.";
                        didacticAlert.style.display = "flex";
                    }
                } catch (err) {
                    // Ignorar fallas de validación
                }

                result = runFixedPointLocal(exprG, expression, x0, tol, maxIter);
            }
            const endTime = performance.now();
            const elapsed = ((endTime - startTime) / 1000).toFixed(6);

            // Mostrar resultados
            metricStatus.textContent = result.status;
            metricStatus.className = "metric-card-value";
            
            if (result.status === "success") {
                metricStatus.classList.add("badge-success");
            } else if (result.status === "singularidad" || result.status === "bolzano_violation") {
                metricStatus.classList.add("badge-danger");
            } else {
                metricStatus.classList.add("badge-warning");
            }

            metricRoot.textContent = (result.root !== null && !isNaN(result.root)) ? result.root.toFixed(8) : "N/A";
            metricIter.textContent = result.iterations.length;
            metricTime.textContent = elapsed;

            // Llenar tabla
            populateIterationsTable(result.iterations, method);

            // Graficar
            plotFunctionGraph(expression, result.iterations, result.root, method, result.status);

            // Mostrar Alertas Didácticas Específicas
            if (result.status === "singularidad") {
                didacticAlert.style.backgroundColor = "var(--danger-bg)";
                didacticAlert.style.borderColor = "var(--danger)";
                const alertIconSpan = didacticAlert.querySelector(".didactic-alert-icon");
                if (alertIconSpan) {
                    alertIconSpan.innerHTML = `<i class="fa-solid fa-triangle-exclamation" style="color: var(--danger);"></i>`;
                }
                alertTitle.textContent = "¡Derivada Cero o Singularidad!";
                alertDescription.textContent = "El algoritmo se ha interrumpido porque en la iteración actual se encontró un punto de singularidad o una derivada igual a cero (f'(x) = 0), impidiendo realizar la división de proyección.";
                alertRecommendation.textContent = "Recomendación del Tutor: Modifica el punto inicial (x₀) a un valor más lejano del extremo/máximo de la curva, o cambia el método a Bisección (método cerrado) que no depende de derivadas.";
                didacticAlert.style.display = "flex";
            } else if (result.status === "bolzano_violation") {
                didacticAlert.style.backgroundColor = "var(--danger-bg)";
                didacticAlert.style.borderColor = "var(--danger)";
                const alertIconSpan = didacticAlert.querySelector(".didactic-alert-icon");
                if (alertIconSpan) {
                    alertIconSpan.innerHTML = `<i class="fa-solid fa-triangle-exclamation" style="color: var(--danger);"></i>`;
                }
                alertTitle.textContent = "Error de Intervalo Inicial";
                alertDescription.textContent = "El teorema de Bolzano no se cumple ya que f(a) y f(b) tienen el mismo signo. No se puede garantizar la existencia de una raíz en este intervalo.";
                alertRecommendation.textContent = "Sugerencia: Haz clic en el botón '✨ Sugerir Valores' o cambia los límites del intervalo para que rodeen la intersección con el eje X.";
                didacticAlert.style.display = "flex";
            }

            // Guardar en el Historial
            saveToHistory(expression, method, result.root, result.iterations.length, result.status);

        } catch (err) {
            const endTime = performance.now();
            metricStatus.textContent = "error";
            metricStatus.className = "metric-card-value badge-danger";
            metricRoot.textContent = "N/A";
            metricIter.textContent = "-";
            metricTime.textContent = ((endTime - startTime) / 1000).toFixed(6);
            
            // Limpiar tabla
            tableBody.innerHTML = `<tr><td colspan="6" style="text-align: center; color: var(--danger);">Ocurrió un error al evaluar la función.</td></tr>`;

            // Mostrar Alerta General
            didacticAlert.style.backgroundColor = "var(--danger-bg)";
            didacticAlert.style.borderColor = "var(--danger)";
            const alertIconSpan = didacticAlert.querySelector(".didactic-alert-icon");
            if (alertIconSpan) {
                alertIconSpan.innerHTML = `<i class="fa-solid fa-triangle-exclamation" style="color: var(--danger);"></i>`;
            }
            alertTitle.textContent = "Error en la Simulación";
            alertDescription.textContent = "Hubo un problema al evaluar la función. Asegúrate de ingresar una expresión matemática válida (ej. x^3 - 3*x o sin(x)).";
            alertRecommendation.textContent = "Sugerencia: Revisa la sintaxis de la función y los valores de entrada.";
            didacticAlert.style.display = "flex";
            
            renderEmptyPlot();
        }
    }

    // Algoritmo local de Bisección
    function runBisectionLocal(expr, a, b, tol, maxIter) {
        let fa, fb;
        try {
            fa = evaluateFunction(expr, a);
            fb = evaluateFunction(expr, b);
        } catch (err) {
            return {
                root: null,
                iterations: [],
                status: "singularidad"
            };
        }

        if (fa * fb >= 0) {
            return {
                root: null,
                iterations: [],
                status: "bolzano_violation"
            };
        }

        let iterations = [];
        let root = null;
        let status = "max_iter";

        for (let i = 1; i <= maxIter; i++) {
            try {
                let c = (a + b) / 2;
                let fc = evaluateFunction(expr, c);
                let err = Math.abs(b - a) / 2;

                iterations.push({
                    iter: i,
                    xi: a,
                    sup: b,
                    root: c,
                    error: i === 1 ? "-" : err.toFixed(8),
                    residual: fc
                });

                if (err < tol || Math.abs(fc) < 1e-12) {
                    root = c;
                    status = "success";
                    break;
                }

                if (fa * fc < 0) {
                    b = c;
                    fb = fc;
                } else {
                    a = c;
                    fa = fc;
                }
            } catch (err) {
                status = "singularidad";
                iterations.push({
                    iter: i,
                    xi: a,
                    sup: b,
                    root: null,
                    error: "FALLO",
                    residual: null
                });
                break;
            }
        }

        if (!root && iterations.length > 0) {
            let lastIter = iterations[iterations.length - 1];
            if (lastIter.root !== null) {
                root = lastIter.root;
            }
        }

        return { root, iterations, status };
    }

    // Algoritmo local de Newton-Raphson
    function runNewtonLocal(expr, x0, tol, maxIter) {
        let iterations = [];
        let root = null;
        let status = "max_iter";
        let x = x0;

        for (let i = 1; i <= maxIter; i++) {
            try {
                let fx = evaluateFunction(expr, x);
                let dfx = evaluateDerivative(expr, x);

                // Detección de singularidad (derivada cero)
                if (Math.abs(dfx) < 1e-3) {
                    status = "singularidad";
                    iterations.push({
                        iter: i,
                        xi: x,
                        sup: null,
                        root: null,
                        error: "FALLO",
                        residual: fx
                    });
                    break;
                }

                let nextX = x - (fx / dfx);
                let err = Math.abs(nextX - x);
                let relErr = nextX !== 0 ? err / Math.abs(nextX) : 0;

                iterations.push({
                    iter: i,
                    xi: x,
                    sup: nextX,
                    root: nextX,
                    error: i === 1 ? "-" : relErr.toFixed(8),
                    residual: fx
                });

                if (err < tol || Math.abs(fx) < 1e-12) {
                    root = nextX;
                    status = "success";
                    break;
                }

                x = nextX;
            } catch (err) {
                status = "singularidad";
                iterations.push({
                    iter: i,
                    xi: x,
                    sup: null,
                    root: null,
                    error: "FALLO",
                    residual: null
                });
                break;
            }
        }

        if (!root && iterations.length > 0) {
            for (let i = iterations.length - 1; i >= 0; i--) {
                if (typeof iterations[i].sup === 'number' && !isNaN(iterations[i].sup)) {
                    root = iterations[i].sup;
                    break;
                }
            }
        }

        return { root, iterations, status };
    }

    // Algoritmo local de Secante
    function runSecantLocal(expr, x0, x1, tol, maxIter) {
        let iterations = [];
        let root = null;
        let status = "max_iter";

        for (let i = 1; i <= maxIter; i++) {
            try {
                let fx0 = evaluateFunction(expr, x0);
                let fx1 = evaluateFunction(expr, x1);
                let denominator = fx1 - fx0;

                if (Math.abs(denominator) < 1e-12) {
                    status = "singularidad";
                    iterations.push({
                        iter: i,
                        xi: x0,
                        sup: x1,
                        root: null,
                        error: "FALLO",
                        residual: fx1
                    });
                    break;
                }

                let x2 = x1 - fx1 * (x1 - x0) / denominator;
                let fx2 = evaluateFunction(expr, x2);
                let err = Math.abs(x2 - x1);

                iterations.push({
                    iter: i,
                    xi: x0,
                    sup: x1,
                    root: x2,
                    error: i === 1 ? "-" : err.toFixed(8),
                    residual: fx2
                });

                if (Math.abs(fx2) < tol || err < tol) {
                    root = x2;
                    status = "success";
                    break;
                }

                x0 = x1;
                x1 = x2;
            } catch (err) {
                status = "singularidad";
                iterations.push({
                    iter: i,
                    xi: x0,
                    sup: x1,
                    root: null,
                    error: "FALLO",
                    residual: null
                });
                break;
            }
        }

        if (!root && iterations.length > 0) {
            let lastIter = iterations[iterations.length - 1];
            if (lastIter.root !== null) {
                root = lastIter.root;
            }
        }

        return { root, iterations, status };
    }

    // Algoritmo local de Punto Fijo
    function runFixedPointLocal(exprG, exprF, x0, tol, maxIter) {
        let iterations = [];
        let root = null;
        let status = "max_iter";
        let xVal = x0;

        for (let i = 1; i <= maxIter; i++) {
            try {
                let nextX = evaluateFunction(exprG, xVal);
                let diff = Math.abs(nextX - xVal);
                let relErr = nextX !== 0 ? diff / Math.abs(nextX) : 0;

                // residual f(x)
                let fVal = exprF ? evaluateFunction(exprF, xVal) : (xVal - nextX);

                iterations.push({
                    iter: i,
                    xi: xVal,
                    sup: nextX,
                    root: nextX,
                    error: i === 1 ? "-" : relErr.toFixed(8),
                    residual: fVal
                });

                if (diff < tol) {
                    root = nextX;
                    status = "success";
                    break;
                }

                xVal = nextX;
            } catch (err) {
                status = "singularidad";
                iterations.push({
                    iter: i,
                    xi: xVal,
                    sup: null,
                    root: null,
                    error: "FALLO",
                    residual: null
                });
                break;
            }
        }

        if (!root && iterations.length > 0) {
            for (let i = iterations.length - 1; i >= 0; i--) {
                if (typeof iterations[i].sup === 'number' && !isNaN(iterations[i].sup)) {
                    root = iterations[i].sup;
                    break;
                }
            }
        }

        return { root, iterations, status };
    }

    // Validación didáctica de correspondencia de g(x) con f(x)
    function checkGExpressionCompatibility(exprF, exprG, x0) {
        let root = null;
        let x = x0;
        const tol = 1e-7;
        const maxIter = 100;

        for (let i = 0; i < maxIter; i++) {
            try {
                let fx = evaluateFunction(exprF, x);
                let dfx = evaluateDerivative(exprF, x);
                if (Math.abs(dfx) < 1e-12) {
                    break;
                }
                let nextX = x - (fx / dfx);
                if (Math.abs(nextX - x) < tol) {
                    if (Math.abs(evaluateFunction(exprF, nextX)) < 1e-5) {
                        root = nextX;
                    }
                    break;
                }
                x = nextX;
            } catch (err) {
                break;
            }
        }

        if (root === null) {
            const scanPoints = [x0 - 1.0, x0 + 1.0, x0 - 0.5, x0 + 0.5, x0 - 2.0, x0 + 2.0];
            for (let startPt of scanPoints) {
                let currX = startPt;
                let found = false;
                for (let j = 0; j < 30; j++) {
                    try {
                        let fx = evaluateFunction(exprF, currX);
                        let dfx = evaluateDerivative(exprF, currX);
                        if (Math.abs(dfx) < 1e-12) break;
                        let nextX = currX - (fx / dfx);
                        if (Math.abs(nextX - currX) < tol) {
                            if (Math.abs(evaluateFunction(exprF, nextX)) < 1e-5) {
                                root = nextX;
                                found = true;
                            }
                            break;
                        }
                        currX = nextX;
                    } catch (e) {
                        break;
                    }
                }
                if (found) break;
            }
        }

        if (root !== null) {
            try {
                let gVal = evaluateFunction(exprG, root);
                let diff = Math.abs(gVal - root);
                if (diff > 0.005) {
                    return { compatible: false, root: root, gVal: gVal, discrepancy: diff };
                }
            } catch (err) {
                return { compatible: false, root: root, gVal: null, discrepancy: null };
            }
        }

        return { compatible: true };
    }

    // 5. Rellenar Tabla
    function populateIterationsTable(iterations, method) {
        tableBody.innerHTML = "";
        
        // Ajustar columnas de la cabecera
        const headers = document.getElementById("table-headers");
        if (method === "bisection") {
            headers.innerHTML = `<th>Iteración</th><th>a (Lím. Inf)</th><th>b (Lím. Sup)</th><th>c (Raíz Aprox.)</th><th>Error Rel.</th><th>Residual f(x)</th>`;
        } else if (method === "secant") {
            headers.innerHTML = `<th>Iteración</th><th>x_{i-1} (Anterior)</th><th>x_i (Actual)</th><th>x_{i+1} (Siguiente)</th><th>Diferencia</th><th>Residual f(x)</th>`;
        } else {
            headers.innerHTML = `<th>Iteración</th><th>x_i (Actual)</th><th>x_{i+1} (Siguiente)</th><th>Diferencia</th><th>Error Rel.</th><th>Residual f(x)</th>`;
        }

        iterations.forEach(row => {
            const tr = document.createElement("tr");
            
            let residualText = "-";
            let residualColor = "inherit";
            if (typeof row.residual === 'number' && !isNaN(row.residual)) {
                residualText = row.residual.toExponential(4);
                if (Math.abs(row.residual) < 1e-5) {
                    residualColor = "var(--success)";
                }
            } else if (row.residual !== null && row.residual !== undefined) {
                residualText = row.residual.toString();
            }

            let xiText = typeof row.xi === 'number' ? row.xi.toFixed(8) : row.xi;
            let supText = typeof row.sup === 'number' ? row.sup.toFixed(8) : row.sup;
            let rootText = typeof row.root === 'number' ? row.root.toFixed(8) : (row.root === null ? "[FALLO]" : row.root);
            let errorText = row.error;

            tr.innerHTML = `
                <td style="text-align: center; font-weight: 600; color: var(--text-secondary);">${row.iter}</td>
                <td>${xiText}</td>
                <td>${supText}</td>
                <td>${rootText}</td>
                <td>${errorText}</td>
                <td style="font-family: 'Fira Code', monospace; color: ${residualColor};">${residualText}</td>
            `;
            tableBody.appendChild(tr);
        });
    }

    // 6. Graficar función en Plotly.js
    function plotFunctionGraph(expr, iterations, root, method, status) {
        // Encontrar rango x
        let xMin = -2;
        let xMax = 4;
        
        if (iterations.length > 0) {
            let xs = iterations.map(it => it.xi).filter(x => typeof x === 'number' && !isNaN(x) && isFinite(x));
            if (root !== null && !isNaN(root) && isFinite(root)) xs.push(root);
            iterations.forEach(it => {
                if (typeof it.sup === 'number' && !isNaN(it.sup) && isFinite(it.sup)) xs.push(it.sup);
                if (typeof it.root === 'number' && !isNaN(it.root) && isFinite(it.root)) xs.push(it.root);
            });
            let minVal = xs.length > 0 ? Math.min(...xs) : -2;
            let maxVal = xs.length > 0 ? Math.max(...xs) : 4;
            if (minVal === maxVal) {
                xMin = minVal - 2;
                xMax = maxVal + 2;
            } else {
                xMin = minVal - Math.abs(maxVal - minVal) * 0.4 - 1;
                xMax = maxVal + Math.abs(maxVal - minVal) * 0.4 + 1;
            }
        }

        // Generar puntos de la función
        let xPlot = [];
        let yPlot = [];
        const steps = 200;
        const dx = (xMax - xMin) / steps;

        for (let i = 0; i <= steps; i++) {
            let x = xMin + i * dx;
            try {
                let y = evaluateFunction(expr, x);
                xPlot.push(x);
                yPlot.push(y);
            } catch (e) {
                // Saltar singularidades para no graficar líneas locas
                xPlot.push(x);
                yPlot.push(null);
            }
        }

        // Curva de la función
        let traceFunc = {
            x: xPlot,
            y: yPlot,
            type: 'scatter',
            mode: 'lines',
            name: 'f(x)',
            line: { color: '#3b82f6', width: 3 }
        };

        // Eje X (Y = 0)
        let traceAxis = {
            x: [xMin, xMax],
            y: [0, 0],
            type: 'scatter',
            mode: 'lines',
            name: 'Eje X',
            line: { color: 'rgba(255, 255, 255, 0.15)', width: 1.5, dash: 'dash' },
            showlegend: false
        };

        let traces = [traceFunc, traceAxis];

        if (root !== null && !isNaN(root)) {
            traces.push({
                x: [root],
                y: [0],
                type: 'scatter',
                mode: 'markers',
                name: 'Raíz Aprox.',
                marker: { color: '#10b981', size: 10, line: { color: '#0f1624', width: 2 } }
            });
        }

        // Si es Newton-Raphson, trazamos la última tangente didáctica exitosa
        if (method === "newton" && iterations.length > 0) {
            let successfulIt = null;
            for (let i = iterations.length - 1; i >= 0; i--) {
                if (typeof iterations[i].root === 'number' && !isNaN(iterations[i].root)) {
                    successfulIt = iterations[i];
                    break;
                }
            }
            if (successfulIt) {
                let xVal = successfulIt.xi;
                let yVal = successfulIt.residual;
                
                traces.push({
                    x: [xVal, successfulIt.root],
                    y: [yVal, 0],
                    type: 'scatter',
                    mode: 'lines+markers',
                    name: 'Última Tangente',
                    line: { color: '#f59e0b', width: 1.5, dash: 'dot' },
                    marker: { color: '#f59e0b', size: 6 }
                });
            }
        }

        // Si es Secante, trazamos la última secante didáctica exitosa
        if (method === "secant" && iterations.length > 0) {
            let successfulIt = null;
            for (let i = iterations.length - 1; i >= 0; i--) {
                if (typeof iterations[i].root === 'number' && !isNaN(iterations[i].root)) {
                    successfulIt = iterations[i];
                    break;
                }
            }
            if (successfulIt) {
                let x0 = successfulIt.xi;
                let x1 = successfulIt.sup;
                let y0 = null;
                let y1 = null;
                try { y0 = evaluateFunction(expr, x0); } catch(e){}
                try { y1 = evaluateFunction(expr, x1); } catch(e){}
                
                if (y0 !== null && y1 !== null) {
                    traces.push({
                        x: [x0, x1, successfulIt.root],
                        y: [y0, y1, 0],
                        type: 'scatter',
                        mode: 'lines+markers',
                        name: 'Última Secante',
                        line: { color: '#f59e0b', width: 1.5, dash: 'dot' },
                        marker: { color: '#f59e0b', size: 6 }
                    });
                }
            }
        }

        // Si es Bisección, trazamos los límites del intervalo de la última iteración exitosa
        if (method === "bisection" && iterations.length > 0) {
            let successfulIt = null;
            for (let i = iterations.length - 1; i >= 0; i--) {
                if (typeof iterations[i].root === 'number' && !isNaN(iterations[i].root)) {
                    successfulIt = iterations[i];
                    break;
                }
            }
            if (successfulIt) {
                // Usamos los límites de la primera iteración para mostrar el intervalo inicial completo en la gráfica
                let aVal = iterations[0].xi;
                let bVal = iterations[0].sup;
                let yRange = yPlot.filter(y => y !== null);
                let yMinVal = yRange.length > 0 ? Math.min(...yRange) : -10;
                let yMaxVal = yRange.length > 0 ? Math.max(...yRange) : 10;
                
                traces.push({
                    x: [aVal, aVal],
                    y: [yMinVal, yMaxVal],
                    type: 'scatter',
                    mode: 'lines',
                    name: 'Intervalo a',
                    line: { color: '#8b5cf6', width: 1, dash: 'dash' }
                });
                traces.push({
                    x: [bVal, bVal],
                    y: [yMinVal, yMaxVal],
                    type: 'scatter',
                    mode: 'lines',
                    name: 'Intervalo b',
                    line: { color: '#ec4899', width: 1, dash: 'dash' }
                });
            }
        }

        // Si terminó con singularidad o error, graficamos la asíntota de fallo en la gráfica activa
        if ((status === "singularidad" || status === "error") && iterations.length > 0) {
            let lastIt = iterations[iterations.length - 1];
            let singularityX = lastIt.xi;
            if (method === "bisection" && typeof lastIt.sup === 'number') {
                singularityX = (lastIt.xi + lastIt.sup) / 2;
            }
            if (typeof singularityX === 'number' && !isNaN(singularityX)) {
                let yRange = yPlot.filter(y => y !== null);
                let yMinVal = yRange.length > 0 ? Math.min(...yRange) : -10;
                let yMaxVal = yRange.length > 0 ? Math.max(...yRange) : 10;
                
                traces.push({
                    x: [singularityX, singularityX],
                    y: [yMinVal, yMaxVal],
                    type: 'scatter',
                    mode: 'lines',
                    name: 'Asíntota/Singularidad (Fallo)',
                    line: { color: '#ef4444', width: 2, dash: 'dash' }
                });
            }
        }

        let layout = {
            paper_bgcolor: 'rgba(0,0,0,0)',
            plot_bgcolor: 'rgba(0,0,0,0)',
            font: { color: '#94a3b8', family: 'Outfit, sans-serif' },
            margin: { t: 20, b: 40, l: 50, r: 20 },
            xaxis: { gridcolor: 'rgba(255, 255, 255, 0.05)', zeroline: false },
            yaxis: { gridcolor: 'rgba(255, 255, 255, 0.05)', zeroline: false },
            showlegend: true,
            legend: { x: 0, y: 1 }
        };

        Plotly.newPlot('plot-container', traces, layout, { responsive: true, displayModeBar: false });
    }

    // Grafica inicial vacía
    function renderEmptyPlot() {
        let trace = {
            x: [-5, 5],
            y: [-5, 5],
            type: 'scatter',
            mode: 'lines',
            line: { color: 'rgba(255,255,255,0.05)' }
        };
        let layout = {
            paper_bgcolor: 'rgba(0,0,0,0)',
            plot_bgcolor: 'rgba(0,0,0,0)',
            font: { color: '#64748b' },
            margin: { t: 20, b: 40, l: 50, r: 20 }
        };
        Plotly.newPlot('plot-container', [trace], layout, { responsive: true, displayModeBar: false });
    }

    // 7. Mostrar Alerta Didáctica de Singularidad y dibujar asíntota
    function showSingularAlert(expr, method) {
        alertTitle.textContent = "¡Derivada Cero o Singularidad!";
        alertDescription.textContent = "El algoritmo se ha interrumpido porque en la iteración actual se encontró un punto de singularidad o una derivada igual a cero (f'(x) = 0), impidiendo realizar la división de proyección.";
        alertRecommendation.textContent = "Recomendación del Tutor: Modifica el punto inicial (x0) a un valor más lejano del extremo/máximo de la curva, o cambia el método a Bisección (método cerrado) que no depende de derivadas.";
        didacticAlert.style.display = "flex";

        // Graficar singularidad aproximada
        let lastVal = method === "bisection" ? parseFloat(aInput.value) : parseFloat(x0Input.value);
        
        let traceFunc = {
            x: [lastVal, lastVal],
            y: [-10, 10],
            type: 'scatter',
            mode: 'lines',
            name: 'Singularidad (Fallo)',
            line: { color: '#ef4444', width: 2, dash: 'dash' }
        };

        let layout = {
            paper_bgcolor: 'rgba(0,0,0,0)',
            plot_bgcolor: 'rgba(0,0,0,0)',
            font: { color: '#94a3b8' },
            margin: { t: 20, b: 40, l: 50, r: 20 }
        };
        Plotly.newPlot('plot-container', [traceFunc], layout, { responsive: true, displayModeBar: false });
    }

    // 8. Guardar simulaciones en Historial y persistencia
    function saveToHistory(expr, method, root, iters, status) {
        let record = {
            id: Date.now(),
            expr,
            method,
            root: root !== null ? root.toFixed(6) : "N/A",
            iters,
            status,
            date: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        };
        history.unshift(record);
        if (history.length > 5) history.pop(); // Solo guardamos las últimas 5 en esta sesión
        localStorage.setItem("simulations_history", JSON.stringify(history));
        updateHistoryUI();
    }

    function updateHistoryUI() {
        if (history.length === 0) {
            historyList.innerHTML = `<div class="text-muted" style="font-size: 0.9rem; text-align: center; padding: 1rem;">No hay simulaciones en esta sesión.</div>`;
            return;
        }
        historyList.innerHTML = "";
        history.forEach(item => {
            const div = document.createElement("div");
            div.className = "history-item";
            
            // Traducir método
            let methodLabel = "Newton-Raphson";
            if (item.method === "bisection") methodLabel = "Bisección";
            else if (item.method === "secant") methodLabel = "Secante";
            else if (item.method === "fixedpoint") methodLabel = "Punto Fijo";

            // Clase de distintivo
            let badgeClass = "badge-warning";
            if (item.status === "success") {
                badgeClass = "badge-success";
            } else if (item.status === "singularidad" || item.status === "bolzano_violation") {
                badgeClass = "badge-danger";
            }

            div.innerHTML = `
                <div class="history-item-header">
                    <span class="history-item-title">${item.expr}</span>
                    <span class="badge ${badgeClass}">${item.status}</span>
                </div>
                <div class="history-item-header" style="margin-top: 0.25rem;">
                    <span class="history-item-meta">${methodLabel} | Raíz: ${item.root}</span>
                    <span class="history-item-meta" style="font-size: 0.75rem;">${item.date}</span>
                </div>
            `;
            // Cargar de nuevo al simulador
            div.addEventListener("click", () => {
                expressionInput.value = item.expr;
                methodSelect.value = item.method;
                methodSelect.dispatchEvent(new Event("change"));
                renderMathPreview();
                resetSimulationOutputs();
            });
            historyList.appendChild(div);
        });
    }

    // --- MÓDULO DEL TUTOR DIDÁCTICO (EL GENERADOR) ---

    const databaseQuestions = [
        {
            type: "theoretical",
            difficulty: "easy",
            question: "¿Qué condición matemática garantiza la existencia de al menos una raíz de f(x) en el intervalo [a, b] según el Teorema del Valor Intermedio (Bolzano)?",
            options: [
                "f(a) y f(b) deben ser mayores que cero.",
                "f(a) y f(b) deben tener signos opuestos (f(a) * f(b) < 0) y f(x) debe ser continua.",
                "La derivada f'(x) debe ser constante en todo el dominio."
            ],
            correct: 1,
            feedback: "El teorema de Bolzano requiere obligatoriamente que la función sea continua en el intervalo y que sus extremos tengan signos opuestos para asegurar el cruce con el eje X."
        },
        {
            type: "theoretical",
            difficulty: "easy",
            question: "¿Cuál de los siguientes es un método cerrado (también conocido como método de intervalo)?",
            options: [
                "Método de Newton-Raphson",
                "Método de la Secante",
                "Método de Bisección"
            ],
            correct: 2,
            feedback: "Bisección es un método cerrado porque requiere dos límites iniciales que rodeen la raíz y siempre converge de forma segura, aunque más lenta."
        },
        {
            type: "practical",
            difficulty: "easy",
            question: "Si aplicamos el método de bisección en el intervalo [1, 2], ¿cuál es el punto medio c calculado en la primera iteración?",
            options: [
                "c = 1.25",
                "c = 1.5",
                "c = 1.75"
            ],
            correct: 1,
            feedback: "La fórmula para el punto medio es c = (a + b) / 2. Por lo tanto, c = (1 + 2) / 2 = 1.5."
        },
        {
            type: "practical",
            difficulty: "easy",
            question: "En el método de la Secante, si los puntos iniciales son x₀ = 0 y x₁ = 1, y los valores de la función son f(x₀) = -1 y f(x₁) = 1, ¿cuál es el valor de la aproximación x₂?",
            options: [
                "x₂ = 0.5",
                "x₂ = 0.75",
                "x₂ = 1.5"
            ],
            correct: 0,
            feedback: "La fórmula de la Secante es x₂ = x₁ - f(x₁)(x₁ - x₀)/(f(x₁) - f(x₀)). Sustituyendo: x₂ = 1 - 1*(1 - 0)/(1 - (-1)) = 1 - 0.5 = 0.5."
        },
        {
            type: "theoretical",
            difficulty: "medium",
            question: "¿Cuál es el principal riesgo al utilizar el método abierto de Newton-Raphson cerca de un punto crítico (un extremo local)?",
            options: [
                "El error relativo se hace cero instantáneamente.",
                "La derivada f'(x) se aproxima a cero, provocando una división por cero (singularidad) y posible divergencia.",
                "El método cambia automáticamente al método de la secante."
            ],
            correct: 1,
            feedback: "En Newton-Raphson, la división se hace sobre la derivada f'(x). Si la derivada es cero (tangente horizontal), el paso tiende a infinito y el método falla."
        },
        {
            type: "theoretical",
            difficulty: "medium",
            question: "¿Cómo es la velocidad de convergencia del método de Newton-Raphson en comparación con el de Bisección para raíces simples?",
            options: [
                "Newton-Raphson tiene convergencia cuadrática (más rápida), mientras que Bisección es lineal (lenta).",
                "Bisección converge cuadráticamente y Newton linealmente.",
                "Ambos tienen exactamente la misma tasa de convergencia."
            ],
            correct: 0,
            feedback: "Newton-Raphson duplica aproximadamente el número de dígitos significativos en cada paso (convergencia cuadrática), superando ampliamente la convergencia lineal de Bisección."
        },
        {
            type: "practical",
            difficulty: "medium",
            question: "Sea f(x) = x² - 2. Si usamos el método de Newton-Raphson con una aproximación inicial x₀ = 2, ¿cuál es el valor de x₁ tras la primera iteración?",
            options: [
                "x₁ = 1.5",
                "x₁ = 1.414",
                "x₁ = 1.25"
            ],
            correct: 0,
            feedback: "En Newton-Raphson: x₁ = x₀ - f(x₀)/f'(x₀). Aquí f'(x) = 2x. Para x₀ = 2, f(2) = 2 y f'(2) = 4. Por lo tanto, x₁ = 2 - 2/4 = 1.5."
        },
        {
            type: "theoretical",
            difficulty: "hard",
            question: "Si una función posee una raíz de multiplicidad m > 1, ¿qué le ocurre al método estándar de Newton-Raphson al aproximarse a ella?",
            options: [
                "Sigue convergiendo cuadráticamente sin cambios.",
                "La velocidad de convergencia disminuye de cuadrática a lineal.",
                "El método oscila infinitamente y entra en bucle cerrado."
            ],
            correct: 1,
            feedback: "Para raíces múltiples, la derivada f'(x) también se hace cero en la raíz, lo que degrada la velocidad de convergencia de Newton-Raphson a lineal."
        },
        {
            type: "practical",
            difficulty: "hard",
            question: "Para resolver la ecuación x - cos(x) = 0 usando el método de Punto Fijo con la función de iteración g(x) = cos(x) y valor inicial x₀ = 0.5, ¿cuál es el valor aproximado de x₁ redondeado a tres decimales?",
            options: [
                "x₁ = 0.878",
                "x₁ = 0.732",
                "x₁ = 0.542"
            ],
            correct: 0,
            feedback: "Evaluando la función de iteración: x₁ = g(x₀) = cos(0.5 rad) ≈ 0.87758. Redondeado a tres decimales es 0.878."
        }
    ];

    function startQuiz() {
        tutorSetup.style.display = "none";
        quizFocusContainer.style.display = "block";
        quizResultsContainer.style.display = "none";

        // Generar preguntas basadas en la dificultad seleccionada
        const qTotal = parseInt(quizTotalQuestionsInput.value) || 10;
        const timeLimit = parseInt(quizTimeLimitInput.value) || 10;

        let nEasy = Math.round((parseInt(easySlider.value) * qTotal) / 100);
        let nMed = Math.round((parseInt(mediumSlider.value) * qTotal) / 100);
        let nHard = qTotal - (nEasy + nMed);
        
        if (nHard < 0) {
            nHard = 0;
            nEasy = qTotal - nMed;
        }

        let poolEasy = databaseQuestions.filter(q => q.difficulty === "easy" && q.type === quizModes.easy);
        if (poolEasy.length === 0) poolEasy = databaseQuestions.filter(q => q.difficulty === "easy");

        let poolMed = databaseQuestions.filter(q => q.difficulty === "medium" && q.type === quizModes.medium);
        if (poolMed.length === 0) poolMed = databaseQuestions.filter(q => q.difficulty === "medium");

        let poolHard = databaseQuestions.filter(q => q.difficulty === "hard" && q.type === quizModes.hard);
        if (poolHard.length === 0) poolHard = databaseQuestions.filter(q => q.difficulty === "hard");

        // Mezclar y tomar cantidad solicitada
        currentQuizQuestions = [
            ...shuffleArray(poolEasy).slice(0, nEasy),
            ...shuffleArray(poolMed).slice(0, nMed),
            ...shuffleArray(poolHard).slice(0, nHard)
        ];

        // Rellenar de forma segura si nos faltan preguntas
        if (currentQuizQuestions.length < qTotal) {
            let remaining = databaseQuestions.filter(q => !currentQuizQuestions.includes(q));
            currentQuizQuestions = [...currentQuizQuestions, ...shuffleArray(remaining).slice(0, qTotal - currentQuizQuestions.length)];
        }

        // Asegurarnos de tener al menos 3 preguntas para test
        if (currentQuizQuestions.length === 0) {
            currentQuizQuestions = [...databaseQuestions];
        }

        currentQuestionIndex = 0;
        userAnswers = new Array(currentQuizQuestions.length).fill(null);

        // Iniciar cronómetro
        quizTimeLeft = timeLimit * 60; // tiempo personalizado en minutos
        updateTimerUI();
        clearInterval(quizTimerInterval);
        quizTimerInterval = setInterval(() => {
            quizTimeLeft--;
            updateTimerUI();
            if (quizTimeLeft <= 0) {
                endQuiz();
            }
        }, 1000);

        renderQuestion();
    }

    function shuffleArray(array) {
        return array.sort(() => Math.random() - 0.5);
    }

    function updateTimerUI() {
        let mins = Math.floor(quizTimeLeft / 60);
        let secs = quizTimeLeft % 60;
        timerText.textContent = `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
        
        if (quizTimeLeft <= 120) {
            quizTimer.classList.add("warning");
        } else {
            quizTimer.classList.remove("warning");
        }
    }

    function renderQuestion() {
        const q = currentQuizQuestions[currentQuestionIndex];
        quizQuestionCounter.textContent = `Pregunta ${currentQuestionIndex + 1} de ${currentQuizQuestions.length}`;
        quizQuestionText.textContent = q.question;
        
        // Renderizar opciones
        quizOptionsList.innerHTML = "";
        q.options.forEach((opt, idx) => {
            const div = document.createElement("div");
            div.className = "option-item";
            if (userAnswers[currentQuestionIndex] === idx) {
                div.classList.add("selected");
                div.innerHTML = `<i class="fa-solid fa-circle-check" style="color: var(--primary);"></i> <span>${opt}</span>`;
            } else {
                div.innerHTML = `<i class="fa-regular fa-circle"></i> <span>${opt}</span>`;
            }
            div.addEventListener("click", () => selectOption(idx));
            quizOptionsList.appendChild(div);
        });

        // Visibilidad de botones de navegación
        quizPrevBtn.style.display = currentQuestionIndex > 0 ? "block" : "none";
        quizNextBtn.textContent = currentQuestionIndex === currentQuizQuestions.length - 1 ? "Finalizar Reto" : "Siguiente Pregunta";
    }

    function selectOption(index) {
        userAnswers[currentQuestionIndex] = index;
        renderQuestion();
    }

    function navigateQuiz(dir) {
        if (dir === 1) {
            // Siguiente o finalizar
            if (currentQuestionIndex === currentQuizQuestions.length - 1) {
                endQuiz();
            } else {
                currentQuestionIndex++;
                renderQuestion();
            }
        } else {
            // Atrás
            currentQuestionIndex--;
            renderQuestion();
        }
    }

    function endQuiz() {
        clearInterval(quizTimerInterval);
        quizFocusContainer.style.display = "none";
        quizResultsContainer.style.display = "block";

        // Calcular Score
        let correctCount = 0;
        currentQuizQuestions.forEach((q, idx) => {
            if (userAnswers[idx] === q.correct) {
                correctCount++;
            }
        });

        scoreText.textContent = `${correctCount} / ${currentQuizQuestions.length}`;
        
        // Comentarios según nota
        let pct = correctCount / currentQuizQuestions.length;
        if (pct >= 0.8) {
            scoreComment.textContent = "¡Excelente trabajo! Has demostrado dominio en el motor modular y la teoría de convergencia.";
        } else if (pct >= 0.5) {
            scoreComment.textContent = "Buen intento. Te sugerimos revisar las tarjetas de corrección de tus errores.";
        } else {
            scoreComment.textContent = "Es recomendable repasar los temas teóricos antes de volver a realizar simulaciones.";
        }

        // Renderizar tarjetas de feedback didáctico
        renderInsightCards();

        // Renderizar gráfico de Radar (Plotly.js)
        renderRadarChart(correctCount, currentQuizQuestions.length);
    }

    function renderInsightCards() {
        insightCardsContainer.innerHTML = "";
        currentQuizQuestions.forEach((q, idx) => {
            const isCorrect = userAnswers[idx] === q.correct;
            const card = document.createElement("div");
            card.className = "insight-card";
            card.style.borderLeft = isCorrect ? "4px solid var(--success)" : "4px solid var(--danger)";
            card.innerHTML = `
                <span style="font-size: 1.5rem; color: ${isCorrect ? 'var(--success)' : 'var(--danger)'};">
                    <i class="${isCorrect ? 'fa-solid fa-circle-check' : 'fa-solid fa-circle-xmark'}"></i>
                </span>
                <div>
                    <h4 style="margin-bottom: 0.25rem;">Pregunta ${idx + 1}: ${isCorrect ? 'Correcta' : 'Incorrecta'}</h4>
                    <p style="font-size: 0.95rem; font-weight: 500; margin-bottom: 0.5rem;">${q.question}</p>
                    <p class="text-secondary" style="font-size: 0.88rem;">${q.feedback}</p>
                </div>
            `;
            insightCardsContainer.appendChild(card);
        });
    }

    function renderRadarChart(correct, total) {
        // Graficamos las fortalezas
        let data = [{
            type: 'scatterpolar',
            r: [correct * 10, (total - correct) * 10, total * 5, 80],
            theta: ['Precisión', 'Análisis Errores', 'Velocidad', 'Convergencia'],
            fill: 'toself',
            fillcolor: 'rgba(59, 130, 246, 0.2)',
            line: { color: 'var(--primary)', width: 2 }
        }];

        let layout = {
            polar: {
                radialaxis: { visible: true, range: [0, 100], gridcolor: 'rgba(255,255,255,0.05)' },
                angularaxis: { gridcolor: 'rgba(255,255,255,0.05)' },
                bgcolor: 'rgba(0,0,0,0)'
            },
            paper_bgcolor: 'rgba(0,0,0,0)',
            plot_bgcolor: 'rgba(0,0,0,0)',
            margin: { t: 40, b: 40, l: 40, r: 40 },
            font: { color: '#94a3b8' }
        };

        Plotly.newPlot('radar-chart', data, layout, { responsive: true, displayModeBar: false });
    }

    function resetQuiz() {
        clearInterval(quizTimerInterval);
        tutorSetup.style.display = "block";
        quizFocusContainer.style.display = "none";
        quizResultsContainer.style.display = "none";
    }

    // ==========================================================================
    // NUEVAS FUNCIONALIDADES LOCALES (MIGRACIÓN DESDE LEGACY)
    // ==========================================================================

    // --- LÓGICA DE EVASIÓN DE SINGULARIDADES ---
    function renderSingMathPreview() {
        let raw = singExprInput.value.trim();
        if (!raw) {
            singMathPreview.innerHTML = "<span style='color: var(--text-muted);'>Esperando función...</span>";
            return;
        }
        let parsed = raw
            .replace(/\*\*/g, "^")
            .replace(/\*/g, " \\cdot ")
            .replace(/sin/g, "\\sin")
            .replace(/cos/g, "\\cos")
            .replace(/tan/g, "\\tan")
            .replace(/exp/g, "e^")
            .replace(/log/g, "\\ln")
            .replace(/sqrt/g, "\\sqrt");
        try {
            katex.render("f(x) = " + parsed, singMathPreview, {
                throwOnError: false,
                displayMode: true
            });
            singExprInput.style.borderColor = "var(--border-color)";
        } catch (err) {
            singExprInput.style.borderColor = "var(--danger)";
        }
    }

    function renderGMathPreview() {
        const previewEl = document.getElementById("g-math-preview");
        if (!previewEl) return;
        let raw = gExprInput.value.trim();
        if (!raw) {
            previewEl.innerHTML = "<span style='color: var(--text-muted);'>Esperando función...</span>";
            return;
        }
        let parsed = raw
            .replace(/\*\*/g, "^")
            .replace(/\*/g, " \\cdot ")
            .replace(/sin/g, "\\sin")
            .replace(/cos/g, "\\cos")
            .replace(/tan/g, "\\tan")
            .replace(/exp/g, "e^")
            .replace(/log/g, "\\ln")
            .replace(/sqrt/g, "\\sqrt");
        try {
            katex.render("g(x) = " + parsed, previewEl, {
                throwOnError: false,
                displayMode: true
            });
            gExprInput.style.borderColor = "var(--border-color)";
        } catch (err) {
            gExprInput.style.borderColor = "var(--danger)";
        }
    }

    // Función evaluadora con evasión de singularidades
    function evaluateWithSingularityEvasion(expr, xVal, tol) {
        // Intentar evaluación directa
        try {
            let directVal = evaluateFunction(expr, xVal);
            return {
                status: "ok",
                value: directVal,
                method: "Directo",
                error: 0.0,
                message: "Evaluación directa estable."
            };
        } catch (e) {
            // Fallo directo, correr límites laterales
        }

        let delta = 1e-2;
        let best = null;
        const maxAttempts = 20;

        for (let attempt = 0; attempt < maxAttempts; attempt++) {
            let x_izq = xVal - delta;
            let x_der = xVal + delta;
            let val_izq = null;
            let val_der = null;

            try { val_izq = evaluateFunction(expr, x_izq); } catch (e) {}
            try { val_der = evaluateFunction(expr, x_der); } catch (e) {}

            if (val_izq !== null && val_der !== null) {
                let limit = (val_izq + val_der) / 2.0;
                let error = Math.abs(val_izq - val_der) / 2.0;
                
                best = {
                    limit: limit,
                    error: error,
                    delta: delta,
                    val_izq: val_izq,
                    val_der: val_der
                };

                if (error <= tol) {
                    return {
                        status: "removible",
                        value: limit,
                        method: "Límite Lateral",
                        error: error,
                        message: `Singularidad removible evadida con delta=${delta.toExponential(2)}.`
                    };
                }
            } else if (!best && (val_izq !== null || val_der !== null)) {
                best = {
                    limit: val_izq !== null ? val_izq : val_der,
                    error: null,
                    delta: delta,
                    val_izq: val_izq,
                    val_der: val_der
                };
            }

            delta *= 0.5;
        }

        if (best) {
            // Clasificar si es un polo
            let v_existente = best.val_izq !== null ? best.val_izq : best.val_der;
            let esPolo = Math.abs(v_existente) > 1e4;
            if (best.val_izq !== null && best.val_der !== null) {
                if (Math.abs(best.val_izq) > 1e4 || Math.abs(best.val_der) > 1e4 || (best.val_izq * best.val_der < 0 && Math.abs(best.val_izq) > 1e2)) {
                    esPolo = true;
                }
            }

            if (esPolo) {
                return {
                    status: "polo",
                    value: null,
                    method: "Límite Lateral",
                    error: null,
                    message: "Singularidad esencial/Polo. Crecimiento sin cota detectado en límites laterales."
                };
            }

            return {
                status: "indeterminada",
                value: best.limit,
                method: "Límite Lateral",
                error: best.error || 0.0,
                message: "Límites laterales inestables o no coincidentes dentro de la tolerancia."
            };
        }

        return {
            status: "no_evaluable",
            value: null,
            method: "N/A",
            error: null,
            message: "No fue posible evaluar la función en el entorno del punto."
        };
    }

    singularityForm.addEventListener("submit", (e) => {
        e.preventDefault();
        const expr = singExprInput.value.trim();
        const xVal = parseFloat(singXInput.value);
        const tol = parseFloat(singTolInput.value);

        singMetricStatus.textContent = "Evaluando...";
        singMetricStatus.className = "metric-card-value";

        try {
            let result = evaluateWithSingularityEvasion(expr, xVal, tol);
            
            singMetricStatus.textContent = result.status;
            singMetricStatus.className = "metric-card-value";
            if (result.status === "ok") singMetricStatus.classList.add("badge-success");
            else if (result.status === "removible") singMetricStatus.classList.add("badge-success");
            else if (result.status === "polo") singMetricStatus.classList.add("badge-danger");
            else singMetricStatus.classList.add("badge-warning");

            singMetricValue.textContent = result.value !== null ? result.value.toFixed(6) : "N/A";
            singMetricMethod.textContent = result.method;
            singMetricError.textContent = result.error !== null ? result.error.toExponential(4) : "-";
            singDetailMessage.textContent = result.message;

            plotSingularitiesAroundPoint(expr, xVal, result.value, result.status);
        } catch (err) {
            singMetricStatus.textContent = "error";
            singMetricStatus.className = "metric-card-value badge-danger";
            singMetricValue.textContent = "N/A";
            singMetricMethod.textContent = "-";
            singMetricError.textContent = "-";
            singDetailMessage.textContent = "Error al procesar la ecuación.";
        }
    });

    function plotSingularitiesAroundPoint(expr, targetX, limitValue, status) {
        let xMin = targetX - 2;
        let xMax = targetX + 2;
        let xPlot = [];
        let yPlot = [];
        const steps = 300;
        const dx = (xMax - xMin) / steps;

        for (let i = 0; i <= steps; i++) {
            let x = xMin + i * dx;
            // Evitar exactamente el punto targetX para no fallar el gráfico si hay un polo
            if (Math.abs(x - targetX) < 1e-6) {
                xPlot.push(x);
                yPlot.push(null);
                continue;
            }
            try {
                let y = evaluateFunction(expr, x);
                if (Math.abs(y) > 1000) y = null; // No graficar picos enormes
                xPlot.push(x);
                yPlot.push(y);
            } catch (e) {
                xPlot.push(x);
                yPlot.push(null);
            }
        }

        let traceFunc = {
            x: xPlot, y: yPlot,
            type: 'scatter', mode: 'lines',
            name: 'f(x)', line: { color: '#3b82f6', width: 3 }
        };

        let traces = [traceFunc];

        // Añadir asíntota vertical si es polo
        if (status === "polo") {
            traces.push({
                x: [targetX, targetX],
                y: [-10, 10],
                type: 'scatter', mode: 'lines',
                name: 'Asíntota de Polo',
                line: { color: '#ef4444', width: 2, dash: 'dash' }
            });
        }

        // Añadir punto límite si es removible
        if (limitValue !== null) {
            traces.push({
                x: [targetX],
                y: [limitValue],
                type: 'scatter', mode: 'markers',
                name: status === "ok" ? 'Punto Evaluado' : 'Límite Evadido',
                marker: { color: status === "ok" ? '#10b981' : '#f59e0b', size: 10, symbol: 'circle-open', line: { width: 3 } }
            });
        }

        let layout = {
            paper_bgcolor: 'rgba(0,0,0,0)',
            plot_bgcolor: 'rgba(0,0,0,0)',
            font: { color: '#94a3b8', family: 'Outfit, sans-serif' },
            margin: { t: 20, b: 40, l: 50, r: 20 },
            xaxis: { gridcolor: 'rgba(255, 255, 255, 0.05)', range: [xMin, xMax] },
            yaxis: { gridcolor: 'rgba(255, 255, 255, 0.05)', range: [-10, 10] },
            showlegend: true
        };

        Plotly.newPlot('plot-singularities', traces, layout, { responsive: true, displayModeBar: false });
    }

    // --- LÓGICA DE CONSTANTES ---

    function initializeConstantsTab() {
        constantSelect.addEventListener("change", updateConstantMethods);
        updateConstantMethods();

        constantsForm.addEventListener("submit", runConstantApproximation);
    }

    function updateConstantMethods() {
        const type = constantSelect.value;
        const methods = type === "e" ? eulerMethods : piMethods;
        constMethodSelect.innerHTML = "";
        methods.forEach(m => {
            const opt = document.createElement("option");
            opt.value = m.value;
            opt.textContent = m.name;
            constMethodSelect.appendChild(opt);
        });
    }

    function runConstantApproximation(e) {
        e.preventDefault();
        const type = constantSelect.value;
        const method = constMethodSelect.value;
        const tol = parseFloat(constTolInput.value);
        const maxIter = parseInt(constMaxIter.value);

        const startTime = performance.now();
        let iterations = [];
        let approx = 0;
        const refVal = type === "e" ? Math.E : Math.PI;

        if (type === "e") {
            if (method === "taylor") {
                let sum = 1.0;
                let term = 1.0;
                iterations.push({ iter: 1, approx: sum, diff: term, error: Math.abs(sum - refVal) });
                for (let k = 1; k <= maxIter; k++) {
                    term = term / k;
                    let nextSum = sum + term;
                    let diff = Math.abs(nextSum - sum);
                    let err = Math.abs(nextSum - refVal);
                    iterations.push({ iter: k + 1, approx: nextSum, diff: diff, error: err });
                    sum = nextSum;
                    if (diff < tol) break;
                }
                approx = sum;
            } else if (method === "limite") {
                let lastVal = 0.0;
                for (let n = 1; n <= maxIter; n++) {
                    let val = Math.pow(1.0 + 1.0 / n, n);
                    let diff = Math.abs(val - lastVal);
                    let err = Math.abs(val - refVal);
                    iterations.push({ iter: n, approx: val, diff: diff, error: err });
                    lastVal = val;
                    if (n > 1 && diff < tol) break;
                }
                approx = lastVal;
            } else if (method === "fraccion") {
                let lastVal = 2.0;
                for (let depth = 0; depth <= Math.min(maxIter, 150); depth++) {
                    let val = evaluateEulerContinuedFraction(depth);
                    let diff = Math.abs(val - lastVal);
                    let err = Math.abs(val - refVal);
                    iterations.push({ iter: depth + 1, approx: val, diff: depth === 0 ? "-" : diff, error: err });
                    lastVal = val;
                    if (depth > 0 && diff < tol) break;
                }
                approx = lastVal;
            } else if (method === "newton") {
                let x = 2.5; 
                let lastVal = x;
                iterations.push({ iter: 1, approx: x, diff: "-", error: Math.abs(x - refVal) });
                for (let i = 1; i <= maxIter; i++) {
                    let fx = Math.log(x) - 1.0;
                    let dfx = 1.0 / x;
                    let nextX = x - (fx / dfx);
                    let diff = Math.abs(nextX - x);
                    let err = Math.abs(nextX - refVal);
                    iterations.push({ iter: i + 1, approx: nextX, diff: diff, error: err });
                    x = nextX;
                    if (diff < tol) break;
                }
                approx = x;
            }
        } else { 
            if (method === "leibniz") {
                let sum = 0.0;
                let lastVal = 0.0;
                for (let k = 0; k < maxIter; k++) {
                    let term = (k % 2 === 0 ? 1.0 : -1.0) / (2 * k + 1);
                    sum += term;
                    let val = 4.0 * sum;
                    let diff = Math.abs(val - lastVal);
                    let err = Math.abs(val - refVal);
                    if (k === 0 || k === maxIter - 1 || k % Math.ceil(maxIter / 500) === 0 || diff < tol) {
                        iterations.push({ iter: k + 1, approx: val, diff: diff, error: err });
                    }
                    lastVal = val;
                    if (k > 0 && diff < tol) break;
                }
                approx = lastVal;
            } else if (method === "nilakantha") {
                let val = 3.0;
                let lastVal = val;
                let signo = 1.0;
                let n = 2;
                iterations.push({ iter: 1, approx: val, diff: "-", error: Math.abs(val - refVal) });
                for (let i = 1; i <= maxIter; i++) {
                    let term = 4.0 / (n * (n + 1) * (n + 2));
                    val += signo * term;
                    let diff = Math.abs(val - lastVal);
                    let err = Math.abs(val - refVal);
                    iterations.push({ iter: i + 1, approx: val, diff: diff, error: err });
                    lastVal = val;
                    signo *= -1.0;
                    n += 2;
                    if (diff < tol) break;
                }
                approx = val;
            } else if (method === "archimedes") {
                let lados = 6;
                let lastVal = 0.0;
                for (let i = 1; i <= Math.min(maxIter, 30); i++) { 
                    let val = lados * Math.sin(Math.PI / lados);
                    let diff = Math.abs(val - lastVal);
                    let err = Math.abs(val - refVal);
                    iterations.push({ iter: i, approx: val, diff: i === 1 ? "-" : diff, error: err });
                    lastVal = val;
                    lados *= 2;
                    if (i > 1 && diff < tol) break;
                }
                approx = lastVal;
            } else if (method === "ramanujan") {
                let sum = 0.0;
                let lastVal = 0.0;
                for (let k = 0; k <= Math.min(maxIter, 8); k++) { 
                    let termNum = fact(4 * k) * (1103 + 26390 * k);
                    let termDen = Math.pow(fact(k), 4) * Math.pow(396, 4 * k);
                    sum += termNum / termDen;
                    let invPi = (2.0 * Math.sqrt(2.0) / 9801.0) * sum;
                    let val = 1.0 / invPi;
                    let diff = Math.abs(val - lastVal);
                    let err = Math.abs(val - refVal);
                    iterations.push({ iter: k + 1, approx: val, diff: k === 0 ? "-" : diff, error: err });
                    lastVal = val;
                    if (k > 0 && diff < tol) break;
                }
                approx = lastVal;
            } else if (method === "chudnovsky") {
                let sum = 0.0;
                let lastVal = 0.0;
                const constante = 426880 * Math.sqrt(10005);
                for (let k = 0; k <= Math.min(maxIter, 6); k++) {
                    let termNum = (k % 2 === 0 ? 1.0 : -1.0) * fact(6 * k) * (13591409 + 545140134 * k);
                    let termDen = fact(3 * k) * Math.pow(fact(k), 3) * Math.pow(640320, 3 * k);
                    sum += termNum / termDen;
                    let val = constante / sum;
                    let diff = Math.abs(val - lastVal);
                    let err = Math.abs(val - refVal);
                    iterations.push({ iter: k + 1, approx: val, diff: k === 0 ? "-" : diff, error: err });
                    lastVal = val;
                    if (k > 0 && diff < tol) break;
                }
                approx = lastVal;
            }
        }

        const endTime = performance.now();
        const elapsed = ((endTime - startTime) / 1000).toFixed(6);

        // Actualizar UI de métricas
        constMetricIter.textContent = iterations.length > 0 ? iterations[iterations.length - 1].iter : 0;
        constMetricValue.textContent = approx.toFixed(15);
        let finalError = Math.abs(approx - refVal);
        constMetricError.textContent = finalError.toExponential(4);
        constMetricTime.textContent = elapsed;

        // Llenar tabla
        constTableBody.innerHTML = "";
        iterations.forEach(row => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td style="text-align: center; font-weight: 600;">${row.iter}</td>
                <td style="font-family: 'Fira Code', monospace;">${row.approx.toFixed(14)}</td>
                <td style="font-family: 'Fira Code', monospace;">${typeof row.diff === 'number' ? row.diff.toExponential(2) : row.diff}</td>
                <td style="font-family: 'Fira Code', monospace; color: var(--accent);">${row.error.toExponential(2)}</td>
            `;
            constTableBody.appendChild(tr);
        });

        // Graficar convergencia
        plotConstantConvergence(iterations);
    }

    function evaluateEulerContinuedFraction(depth) {
        function coef(idx) {
            if (idx === 0) return 2.0;
            if (idx % 3 === 2) return 2.0 * Math.floor((idx + 1) / 3);
            return 1.0;
        }
        let val = coef(depth);
        for (let i = depth - 1; i >= 0; i--) {
            val = coef(i) + 1.0 / val;
        }
        return val;
    }

    function fact(n) {
        if (n <= 1) return 1.0;
        let f = 1.0;
        for (let i = 2; i <= n; i++) f *= i;
        return f;
    }

    function plotConstantConvergence(iterations) {
        let traceError = {
            x: iterations.map(it => it.iter),
            y: iterations.map(it => it.error + 1e-30),
            type: 'scatter', mode: 'lines+markers',
            name: 'Error Absoluto',
            line: { color: '#06b6d4', width: 2 },
            marker: { size: 5 }
        };

        let layout = {
            paper_bgcolor: 'rgba(0,0,0,0)',
            plot_bgcolor: 'rgba(0,0,0,0)',
            font: { color: '#94a3b8', family: 'Outfit, sans-serif' },
            margin: { t: 10, b: 35, l: 45, r: 10 },
            xaxis: { gridcolor: 'rgba(255, 255, 255, 0.05)', title: 'Iteración' },
            yaxis: { gridcolor: 'rgba(255, 255, 255, 0.05)', type: 'log', title: 'Error (Log)' },
            showlegend: false
        };

        Plotly.newPlot('plot-constants', [traceError], layout, { responsive: true, displayModeBar: false });
    }

    // --- LÓGICA DE FIGURAS 3D ---
    function initializeShapes3DTab() {
        shapeSelect.addEventListener("change", () => {
            const val = shapeSelect.value;
            document.querySelectorAll(".shape-params").forEach(el => el.style.display = "none");
            document.getElementById(`shape-params-${val}`).style.display = "block";
        });

        shapes3DForm.addEventListener("submit", (e) => {
            e.preventDefault();
            renderShape3D();
        });

        setTimeout(renderShape3D, 200);
    }

    function renderShape3D() {
        const type = shapeSelect.value;
        const cmap = shapeColorSelect.value;
        let traces = [];

        if (type === "line") {
            const x0 = parseFloat(document.getElementById("line-x0").value);
            const y0 = parseFloat(document.getElementById("line-y0").value);
            const z0 = parseFloat(document.getElementById("line-z0").value);
            const vx = parseFloat(document.getElementById("line-vx").value);
            const vy = parseFloat(document.getElementById("line-vy").value);
            const vz = parseFloat(document.getElementById("line-vz").value);

            let xPlot = [];
            let yPlot = [];
            let zPlot = [];
            for (let t = -10; t <= 10; t += 0.5) {
                xPlot.push(x0 + t * vx);
                yPlot.push(y0 + t * vy);
                zPlot.push(z0 + t * vz);
            }

            traces.push({
                type: 'scatter3d',
                mode: 'lines+markers',
                x: xPlot, y: yPlot, z: zPlot,
                line: { width: 6, color: '#3b82f6' },
                marker: { size: 3.5, color: '#06b6d4' },
                name: 'Recta 3D'
            });
        } else if (type === "sphere") {
            const xc = parseFloat(document.getElementById("sphere-xc").value);
            const yc = parseFloat(document.getElementById("sphere-yc").value);
            const zc = parseFloat(document.getElementById("sphere-zc").value);
            const r = parseFloat(document.getElementById("sphere-r").value);

            let theta = [];
            let phi = [];
            for (let i = 0; i <= 30; i++) {
                theta.push((i * 2 * Math.PI) / 30);
                phi.push((i * Math.PI) / 30);
            }

            let xSphere = [];
            let ySphere = [];
            let zSphere = [];

            for (let i = 0; i <= 30; i++) {
                let xRow = [];
                let yRow = [];
                let zRow = [];
                for (let j = 0; j <= 30; j++) {
                    xRow.push(xc + r * Math.cos(theta[j]) * Math.sin(phi[i]));
                    yRow.push(yc + r * Math.sin(theta[j]) * Math.sin(phi[i]));
                    zRow.push(zc + r * Math.cos(phi[i]));
                }
                xSphere.push(xRow);
                ySphere.push(yRow);
                zSphere.push(zRow);
            }

            traces.push({
                type: 'surface',
                x: xSphere, y: ySphere, z: zSphere,
                colorscale: cmap,
                showscale: false,
                name: 'Esfera'
            });
        } else if (type === "cylinder") {
            const xc = parseFloat(document.getElementById("cyl-xc").value);
            const yc = parseFloat(document.getElementById("cyl-yc").value);
            const r = parseFloat(document.getElementById("cyl-r").value);
            const h = parseFloat(document.getElementById("cyl-h").value);

            let theta = [];
            for (let i = 0; i <= 30; i++) {
                theta.push((i * 2 * Math.PI) / 30);
            }

            let xCyl = [];
            let yCyl = [];
            let zCyl = [];

            for (let i = 0; i <= 10; i++) {
                let zVal = (i * h) / 10;
                let xRow = [];
                let yRow = [];
                let zRow = [];
                for (let j = 0; j <= 30; j++) {
                    xRow.push(xc + r * Math.cos(theta[j]));
                    yRow.push(yc + r * Math.sin(theta[j]));
                    zRow.push(zVal);
                }
                xCyl.push(xRow);
                yCyl.push(yRow);
                zCyl.push(zRow);
            }

            traces.push({
                type: 'surface',
                x: xCyl, y: yCyl, z: zCyl,
                colorscale: cmap,
                showscale: false,
                name: 'Cilindro'
            });
        } else if (type === "cone") {
            const xc = parseFloat(document.getElementById("cone-xc").value);
            const yc = parseFloat(document.getElementById("cone-yc").value);
            const r = parseFloat(document.getElementById("cone-r").value);
            const h = parseFloat(document.getElementById("cone-h").value);

            let theta = [];
            for (let i = 0; i <= 30; i++) {
                theta.push((i * 2 * Math.PI) / 30);
            }

            let xCone = [];
            let yCone = [];
            let zCone = [];

            for (let i = 0; i <= 10; i++) {
                let zVal = (i * h) / 10;
                let currentR = (1.0 - zVal / h) * r;
                let xRow = [];
                let yRow = [];
                let zRow = [];
                for (let j = 0; j <= 30; j++) {
                    xRow.push(xc + currentR * Math.cos(theta[j]));
                    yRow.push(yc + currentR * Math.sin(theta[j]));
                    zRow.push(zVal);
                }
                xCone.push(xRow);
                yCone.push(yRow);
                zCone.push(zRow);
            }

            traces.push({
                type: 'surface',
                x: xCone, y: yCone, z: zCone,
                colorscale: cmap,
                showscale: false,
                name: 'Cono'
            });
        } else if (type === "paraboloid") {
            const a = parseFloat(document.getElementById("para-a").value);
            const b = parseFloat(document.getElementById("para-b").value);

            let xVal = [];
            let yVal = [];
            for (let i = -15; i <= 15; i++) {
                xVal.push(i * 2.0 / 15.0);
                yVal.push(i * 2.0 / 15.0);
            }

            let xPara = [];
            let yPara = [];
            let zPara = [];

            for (let i = 0; i < xVal.length; i++) {
                let xRow = [];
                let yRow = [];
                let zRow = [];
                for (let j = 0; j < yVal.length; j++) {
                    xRow.push(xVal[i]);
                    yRow.push(yVal[j]);
                    zRow.push(Math.pow(xVal[i], 2) / Math.pow(a, 2) + Math.pow(yVal[j], 2) / Math.pow(b, 2));
                }
                xPara.push(xRow);
                yPara.push(yRow);
                zPara.push(zRow);
            }

            traces.push({
                type: 'surface',
                x: xPara, y: yPara, z: zPara,
                colorscale: cmap,
                showscale: false,
                name: 'Paraboloide'
            });
        }

        let layout = {
            paper_bgcolor: 'rgba(0,0,0,0)',
            plot_bgcolor: 'rgba(0,0,0,0)',
            font: { color: '#94a3b8', family: 'Outfit, sans-serif' },
            margin: { t: 0, b: 0, l: 0, r: 0 },
            scene: {
                xaxis: { gridcolor: 'rgba(255,255,255,0.05)', zerolinecolor: 'rgba(255,255,255,0.1)' },
                yaxis: { gridcolor: 'rgba(255,255,255,0.05)', zerolinecolor: 'rgba(255,255,255,0.1)' },
                zaxis: { gridcolor: 'rgba(255,255,255,0.05)', zerolinecolor: 'rgba(255,255,255,0.1)' }
            },
            showlegend: false
        };

        Plotly.newPlot('plot-3d', traces, layout, { responsive: true, displayModeBar: false });
    }

    // --- LÓGICA DE ANIMACIONES Y ONDAS ---

    function initializeAnimationsTab() {
        animationType.addEventListener("change", () => {
            const type = animationType.value;
            animDescription.textContent = animDescriptions[type];
            resetAnimation();
        });

        animPlayBtn.addEventListener("click", startAnimationLoop);
        animPauseBtn.addEventListener("click", stopAnimationLoop);
        animResetBtn.addEventListener("click", resetAnimation);

        resetAnimation();
    }

    function startAnimationLoop() {
        if (animRunning) return;
        animRunning = true;
        animStartTime = performance.now() - animTimeOffset * 1000;
        loop();
    }

    function stopAnimationLoop() {
        animRunning = false;
        if (animationFrameId) {
            cancelAnimationFrame(animationFrameId);
            animationFrameId = null;
        }
    }

    function resetAnimation() {
        stopAnimationLoop();
        animTimeOffset = 0;
        drawAnimationFrame(0.0);
    }

    function loop() {
        if (!animRunning) return;
        let elapsed = (performance.now() - animStartTime) / 1000;
        animTimeOffset = elapsed;
        drawAnimationFrame(elapsed);
        animationFrameId = requestAnimationFrame(loop);
    }

    function drawAnimationFrame(t) {
        const type = animationType.value;
        let traces = [];
        let layout = {};

        if (type === "sine") {
            let xPlot = [];
            let yPlot = [];
            const steps = 300;
            const xMin = -2 * Math.PI;
            const xMax = 2 * Math.PI;
            const dx = (xMax - xMin) / steps;

            let amplitud = 1.0 + 0.6 * Math.sin(0.8 * t);
            let frecuencia = 1.0 + 0.35 * Math.cos(0.55 * t);
            let fase = 1.1 * t;

            for (let i = 0; i <= steps; i++) {
                let x = xMin + i * dx;
                xPlot.push(x);
                yPlot.push(amplitud * Math.sin(frecuencia * x + fase));
            }

            traces.push({
                x: xPlot, y: yPlot,
                type: 'scatter', mode: 'lines',
                name: 'y = A sin(wx + phi)',
                line: { color: '#3b82f6', width: 3 }
            });

            layout = {
                paper_bgcolor: 'rgba(0,0,0,0)',
                plot_bgcolor: 'rgba(0,0,0,0)',
                font: { color: '#94a3b8', family: 'Outfit, sans-serif' },
                margin: { t: 30, b: 40, l: 45, r: 15 },
                xaxis: { gridcolor: 'rgba(255, 255, 255, 0.05)', range: [xMin, xMax] },
                yaxis: { gridcolor: 'rgba(255, 255, 255, 0.05)', range: [-2.2, 2.2] },
                title: `A=${amplitud.toFixed(3)}   w=${frecuencia.toFixed(3)}   phi=${fase.toFixed(3)}`,
                showlegend: true
            };
            Plotly.react('plot-animations', traces, layout, { responsive: true, displayModeBar: false });

        } else if (type === "interference") {
            let xPlot = [];
            let y1Plot = [];
            let y2Plot = [];
            let ySumPlot = [];
            const steps = 300;
            const xMin = -2 * Math.PI;
            const xMax = 2 * Math.PI;
            const dx = (xMax - xMin) / steps;

            for (let i = 0; i <= steps; i++) {
                let x = xMin + i * dx;
                let y1 = 1.2 * Math.sin(1.25 * x + 0.9 * t);
                let y2 = 0.9 * Math.sin(1.15 * x - 1.15 * t);
                xPlot.push(x);
                y1Plot.push(y1);
                y2Plot.push(y2);
                ySumPlot.push(y1 + y2);
            }

            traces.push({
                x: xPlot, y: y1Plot,
                type: 'scatter', mode: 'lines',
                name: 'Onda Viajera 1 (y1)',
                line: { color: '#3b82f6', width: 1.5 }
            });

            traces.push({
                x: xPlot, y: y2Plot,
                type: 'scatter', mode: 'lines',
                name: 'Onda Viajera 2 (y2)',
                line: { color: '#f59e0b', width: 1.5 }
            });

            traces.push({
                x: xPlot, y: ySumPlot,
                type: 'scatter', mode: 'lines',
                name: 'Interferencia (y1 + y2)',
                line: { color: '#ef4444', width: 3 }
            });

            layout = {
                paper_bgcolor: 'rgba(0,0,0,0)',
                plot_bgcolor: 'rgba(0,0,0,0)',
                font: { color: '#94a3b8', family: 'Outfit, sans-serif' },
                margin: { t: 30, b: 40, l: 45, r: 15 },
                xaxis: { gridcolor: 'rgba(255, 255, 255, 0.05)', range: [xMin, xMax] },
                yaxis: { gridcolor: 'rgba(255, 255, 255, 0.05)', range: [-3.2, 3.2] },
                title: `Tiempo de propagación: ${t.toFixed(2)} s`,
                showlegend: true
            };
            Plotly.react('plot-animations', traces, layout, { responsive: true, displayModeBar: false });

        } else if (type === "surface3d") {
            const resolution = 30; 
            let xVal = [];
            let yVal = [];
            for (let i = 0; i <= resolution; i++) {
                xVal.push(-3.5 + (i * 7.0) / resolution);
                yVal.push(-3.5 + (i * 7.0) / resolution);
            }

            let xMesh = [];
            let yMesh = [];
            let zMesh = [];

            for (let i = 0; i <= resolution; i++) {
                let xRow = [];
                let yRow = [];
                let zRow = [];
                for (let j = 0; j <= resolution; j++) {
                    xRow.push(xVal[i]);
                    yRow.push(yVal[j]);
                    zRow.push(Math.sin(xVal[i] + t) * Math.cos(yVal[j] - 0.6 * t));
                }
                xMesh.push(xRow);
                yMesh.push(yRow);
                zMesh.push(zRow);
            }

            traces.push({
                type: 'surface',
                x: xMesh, y: yMesh, z: zMesh,
                colorscale: 'Viridis',
                showscale: false
            });

            let azim = 45.0 + 20.0 * Math.sin(t);

            layout = {
                paper_bgcolor: 'rgba(0,0,0,0)',
                plot_bgcolor: 'rgba(0,0,0,0)',
                font: { color: '#94a3b8', family: 'Outfit, sans-serif' },
                margin: { t: 0, b: 0, l: 0, r: 0 },
                scene: {
                    camera: {
                        eye: {
                            x: 1.3 * Math.cos(azim * Math.PI / 180),
                            y: 1.3 * Math.sin(azim * Math.PI / 180),
                            z: 0.8
                        }
                    },
                    xaxis: { gridcolor: 'rgba(255,255,255,0.05)', range: [-3.5, 3.5] },
                    yaxis: { gridcolor: 'rgba(255,255,255,0.05)', range: [-3.5, 3.5] },
                    zaxis: { gridcolor: 'rgba(255,255,255,0.05)', range: [-1.2, 1.2] }
                },
                showlegend: false
            };

            Plotly.react('plot-animations', traces, layout, { responsive: true, displayModeBar: false });
        }
    }
});

