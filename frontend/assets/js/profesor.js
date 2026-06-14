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

    // Evaluaciones y Código
    const examTemplate = document.getElementById("exam-template");
    const barEasy = document.getElementById("bar-easy");
    const barMed = document.getElementById("bar-med");
    const barHard = document.getElementById("bar-hard");
    const lblEasy = document.getElementById("lbl-easy");
    const lblMed = document.getElementById("lbl-med");
    const lblHard = document.getElementById("lbl-hard");
    const btnGenerateKey = document.getElementById("btn-generate-key");
    const classCodeOutput = document.getElementById("class-code-output");
    const btnExportExam = document.getElementById("btn-export-exam");

    // --- INITIALIZATION ---
    renderMathPreview();
    renderRadarChartClass();
    renderEmptyPlot();

    // --- EVENT LISTENERS ---
    exprInputProf.addEventListener("input", renderMathPreview);
    
    comparatorForm.addEventListener("submit", (e) => {
        e.preventDefault();
        compareAlgorithms();
    });

    examTemplate.addEventListener("change", updateExamTemplateUI);
    btnGenerateKey.addEventListener("click", generateClassCode);
    btnExportExam.addEventListener("click", exportExamConfiguration);

    // --- FUNCIONES CORE ---

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

    // 2. Evaluar Función f(x)
    function evaluateFunction(expr, x) {
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

        while (formatted.includes("^")) {
            formatted = formatted.replace(/([0-9x\(\)]+)\^([0-9x\(\)\.]+)/g, "Math.pow($1, $2)");
        }

        let evaluatedExpression = formatted.replace(/x/g, `(${x})`);
        
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

    // 3. Comparación de Algoritmos (Bisección vs Newton)
    function compareAlgorithms() {
        const expr = exprInputProf.value.trim();
        const a = parseFloat(aInputProf.value);
        const b = parseFloat(bInputProf.value);
        const x0 = parseFloat(x0InputProf.value);
        const tol = parseFloat(toleranceInputProf.value);
        const maxIter = parseInt(maxIterInputProf.value);

        comparisonTableBody.innerHTML = "";
        
        // 3.1. Correr Bisección
        let startBis = performance.now();
        let bisResult = null;
        try {
            bisResult = runBisectionLocal(expr, a, b, tol, maxIter);
            bisResult.time = ((performance.now() - startBis) / 1000).toFixed(6);
        } catch (e) {
            bisResult = { root: null, iterations: [], status: "error", time: "0.000000" };
        }

        // 3.2. Correr Newton-Raphson
        let startNewt = performance.now();
        let newtResult = null;
        try {
            newtResult = runNewtonLocal(expr, x0, tol, maxIter);
            newtResult.time = ((performance.now() - startNewt) / 1000).toFixed(6);
        } catch (e) {
            newtResult = { root: null, iterations: [], status: "error", time: "0.000000" };
        }

        // Llenar la Tabla Comparativa
        renderComparisonTableRow("Bisección (Cerrado)", bisResult, "var(--success)");
        renderComparisonTableRow("Newton-Raphson (Abierto)", newtResult, "var(--warning)");

        // Graficar comparativa en Plotly
        plotComparisonGraphs(expr, bisResult, newtResult);
    }

    function renderComparisonTableRow(name, result, color) {
        const tr = document.createElement("tr");
        const lastResidual = result.iterations.length > 0 ? result.iterations[result.iterations.length - 1].residual : 0;
        
        tr.innerHTML = `
            <td style="text-align: left; font-weight: 600; color: ${color};"><i class="fa-solid fa-calculator"></i> ${name}</td>
            <td><span class="badge ${result.status === 'success' ? 'badge-success' : 'badge-danger'}">${result.status}</span></td>
            <td style="font-family: 'Fira Code', monospace;">${result.root !== null ? result.root.toFixed(8) : 'N/A'}</td>
            <td>${result.iterations.length}</td>
            <td style="font-family: 'Fira Code', monospace;">${result.iterations.length > 0 ? lastResidual.toExponential(4) : '-'}</td>
            <td>${result.time} s</td>
        `;
        comparisonTableBody.appendChild(tr);
    }

    // Bisección local
    function runBisectionLocal(expr, a, b, tol, maxIter) {
        let fa = evaluateFunction(expr, a);
        let fb = evaluateFunction(expr, b);

        if (fa * fb >= 0) return { root: null, iterations: [], status: "interval_invalid" };

        let iterations = [];
        let root = null;
        let status = "max_iter";

        for (let i = 1; i <= maxIter; i++) {
            let c = (a + b) / 2;
            let fc = evaluateFunction(expr, c);
            let err = Math.abs(b - a) / 2;

            iterations.push({ iter: i, xi: c, residual: fc });

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

        return { root, iterations, status };
    }

    // Newton local
    function runNewtonLocal(expr, x0, tol, maxIter) {
        let iterations = [];
        let root = null;
        let status = "max_iter";
        let x = x0;

        for (let i = 1; i <= maxIter; i++) {
            let fx = evaluateFunction(expr, x);
            let dfx = evaluateDerivative(expr, x);

            if (Math.abs(dfx) < 1e-12) return { root: null, iterations: [], status: "singularidad" };

            let nextX = x - (fx / dfx);
            let err = Math.abs(nextX - x);

            iterations.push({ iter: i, xi: x, residual: fx });

            if (err < tol || Math.abs(fx) < 1e-12) {
                root = nextX;
                status = "success";
                break;
            }

            x = nextX;
        }

        return { root, iterations, status };
    }

    // 4. Graficar Comparativa Simultánea (Plotly.js)
    function plotComparisonGraphs(expr, bisResult, newtResult) {
        let xMin = -2;
        let xMax = 4;

        let allXs = [];
        if (bisResult.root !== null) allXs.push(bisResult.root);
        if (newtResult.root !== null) allXs.push(newtResult.root);
        bisResult.iterations.forEach(it => allXs.push(it.xi));
        newtResult.iterations.forEach(it => allXs.push(it.xi));

        if (allXs.length > 0) {
            let minVal = Math.min(...allXs);
            let maxVal = Math.max(...allXs);
            xMin = minVal - Math.abs(maxVal - minVal) * 0.4 - 1;
            xMax = maxVal + Math.abs(maxVal - minVal) * 0.4 + 1;
        }

        // Generar curva f(x)
        let xPlot = [];
        let yPlot = [];
        const steps = 200;
        const dx = (xMax - xMin) / steps;

        for (let i = 0; i <= steps; i++) {
            let x = xMin + i * dx;
            try {
                xPlot.push(x);
                yPlot.push(evaluateFunction(expr, x));
            } catch (e) {
                xPlot.push(x);
                yPlot.push(null);
            }
        }

        // Trazas de Plotly
        let traceFunc = {
            x: xPlot, y: yPlot,
            type: 'scatter', mode: 'lines',
            name: 'f(x)', line: { color: '#3b82f6', width: 2.5 }
        };

        let traceAxis = {
            x: [xMin, xMax], y: [0, 0],
            type: 'scatter', mode: 'lines',
            line: { color: 'rgba(255, 255, 255, 0.1)', width: 1.5, dash: 'dash' },
            showlegend: false
        };

        // Trayectoria de Bisección (Puntos verdes)
        let traceBis = {
            x: bisResult.iterations.map(it => it.xi),
            y: bisResult.iterations.map(it => it.residual),
            type: 'scatter', mode: 'markers+lines',
            name: 'Puntos Bisección',
            marker: { color: '#10b981', size: 6 },
            line: { color: '#10b981', width: 1, dash: 'dot' }
        };

        // Trayectoria de Newton (Puntos naranjas)
        let traceNewt = {
            x: newtResult.iterations.map(it => it.xi),
            y: newtResult.iterations.map(it => it.residual),
            type: 'scatter', mode: 'markers+lines',
            name: 'Puntos Newton',
            marker: { color: '#f59e0b', size: 6 },
            line: { color: '#f59e0b', width: 1, dash: 'dot' }
        };

        let layout = {
            paper_bgcolor: 'rgba(0,0,0,0)',
            plot_bgcolor: 'rgba(0,0,0,0)',
            font: { color: '#94a3b8', family: 'Outfit, sans-serif' },
            margin: { t: 20, b: 40, l: 50, r: 20 },
            xaxis: { gridcolor: 'rgba(255, 255, 255, 0.05)', zeroline: false },
            yaxis: { gridcolor: 'rgba(255, 255, 255, 0.05)', zeroline: false },
            showlegend: true
        };

        Plotly.newPlot('plot-container-prof', [traceFunc, traceAxis, traceBis, traceNewt], layout, { responsive: true, displayModeBar: false });
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

    // 6. Actualizar barras de dificultad de exámenes
    function updateExamTemplateUI() {
        const val = examTemplate.value;
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
        }

        // Animar barras
        barEasy.style.width = `${easyPct}%`;
        barMed.style.width = `${medPct}%`;
        barHard.style.width = `${hardPct}%`;

        // Actualizar textos
        lblEasy.textContent = `${easyPct}%`;
        lblMed.textContent = `${medPct}%`;
        lblHard.textContent = `${hardPct}%`;
    }

    // 7. Generador de código de clase interactivo
    function generateClassCode() {
        classCodeOutput.style.display = "block";
        
        // Efecto glow de generación
        classCodeOutput.style.boxShadow = "var(--shadow-glow)";
        setTimeout(() => classCodeOutput.style.boxShadow = "none", 1500);
    }

    // 8. Exportador JSON del parcial configurado
    function exportExamConfiguration() {
        const val = examTemplate.value;
        const config = {
            exam_id: "exam_" + Date.now(),
            template: val,
            easy_distribution: lblEasy.textContent,
            medium_distribution: lblMed.textContent,
            hard_distribution: lblHard.textContent,
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
