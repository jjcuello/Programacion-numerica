import numpy as np
from scipy.optimize import fsolve
from sympy import Eq, solve, symbols


def mostrar_titulo():
    print("==================================================================================")
    print(" Programacion Numerica - Sistemas No Lineales - Jose Javier Cuello")
    print("==================================================================================")


def mostrar_menu():
    print("\nMenu principal:")
    print("1. Sistema polinomial con solucion simbolica")
    print("2. Ecuacion trigonometrica con fsolve")
    print("3. Sistema mixto de 2 ecuaciones con fsolve")
    print("4. Sistema de 3 ecuaciones con fsolve")
    print("5. Tres numeros consecutivos con SymPy")
    print("6. Ecuacion seno + coseno con fsolve")
    print("7. Salir")


def leer_opcion():
    opcion = input("Elige una opcion (1-7): ").strip()
    return opcion


def resolver_opcion_1():
    x, y = symbols("x y")
    ecuacion1 = Eq(x**2 + y**2 - 1, 0)
    ecuacion2 = Eq(x**2 - y - 1, 0)
    soluciones = solve((ecuacion1, ecuacion2), (x, y))

    print("\nSoluciones del sistema polinomial:")
    print(soluciones)


def ecuacion_trig(x):
    return np.cos(x) - x


def resolver_opcion_2():
    valor_inicial_txt = input("Valor inicial estimado (Enter para 0.5): ").strip()
    valor_inicial = float(valor_inicial_txt) if valor_inicial_txt else 0.5
    solucion = fsolve(ecuacion_trig, valor_inicial)

    print("\nSolucion numerica de la ecuacion trigonometrica:")
    print(solucion)


def sistema_mixto(variables):
    x = variables[0]
    y = variables[1]
    eq1 = x + np.exp(y) - 7
    eq2 = x**2 - y - 1
    return [eq1, eq2]


def resolver_opcion_3():
    x0_txt = input("Valor inicial para x (Enter para 1.0): ").strip()
    y0_txt = input("Valor inicial para y (Enter para 1.0): ").strip()
    x0 = float(x0_txt) if x0_txt else 1.0
    y0 = float(y0_txt) if y0_txt else 1.0
    valores_iniciales = [x0, y0]
    soluciones = fsolve(sistema_mixto, valores_iniciales)

    print("\nSolucion numerica del sistema mixto [x, y]:")
    print(soluciones)


def sistema_3d(variables):
    x, y, z = variables
    eq1 = x**2 + y**2 + z**2 - 1
    eq2 = x + y + z - 0.5
    eq3 = x * y * z - 0.1
    return [eq1, eq2, eq3]


def resolver_opcion_4():
    x0_txt = input("Valor inicial para x (Enter para 0.5): ").strip()
    y0_txt = input("Valor inicial para y (Enter para 0.5): ").strip()
    z0_txt = input("Valor inicial para z (Enter para 0.5): ").strip()
    x0 = float(x0_txt) if x0_txt else 0.5
    y0 = float(y0_txt) if y0_txt else 0.5
    z0 = float(z0_txt) if z0_txt else 0.5
    valores_iniciales = [x0, y0, z0]
    soluciones = fsolve(sistema_3d, valores_iniciales)

    print("\nSoluciones para [x, y, z]:")
    print(soluciones)


def resolver_opcion_5():
    x = symbols("x")
    ecuacion = Eq(x + (x + 1) + (x + 2), 0)
    solucion = solve(ecuacion, x)
    primer_numero = solucion[0]

    print("\nLa ecuacion abstracta es:", ecuacion)
    print("El primer numero encontrado es:", primer_numero)
    print("Los tres numeros consecutivos son:")
    print(primer_numero, primer_numero + 1, primer_numero + 2)


def ecuacion_seno_coseno(x):
    return np.sin(x) + np.cos(x) - 1.2


def resolver_opcion_6():
    valor_inicial_txt = input("Valor inicial estimado (Enter para 0.5): ").strip()
    valor_inicial = float(valor_inicial_txt) if valor_inicial_txt else 0.5
    solucion = fsolve(ecuacion_seno_coseno, valor_inicial)

    print("\nLa solucion numerica para la ecuacion es:")
    print(solucion)


def main():
    mostrar_titulo()

    while True:
        mostrar_menu()
        opcion = leer_opcion()

        if opcion == "1":
            try:
                resolver_opcion_1()
            except Exception as error:
                print(f"Error en la opcion 1: {error}")
        elif opcion == "2":
            try:
                resolver_opcion_2()
            except Exception as error:
                print(f"Error en la opcion 2: {error}")
        elif opcion == "3":
            try:
                resolver_opcion_3()
            except Exception as error:
                print(f"Error en la opcion 3: {error}")
        elif opcion == "4":
            try:
                resolver_opcion_4()
            except Exception as error:
                print(f"Error en la opcion 4: {error}")
        elif opcion == "5":
            try:
                resolver_opcion_5()
            except Exception as error:
                print(f"Error en la opcion 5: {error}")
        elif opcion == "6":
            try:
                resolver_opcion_6()
            except Exception as error:
                print(f"Error en la opcion 6: {error}")
        elif opcion == "7":
            print("Cerrando programa. Hasta luego.")
            break
        else:
            print("Opcion invalida. Intenta nuevamente.")


if __name__ == "__main__":
    main()