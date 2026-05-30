import math

from sympy import E, lambdify, pi, symbols
from sympy.parsing.sympy_parser import (
    convert_xor,
    implicit_multiplication_application,
    parse_expr,
    standard_transformations,
)

from metodos.biseccion import abrir_grafica, graficar_funcion, sugerir_intervalos


class FuncionPuntoFijo:
    def __init__(self, expresion):
        self.expresion = expresion
        self._x = symbols("x")
        self._simbolica = self._construir_expresion(expresion)
        self._funcion = lambdify(self._x, self._simbolica, modules=["math"])

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


class PuntoFijo:
    def __init__(self, funcion_g, tolerancia=1e-6, max_iteraciones=100):
        self.funcion_g = funcion_g
        self.tolerancia = tolerancia
        self.max_iteraciones = max_iteraciones

    def resolver(self, x0):
        print("Iter |         x(i) |      g(x(i)) |   |x(i+1)-x(i)|")
        print("-" * 62)

        x_actual = float(x0)

        for i in range(1, self.max_iteraciones + 1):
            x_siguiente = self.funcion_g.evaluar(x_actual)

            if not math.isfinite(x_siguiente):
                raise ValueError("Se obtuvo un valor no finito durante la iteracion.")

            diferencia = abs(x_siguiente - x_actual)
            print(f"{i:4d} | {x_actual:12.6f} | {x_siguiente:12.6f} | {diferencia:14.6e}")

            if diferencia < self.tolerancia:
                return x_siguiente, i

            x_actual = x_siguiente

        return x_actual, self.max_iteraciones


def mostrar_titulo():
    print("==================================================================================")
    print(" Programacion Numerica - Metodo Punto Fijo - Jose Javier Cuello")
    print("==================================================================================")


def mostrar_menu():
    print("\nMenu principal:")
    print("1. Ejemplo Punto Fijo, x^3 - x - 2 = 0")
    print("2. Introduce tu propia funcion g(x)")
    print("3. Salir")


def leer_opcion():
    return input("Elige una opcion (1-3): ").strip()


def resolver_ejemplo_fijo():
    expresion_f = "x**3 - x - 2"
    expresion_g = "(x + 2)**(1/3)"

    funcion_f = FuncionPuntoFijo(expresion_f)
    funcion_g = FuncionPuntoFijo(expresion_g)
    metodo = PuntoFijo(funcion_g, tolerancia=1e-6, max_iteraciones=100)

    x0 = 1.5
    raiz, iteraciones = metodo.resolver(x0)

    print("\nResultado:")
    print(f"Raiz aproximada: {raiz:.6f}")
    print(f"Iteraciones: {iteraciones}")
    print(f"Comprobacion f(raiz): {funcion_f.evaluar(raiz):.6e}")

    try:
        ruta_grafica = graficar_funcion(funcion_f.evaluar, expresion_f, 1.0, 2.0, raiz=raiz)
        print(f"Grafica guardada en: {ruta_grafica}")

        try:
            abrir_grafica(ruta_grafica)
            print("Se intento abrir la grafica en el visor del sistema.")
        except Exception as error_apertura:
            print(f"No se pudo abrir la grafica en pantalla: {error_apertura}")
    except Exception as error_grafica:
        print(f"No se pudo generar la grafica: {error_grafica}")


def resolver_funcion_usuario():
    expresion_g = input(
        "Escribe g(x) para iterar x(i+1)=g(x(i)) (ej: cos(x), (x+2)**(1/3)): "
    ).strip()

    expresion_f = input(
        "Escribe f(x) opcional para verificar la raiz (Enter para usar x-g(x)): "
    ).strip()

    try:
        funcion_g = FuncionPuntoFijo(expresion_g)
    except ValueError as error:
        print(error)
        return
    except Exception:
        print("Expresion invalida para g(x). Revisa parentesis, operadores y funciones.")
        return

    if expresion_f:
        try:
            funcion_f = FuncionPuntoFijo(expresion_f)
            funcion_residual = funcion_f.evaluar
            expresion_residual = expresion_f
        except ValueError as error:
            print(error)
            return
        except Exception:
            print("Expresion invalida para f(x). Revisa parentesis, operadores y funciones.")
            return
    else:
        funcion_residual = lambda x: x - funcion_g.evaluar(x)
        expresion_residual = "x - g(x)"

    intervalos_sugeridos = sugerir_intervalos(funcion_residual)
    if intervalos_sugeridos:
        print("\nIntervalos sugeridos para orientar x0:")
        for indice, (inicio, fin) in enumerate(intervalos_sugeridos, start=1):
            if inicio == fin:
                print(f"{indice}. x = {inicio:.6f} parece raiz aproximada en la exploracion.")
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
        metodo = PuntoFijo(
            funcion_g,
            tolerancia=tolerancia,
            max_iteraciones=max_iteraciones,
        )
        raiz, iteraciones = metodo.resolver(x0)

        print("\nResultado:")
        print(f"Raiz aproximada: {raiz:.6f}")
        print(f"Iteraciones: {iteraciones}")
        print(f"Comprobacion residual: {funcion_residual(raiz):.6e}")

        try:
            limite_inferior = min(x0, raiz)
            limite_superior = max(x0, raiz)
            ancho = limite_superior - limite_inferior
            if ancho < 1:
                limite_inferior -= 1
                limite_superior += 1

            ruta_grafica = graficar_funcion(
                funcion_residual,
                expresion_residual,
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
                print(f"Error en metodo de Punto Fijo: {error}")
        elif opcion == "2":
            resolver_funcion_usuario()
        elif opcion == "3":
            print("Cerrando programa. Hasta luego.")
            break
        else:
            print("Opcion invalida. Intenta nuevamente.")


if __name__ == "__main__":
    main()
