import math
import os
from pathlib import Path
import re
import shutil
import subprocess

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sympy import E, lambdify, pi, symbols
from sympy.parsing.sympy_parser import (
    convert_xor,
    implicit_multiplication_application,
    parse_expr,
    standard_transformations,
)


def funcion(x):
    """Funcion de ejemplo: f(x) = x^3 - x - 2."""
    return x**3 - x - 2

def mostrar_titulo():
    print("==================================================================================")
    print(" Programacion Numerica - Resolucion de Ecuaciones No lineales - Jose Javier Cuello")
    print("==================================================================================")

def mostrar_menu():
    print("\nMenu principal:")
    print("1. Ejemplo de Metodo de biseccion, x**3 - x - 2 = 0")
    print("2. Introduce tu propia funcion")
    print("3. Salir")

def leer_opcion():
    opcion = input("Elige una opcion (1-3): ").strip()
    return opcion

def biseccion(func, a, b, tolerancia=1e-6, max_iteraciones=100):
    if func(a) * func(b) >= 0:
        raise ValueError(
            "El intervalo [a, b] no es valido: f(a) y f(b) deben tener signos opuestos."
        )

    print("Iter |         a |         b |         c |       f(c)")
    print("-" * 58)

    for i in range(1, max_iteraciones + 1):
        c = (a + b) / 2
        fc = func(c)

        print(f"{i:4d} | {a:9.6f} | {b:9.6f} | {c:9.6f} | {fc:10.6f}")

        if abs(fc) < tolerancia or (b - a) / 2 < tolerancia:
            return c, i

        if func(a) * func(c) < 0:
            b = c  # La raiz esta en la mitad izquierda
        else:
            a = c  # La raiz esta en la mitad derecha

    return c, max_iteraciones


def resolver_ejemplo_fijo():
    a = 1
    b = 2
    tolerancia = 1e-6

    raiz, iteraciones = biseccion(funcion, a, b, tolerancia)
    print("\nResultado:")
    print(f"Raiz aproximada: {raiz:.6f}")
    print(f"Iteraciones: {iteraciones}")
    print(f"Comprobacion f(raiz): {funcion(raiz):.6e}")


def sugerir_intervalos(func, inicio=-10, fin=10, puntos=400, limite=5):
    valores_x = np.linspace(inicio, fin, puntos)
    intervalos = []
    punto_previo = None
    valor_previo = None

    for punto in valores_x:
        try:
            valor_actual = float(func(float(punto)))
        except (ValueError, ZeroDivisionError, OverflowError):
            punto_previo = None
            valor_previo = None
            continue

        if not math.isfinite(valor_actual):
            punto_previo = None
            valor_previo = None
            continue

        if valor_actual == 0:
            intervalo = (float(punto), float(punto))
            if intervalo not in intervalos:
                intervalos.append(intervalo)
        elif punto_previo is not None and valor_previo * valor_actual < 0:
            intervalo = (float(punto_previo), float(punto))
            intervalos.append(intervalo)

        if len(intervalos) >= limite:
            break

        punto_previo = float(punto)
        valor_previo = valor_actual

    return intervalos


def limpiar_texto_para_archivo(texto):
    texto_limpio = texto.lower().replace("**", "_pot_")
    texto_limpio = re.sub(r"[^a-z0-9]+", "_", texto_limpio)
    texto_limpio = texto_limpio.strip("_")
    return texto_limpio[:80] or "funcion"


def formatear_valor_para_archivo(valor):
    texto = f"{valor:.4f}".replace("-", "m").replace(".", "_")
    return texto


def abrir_grafica(ruta_grafica):
    if hasattr(os, "startfile"):
        os.startfile(ruta_grafica)
        return

    for programa in ("open", "xdg-open"):
        ruta_programa = shutil.which(programa)
        if ruta_programa:
            subprocess.Popen(
                [ruta_programa, str(ruta_grafica)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            return

    raise ValueError("No se pudo abrir la grafica automaticamente en este sistema.")


def graficar_funcion(func, expresion, a, b, raiz=None, puntos=300):
    valores_x = np.linspace(a, b, puntos)
    puntos_validos_x = []
    puntos_validos_y = []

    for punto in valores_x:
        try:
            valor = float(func(float(punto)))
        except (ValueError, ZeroDivisionError, OverflowError):
            continue

        if math.isfinite(valor):
            puntos_validos_x.append(float(punto))
            puntos_validos_y.append(valor)

    if not puntos_validos_x:
        raise ValueError("No se pudo generar la grafica en el intervalo indicado.")

    figura, eje = plt.subplots(figsize=(8, 5))
    eje.plot(puntos_validos_x, puntos_validos_y, label="f(x)", color="tab:blue")
    eje.axhline(0, color="black", linewidth=1)
    eje.axvline(a, color="tab:gray", linestyle="--", linewidth=1, label="Intervalo")
    eje.axvline(b, color="tab:gray", linestyle="--", linewidth=1)

    if raiz is not None:
        try:
            valor_raiz = float(func(float(raiz)))
            if math.isfinite(valor_raiz):
                eje.scatter([raiz], [valor_raiz], color="tab:red", zorder=3, label="Raiz aproximada")
        except (ValueError, ZeroDivisionError, OverflowError):
            pass

    eje.set_title("Grafica de la funcion en el intervalo elegido")
    eje.set_xlabel("x")
    eje.set_ylabel("f(x)")
    eje.grid(True, linestyle=":", linewidth=0.7)
    eje.legend()

    nombre_funcion = limpiar_texto_para_archivo(expresion)
    valor_a = formatear_valor_para_archivo(a)
    valor_b = formatear_valor_para_archivo(b)
    nombre_archivo = f"grafica_{nombre_funcion}_a_{valor_a}_b_{valor_b}.png"
    carpeta_graficas = Path(__file__).resolve().parent.parent / "graficas"
    carpeta_graficas.mkdir(exist_ok=True)
    ruta_salida = carpeta_graficas / nombre_archivo
    figura.tight_layout()
    figura.savefig(ruta_salida, dpi=150)
    plt.close(figura)
    return ruta_salida


def construir_funcion_desde_expresion(expresion):
    x = symbols("x")
    transformaciones = standard_transformations + (
        implicit_multiplication_application,
        convert_xor,
    )

    expresion_simbolica = parse_expr(
        expresion,
        local_dict={"x": x, "pi": pi, "e": E},
        transformations=transformaciones,
    )

    if expresion_simbolica.free_symbols - {x}:
        raise ValueError("Solo se permite la variable x en la funcion.")

    funcion_usuario = lambdify(x, expresion_simbolica, modules=["math"])
    return expresion_simbolica, funcion_usuario


def resolver_funcion_usuario():
    expresion = input(
        "Escribe f(x) (ej: x**3 - x - 2, x^2 + 2x - 9, sin(x) - 0.5): "
    ).strip()

    try:
        _, funcion_usuario = construir_funcion_desde_expresion(expresion)
    except ValueError as error:
        print(error)
        return
    except Exception:
        print("Expresion invalida. Revisa parentesis, operadores y funciones matematicas.")
        return

    intervalos_sugeridos = sugerir_intervalos(funcion_usuario)
    if intervalos_sugeridos:
        print("\nIntervalos sugeridos para iniciar biseccion:")
        for indice, (inicio, fin) in enumerate(intervalos_sugeridos, start=1):
            if inicio == fin:
                print(f"{indice}. x = {inicio:.6f} parece ser una raiz exacta en la exploracion.")
            else:
                print(f"{indice}. [{inicio:.6f}, {fin:.6f}]")
    else:
        print("\nNo se encontraron intervalos sugeridos en la exploracion automatica [-10, 10].")

    try:
        a = float(input("Ingresa el limite inferior a: ").strip())
        b = float(input("Ingresa el limite superior b: ").strip())
        tolerancia_txt = input("Tolerancia (Enter para 1e-6): ").strip()
        max_iter_txt = input("Maximo de iteraciones (Enter para 100): ").strip()
    except ValueError:
        print("Entrada numerica invalida.")
        return

    tolerancia = float(tolerancia_txt) if tolerancia_txt else 1e-6
    max_iteraciones = int(max_iter_txt) if max_iter_txt else 100

    try:
        raiz, iteraciones = biseccion(
            funcion_usuario, a, b, tolerancia=tolerancia, max_iteraciones=max_iteraciones
        )
        print("\nResultado:")
        print(f"Raiz aproximada: {raiz:.6f}")
        print(f"Iteraciones: {iteraciones}")
        print(f"Comprobacion f(raiz): {funcion_usuario(raiz):.6e}")

        try:
            ruta_grafica = graficar_funcion(funcion_usuario, expresion, a, b, raiz=raiz)
            print(f"Grafica guardada en: {ruta_grafica}")

            try:
                abrir_grafica(ruta_grafica)
                print("Se intento abrir la grafica en el visor del sistema.")
            except Exception as error_apertura:
                print(f"No se pudo abrir la grafica en pantalla: {error_apertura}")
        except Exception as error_grafica:
            print(f"No se pudo generar la grafica: {error_grafica}")
    except Exception as error:
        print(f"Error: {error}")


def main():
    mostrar_titulo()

    while True:
        mostrar_menu()
        opcion = leer_opcion()

        if opcion == "1":
            try:
                resolver_ejemplo_fijo()
            except Exception as error:
                print(f"Error en metodo de biseccion: {error}")

        elif opcion == "2":
            resolver_funcion_usuario()
        elif opcion == "3":
            print("Cerrando programa. Hasta luego.")
            break
        else:
            print("Opcion invalida. Intenta nuevamente.")

if __name__ == "__main__":
    main()
