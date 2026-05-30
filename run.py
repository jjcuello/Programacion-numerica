from metodos import (
    animaciones_trigonometricas,
    biseccion,
    euler,
    evasion_singularidad,
    graficas_3d,
    newton_raphson,
    pi as modulo_pi,
    punto_fijo,
    secante,
)

def mostrar_titulo():
    print("==================================================================================")
    print(" Programacion Numerica - Resolucion de Ecuaciones No lineales - Jose Javier Cuello")
    print("==================================================================================")

def mostrar_menu():
    print("\nMenu principal:")
    print("1. Metodo de biseccion")
    print("2. Metodo de interpolacion lineal secante")
    print("3. Metodo Newton / Raphson")
    print("4. Metodo Punto Fijo")
    print("5. Metodo Blasr-Tron")
    print("6. Division Sintetica")
    print("7. Graficas 3D con POO")
    print("8. Analisis del numero de Euler (e)")
    print("9. Evaluacion con evasion de singularidad")
    print("10. Analisis del numero Pi")
    print("11. Animaciones trigonometricas")
    print("12. Salir")

def leer_opcion():
    opcion = input("Elige una opcion (1-12): ").strip()
    return opcion


def mostrar_menu_euler():
    print("\nSubmenu de Euler:")
    print("1. Metodos de generacion de e")
    print("2. Demostracion Euler")
    print("3. Volver")


def ejecutar_submenu_euler():
    while True:
        mostrar_menu_euler()
        opcion = input("Elige una opcion (1-3): ").strip()

        if opcion == "1":
            euler.main()
        elif opcion == "2":
            euler.demostracion_euler()
        elif opcion == "3":
            break
        else:
            print("Opcion invalida. Intenta nuevamente.")


def mostrar_menu_pi():
    print("\nSubmenu de Pi:")
    print("1. Metodos de calculo de pi")
    print("2. Demostracion Pi")
    print("3. Volver")


def ejecutar_submenu_pi():
    while True:
        mostrar_menu_pi()
        opcion = input("Elige una opcion (1-3): ").strip()

        if opcion == "1":
            modulo_pi.main()
        elif opcion == "2":
            modulo_pi.demostracion_pi()
        elif opcion == "3":
            break
        else:
            print("Opcion invalida. Intenta nuevamente.")

def main():
    mostrar_titulo()

    while True:
        mostrar_menu()
        opcion = leer_opcion()

        if opcion == "1":
            try:
                biseccion.main()
            except Exception as e:
                print(f"Error en metodo de biseccion: {e}")

        elif opcion == "2":
            try:
                secante.main()
            except Exception as e:
                print(f"Error en metodo de la secante: {e}")
        elif opcion == "3":
            try:
                newton_raphson.main()
            except Exception as e:
                print(f"Error en metodo de Newton / Raphson: {e}")
        elif opcion == "4":
            try:
                punto_fijo.main()
            except Exception as e:
                print(f"Error en metodo de Punto Fijo: {e}")
        elif opcion == "5":
            print("Proximamente: Blasr-Tron")
        elif opcion == "6":
            print("Proximamente: Division Sintetica")
        elif opcion == "7":
            try:
                graficas_3d.main()
            except Exception as e:
                print(f"Error en graficas 3D: {e}")
        elif opcion == "8":
            try:
                ejecutar_submenu_euler()
            except Exception as e:
                print(f"Error en modulo Euler: {e}")
        elif opcion == "9":
            try:
                evasion_singularidad.main()
            except Exception as e:
                print(f"Error en modulo de evasion de singularidad: {e}")
        elif opcion == "10":
            try:
                ejecutar_submenu_pi()
            except Exception as e:
                print(f"Error en modulo Pi: {e}")
        elif opcion == "11":
            try:
                animaciones_trigonometricas.main()
            except Exception as e:
                print(f"Error en modulo de animaciones trigonometricas: {e}")
        elif opcion == "12":
            print("Cerrando programa. Hasta luego.")
            break
        else:
            print("Opcion invalida. Intenta nuevamente.")

if __name__ == "__main__":
    main()