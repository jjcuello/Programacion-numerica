import math

from sympy import E, lambdify, pi, symbols
from sympy.parsing.sympy_parser import (
    convert_xor,
    implicit_multiplication_application,
    parse_expr,
    standard_transformations,
)

from metodos.biseccion import abrir_grafica, graficar_funcion, sugerir_intervalos


class FuncionDerivable:
    def __init__(self, expresion):
        self.expresion = expresion
        self._x = symbols("x")
        self._simbolica = self._construir_expresion(expresion)
        self._funcion = lambdify(self._x, self._simbolica, modules=["math"])
        self._derivada_simbolica = self._simbolica.diff(self._x)
        self._derivada = lambdify(self._x, self._derivada_simbolica, modules=["math"])

    def _construir_expresion(self, expresion):
        transformaciones = standard_transformations + (
            implicit_multiplication_application,
            convert_xor,
        )

        expresion_simbolica = parse_expr(
            expresion,
            local_dict={"x": self._x, "pi": pi, "e": E},
            transformations=transformaciones,
        )

        if expresion_simbolica.free_symbols - {self._x}:
            raise ValueError("Solo se permite la variable x en la funcion.")

        return expresion_simbolica

    def evaluar(self, x):
        return float(self._funcion(float(x)))

    def evaluar_derivada(self, x):
        return float(self._derivada(float(x)))


class NewtonRaphson:
    def __init__(self, funcion, tolerancia=1e-6, max_iteraciones=100):
        self.funcion = funcion
        self.tolerancia = tolerancia
        self.max_iteraciones = max_iteraciones

    def resolver(self, x0):
        print("Iter |         x(i) |       f(x) |      f'(x) |      x(i+1)")
        print("-" * 68)

        x_actual = float(x0)

        for i in range(1, self.max_iteraciones + 1):
            fx = self.funcion.evaluar(x_actual)
            dfx = self.funcion.evaluar_derivada(x_actual)

            if not math.isfinite(fx) or not math.isfinite(dfx):
                raise ValueError("Se obtuvieron valores no finitos durante la iteracion.")

            if dfx == 0:
                raise ValueError(
                    "La derivada es cero en el punto actual; Newton-Raphson no puede continuar."
                )

            x_siguiente = x_actual - (fx / dfx)
            print(f"{i:4d} | {x_actual:12.6f} | {fx:10.6f} | {dfx:10.6f} | {x_siguiente:12.6f}")

            if abs(fx) < self.tolerancia or abs(x_siguiente - x_actual) < self.tolerancia:
                return x_siguiente, i

            x_actual = x_siguiente

        return x_actual, self.max_iteraciones


def mostrar_titulo():
    print("==================================================================================")
    print(" Programacion Numerica - Metodo Newton / Raphson - Jose Javier Cuello")
    print("==================================================================================")


def mostrar_menu():
    print("\nMenu principal:")
    print("1. Ejemplo Newton-Raphson, x**3 - x - 2 = 0")
    print("2. Introduce tu propia funcion")
    print("3. Salir")


def leer_opcion():
    return input("Elige una opcion (1-3): ").strip()


def resolver_ejemplo_fijo():
    funcion = FuncionDerivable("x**3 - x - 2")
    metodo = NewtonRaphson(funcion, tolerancia=1e-6, max_iteraciones=100)

    x0 = 1.5
    raiz, iteraciones = metodo.resolver(x0)

    print("\nResultado:")
    print(f"Raiz aproximada: {raiz:.6f}")
    print(f"Iteraciones: {iteraciones}")
    print(f"Comprobacion f(raiz): {funcion.evaluar(raiz):.6e}")

    try:
        ruta_grafica = graficar_funcion(funcion.evaluar, "x**3 - x - 2", 1.0, 2.0, raiz=raiz)
        print(f"Grafica guardada en: {ruta_grafica}")

        try:
            abrir_grafica(ruta_grafica)
            print("Se intento abrir la grafica en el visor del sistema.")
        except Exception as error_apertura:
            print(f"No se pudo abrir la grafica en pantalla: {error_apertura}")
    except Exception as error_grafica:
        print(f"No se pudo generar la grafica: {error_grafica}")


def resolver_funcion_usuario():
    expresion = input(
        "Escribe f(x) (ej: x**3 - x - 2, x^2 + 2x - 9, sin(x) - 0.5): "
    ).strip()

    try:
        funcion = FuncionDerivable(expresion)
    except ValueError as error:
        print(error)
        return
    except Exception:
        print("Expresion invalida. Revisa parentesis, operadores y funciones matematicas.")
        return

    intervalos_sugeridos = sugerir_intervalos(funcion.evaluar)
    if intervalos_sugeridos:
        print("\nIntervalos sugeridos para orientar el valor inicial x0:")
        for indice, (inicio, fin) in enumerate(intervalos_sugeridos, start=1):
            if inicio == fin:
                print(f"{indice}. x = {inicio:.6f} parece ser una raiz exacta en la exploracion.")
            else:
                print(f"{indice}. [{inicio:.6f}, {fin:.6f}]  -> punto medio {(inicio + fin) / 2:.6f}")
    else:
        print("\nNo se encontraron intervalos sugeridos en la exploracion automatica [-10, 10].")

    try:
        x0 = float(input("Ingresa el valor inicial x0: ").strip())
        tolerancia_txt = input("Tolerancia (Enter para 1e-6): ").strip()
        max_iter_txt = input("Maximo de iteraciones (Enter para 100): ").strip()
    except ValueError:
        print("Entrada numerica invalida.")
        return

    tolerancia = float(tolerancia_txt) if tolerancia_txt else 1e-6
    max_iteraciones = int(max_iter_txt) if max_iter_txt else 100

    try:
        metodo = NewtonRaphson(
            funcion,
            tolerancia=tolerancia,
            max_iteraciones=max_iteraciones,
        )
        raiz, iteraciones = metodo.resolver(x0)

        print("\nResultado:")
        print(f"Raiz aproximada: {raiz:.6f}")
        print(f"Iteraciones: {iteraciones}")
        print(f"Comprobacion f(raiz): {funcion.evaluar(raiz):.6e}")

        try:
            limite_inferior = min(x0, raiz)
            limite_superior = max(x0, raiz)
            ancho = limite_superior - limite_inferior
            if ancho < 1:
                limite_inferior -= 1
                limite_superior += 1

            ruta_grafica = graficar_funcion(
                funcion.evaluar,
                expresion,
                limite_inferior,
                limite_superior,
                raiz=raiz,
            )
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
                print(f"Error en metodo de Newton / Raphson: {error}")
        elif opcion == "2":
            resolver_funcion_usuario()
        elif opcion == "3":
            print("Cerrando programa. Hasta luego.")
            break
        else:
            print("Opcion invalida. Intenta nuevamente.")


if __name__ == "__main__":
    main()
