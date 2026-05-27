from metodos import biseccion, euler, evasion_singularidad, graficas_3d, secante

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
    print("10. Salir")

def leer_opcion():
    opcion = input("Elige una opcion (1-10): ").strip()
    return opcion

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
            print("Proximamente: Newton / Raphson")
        elif opcion == "4":
            print("Proximamente: Punto Fijo")
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
                euler.main()
            except Exception as e:
                print(f"Error en modulo Euler: {e}")
        elif opcion == "9":
            try:
                evasion_singularidad.main()
            except Exception as e:
                print(f"Error en modulo de evasion de singularidad: {e}")
        elif opcion == "10":
            print("Cerrando programa. Hasta luego.")
            break
        else:
            print("Opcion invalida. Intenta nuevamente.")

if __name__ == "__main__":
    main()