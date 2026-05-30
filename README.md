# Proyecto de Programacion Numerica

Aplicacion de consola en Python para practicar metodos numericos, comparar convergencia de algoritmos y visualizar resultados. El proyecto actualmente cubre ecuaciones no lineales, numero de Euler, numero Pi, evaluacion segura con evasion de singularidades y graficas 3D usando POO.

## En que consiste

El sistema centraliza practicas de metodos numericos en un menu interactivo con submenus por tema. El enfoque actual del desarrollo prioriza:

- Simplicidad de uso para estudiantes.
- Codigo orientado a objetos en modulos clave.
- Comparacion didactica entre metodos lentos y metodos de alta precision.

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