from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

from metodos.biseccion import abrir_grafica


class AnimacionBase:
    def __init__(self, nombre, archivo_base, duracion_segundos=6, fps=20):
        self.nombre = nombre
        self.archivo_base = archivo_base
        self.duracion_segundos = duracion_segundos
        self.fps = fps

    @property
    def total_frames(self):
        return max(20, int(self.duracion_segundos * self.fps))

    def _ruta_salida(self, extension):
        carpeta_graficas = Path(__file__).resolve().parent.parent / "graficas"
        carpeta_graficas.mkdir(exist_ok=True)
        return carpeta_graficas / f"{self.archivo_base}.{extension}"

    def guardar_animacion(self, animacion, figura):
        ruta_gif = self._ruta_salida("gif")
        try:
            from matplotlib.animation import PillowWriter

            animacion.save(ruta_gif, writer=PillowWriter(fps=self.fps))
            plt.close(figura)
            return ruta_gif, "gif"
        except Exception:
            ruta_png = self._ruta_salida("png")
            figura.savefig(ruta_png, dpi=150)
            plt.close(figura)
            return ruta_png, "png"

    def generar(self):
        raise NotImplementedError


class AnimacionSenoDinamica(AnimacionBase):
    def __init__(self):
        super().__init__(
            nombre="Seno dinamica A-w-fase",
            archivo_base="animacion_seno_dinamica",
            duracion_segundos=7,
            fps=20,
        )

    def generar(self):
        figura, eje = plt.subplots(figsize=(9, 5))
        x = np.linspace(-2 * np.pi, 2 * np.pi, 800)

        linea, = eje.plot([], [], color="tab:blue", linewidth=2, label="y = A sin(wx + phi)")
        texto = eje.text(0.02, 0.93, "", transform=eje.transAxes)

        eje.set_xlim(float(x[0]), float(x[-1]))
        eje.set_ylim(-2.2, 2.2)
        eje.set_title("Funcion trigonometrica en movimiento")
        eje.set_xlabel("x")
        eje.set_ylabel("y")
        eje.grid(True, linestyle=":", linewidth=0.7)
        eje.legend(loc="upper right")

        def update(frame):
            t = frame / self.fps
            amplitud = 1.0 + 0.6 * np.sin(0.8 * t)
            frecuencia = 1.0 + 0.35 * np.cos(0.55 * t)
            fase = 1.1 * t
            y = amplitud * np.sin(frecuencia * x + fase)
            linea.set_data(x, y)
            texto.set_text(
                f"A={amplitud:.3f}   w={frecuencia:.3f}   phi={fase:.3f}"
            )
            return linea, texto

        animacion = FuncAnimation(
            figura,
            update,
            frames=self.total_frames,
            interval=1000 / self.fps,
            blit=True,
        )
        return figura, animacion


class AnimacionInterferencia(AnimacionBase):
    def __init__(self):
        super().__init__(
            nombre="Interferencia de ondas",
            archivo_base="animacion_interferencia_ondas",
            duracion_segundos=7,
            fps=20,
        )

    def generar(self):
        figura, eje = plt.subplots(figsize=(9, 5))
        x = np.linspace(-2 * np.pi, 2 * np.pi, 800)

        linea_1, = eje.plot([], [], color="tab:blue", linewidth=1.5, label="y1")
        linea_2, = eje.plot([], [], color="tab:orange", linewidth=1.5, label="y2")
        linea_suma, = eje.plot([], [], color="tab:red", linewidth=2.0, label="y = y1 + y2")
        texto = eje.text(0.02, 0.93, "", transform=eje.transAxes)

        eje.set_xlim(float(x[0]), float(x[-1]))
        eje.set_ylim(-3.2, 3.2)
        eje.set_title("Interferencia trigonometrica")
        eje.set_xlabel("x")
        eje.set_ylabel("y")
        eje.grid(True, linestyle=":", linewidth=0.7)
        eje.legend(loc="upper right")

        def update(frame):
            t = frame / self.fps
            y1 = 1.2 * np.sin(1.25 * x + 0.9 * t)
            y2 = 0.9 * np.sin(1.15 * x - 1.15 * t)
            y = y1 + y2

            linea_1.set_data(x, y1)
            linea_2.set_data(x, y2)
            linea_suma.set_data(x, y)
            texto.set_text(f"t={t:.2f} s")
            return linea_1, linea_2, linea_suma, texto

        animacion = FuncAnimation(
            figura,
            update,
            frames=self.total_frames,
            interval=1000 / self.fps,
            blit=True,
        )
        return figura, animacion


class AnimacionSuperficieTrigonometrica3D(AnimacionBase):
    def __init__(self):
        super().__init__(
            nombre="Superficie 3D trigonometrica",
            archivo_base="animacion_superficie_trig_3d",
            duracion_segundos=6,
            fps=16,
        )

    def generar(self):
        figura = plt.figure(figsize=(8, 6))
        eje = figura.add_subplot(111, projection="3d")

        x = np.linspace(-3.5, 3.5, 70)
        y = np.linspace(-3.5, 3.5, 70)
        xx, yy = np.meshgrid(x, y)

        def update(frame):
            t = 2.0 * np.pi * frame / self.total_frames
            zz = np.sin(xx + t) * np.cos(yy - 0.6 * t)
            eje.cla()
            eje.plot_surface(xx, yy, zz, cmap="viridis", linewidth=0, antialiased=True)
            eje.set_title("z = sin(x + t) cos(y - 0.6t)")
            eje.set_xlabel("X")
            eje.set_ylabel("Y")
            eje.set_zlabel("Z")
            eje.set_zlim(-1.2, 1.2)
            eje.view_init(elev=28, azim=45 + 20 * np.sin(t))
            return tuple()

        animacion = FuncAnimation(
            figura,
            update,
            frames=self.total_frames,
            interval=1000 / self.fps,
            blit=False,
        )
        return figura, animacion


def mostrar_titulo():
    print("==================================================================================")
    print(" Programacion Numerica - Animaciones Trigonometricas - Jose Javier Cuello")
    print("==================================================================================")


def mostrar_menu():
    print("\nMenu principal:")
    print("1. Seno dinamica (amplitud, frecuencia, fase)")
    print("2. Interferencia de ondas")
    print("3. Superficie trigonometrica 3D")
    print("4. Salir")


def leer_opcion():
    return input("Elige una opcion (1-4): ").strip()


def ejecutar_animacion(animador):
    print(f"\nGenerando: {animador.nombre}")
    figura, animacion = animador.generar()
    ruta, tipo_salida = animador.guardar_animacion(animacion, figura)

    if tipo_salida == "gif":
        print(f"Animacion guardada en: {ruta}")
    else:
        print(
            f"No fue posible exportar GIF en este entorno. Se guardo imagen de referencia en: {ruta}"
        )

    try:
        abrir_grafica(ruta)
        print("Se intento abrir el archivo en el visor del sistema.")
    except Exception as error_apertura:
        print(f"No se pudo abrir automaticamente: {error_apertura}")


def main():
    mostrar_titulo()

    while True:
        mostrar_menu()
        opcion = leer_opcion()

        if opcion == "1":
            try:
                ejecutar_animacion(AnimacionSenoDinamica())
            except Exception as error:
                print(f"Error en animacion seno dinamica: {error}")
        elif opcion == "2":
            try:
                ejecutar_animacion(AnimacionInterferencia())
            except Exception as error:
                print(f"Error en animacion de interferencia: {error}")
        elif opcion == "3":
            try:
                ejecutar_animacion(AnimacionSuperficieTrigonometrica3D())
            except Exception as error:
                print(f"Error en animacion 3D: {error}")
        elif opcion == "4":
            print("Cerrando programa. Hasta luego.")
            break
        else:
            print("Opcion invalida. Intenta nuevamente.")


if __name__ == "__main__":
    main()
