import os
from abc import ABC, abstractmethod
from pathlib import Path
from textwrap import dedent

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

try:
    from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
except Exception:
    Axes3D = None


def mostrar_titulo():
    print("==================================================================================")
    print(" Programacion Numerica - Graficas 3D - Jose Javier Cuello")
    print("==================================================================================")


def mostrar_conceptos_poo():
    print(
        dedent(
            """
            Conceptos de Programacion Orientada a Objetos:
            - Encapsulamiento: cada figura guarda sus datos internos en atributos privados.
            - Herencia: las figuras concretas heredan de una clase base llamada Figura3D.
            - Polimorfismo: el programa llama al mismo metodo 'mostrar' para figuras distintas.
            """.strip()
        )
    )


def mostrar_menu():
    print("\nMenu principal:")
    print("1. Recta en 3D")
    print("2. Esfera")
    print("3. Cilindro")
    print("4. Cono")
    print("5. Paraboloide Eliptico")
    print("6. Ver conceptos POO")
    print("7. Salir")


def leer_opcion():
    return input("Elige una opcion (1-7): ").strip()


def leer_float(mensaje, valor_por_defecto):
    texto = input(mensaje).strip()
    return float(texto) if texto else valor_por_defecto


def abrir_grafica(ruta_grafica):
    if hasattr(os, "startfile"):
        os.startfile(ruta_grafica)
        return

    import shutil
    import subprocess

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


class Figura3D(ABC):
    def __init__(self, nombre, archivo_base, color="tab:blue"):
        self._nombre = nombre
        self._archivo_base = archivo_base
        self._color = color

    @property
    def nombre(self):
        return self._nombre

    def mostrar(self):
        figura = plt.figure(figsize=(8, 6))
        eje = figura.add_subplot(111, projection="3d")
        self.dibujar(eje)
        configurar_ejes(eje, self._nombre)
        figura.tight_layout()

        carpeta_graficas = Path(__file__).resolve().parent.parent / "graficas"
        carpeta_graficas.mkdir(exist_ok=True)
        ruta_salida = carpeta_graficas / f"{self._archivo_base}.png"
        figura.savefig(ruta_salida, dpi=150)
        plt.close(figura)
        return ruta_salida

    @abstractmethod
    def dibujar(self, eje):
        raise NotImplementedError


class Recta3D(Figura3D):
    def __init__(self, punto_inicial, punto_final, color="tab:blue"):
        super().__init__("Recta en 3D", "recta_3d", color)
        self._punto_inicial = punto_inicial
        self._punto_final = punto_final

    def dibujar(self, eje):
        x = np.linspace(self._punto_inicial[0], self._punto_final[0], 100)
        y = np.linspace(self._punto_inicial[1], self._punto_final[1], 100)
        z = np.linspace(self._punto_inicial[2], self._punto_final[2], 100)
        eje.plot(x, y, z, color=self._color, linewidth=2)
        eje.scatter(*self._punto_inicial, color="tab:red", s=40, label="Inicio")
        eje.scatter(*self._punto_final, color="tab:green", s=40, label="Fin")
        eje.legend()


class Esfera(Figura3D):
    def __init__(self, radio, centro=(0.0, 0.0, 0.0), color="tab:orange"):
        super().__init__("Esfera", "esfera_3d", color)
        self._radio = radio
        self._centro = centro

    def dibujar(self, eje):
        u = np.linspace(0, 2 * np.pi, 60)
        v = np.linspace(0, np.pi, 40)
        x = self._centro[0] + self._radio * np.outer(np.cos(u), np.sin(v))
        y = self._centro[1] + self._radio * np.outer(np.sin(u), np.sin(v))
        z = self._centro[2] + self._radio * np.outer(np.ones_like(u), np.cos(v))
        eje.plot_surface(x, y, z, color=self._color, alpha=0.7, linewidth=0)


class Cilindro(Figura3D):
    def __init__(self, radio, altura, centro=(0.0, 0.0, 0.0), color="tab:green"):
        super().__init__("Cilindro", "cilindro_3d", color)
        self._radio = radio
        self._altura = altura
        self._centro = centro

    def dibujar(self, eje):
        theta = np.linspace(0, 2 * np.pi, 60)
        z = np.linspace(self._centro[2], self._centro[2] + self._altura, 40)
        theta, z = np.meshgrid(theta, z)
        x = self._centro[0] + self._radio * np.cos(theta)
        y = self._centro[1] + self._radio * np.sin(theta)
        eje.plot_surface(x, y, z, color=self._color, alpha=0.75, linewidth=0)


class Cono(Figura3D):
    def __init__(self, radio_base, altura, centro=(0.0, 0.0, 0.0), color="tab:purple"):
        super().__init__("Cono", "cono_3d", color)
        self._radio_base = radio_base
        self._altura = altura
        self._centro = centro

    def dibujar(self, eje):
        theta = np.linspace(0, 2 * np.pi, 60)
        z = np.linspace(self._centro[2], self._centro[2] + self._altura, 40)
        theta, z = np.meshgrid(theta, z)
        factor = 1 - (z - self._centro[2]) / self._altura
        x = self._centro[0] + self._radio_base * factor * np.cos(theta)
        y = self._centro[1] + self._radio_base * factor * np.sin(theta)
        eje.plot_surface(x, y, z, color=self._color, alpha=0.75, linewidth=0)


class ParaboloideEliptico(Figura3D):
    def __init__(self, a, b, escala_z=1.0, color="tab:cyan"):
        super().__init__("Paraboloide Eliptico", "paraboloide_eliptico_3d", color)
        self._a = a
        self._b = b
        self._escala_z = escala_z

    def dibujar(self, eje):
        x = np.linspace(-self._a, self._a, 60)
        y = np.linspace(-self._b, self._b, 60)
        x, y = np.meshgrid(x, y)
        z = self._escala_z * ((x**2) / (self._a**2) + (y**2) / (self._b**2))
        eje.plot_surface(x, y, z, color=self._color, alpha=0.75, linewidth=0)


def mostrar_figura(figura):
    ruta_grafica = figura.mostrar()
    print(f"Grafica guardada en: {ruta_grafica}")

    try:
        abrir_grafica(ruta_grafica)
        print("Se intento abrir la grafica en el visor del sistema.")
    except Exception as error:
        print(f"No se pudo abrir la grafica automaticamente: {error}")


def configurar_ejes(eje, titulo):
    eje.set_title(titulo)
    eje.set_xlabel("X")
    eje.set_ylabel("Y")
    eje.set_zlabel("Z")
    eje.grid(True, linestyle=":", linewidth=0.7)


def resolver_recta_3d():
    print("\nRecta en 3D: se dibuja a partir de dos puntos.")
    x1 = leer_float("Ingresa x1 (Enter para 0): ", 0.0)
    y1 = leer_float("Ingresa y1 (Enter para 0): ", 0.0)
    z1 = leer_float("Ingresa z1 (Enter para 0): ", 0.0)
    x2 = leer_float("Ingresa x2 (Enter para 1): ", 1.0)
    y2 = leer_float("Ingresa y2 (Enter para 1): ", 1.0)
    z2 = leer_float("Ingresa z2 (Enter para 1): ", 1.0)
    figura = Recta3D((x1, y1, z1), (x2, y2, z2))
    mostrar_figura(figura)


def resolver_esfera():
    print("\nEsfera: se dibuja con centro y radio.")
    radio = leer_float("Radio (Enter para 1): ", 1.0)
    cx = leer_float("Centro x (Enter para 0): ", 0.0)
    cy = leer_float("Centro y (Enter para 0): ", 0.0)
    cz = leer_float("Centro z (Enter para 0): ", 0.0)
    figura = Esfera(radio, (cx, cy, cz))
    mostrar_figura(figura)


def resolver_cilindro():
    print("\nCilindro: se dibuja con radio y altura.")
    radio = leer_float("Radio (Enter para 1): ", 1.0)
    altura = leer_float("Altura (Enter para 2): ", 2.0)
    cx = leer_float("Centro x (Enter para 0): ", 0.0)
    cy = leer_float("Centro y (Enter para 0): ", 0.0)
    cz = leer_float("Centro z inferior (Enter para 0): ", 0.0)
    figura = Cilindro(radio, altura, (cx, cy, cz))
    mostrar_figura(figura)


def resolver_cono():
    print("\nCono: se dibuja con radio de base y altura.")
    radio_base = leer_float("Radio de base (Enter para 1): ", 1.0)
    altura = leer_float("Altura (Enter para 2): ", 2.0)
    cx = leer_float("Centro x (Enter para 0): ", 0.0)
    cy = leer_float("Centro y (Enter para 0): ", 0.0)
    cz = leer_float("Centro z base (Enter para 0): ", 0.0)
    figura = Cono(radio_base, altura, (cx, cy, cz))
    mostrar_figura(figura)


def resolver_paraboloide_eliptico():
    print("\nParaboloide eliptico: se dibuja con dos escalas horizontales y una vertical.")
    a = leer_float("Escala en x (Enter para 2): ", 2.0)
    b = leer_float("Escala en y (Enter para 2): ", 2.0)
    escala_z = leer_float("Escala vertical (Enter para 1): ", 1.0)
    figura = ParaboloideEliptico(a, b, escala_z)
    mostrar_figura(figura)


def main():
    mostrar_titulo()
    mostrar_conceptos_poo()

    while True:
        mostrar_menu()
        opcion = leer_opcion()

        if opcion == "1":
            try:
                resolver_recta_3d()
            except Exception as error:
                print(f"Error en la recta en 3D: {error}")
        elif opcion == "2":
            try:
                resolver_esfera()
            except Exception as error:
                print(f"Error en la esfera: {error}")
        elif opcion == "3":
            try:
                resolver_cilindro()
            except Exception as error:
                print(f"Error en el cilindro: {error}")
        elif opcion == "4":
            try:
                resolver_cono()
            except Exception as error:
                print(f"Error en el cono: {error}")
        elif opcion == "5":
            try:
                resolver_paraboloide_eliptico()
            except Exception as error:
                print(f"Error en el paraboloide eliptico: {error}")
        elif opcion == "6":
            mostrar_conceptos_poo()
        elif opcion == "7":
            print("Cerrando programa. Hasta luego.")
            break
        else:
            print("Opcion invalida. Intenta nuevamente.")


if __name__ == "__main__":
    main()