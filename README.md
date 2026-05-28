# Proyecto de Programacion Numerica

Aplicacion de consola en Python para practicar metodos numericos y visualizacion de resultados. El proyecto incluye resolucion de ecuaciones no lineales, aproximacion del numero de Euler, evaluacion segura de funciones con posibles singularidades y graficas 3D usando POO.

## En que consiste

El programa principal centraliza varias practicas numericas en un menu interactivo. Cada modulo implementa un enfoque distinto:

- Busqueda de raices por biseccion.
- Busqueda de raices por secante.
- Analisis de aproximaciones para el numero de Euler (e).
- Evaluacion robusta de funciones cerca de singularidades.
- Generacion de figuras 3D con enfoque orientado a objetos.

## Estructura del proyecto

- [run.py](run.py): punto de entrada principal con menu general.
- [metodos](metodos): paquete con los modulos de metodos numericos.
- [graficas](graficas): imagenes generadas por los modulos.
- [documentacion](documentacion): notas explicativas y material de apoyo.
- [requirements.txt](requirements.txt): dependencias del proyecto.

## Requisitos

- Python 3.10 o superior.
- `pip` disponible.

Dependencias principales:

- `numpy`
- `scipy`
- `sympy`
- `matplotlib`

## Guia de instalacion

### 1) Clonar repositorio

```bash
git clone https://github.com/jjcuello/ver-0-1-0-numericos.git
cd ver-0-1-0-numericos
```

### 2) Crear entorno virtual

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

Ejecutar el menu principal:

```bash
python run.py
```

Opciones actuales del menu en [run.py](run.py):

- `1`: Metodo de biseccion.
- `2`: Metodo de secante.
- `7`: Graficas 3D con POO.
- `8`: Analisis del numero de Euler.
- `9`: Evaluacion con evasion de singularidad.

Las opciones `3`, `4`, `5` y `6` estan reservadas para futuras ampliaciones.

## Modulos y responsabilidades

- [metodos/biseccion.py](metodos/biseccion.py):
  Implementa el metodo de biseccion, parseo seguro de expresiones con SymPy, sugerencia automatica de intervalos y generacion de grafica 2D de la funcion.

- [metodos/secante.py](metodos/secante.py):
  Implementa el metodo de la secante. Reutiliza utilidades de [metodos/biseccion.py](metodos/biseccion.py) para parseo, sugerencias y graficacion.

- [metodos/euler.py](metodos/euler.py):
  Incluye la clase `AnalizadorEuler` para aproximar `e` con distintos metodos (Taylor, limite, fraccion continua, entre otros), comparar error, tiempo e iteraciones, y soportar precision decimal.

- [metodos/evasion_singularidad.py](metodos/evasion_singularidad.py):
  Provee una estrategia para evaluar funciones en puntos problematicos. Usa deteccion de singularidades y limites laterales para clasificar casos como removible, polo o indeterminado.

- [metodos/graficas_3d.py](metodos/graficas_3d.py):
  Implementa figuras 3D con POO (clase base abstracta y clases concretas como `Esfera`, `Cilindro`, `Cono`, etc.), guarda imagenes en [graficas](graficas) y gestiona apertura automatica multiplataforma.

- [metodos/run_graficas_3d.py](metodos/run_graficas_3d.py):
  Lanzador directo del modulo de graficas 3D.

- [metodos/sistemas_no_lineales.py](metodos/sistemas_no_lineales.py):
  Coleccion de ejercicios de sistemas no lineales usando SymPy y `scipy.optimize.fsolve`.

- [metodos/sistemas_no_lineales_basico.py](metodos/sistemas_no_lineales_basico.py):
  Variante simplificada del modulo de sistemas no lineales.

## Salidas del programa

- Las graficas se guardan en [graficas](graficas).
- La apertura de imagenes intenta usar el visor del sistema operativo (Windows, macOS o Linux).

## Creditos

- Autor: José Javier Cuello
- Profesor: Yancelis Noguera
- Institucion: I.U. Santiago Mariño