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


def resolver_funcion_usuario():
    import math
    import re

    def normalizar_expresion(expresion):
        expr = expresion.replace("^", "**").replace(" ", "")
        expr = re.sub(r"(\d)([a-zA-Z(])", r"\1*\2", expr)
        expr = re.sub(r"([x\)])(\d)", r"\1*\2", expr)
        expr = re.sub(r"([x\)])([a-zA-Z(])", r"\1*\2", expr)
        return expr

    expresion = input(
        "Escribe f(x) (ej: x**3 - x - 2, x^2 + 2x - 9, sin(x) - 0.5): "
    ).strip()
    expresion = normalizar_expresion(expresion)

    try:
        compile(expresion, "<string>", "eval")
    except SyntaxError:
        print("Expresion invalida. Revisa parentesis y multiplicaciones (usa 2*x o 2x).")
        return

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

    entorno = {
        "__builtins__": {},
        "math": math,
        "abs": abs,
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "exp": math.exp,
        "log": math.log,
        "sqrt": math.sqrt,
        "pi": math.pi,
        "e": math.e,
    }

    def funcion_usuario(x):
        return eval(expresion, entorno, {"x": x})

    try:
        raiz, iteraciones = biseccion(
            funcion_usuario, a, b, tolerancia=tolerancia, max_iteraciones=max_iteraciones
        )
        print("\nResultado:")
        print(f"Raiz aproximada: {raiz:.6f}")
        print(f"Iteraciones: {iteraciones}")
        print(f"Comprobacion f(raiz): {funcion_usuario(raiz):.6e}")
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
