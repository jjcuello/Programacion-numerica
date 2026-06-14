from metodos.biseccion import (
    abrir_grafica,
    construir_funcion_desde_expresion,
    funcion,
    graficar_funcion,
    mostrar_titulo,
    sugerir_intervalos,
)


def mostrar_menu():
    print("\nMenu principal:")
    print("1. Ejemplo de Metodo de la secante, x**3 - x - 2 = 0")
    print("2. Introduce tu propia funcion")
    print("3. Salir")


def leer_opcion():
    opcion = input("Elige una opcion (1-3): ").strip()
    return opcion


def secante(func, x0, x1, tolerancia=1e-6, max_iteraciones=100):
    print("Iter |        x(i-1) |          x(i) |      x(i+1) |     f(x(i+1))")
    print("-" * 72)

    for i in range(1, max_iteraciones + 1):
        fx0 = func(x0)
        fx1 = func(x1)
        denominador = fx1 - fx0

        if denominador == 0:
            raise ValueError(
                "La division entre f(x1) - f(x0) es cero. Elige otros valores iniciales."
            )

        x2 = x1 - fx1 * (x1 - x0) / denominador
        fx2 = func(x2)

        print(f"{i:4d} | {x0:12.6f} | {x1:12.6f} | {x2:12.6f} | {fx2:13.6f}")

        if abs(fx2) < tolerancia or abs(x2 - x1) < tolerancia:
            return x2, i

        x0 = x1
        x1 = x2

    return x2, max_iteraciones


def resolver_ejemplo_fijo():
    x0 = 1
    x1 = 2
    tolerancia = 1e-6

    raiz, iteraciones = secante(funcion, x0, x1, tolerancia)
    print("\nResultado:")
    print(f"Raiz aproximada: {raiz:.6f}")
    print(f"Iteraciones: {iteraciones}")
    print(f"Comprobacion f(raiz): {funcion(raiz):.6e}")

    try:
        ruta_grafica = graficar_funcion(funcion, "x**3 - x - 2", x0, x1, raiz=raiz)
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
        _, funcion_usuario = construir_funcion_desde_expresion(expresion)
    except ValueError as error:
        print(error)
        return
    except Exception:
        print("Expresion invalida. Revisa parentesis, operadores y funciones matematicas.")
        return

    intervalos_sugeridos = sugerir_intervalos(funcion_usuario)
    if intervalos_sugeridos:
        print("\nIntervalos sugeridos para orientar los valores iniciales de la secante:")
        for indice, (inicio, fin) in enumerate(intervalos_sugeridos, start=1):
            if inicio == fin:
                print(f"{indice}. x = {inicio:.6f} parece ser una raiz exacta en la exploracion.")
            else:
                print(f"{indice}. [{inicio:.6f}, {fin:.6f}]")
    else:
        print("\nNo se encontraron intervalos sugeridos en la exploracion automatica [-10, 10].")

    try:
        x0 = float(input("Ingresa el valor inicial x0: ").strip())
        x1 = float(input("Ingresa el valor inicial x1: ").strip())
        tolerancia_txt = input("Tolerancia (Enter para 1e-6): ").strip()
        max_iter_txt = input("Maximo de iteraciones (Enter para 100): ").strip()
    except ValueError:
        print("Entrada numerica invalida.")
        return

    tolerancia = float(tolerancia_txt) if tolerancia_txt else 1e-6
    max_iteraciones = int(max_iter_txt) if max_iter_txt else 100

    try:
        raiz, iteraciones = secante(
            funcion_usuario,
            x0,
            x1,
            tolerancia=tolerancia,
            max_iteraciones=max_iteraciones,
        )
        print("\nResultado:")
        print(f"Raiz aproximada: {raiz:.6f}")
        print(f"Iteraciones: {iteraciones}")
        print(f"Comprobacion f(raiz): {funcion_usuario(raiz):.6e}")

        try:
            limite_inferior = min(x0, x1, raiz)
            limite_superior = max(x0, x1, raiz)
            if limite_inferior == limite_superior:
                limite_inferior -= 1
                limite_superior += 1

            ruta_grafica = graficar_funcion(
                funcion_usuario,
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
                print(f"Error en metodo de la secante: {error}")

        elif opcion == "2":
            resolver_funcion_usuario()
        elif opcion == "3":
            print("Cerrando programa. Hasta luego.")
            break
        else:
            print("Opcion invalida. Intenta nuevamente.")


if __name__ == "__main__":
    main()