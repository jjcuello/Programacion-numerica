# Proyecto de Programacion Numerica

Aplicacion de consola en Python para practicar metodos numericos, comparar convergencia de algoritmos y visualizar resultados. El proyecto actualmente cubre ecuaciones no lineales, numero de Euler, numero Pi, evaluacion segura con evasion de singularidades y graficas 3D usando POO.

## En que consiste

El sistema centraliza practicas de metodos numericos en un menu interactivo con submenus por tema. El enfoque actual del desarrollo prioriza:

- Simplicidad de uso para estudiantes.
- Codigo orientado a objetos en modulos clave.
- Comparacion didactica entre metodos lentos y metodos de alta precision.

## Utilidad actual y proyeccion academica

En su estado actual, el proyecto ya es util como laboratorio academico de metodos numericos. No se limita a calcular resultados: tambien permite observar convergencia, comparar precision entre algoritmos, visualizar funciones y reforzar conceptos matematicos con ejemplos guiados.

Su utilidad actual se concentra en cinco frentes:

- Practica de resolucion de ecuaciones no lineales con metodos clasicos.
- Comparacion didactica de velocidad, error y estabilidad entre algoritmos.
- Analisis numerico de constantes matematicas como e y pi.
- Evaluacion segura de funciones con singularidades o puntos problematicos.
- Visualizacion matematica con graficas 2D, figuras 3D y animaciones.

La direccion de crecimiento recomendada no es convertir el repositorio en una coleccion mas grande de scripts aislados, sino en una plataforma de aprendizaje y analisis numerico. En esa linea, el proyecto puede escalar hacia:

- Plataforma docente para cursos de metodos numericos.
- Banco reproducible de experimentos numericos.
- Herramienta de apoyo para tutorias, estudio autonomo y clases practicas.
- Base de un trabajo de investigacion de pregrado orientado a aprendizaje asistido por software.

## Vision v0.2

La version v0.2 propone evolucionar desde una aplicacion CLI monolitica hacia una arquitectura modular centrada en reutilizacion, trazabilidad de experimentos y escalabilidad academica.

Objetivo central de v0.2:

- Separar el motor numerico de la interfaz de usuario para que el proyecto pueda crecer hacia CLI avanzada, interfaz web, exportacion de reportes y evaluacion formal en contexto academico.

Preguntas que v0.2 busca responder:

- Que metodo conviene segun el tipo de problema y las condiciones iniciales.
- Como cambia la convergencia cuando varian tolerancia, semilla o precision.
- Que errores o patrones de uso cometen con mas frecuencia los estudiantes.
- Como transformar ejecuciones sueltas en experimentos comparables y reproducibles.

## Arquitectura objetivo v0.2

La arquitectura propuesta para v0.2 se organiza por capas y responsabilidades.

```mermaid
flowchart TD
    UI[Interfaces de usuario\nCLI / Web / Reportes] --> APP[Casos de uso y orquestacion]
    APP --> CORE[Core numerico]
    APP --> ANALYSIS[Analisis y metricas]
    APP --> TUTOR[Tutor didactico y recomendador]
    CORE --> METHODS[Metodos numericos]
    CORE --> MODELS[Modelos de problema]
    ANALYSIS --> STORE[Persistencia de sesiones y experimentos]
    TUTOR --> STORE
    UI --> STORE
```

### 1) Capa de interfaces

Responsabilidad:

- Recibir entradas del usuario y presentar resultados sin mezclar la logica numerica con `input()` y `print()`.

Versiones previstas:

- CLI mejorada para uso rapido en clase o laboratorio.
- Interfaz web para comparaciones visuales, historiales y dashboards.
- Exportacion de resultados a JSON, CSV y PDF.

### 2) Capa de aplicacion u orquestacion

Responsabilidad:

- Convertir una accion de usuario en un flujo reproducible: construir el problema, ejecutar el metodo, capturar iteraciones, medir error y devolver un reporte.

Casos de uso esperados:

- Resolver un problema con un metodo.
- Comparar varios metodos sobre el mismo problema.
- Repetir un experimento con diferentes tolerancias o semillas.
- Guardar y recuperar sesiones.

### 3) Core numerico

Responsabilidad:

- Definir contratos estables para funciones, problemas, resultados e iteraciones.

Elementos clave:

- Parser seguro de expresiones matematicas.
- Modelo comun para problemas escalares, sistemas no lineales y evaluaciones seguras.
- Estructura comun de salida para todos los metodos: estado, raiz o aproximacion, residual, iteraciones, tiempo, error y metadatos.

### 4) Capa de metodos numericos

Responsabilidad:

- Implementar los algoritmos como componentes reutilizables, independientes de la interfaz.

Familias de metodos objetivo:

- Raices de ecuaciones: biseccion, secante, Newton-Raphson, punto fijo.
- Sistemas no lineales.
- Analisis de constantes: e y pi.
- Evaluacion segura con evasion de singularidades.
- Futuro v0.2+: matrices, sistemas lineales, interpolacion y EDO.

### 5) Capa de analisis y metricas

Responsabilidad:

- Convertir una ejecucion en evidencia numerica interpretable.

Indicadores recomendados:

- Error absoluto y error relativo.
- Residual por iteracion.
- Tiempo de ejecucion.
- Tasa de convergencia observada.
- Sensibilidad a semilla inicial.
- Estabilidad ante cambios de precision y tolerancia.

### 6) Capa didactica y recomendador

Responsabilidad:

- Agregar valor pedagogico, no solo computacional.

Funciones objetivo:

- Sugerir el metodo mas conveniente segun propiedades del problema.
- Advertir por que un metodo puede fallar.
- Explicar la interpretacion de una tabla de iteraciones.
- Proponer ejercicios, preguntas de autoevaluacion y retroalimentacion.

### 7) Persistencia y trazabilidad

Responsabilidad:

- Guardar sesiones y experimentos para comparacion posterior.

Datos a persistir:

- Funcion o sistema evaluado.
- Parametros de entrada.
- Metodo usado.
- Historial de iteraciones.
- Resultados finales y metricas.
- Fecha, version y entorno de ejecucion.

## Estructura propuesta del proyecto para v0.2

La siguiente estructura no reemplaza de inmediato la organizacion actual; funciona como objetivo de refactor progresivo.

```text
src/
  app/
    use_cases/
    services/
  core/
    expressions/
    models/
    results/
    validation/
  methods/
    roots/
    systems/
    constants/
    safe_eval/
    linear_algebra/
  analysis/
    convergence/
    benchmarking/
    reports/
  tutoring/
    recommendations/
    explanations/
    quizzes/
  infrastructure/
    storage/
    exporters/
    plotting/
  interfaces/
    cli/
    web/
tests/
docs/
examples/
```

## Ruta de migracion hacia v0.2

La evolucion propuesta puede hacerse por etapas, sin romper el valor actual del proyecto.

### Etapa 1: desacople del nucleo

- Extraer la logica numerica de los modulos actuales a funciones y clases sin dependencias de consola.
- Estandarizar un formato comun de resultado.
- Agregar pruebas unitarias para los metodos principales.

### Etapa 2: comparacion y trazabilidad

- Registrar iteraciones, errores y tiempos de todos los metodos.
- Implementar comparacion de varios metodos sobre una misma funcion.
- Guardar sesiones de experimentos en JSON o SQLite.

### Etapa 3: capa didactica

- Incorporar recomendaciones automaticas por reglas.
- Agregar explicaciones contextuales y alertas de convergencia.
- Construir ejercicios guiados y mini evaluaciones.

### Etapa 4: interfaz escalable

- Mantener la CLI como modo base.
- Incorporar una interfaz web para analisis visual y seguimiento de sesiones.
- Preparar exportacion de reportes para uso docente y academico.

## Potencial como tesis de pregrado

La linea mas prometedora para investigacion no es solo ampliar el numero de metodos, sino estudiar como una plataforma de analisis numerico guiado mejora el aprendizaje.

Una formulacion posible del proyecto de tesis seria:

- Diseno e implementacion de una plataforma didactica para el aprendizaje de metodos numericos con analisis de convergencia, recomendacion automatica y trazabilidad de experimentos.

El aporte academico de v0.2 puede sostenerse sobre cuatro ejes:

- Ingenieria de software: arquitectura modular y extensible.
- Analisis numerico: comparacion rigurosa de metodos y metricas.
- Visualizacion: interpretacion grafica de convergencia y error.
- Innovacion educativa: apoyo al aprendizaje, autoevaluacion y seguimiento.

## Estructura del proyecto

- [run.py](run.py): punto de entrada principal y navegacion por menus/submenus.
- [metodos](metodos): paquete con todos los modulos numericos.
- [graficas](graficas): imagenes generadas por los modulos.
- [documentacion](documentacion): notas y material de apoyo.
- [requirements.txt](requirements.txt): dependencias del entorno.

## Requisitos

- Python 3.10 o superior.
- pip disponible.

Dependencias principales:

- numpy
- scipy
- sympy
- matplotlib

## Guia de instalacion

### 1) Clonar repositorio

```bash
git clone https://github.com/jjcuello/ver-0-1-0-numericos.git
cd ver-0-1-0-numericos
```

### 2) Crear entorno virtual local del proyecto

Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3) Instalar dependencias

```bash
pip install -r requirements.txt
```

## Guia de ejecucion

```bash
python run.py
```

Menu principal actual en [run.py](run.py):

- 1: Metodo de biseccion
- 2: Metodo de interpolacion lineal secante
- 3: Metodo Newton / Raphson
- 4: Metodo Punto Fijo
- 5: Proximamente (Blasr-Tron)
- 6: Proximamente (Division Sintetica)
- 7: Graficas 3D con POO
- 8: Analisis del numero de Euler (e)
- 9: Evaluacion con evasion de singularidad
- 10: Analisis del numero Pi
- 11: Animaciones trigonometricas
- 12: Salir

Submenu de Euler en [run.py](run.py):

- 1: Metodos de generacion de e
- 2: Demostracion Euler
- 3: Volver

Submenu de Pi en [run.py](run.py):

- 1: Metodos de calculo de pi
- 2: Demostracion Pi
- 3: Volver

## Modulos y responsabilidades

- [metodos/biseccion.py](metodos/biseccion.py):
  Metodo de biseccion, parseo de expresiones con SymPy, sugerencia de intervalos y grafica 2D.

- [metodos/secante.py](metodos/secante.py):
  Metodo de la secante con soporte de graficacion y evaluacion de funciones del usuario.

- [metodos/newton_raphson.py](metodos/newton_raphson.py):
  Metodo de Newton / Raphson con estructura POO. Construye la funcion y su derivada desde expresiones de SymPy, ejecuta iteraciones con tabla de convergencia y soporta caso fijo + funcion del usuario.

  Formula principal:
  - x_{n+1} = x_n - f(x_n)/f'(x_n)

- [metodos/punto_fijo.py](metodos/punto_fijo.py):
  Metodo de Punto Fijo con estructura POO para iteraciones de la forma x(i+1)=g(x(i)). Incluye ejemplo guiado, modo con funcion del usuario y verificacion del resultado por residual.

  Formula principal:
  - x_{n+1} = g(x_n)

- [metodos/euler.py](metodos/euler.py):
  Analisis de e con metodos numericos y demostracion incremental orientada a objetos.

  Metodos de generacion de e:
  - Serie de Taylor
  - Limite (1 + 1/n)^n
  - Fraccion continua
  - Newton sobre ln(x)-1

  Demostracion Euler:
  - Formula fija mostrada en pantalla: lim_{x->inf} (1 + 1/x)^x = e
  - Valor de e mostrado con 20 decimales junto a la formula
  - Modos: Demo, Rapido y En vivo (resultado sobre resultado)
  - Control de delay y muestreo (mostrar cada k iteraciones)

- [metodos/pi.py](metodos/pi.py):
  Nuevo modulo para analisis del numero Pi, siguiendo la misma estructura de trabajo que Euler.

  Metodos de calculo de pi:
  - Leibniz
  - Nilakantha
  - Arquimedes (poligono inscrito)
  - Ramanujan
  - Chudnovsky

  Caracteristicas didacticas:
  - Muestra formulas en pantalla (comparacion global y metodo individual)
  - Evidencia pedagogica de Leibniz con 10.000 iteraciones
  - Reporte de decimales correctos fraccionarios y cifras totales correctas

  Demostracion Pi:
  - Formula fija basada en la serie de Leibniz
  - Modos: Demo, Rapido y En vivo
  - Control de delay y muestreo

- [metodos/evasion_singularidad.py](metodos/evasion_singularidad.py):
  Evaluacion segura de funciones con deteccion de singularidades y aproximacion por limites laterales.

- [metodos/graficas_3d.py](metodos/graficas_3d.py):
  Modulo POO de figuras 3D con clase base abstracta y clases concretas.

- [metodos/animaciones_trigonometricas.py](metodos/animaciones_trigonometricas.py):
  Modulo POO para animaciones didacticas de funciones trigonometricas en 2D y 3D.

  Incluye actualmente:
  - Seno dinamica con variacion de amplitud, frecuencia y fase.
  - Interferencia de ondas con visualizacion de senales individuales y su suma.
  - Superficie trigonometrica 3D en movimiento.
  - Exportacion a GIF (con fallback automatico a PNG cuando el entorno no permite GIF).

  Proximamente:
  - Ingreso de funciones personalizadas del usuario para animarlas en 2D y 3D.

- [metodos/run_graficas_3d.py](metodos/run_graficas_3d.py):
  Lanzador directo del modulo de graficas 3D.

- [metodos/sistemas_no_lineales.py](metodos/sistemas_no_lineales.py):
  Ejercicios de sistemas no lineales con SymPy y scipy.optimize.fsolve.

- [metodos/sistemas_no_lineales_basico.py](metodos/sistemas_no_lineales_basico.py):
  Variante simplificada del modulo anterior.

## Proximas actualizaciones sugeridas

- Agregar un modulo educativo de matrices, manteniendo POO y simplicidad, que incluya operaciones basicas (suma, producto, transpuesta), resolucion de sistemas lineales $Ax=b$ (Gauss, Gauss-Jordan y LU), metodos iterativos (Jacobi y Gauss-Seidel), determinante e inversa, y visualizaciones didacticas de convergencia (residual $||Ax-b||$, error por iteracion y mapas de calor), con modos Demo, Rapido y En vivo para reforzar la interpretacion matematica.

## Formulas matematicas implementadas

Esta seccion resume las expresiones matematicas que el programa calcula, compara o demuestra. Esta orientada a usuarios de perfil matematico.

### 1) Ecuaciones no lineales

- Metodo de biseccion sobre una funcion $f(x)$ en un intervalo $[a,b]$ con cambio de signo:

$$
c_n = \frac{a_n + b_n}{2}
$$

- Metodo de la secante:

$$
x_{n+1} = x_n - f(x_n)\frac{x_n - x_{n-1}}{f(x_n)-f(x_{n-1})}
$$

- Metodo de Newton / Raphson:

$$
x_{n+1} = x_n - \frac{f(x_n)}{f'(x_n)}
$$

### 2) Numero de Euler $e$

- Definicion por limite (demostracion incremental):

$$
e = \lim_{x\to\infty}\left(1+\frac{1}{x}\right)^x
$$

- Serie de Taylor:

$$
e = \sum_{k=0}^{\infty}\frac{1}{k!}
$$

- Fraccion continua de $e$ (forma usada en el modulo):

$$
e = [2; 1,2,1,1,4,1,1,6,1,\dots]
$$

- Newton aplicado a $\ln(x)-1=0$:

$$
x_{n+1} = x_n - \frac{\ln(x_n)-1}{1/x_n}
$$

### 3) Numero $\pi$

- Serie de Leibniz (demostracion incremental y contraste didactico):

$$
\pi = 4\sum_{k=0}^{\infty}\frac{(-1)^k}{2k+1}
$$

- Serie de Nilakantha:

$$
\pi = 3 + \sum_{k=1}^{\infty}(-1)^{k+1}\frac{4}{(2k)(2k+1)(2k+2)}
$$

- Aproximacion de Arquimedes por poligono inscrito (radio 1):

$$
\pi \approx n\sin\left(\frac{\pi}{n}\right)
$$

- Serie de Ramanujan:

$$
\frac{1}{\pi} = \frac{2\sqrt{2}}{9801}
\sum_{k=0}^{\infty}
\frac{(4k)!(1103+26390k)}{(k!)^4\,396^{4k}}
$$

- Serie de Chudnovsky (forma computacional de alta precision):

$$
\pi = \frac{426880\sqrt{10005}}
{\sum_{k=0}^{\infty}
\frac{(-1)^k(6k)!(13591409+545140134k)}{(3k)!(k!)^3\,640320^{3k}}}
$$

### Utilidad matematica del programa

- Permite comparar velocidad de convergencia entre metodos.
- Muestra error absoluto y decimales correctos para evaluar precision real.
- Evidencia por que algunas formulas son didacticas pero poco practicas (por ejemplo Leibniz) y por que otras son eficientes para alta precision (Ramanujan/Chudnovsky).

## Compatibilidad y entorno

- Se normalizo el conflicto de rutas por mayusculas/minusculas para compatibilidad entre Windows y Linux.
- La apertura de graficas se unifico para Windows, macOS y Linux.
- Se agrego [requirements.txt](requirements.txt) para reproducibilidad.
- Se recomienda usar .venv local dentro del proyecto.

## Historial reciente de cambios (resumen)

- Clonacion y normalizacion de rutas de modulo para evitar colisiones en Windows.
- Incorporacion de requirements y ajuste de entorno virtual local.
- Mejora multiplataforma de apertura de graficas.
- Creacion de README y documentacion inicial del proyecto.
- Submenu de Euler con separacion entre metodos y demostracion.
- Implementacion de demostracion incremental de Euler en POO.
- Modos de visualizacion para Euler: Demo, Rapido y En vivo.
- Visualizacion de e con 20 decimales junto a la formula objetivo.
- Creacion del modulo de Pi con estructura homologa a Euler.
- Inclusion de Ramanujan y Chudnovsky para alta precision.
- Inclusiones didacticas de formulas y analisis de convergencia de Leibniz.

## Creditos

- Autor: José Javier Cuello
- Profesor: Yancelis Noguera
- Institucion: I.U. Santiago Mariño