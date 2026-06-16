/* ==========================================================================
   LÓGICA INTERACTIVA DEL PROFESOR - PROFESOR.JS
   Responsable: Leonardo González
   Aesthetics: Comparator graphs, radar analytics, exam setup and exports
   ========================================================================== */

document.addEventListener("DOMContentLoaded", () => {
    // --- ELEMENTOS DEL DOM ---
    const exprInputProf = document.getElementById("expr-input-prof");
    const mathPreviewProf = document.getElementById("math-preview-prof");
    const aInputProf = document.getElementById("a-input-prof");
    const bInputProf = document.getElementById("b-input-prof");
    const x0InputProf = document.getElementById("x0-input-prof");
    const toleranceInputProf = document.getElementById("tolerance-input-prof");
    const maxIterInputProf = document.getElementById("max-iter-input-prof");
    const comparatorForm = document.getElementById("comparator-form");
    const comparisonTableBody = document.getElementById("comparison-table-body");

    // Checkboxes del comparador
    const compareBisection = document.getElementById("compare-bisection");
    const compareSecant = document.getElementById("compare-secant");
    const compareNewton = document.getElementById("compare-newton");
    const compareFixedPoint = document.getElementById("compare-fixedpoint");

    // Campo g(x) para Punto Fijo
    const gExprInputProf = document.getElementById("g-expr-input-prof");
    const gMathPreviewProf = document.getElementById("g-math-preview-prof");
    const gExprGroupProf = document.getElementById("g-expression-group-prof");

    // Alertas didácticas
    const didacticAlert = document.getElementById("didactic-alert");
    const alertTitle = document.getElementById("alert-title");
    const alertDescription = document.getElementById("alert-description");
    const alertRecommendation = document.getElementById("alert-recommendation");

    // Evaluaciones y Código
    const examTemplate = document.getElementById("exam-template");
    const btnGenerateKey = document.getElementById("btn-generate-key");
    const classCodeOutput = document.getElementById("class-code-output");
    const btnExportExam = document.getElementById("btn-export-exam");
    const quizTotalQuestionsProf = document.getElementById("quiz-total-questions-prof");

    // Sliders de dificultad
    const sliderEasyProf = document.getElementById("slider-easy-prof");
    const sliderMediumProf = document.getElementById("slider-medium-prof");
    const sliderHardProf = document.getElementById("slider-hard-prof");

    // Etiquetas de dificultad
    const lblEasyPct = document.getElementById("lbl-easy-pct");
    const lblMedPct = document.getElementById("lbl-med-pct");
    const lblHardPct = document.getElementById("lbl-hard-pct");

    const lblEasyCount = document.getElementById("lbl-easy-count");
    const lblMedCount = document.getElementById("lbl-med-count");
    const lblHardCount = document.getElementById("lbl-hard-count");

    // Estado del Quiz del Profesor
    let quizModesProf = {
        easy: "theoretical",
        medium: "practical",
        hard: "mixed"
    };

    // --- INITIALIZATION ---
    renderMathPreview();
    renderGMathPreview();
    renderRadarChartClass();
    renderEmptyPlot();
    toggleGExprGroup();
    updateSliderLabelsProf();

    // --- EVENT LISTENERS ---
    exprInputProf.addEventListener("input", renderMathPreview);
    gExprInputProf.addEventListener("input", renderGMathPreview);
    
    // Cambios en los checkboxes del comparador
    compareFixedPoint.addEventListener("change", toggleGExprGroup);
    [compareBisection, compareSecant, compareNewton, compareFixedPoint].forEach(cb => {
        cb.addEventListener("change", () => {
            resetComparisonOutputs();
        });
    });

    // Cambios en inputs limpian salidas de comparación
    const inputsToWatch = [exprInputProf, gExprInputProf, aInputProf, bInputProf, x0InputProf, toleranceInputProf, maxIterInputProf];
    inputsToWatch.forEach(input => {
        if (input) {
            input.addEventListener("input", resetComparisonOutputs);
        }
    });
    
    comparatorForm.addEventListener("submit", (e) => {
        e.preventDefault();
        compareAlgorithms();
    });

    examTemplate.addEventListener("change", updateExamTemplateUI);
    btnGenerateKey.addEventListener("click", generateClassCode);
    btnExportExam.addEventListener("click", exportExamConfiguration);

    // Sliders Proporcionales
    [sliderEasyProf, sliderMediumProf, sliderHardProf].forEach(slider => {
        slider.addEventListener("input", (event) => {
            adjustSlidersProportionallyProf(event.target);
        });
    });

    // Control de total de preguntas
    quizTotalQuestionsProf.addEventListener("input", updateSliderLabelsProf);

    // Modalidad buttons listener (Teo/Prac/Mix)
    const modeButtonsProf = document.querySelectorAll(".mode-btn-prof");
    modeButtonsProf.forEach(btn => {
        btn.addEventListener("click", () => {
            const difficulty = btn.getAttribute("data-difficulty");
            const mode = btn.getAttribute("data-mode");
            
            document.querySelectorAll(`.mode-btn-prof[data-difficulty="${difficulty}"]`).forEach(b => b.classList.remove("active"));
            btn.classList.add("active");
            
            quizModesProf[difficulty] = mode;
        });
    });

    // --- FUNCIONES CORE ------

    // 1. Renderizar Vista Previa de Fórmulas Matemáticas (KaTeX)
    function renderMathPreview() {
        let raw = exprInputProf.value.trim();
        if (!raw) {
            mathPreviewProf.innerHTML = "<span style='color: var(--text-muted);'>Esperando función...</span>";
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
            katex.render("f(x) = " + parsed, mathPreviewProf, {
                throwOnError: false,
                displayMode: true
            });
            exprInputProf.style.borderColor = "var(--border-color)";
        } catch (err) {
            exprInputProf.style.borderColor = "var(--danger)";
        }
    }

    // 1b. Renderizar Vista Previa de g(x) para Punto Fijo
    function renderGMathPreview() {
        let raw = gExprInputProf.value.trim();
        if (!raw) {
            gMathPreviewProf.innerHTML = "<span style='color: var(--text-muted);'>Esperando función...</span>";
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
            katex.render("g(x) = " + parsed, gMathPreviewProf, {
                throwOnError: false,
                displayMode: true
            });
            gExprInputProf.style.borderColor = "var(--border-color)";
        } catch (err) {
            gExprInputProf.style.borderColor = "var(--danger)";
        }
    }

    function toggleGExprGroup() {
        if (compareFixedPoint.checked) {
            gExprGroupProf.style.display = "block";
        } else {
            gExprGroupProf.style.display = "none";
        }
    }

    function resetComparisonOutputs() {
        comparisonTableBody.innerHTML = `
            <tr>
                <td colspan="6" style="color: var(--text-muted);">Haz clic en "Comparar Algoritmos" para ver los resultados.</td>
            </tr>
        `;
        renderEmptyPlot();
        didacticAlert.style.display = "none";
    }

    // 2. Evaluar Función f(x)
    function evaluateFunction(expr, x) {
        let formatted = expr.toLowerCase()
            .replace(/\s+/g, "")
            .replace(/sin\(/g, "Math.sin(")
            .replace(/cos\(/g, "Math.cos(")
            .replace(/tan\(/g, "Math.tan(")
            .replace(/exp\(/g, "Math.exp(")
            .replace(/ln\(/g, "Math.log(")
            .replace(/log\(/g, "Math.log(")
            .replace(/abs\(/g, "Math.abs(")
            .replace(/sqrt\(/g, "Math.sqrt(")
            .replace(/sinh\(/g, "Math.sinh(")
            .replace(/cosh\(/g, "Math.cosh(")
            .replace(/tanh\(/g, "Math.tanh(")
            .replace(/asin\(/g, "Math.asin(")
            .replace(/acos\(/g, "Math.acos(")
            .replace(/atan\(/g, "Math.atan(")
            .replace(/\bpi\b/g, "Math.PI")
            .replace(/\be\b/g, "Math.E")
            .replace(/\^/g, "**");

        let evaluatedExpression = formatted.replace(/\bx\b/g, `(${x})`);
        
        try {
            let result = new Function(`return ${evaluatedExpression}`)();
            if (isNaN(result) || !isFinite(result)) {
                throw new Error("indefinido");
            }
            return result;
        } catch (e) {
            throw new Error("singularidad");
        }
    }

    // Derivada
    function evaluateDerivative(expr, x) {
        const h = 1e-6;
        let fPlus = evaluateFunction(expr, x + h);
        let fMinus = evaluateFunction(expr, x - h);
        return (fPlus - fMinus) / (2 * h);
    }

    // 3. Comparación de Algoritmos (Bisección vs Newton vs Secante vs Punto Fijo)
    function compareAlgorithms() {
        const expr = exprInputProf.value.trim();
        const a = parseFloat(aInputProf.value);
        const b = parseFloat(bInputProf.value);
        const x0 = parseFloat(x0InputProf.value);
        const tol = parseFloat(toleranceInputProf.value);
        const maxIter = parseInt(maxIterInputProf.value);
        const gExpr = gExprInputProf.value.trim();

        comparisonTableBody.innerHTML = "";
        
        let bisResult = null;
        let secResult = null;
        let newtResult = null;
        let fpResult = null;

        let selectedCount = 0;
        let alertTriggered = false;
        let alertMessage = "";
        let alertRec = "";

        // 1. Bisección
        if (compareBisection.checked) {
            selectedCount++;
            let start = performance.now();
            try {
                bisResult = runBisectionLocal(expr, a, b, tol, maxIter);
                bisResult.time = ((performance.now() - start) / 1000).toFixed(6);
            } catch (e) {
                bisResult = { root: null, iterations: [], status: "error", time: "0.000000" };
            }
            renderComparisonTableRow("Bisección", bisResult, "#10b981");
            
            if (bisResult.status === "bolzano_violation") {
                alertTriggered = true;
                alertMessage = "Violación del Teorema de Bolzano en Bisección.";
                alertRec = "El producto f(a) * f(b) debe ser menor que cero. Intenta ajustar el intervalo [a, b] para encerrar una raíz.";
            } else if (bisResult.status === "singularidad") {
                alertTriggered = true;
                alertMessage = "Singularidad detectada en Bisección.";
                alertRec = "La función no se pudo evaluar en algunos puntos del intervalo. Verifica que el intervalo no contenga discontinuidades.";
            }
        }

        // 2. Secante
        if (compareSecant.checked) {
            selectedCount++;
            let start = performance.now();
            try {
                secResult = runSecantLocal(expr, a, b, tol, maxIter);
                secResult.time = ((performance.now() - start) / 1000).toFixed(6);
            } catch (e) {
                secResult = { root: null, iterations: [], status: "error", time: "0.000000" };
            }
            renderComparisonTableRow("Secante", secResult, "#06b6d4");
            
            if (secResult.status === "singularidad" && !alertTriggered) {
                alertTriggered = true;
                alertMessage = "División por cero o singularidad en método de la Secante.";
                alertRec = "El denominador (f(x_1) - f(x_0)) se hizo demasiado pequeño. Intenta usar otros valores iniciales [x₀, x₁] o cambia a un método más estable.";
            }
        }

        // 3. Newton-Raphson
        if (compareNewton.checked) {
            selectedCount++;
            let start = performance.now();
            try {
                newtResult = runNewtonLocal(expr, x0, tol, maxIter);
                newtResult.time = ((performance.now() - start) / 1000).toFixed(6);
            } catch (e) {
                newtResult = { root: null, iterations: [], status: "error", time: "0.000000" };
            }
            renderComparisonTableRow("Newton-Raphson", newtResult, "#f59e0b");
            
            if (newtResult.status === "singularidad" && !alertTriggered) {
                alertTriggered = true;
                alertMessage = "Derivada nula o singularidad detectada en Newton-Raphson.";
                alertRec = "El método encontró una pendiente casi horizontal (f'(x) ≈ 0). Prueba con otro punto inicial x₀.";
            }
        }

        // 4. Punto Fijo
        if (compareFixedPoint.checked) {
            selectedCount++;
            let start = performance.now();

            // Verificar compatibilidad didáctica de g(x)
            try {
                const compResult = checkGExpressionCompatibility(expr, gExpr, x0);
                if (!compResult.compatible && !alertTriggered) {
                    alertTriggered = true;
                    let rootText = compResult.root.toFixed(6);
                    let gValText = compResult.gVal !== null ? compResult.gVal.toFixed(6) : "indefinido/error";
                    alertMessage = `Advertencia de compatibilidad: g(x) = ${gExpr} no es compatible con f(x) = 0.`;
                    alertRec = `En la raíz real de f(x) cercana (x ≈ ${rootText}), evaluar g(x) da ${gValText}, lo que viola la condición fundamental g(r) = r (diferencia de ${compResult.discrepancy !== null ? compResult.discrepancy.toFixed(4) : "N/A"}).`;
                }
            } catch (err) {
                // Ignorar
            }

            try {
                fpResult = runFixedPointLocal(gExpr, expr, x0, tol, maxIter);
                fpResult.time = ((performance.now() - start) / 1000).toFixed(6);
            } catch (e) {
                fpResult = { root: null, iterations: [], status: "error", time: "0.000000" };
            }
            renderComparisonTableRow("Punto Fijo", fpResult, "#a855f7");
            
            if (fpResult.status === "singularidad" && !alertTriggered) {
                alertTriggered = true;
                alertMessage = "Divergencia o singularidad detectada en Punto Fijo.";
                alertRec = "Verifica la condición de convergencia |g'(x)| < 1 alrededor de la raíz. Rediseña g(x) de ser necesario.";
            } else if (fpResult.status === "max_iter" && !alertTriggered) {
                alertTriggered = true;
                alertMessage = "El método de Punto Fijo no convergió en el límite de iteraciones.";
                alertRec = "Es probable que g(x) sea divergente en la región de búsqueda. Prueba modificando la formulación de g(x) o el punto de partida x₀.";
            }
        }

        if (selectedCount === 0) {
            comparisonTableBody.innerHTML = `
                <tr>
                    <td colspan="6" style="color: var(--text-muted);">Por favor selecciona al menos un algoritmo para comparar.</td>
                </tr>
            `;
            renderEmptyPlot();
            didacticAlert.style.display = "none";
            return;
        }

        // Mostrar / Ocultar Alerta Didáctica
        if (alertTriggered) {
            alertTitle.textContent = "Incidencia Didáctica Detectada";
            alertDescription.textContent = alertMessage;
            alertRecommendation.textContent = alertRec;
            didacticAlert.style.display = "flex";
        } else {
            didacticAlert.style.display = "none";
        }

        // Graficar comparativa en Plotly
        plotComparisonGraphs(expr, bisResult, secResult, newtResult, fpResult);
    }

    function renderComparisonTableRow(name, result, color) {
        const tr = document.createElement("tr");
        const lastResidual = result.iterations.length > 0 ? result.iterations[result.iterations.length - 1].residual : 0;
        
        let statusText = result.status;
        let badgeClass = "badge-danger";
        if (result.status === "success") {
            statusText = "Éxito";
            badgeClass = "badge-success";
        } else if (result.status === "max_iter") {
            statusText = "Límite Iter";
            badgeClass = "badge-warning";
        } else if (result.status === "bolzano_violation") {
            statusText = "Bolzano";
            badgeClass = "badge-danger";
        } else if (result.status === "singularidad") {
            statusText = "Singularidad";
            badgeClass = "badge-danger";
        } else if (result.status === "interval_invalid") {
            statusText = "Intervalo Inv.";
            badgeClass = "badge-danger";
        }

        tr.innerHTML = `
            <td style="text-align: left; font-weight: 600; color: ${color};"><i class="fa-solid fa-calculator"></i> ${name}</td>
            <td><span class="badge ${badgeClass}">${statusText}</span></td>
            <td style="font-family: 'Fira Code', monospace;">${result.root !== null && !isNaN(result.root) ? result.root.toFixed(8) : 'N/A'}</td>
            <td>${result.iterations.length}</td>
            <td style="font-family: 'Fira Code', monospace;">${result.iterations.length > 0 && lastResidual !== null && !isNaN(lastResidual) ? lastResidual.toExponential(4) : '-'}</td>
            <td>${result.time} s</td>
        `;
        comparisonTableBody.appendChild(tr);
    }

    // Bisección local
    function runBisectionLocal(expr, a, b, tol, maxIter) {
        let fa, fb;
        try {
            fa = evaluateFunction(expr, a);
            fb = evaluateFunction(expr, b);
        } catch (err) {
            return { root: null, iterations: [], status: "singularidad" };
        }

        if (fa * fb >= 0) return { root: null, iterations: [], status: "bolzano_violation" };

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

    // Newton local
    function runNewtonLocal(expr, x0, tol, maxIter) {
        let iterations = [];
        let root = null;
        let status = "max_iter";
        let x = x0;

        for (let i = 1; i <= maxIter; i++) {
            try {
                let fx = evaluateFunction(expr, x);
                let dfx = evaluateDerivative(expr, x);

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
                    root: err,
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

    // Secante local
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

    // Punto Fijo local
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
                let fVal = exprF ? evaluateFunction(exprF, xVal) : (xVal - nextX);

                iterations.push({
                    iter: i,
                    xi: xVal,
                    sup: nextX,
                    root: diff,
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

    // 4. Graficar Comparativa Simultánea (Plotly.js)
    function plotComparisonGraphs(expr, bisResult, secResult, newtResult, fpResult) {
        let xMin = -2;
        let xMax = 4;

        let allXs = [];
        
        if (bisResult && bisResult.root !== null) allXs.push(bisResult.root);
        if (bisResult) bisResult.iterations.forEach(it => { if (typeof it.xi === 'number') allXs.push(it.xi); if (typeof it.root === 'number') allXs.push(it.root); });
        
        if (secResult && secResult.root !== null) allXs.push(secResult.root);
        if (secResult) secResult.iterations.forEach(it => { if (typeof it.xi === 'number') allXs.push(it.xi); if (typeof it.root === 'number') allXs.push(it.root); });
        
        if (newtResult && newtResult.root !== null) allXs.push(newtResult.root);
        if (newtResult) newtResult.iterations.forEach(it => { if (typeof it.xi === 'number') allXs.push(it.xi); if (typeof it.sup === 'number') allXs.push(it.sup); });

        if (fpResult && fpResult.root !== null) allXs.push(fpResult.root);
        if (fpResult) fpResult.iterations.forEach(it => { if (typeof it.xi === 'number') allXs.push(it.xi); if (typeof it.sup === 'number') allXs.push(it.sup); });

        allXs = allXs.filter(x => typeof x === 'number' && !isNaN(x) && isFinite(x));

        if (allXs.length > 0) {
            let minVal = Math.min(...allXs);
            let maxVal = Math.max(...allXs);
            let spread = Math.abs(maxVal - minVal);
            if (spread < 1e-5) spread = 1.0;
            xMin = minVal - spread * 0.4 - 1;
            xMax = maxVal + spread * 0.4 + 1;
        }

        // Generar curva f(x)
        let xPlot = [];
        let yPlot = [];
        const steps = 200;
        const dx = (xMax - xMin) / steps;

        for (let i = 0; i <= steps; i++) {
            let x = xMin + i * dx;
            try {
                let y = evaluateFunction(expr, x);
                if (typeof y === 'number' && !isNaN(y) && isFinite(y)) {
                    xPlot.push(x);
                    yPlot.push(y);
                } else {
                    xPlot.push(x);
                    yPlot.push(null);
                }
            } catch (e) {
                xPlot.push(x);
                yPlot.push(null);
            }
        }

        let traces = [];

        // Eje X de referencia
        traces.push({
            x: [xMin, xMax], y: [0, 0],
            type: 'scatter', mode: 'lines',
            line: { color: 'rgba(255, 255, 255, 0.1)', width: 1.5, dash: 'dash' },
            showlegend: false
        });

        // Curva f(x)
        traces.push({
            x: xPlot, y: yPlot,
            type: 'scatter', mode: 'lines',
            name: 'f(x)', line: { color: '#3b82f6', width: 2.5 }
        });

        // Dibujar límites iniciales del intervalo [a, b] si Bisección o Secante están activos
        if (compareBisection.checked || compareSecant.checked) {
            const aVal = parseFloat(aInputProf.value);
            const bVal = parseFloat(bInputProf.value);
            if (!isNaN(aVal) && !isNaN(bVal)) {
                let yRange = yPlot.filter(y => y !== null);
                let yMinVal = yRange.length > 0 ? Math.min(...yRange) : -10;
                let yMaxVal = yRange.length > 0 ? Math.max(...yRange) : 10;

                traces.push({
                    x: [aVal, aVal],
                    y: [yMinVal, yMaxVal],
                    type: 'scatter',
                    mode: 'lines',
                    name: 'Intervalo a / x₀',
                    line: { color: 'rgba(139, 92, 246, 0.4)', width: 1.2, dash: 'dash' }
                });
                traces.push({
                    x: [bVal, bVal],
                    y: [yMinVal, yMaxVal],
                    type: 'scatter',
                    mode: 'lines',
                    name: 'Intervalo b / x₁',
                    line: { color: 'rgba(236, 72, 153, 0.4)', width: 1.2, dash: 'dash' }
                });
            }
        }

        // 1. Trayectoria de Bisección (Puntos verdes)
        if (bisResult && bisResult.iterations.length > 0) {
            traces.push({
                x: bisResult.iterations.map(it => it.root).filter(x => x !== null),
                y: bisResult.iterations.map(it => it.residual).filter(y => y !== null),
                type: 'scatter', mode: 'markers+lines',
                name: 'Bisección',
                marker: { color: '#10b981', size: 6 },
                line: { color: '#10b981', width: 1, dash: 'dot' }
            });
        }

        // 2. Trayectoria de Secante (Puntos cian)
        if (secResult && secResult.iterations.length > 0) {
            traces.push({
                x: secResult.iterations.map(it => it.root).filter(x => x !== null),
                y: secResult.iterations.map(it => it.residual).filter(y => y !== null),
                type: 'scatter', mode: 'markers+lines',
                name: 'Secante',
                marker: { color: '#06b6d4', size: 6 },
                line: { color: '#06b6d4', width: 1, dash: 'dot' }
            });
        }

        // 3. Trayectoria de Newton (Puntos naranjas)
        if (newtResult && newtResult.iterations.length > 0) {
            traces.push({
                x: newtResult.iterations.map(it => it.xi).filter(x => x !== null),
                y: newtResult.iterations.map(it => it.residual).filter(y => y !== null),
                type: 'scatter', mode: 'markers+lines',
                name: 'Newton-Raphson',
                marker: { color: '#f59e0b', size: 6 },
                line: { color: '#f59e0b', width: 1, dash: 'dot' }
            });
        }

        // 4. Trayectoria de Punto Fijo (Puntos morados)
        if (fpResult && fpResult.iterations.length > 0) {
            traces.push({
                x: fpResult.iterations.map(it => it.xi).filter(x => x !== null),
                y: fpResult.iterations.map(it => it.residual).filter(y => y !== null),
                type: 'scatter', mode: 'markers+lines',
                name: 'Punto Fijo',
                marker: { color: '#a855f7', size: 6 },
                line: { color: '#a855f7', width: 1, dash: 'dot' }
            });
        }

        let layout = {
            paper_bgcolor: 'rgba(0,0,0,0)',
            plot_bgcolor: 'rgba(0,0,0,0)',
            font: { color: '#94a3b8', family: 'Outfit, sans-serif' },
            margin: { t: 20, b: 40, l: 50, r: 20 },
            xaxis: { gridcolor: 'rgba(255, 255, 255, 0.05)', zeroline: false },
            yaxis: { gridcolor: 'rgba(255, 255, 255, 0.05)', zeroline: false },
            showlegend: true
        };

        Plotly.newPlot('plot-container-prof', traces, layout, { responsive: true, displayModeBar: false });
    }

    function renderEmptyPlot() {
        let trace = {
            x: [-5, 5], y: [-5, 5],
            type: 'scatter', mode: 'lines',
            line: { color: 'rgba(255,255,255,0.05)' }
        };
        let layout = {
            paper_bgcolor: 'rgba(0,0,0,0)',
            plot_bgcolor: 'rgba(0,0,0,0)',
            font: { color: '#64748b' },
            margin: { t: 20, b: 40, l: 50, r: 20 }
        };
        Plotly.newPlot('plot-container-prof', [trace], layout, { responsive: true, displayModeBar: false });
    }

    // 5. Gráfico de Radar: Desempeño General del Grupo (Muestra Analítica Docente)
    function renderRadarChartClass() {
        let data = [{
            type: 'scatterpolar',
            r: [82, 75, 58, 67, 89],
            theta: ['Bisección', 'Newton-Raphson', 'Singularidades', 'Trazabilidad', 'Teoría Errores'],
            fill: 'toself',
            fillcolor: 'rgba(99, 102, 241, 0.15)',
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
            margin: { t: 20, b: 20, l: 40, r: 40 },
            font: { color: '#94a3b8' }
        };

        Plotly.newPlot('radar-chart-prof', data, layout, { responsive: true, displayModeBar: false });
    }

    // 6. Actualizar etiquetas y conteos de preguntas
    function updateSliderLabelsProf() {
        const total = parseInt(quizTotalQuestionsProf.value) || 10;
        const easyVal = parseInt(sliderEasyProf.value) || 0;
        const medVal = parseInt(sliderMediumProf.value) || 0;
        const hardVal = parseInt(sliderHardProf.value) || 0;

        lblEasyPct.textContent = `🟢 Fácil: ${easyVal}%`;
        lblMedPct.textContent = `🟡 Medio: ${medVal}%`;
        lblHardPct.textContent = `🔴 Difícil: ${hardVal}%`;

        const nEasy = Math.round((easyVal / 100) * total);
        const nMed = Math.round((medVal / 100) * total);
        const nHard = Math.max(0, total - nEasy - nMed);

        lblEasyCount.textContent = `(${nEasy} preguntas)`;
        lblMedCount.textContent = `(${nMed} preguntas)`;
        lblHardCount.textContent = `(${nHard} preguntas)`;
    }

    // 6b. Ajustar sliders proporcionalmente (100% total)
    function adjustSlidersProportionallyProf(changedSlider) {
        let vEasy = parseInt(sliderEasyProf.value) || 0;
        let vMed = parseInt(sliderMediumProf.value) || 0;
        let vHard = parseInt(sliderHardProf.value) || 0;

        let total = vEasy + vMed + vHard;
        let diff = 100 - total;

        if (diff !== 0) {
            let activeSliders = [];
            if (sliderEasyProf !== changedSlider) activeSliders.push(sliderEasyProf);
            if (sliderMediumProf !== changedSlider) activeSliders.push(sliderMediumProf);
            if (sliderHardProf !== changedSlider) activeSliders.push(sliderHardProf);

            if (activeSliders.length > 0) {
                let sumActives = activeSliders.reduce((sum, s) => sum + (parseInt(s.value) || 0), 0);
                
                if (sumActives === 0) {
                    let val = (parseInt(activeSliders[0].value) || 0) + diff;
                    activeSliders[0].value = Math.max(0, Math.min(100, val));
                } else {
                    activeSliders.forEach(s => {
                        let valVal = parseInt(s.value) || 0;
                        let proportion = valVal / sumActives;
                        let val = Math.round(valVal + (diff * proportion));
                        s.value = Math.max(0, Math.min(100, val));
                    });
                }
            }
        }

        vEasy = parseInt(sliderEasyProf.value) || 0;
        vMed = parseInt(sliderMediumProf.value) || 0;
        vHard = parseInt(sliderHardProf.value) || 0;
        let currentTotal = vEasy + vMed + vHard;
        
        if (currentTotal !== 100) {
            let error = 100 - currentTotal;
            if (sliderEasyProf !== changedSlider) {
                sliderEasyProf.value = (parseInt(sliderEasyProf.value) || 0) + error;
            } else {
                sliderMediumProf.value = (parseInt(sliderMediumProf.value) || 0) + error;
            }
        }

        updateSliderLabelsProf();
    }

    // 6c. Actualizar UI según la plantilla del examen
    function updateExamTemplateUI() {
        const val = examTemplate.value;
        if (val === "none") return;

        let easyPct = 40;
        let medPct = 40;
        let hardPct = 20;

        if (val === "parcial1") {
            easyPct = 60;
            medPct = 30;
            hardPct = 10;
        } else if (val === "parcial2") {
            easyPct = 20;
            medPct = 50;
            hardPct = 30;
        } else if (val === "custom") {
            return;
        }

        sliderEasyProf.value = easyPct;
        sliderMediumProf.value = medPct;
        sliderHardProf.value = hardPct;

        updateSliderLabelsProf();
    }

    // 7. Generador de código de clase interactivo
    function generateClassCode() {
        const total = parseInt(quizTotalQuestionsProf.value) || 10;
        const easyVal = parseInt(sliderEasyProf.value) || 0;
        const medVal = parseInt(sliderMediumProf.value) || 0;
        
        const nEasy = Math.round((easyVal / 100) * total);
        const nMed = Math.round((medVal / 100) * total);
        const nHard = Math.max(0, total - nEasy - nMed);

        const modeMap = {
            "theoretical": "T",
            "practical": "P",
            "mixed": "M"
        };

        const eMode = modeMap[quizModesProf.easy] || "T";
        const mMode = modeMap[quizModesProf.medium] || "P";
        const hMode = modeMap[quizModesProf.hard] || "M";

        const code = `NUM-2026-E${nEasy}${eMode}-M${nMed}${mMode}-D${nHard}${hMode}`;
        
        classCodeOutput.textContent = `CÓDIGO DE CLASE: ${code}`;
        classCodeOutput.style.display = "block";
        
        classCodeOutput.style.boxShadow = "0 0 15px var(--success)";
        setTimeout(() => classCodeOutput.style.boxShadow = "none", 1500);
    }

    // 8. Exportador JSON del parcial configurado
    function exportExamConfiguration() {
        const val = examTemplate.value;
        const total = parseInt(quizTotalQuestionsProf.value) || 10;
        const easyVal = parseInt(sliderEasyProf.value) || 0;
        const medVal = parseInt(sliderMediumProf.value) || 0;
        
        const nEasy = Math.round((easyVal / 100) * total);
        const nMed = Math.round((medVal / 100) * total);
        const nHard = Math.max(0, total - nEasy - nMed);

        const modeMap = {
            "theoretical": "T",
            "practical": "P",
            "mixed": "M"
        };

        const eMode = modeMap[quizModesProf.easy] || "T";
        const mMode = modeMap[quizModesProf.medium] || "P";
        const hMode = modeMap[quizModesProf.hard] || "M";

        const code = `NUM-2026-E${nEasy}${eMode}-M${nMed}${mMode}-D${nHard}${hMode}`;

        const config = {
            exam_id: "exam_" + Date.now(),
            template: val,
            total_questions: total,
            distribution: {
                easy: { pct: easyVal, count: nEasy, mode: quizModesProf.easy },
                medium: { pct: medVal, count: nMed, mode: quizModesProf.medium },
                hard: { pct: 100 - easyVal - medVal, count: nHard, mode: quizModesProf.hard }
            },
            class_code: code,
            export_date: new Date().toISOString()
        };

        const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(config, null, 2));
        const downloadAnchor = document.createElement("a");
        downloadAnchor.setAttribute("href", dataStr);
        downloadAnchor.setAttribute("download", `configuracion_parcial_${val}.json`);
        document.body.appendChild(downloadAnchor);
        downloadAnchor.click();
        downloadAnchor.remove();
    }
});
