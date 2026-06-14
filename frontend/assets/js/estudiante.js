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
    const quizModeToggle = document.getElementById("quiz-mode-toggle");

    // --- INITIALIZATION ---
    renderMathPreview();
    updateHistoryUI();
    renderEmptyPlot();

    // --- EVENT LISTENERS ---
    
    // Input Matemático (KaTeX Preview)
    expressionInput.addEventListener("input", renderMathPreview);

    // Toggle de Acordeón
    advancedToggle.addEventListener("click", () => {
        advancedContent.classList.toggle("active");
        advancedArrow.classList.toggle("fa-chevron-down");
        advancedArrow.classList.toggle("fa-chevron-up");
    });

    // Selector de Método (Bisección / Newton)
    methodSelect.addEventListener("change", () => {
        const val = methodSelect.value;
        if (val === "bisection") {
            intervalGroup.style.display = "block";
            x0Group.style.display = "none";
        } else {
            intervalGroup.style.display = "none";
            x0Group.style.display = "block";
        }
    });

    // Botón Sugerir Valores
    suggestBtn.addEventListener("click", suggestMathValues);

    // Formulario de Simulación
    simulatorForm.addEventListener("submit", (e) => {
        e.preventDefault();
        runSimulation();
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

    // --- FUNCIONES CORE ---

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
        
        // Diccionario de sugerencias
        const suggestions = [
            { key: "x**3 - x - 2", method: "bisection", a: 1, b: 2, x0: 1.5 },
            { key: "cos(x) - x", method: "bisection", a: 0, b: 1, x0: 0.5 },
            { key: "exp(-x) - x", method: "bisection", a: 0, b: 1, x0: 0.5 },
            { key: "x**2 + 2*x - 9", method: "bisection", a: 2, b: 3, x0: 2.2 },
            { key: "x**2 - 4", method: "newton", a: 1, b: 3, x0: 1.5 }
        ];

        let found = suggestions.find(s => s.key.replace(/\s+/g, "") === rawExpr.replace(/\s+/g, ""));
        
        if (found) {
            methodSelect.value = found.method;
            methodSelect.dispatchEvent(new Event("change"));
            aInput.value = found.a;
            bInput.value = found.b;
            x0Input.value = found.x0;
            
            // Efecto visual de brillo en sugerencia
            suggestBtn.style.boxShadow = "var(--shadow-glow)";
            setTimeout(() => suggestBtn.style.boxShadow = "none", 1000);
        } else {
            // Sugerencia genérica por defecto
            aInput.value = 0;
            bInput.value = 2;
            x0Input.value = 1.0;
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

        // Actualizar etiquetas visuales (Reto de 10 preguntas fijas en total)
        easyValueLabel.textContent = `${easySlider.value}% (${Math.round(easySlider.value / 10)} preguntas)`;
        mediumValueLabel.textContent = `${mediumSlider.value}% (${Math.round(mediumSlider.value / 10)} preguntas)`;
        hardValueLabel.textContent = `${hardSlider.value}% (${Math.round(hardSlider.value / 10)} preguntas)`;
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
            .replace(/pi/g, "Math.PI")
            .replace(/e/g, "Math.E")
            .replace(/\*\*/g, "^");

        // Traducir potencias de JS a math
        while (formatted.includes("^")) {
            formatted = formatted.replace(/([0-9x\(\)]+)\^([0-9x\(\)\.]+)/g, "Math.pow($1, $2)");
        }

        // Reemplazar la variable x con su valor numérico
        let evaluatedExpression = formatted.replace(/x/g, `(${x})`);
        
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
            } else {
                const x0 = parseFloat(x0Input.value);
                result = runNewtonLocal(expression, x0, tol, maxIter);
            }
            const endTime = performance.now();
            const elapsed = ((endTime - startTime) / 1000).toFixed(6);

            // Mostrar resultados
            metricStatus.textContent = result.status;
            metricStatus.classList.add(result.status === "success" ? "badge-success" : "badge-warning");
            metricRoot.textContent = result.root !== null ? result.root.toFixed(8) : "N/A";
            metricIter.textContent = result.iterations.length;
            metricTime.textContent = elapsed;

            // Llenar tabla
            populateIterationsTable(result.iterations, method);

            // Graficar
            plotFunctionGraph(expression, result.iterations, result.root, method);

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
            tableBody.innerHTML = `<tr><td colspan="6" style="text-align: center; color: var(--danger);">Ocurrió un error o singularidad en el cálculo.</td></tr>`;

            // Mostrar Alerta Didáctica de Singularidades
            showSingularAlert(expression, method);
        }
    }

    // Algoritmo local de Bisección
    function runBisectionLocal(expr, a, b, tol, maxIter) {
        let fa = evaluateFunction(expr, a);
        let fb = evaluateFunction(expr, b);

        if (fa * fb >= 0) {
            alertTitle.textContent = "Error de Intervalo Inicial";
            alertDescription.textContent = "El teorema de Bolzano no se cumple ya que f(a) y f(b) tienen el mismo signo. No se puede garantizar la existencia de una raíz en este intervalo.";
            alertRecommendation.textContent = "Sugerencia: Haz clic en el botón '✨ Sugerir Valores' o cambia los límites del intervalo para que rodeen la intersección con el eje X.";
            didacticAlert.style.display = "flex";
            throw new Error("intervalo_invalido");
        }

        let iterations = [];
        let root = null;
        let status = "max_iter";

        for (let i = 1; i <= maxIter; i++) {
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
        }

        if (!root && iterations.length > 0) {
            root = iterations[iterations.length - 1].root;
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
            let fx = evaluateFunction(expr, x);
            let dfx = evaluateDerivative(expr, x);

            // Detección de singularidad (derivada cero)
            if (Math.abs(dfx) < 1e-12) {
                status = "singularidad";
                throw new Error("singularidad");
            }

            let nextX = x - (fx / dfx);
            let err = Math.abs(nextX - x);

            iterations.push({
                iter: i,
                xi: x,
                sup: "-",
                root: nextX,
                error: i === 1 ? "-" : err.toFixed(8),
                residual: fx
            });

            if (err < tol || Math.abs(fx) < 1e-12) {
                root = nextX;
                status = "success";
                break;
            }

            x = nextX;
        }

        if (!root && iterations.length > 0) {
            root = iterations[iterations.length - 1].root;
        }

        return { root, iterations, status };
    }

    // 5. Rellenar Tabla
    function populateIterationsTable(iterations, method) {
        tableBody.innerHTML = "";
        
        // Ajustar columnas de la cabecera
        const headers = document.getElementById("table-headers");
        if (method === "bisection") {
            headers.innerHTML = `<th>Iteración</th><th>a (Lím. Inf)</th><th>b (Lím. Sup)</th><th>c (Raíz Aprox.)</th><th>Error Rel.</th><th>Residual f(x)</th>`;
        } else {
            headers.innerHTML = `<th>Iteración</th><th>x_i (Actual)</th><th>x_{i+1} (Siguiente)</th><th>Diferencia</th><th>Error Rel.</th><th>Residual f(x)</th>`;
        }

        iterations.forEach(row => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td style="text-align: center; font-weight: 600; color: var(--text-secondary);">${row.iter}</td>
                <td>${row.xi.toFixed(8)}</td>
                <td>${typeof row.sup === 'number' ? row.sup.toFixed(8) : row.sup}</td>
                <td>${row.root.toFixed(8)}</td>
                <td>${row.error}</td>
                <td style="font-family: 'Fira Code', monospace; color: ${Math.abs(row.residual) < 1e-5 ? 'var(--success)' : 'inherit'};">${row.residual.toExponential(4)}</td>
            `;
            tableBody.appendChild(tr);
        });
    }

    // 6. Graficar función en Plotly.js
    function plotFunctionGraph(expr, iterations, root, method) {
        // Encontrar rango x
        let xMin = -2;
        let xMax = 4;
        
        if (iterations.length > 0) {
            let xs = iterations.map(it => it.xi).filter(x => typeof x === 'number');
            if (root !== null) xs.push(root);
            let minVal = Math.min(...xs);
            let maxVal = Math.max(...xs);
            xMin = minVal - Math.abs(maxVal - minVal) * 0.4 - 1;
            xMax = maxVal + Math.abs(maxVal - minVal) * 0.4 + 1;
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

        // Raíz encontrada
        let traces = [traceFunc, traceAxis];

        if (root !== null) {
            traces.push({
                x: [root],
                y: [0],
                type: 'scatter',
                mode: 'markers',
                name: 'Raíz Aprox.',
                marker: { color: '#10b981', size: 10, line: { color: '#0f1624', width: 2 } }
            });
        }

        // Si es Newton-Raphson, podemos trazar la última secante/tangente didáctica
        if (method === "newton" && iterations.length > 0) {
            let lastIt = iterations[iterations.length - 1];
            let xVal = lastIt.xi;
            let yVal = lastIt.residual;
            
            traces.push({
                x: [xVal, lastIt.root],
                y: [yVal, 0],
                type: 'scatter',
                mode: 'lines+markers',
                name: 'Última Tangente',
                line: { color: '#f59e0b', width: 1.5, dash: 'dot' },
                marker: { color: '#f59e0b', size: 6 }
            });
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
            div.innerHTML = `
                <div class="history-item-header">
                    <span class="history-item-title">${item.expr}</span>
                    <span class="badge ${item.status === 'success' ? 'badge-success' : 'badge-warning'}">${item.status}</span>
                </div>
                <div class="history-item-header" style="margin-top: 0.25rem;">
                    <span class="history-item-meta">${item.method === 'bisection' ? 'Bisección' : 'Newton'} | Raíz: ${item.root}</span>
                    <span class="history-item-meta" style="font-size: 0.75rem;">${item.date}</span>
                </div>
            `;
            // Cargar de nuevo al simulador
            div.addEventListener("click", () => {
                expressionInput.value = item.expr;
                methodSelect.value = item.method;
                methodSelect.dispatchEvent(new Event("change"));
                renderMathPreview();
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
        }
    ];

    function startQuiz() {
        tutorSetup.style.display = "none";
        quizFocusContainer.style.display = "block";
        quizResultsContainer.style.display = "none";

        // Generar preguntas basadas en la dificultad seleccionada
        const nEasy = Math.round(easySlider.value / 10);
        const nMed = Math.round(mediumSlider.value / 10);
        const nHard = Math.round(hardSlider.value / 10);

        let poolEasy = databaseQuestions.filter(q => q.difficulty === "easy");
        let poolMed = databaseQuestions.filter(q => q.difficulty === "medium");
        let poolHard = databaseQuestions.filter(q => q.difficulty === "hard");

        // Mezclar y tomar cantidad solicitada
        currentQuizQuestions = [
            ...shuffleArray(poolEasy).slice(0, nEasy),
            ...shuffleArray(poolMed).slice(0, nMed),
            ...shuffleArray(poolHard).slice(0, nHard)
        ];

        // Asegurarnos de tener al menos 3 preguntas para test
        if (currentQuizQuestions.length === 0) {
            currentQuizQuestions = [...databaseQuestions];
        }

        currentQuestionIndex = 0;
        userAnswers = new Array(currentQuizQuestions.length).fill(null);

        // Iniciar cronómetro
        quizTimeLeft = currentQuizQuestions.length * 60; // 1 minuto por pregunta
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
});
