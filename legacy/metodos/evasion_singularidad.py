import math
from dataclasses import dataclass

from sympy import E, pi, symbols
from sympy.parsing.sympy_parser import (
    convert_xor,
    implicit_multiplication_application,
    parse_expr,
    standard_transformations,
)
from sympy.utilities.lambdify import lambdify


@dataclass
class ResultadoEvaluacion:
    x: float
    estado: str
    valor: float | None
    metodo: str
    error_estimado: float | None
    mensaje: str


class FuncionObjetivo:
    def __init__(self, expresion):
        self.expresion = expresion
        self._simbolica, self._funcion = self._construir_funcion(expresion)

    def _construir_funcion(self, expresion):
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

        funcion = lambdify(x, expresion_simbolica, modules=["math"])
        return expresion_simbolica, funcion

    def evaluar(self, x):
        return float(self._funcion(float(x)))


class DetectorSingularidades:
    def __init__(self, umbral_infinito=1e12):
        self.umbral_infinito = umbral_infinito

    def evaluar_directo(self, funcion, x):
        try:
            valor = funcion.evaluar(x)
        except ZeroDivisionError:
            return False, None, "division_por_cero"
        except ValueError:
            return False, None, "dominio_invalido"
        except OverflowError:
            return False, None, "overflow"
        except Exception as error:
            return False, None, f"error: {error}"

        if not math.isfinite(valor):
            return False, None, "no_finito"

        if abs(valor) > self.umbral_infinito:
            return False, None, "magnitud_excesiva"

        return True, valor, "ok"

    def clasificar_por_laterales(self, valor_izq, valor_der, error_lateral, tolerancia):
        if valor_izq is None and valor_der is None:
            return "no_evaluable", "No hay evaluaciones laterales validas."

        if valor_izq is not None and valor_der is not None:
            if error_lateral is not None and error_lateral <= tolerancia:
                return "singularidad_removible", "Los limites laterales son consistentes."

            if abs(valor_izq) > self.umbral_infinito or abs(valor_der) > self.umbral_infinito:
                return "singularidad_polo", "Se detecta crecimiento sin cota en al menos un lateral."

            if valor_izq * valor_der < 0 and (
                abs(valor_izq) > self.umbral_infinito * 0.01
                or abs(valor_der) > self.umbral_infinito * 0.01
            ):
                return "singularidad_polo", "Los laterales divergen con signos opuestos."

            return "indeterminada", "Los limites laterales no coinciden con la tolerancia indicada."

        valor_existente = valor_izq if valor_izq is not None else valor_der
        if abs(valor_existente) > self.umbral_infinito * 0.1:
            return "singularidad_polo", "El unico lateral estable sugiere crecimiento abrupto."

        return "indeterminada", "Solo un lateral pudo evaluarse de forma estable."


class EstrategiaLimiteLateral:
    def __init__(self, delta_inicial=1e-2, factor_reduccion=0.5, max_intentos=20):
        self.delta_inicial = delta_inicial
        self.factor_reduccion = factor_reduccion
        self.max_intentos = max_intentos

    def aplicar(self, funcion, detector, x, tolerancia):
        delta = self.delta_inicial
        mejor = None

        for _ in range(self.max_intentos):
            x_izq = x - delta
            x_der = x + delta

            ok_izq, valor_izq, _ = detector.evaluar_directo(funcion, x_izq)
            ok_der, valor_der, _ = detector.evaluar_directo(funcion, x_der)

            valor_izq = valor_izq if ok_izq else None
            valor_der = valor_der if ok_der else None

            if valor_izq is not None and valor_der is not None:
                limite = (valor_izq + valor_der) / 2.0
                error_lateral = abs(valor_izq - valor_der) / 2.0
                mejor = {
                    "limite": limite,
                    "error_lateral": error_lateral,
                    "delta": delta,
                    "valor_izq": valor_izq,
                    "valor_der": valor_der,
                }

                if error_lateral <= tolerancia:
                    return True, mejor

            elif mejor is None and (valor_izq is not None or valor_der is not None):
                mejor = {
                    "limite": valor_izq if valor_izq is not None else valor_der,
                    "error_lateral": None,
                    "delta": delta,
                    "valor_izq": valor_izq,
                    "valor_der": valor_der,
                }

            delta *= self.factor_reduccion

        return mejor is not None, mejor


class EvaluadorSeguro:
    def __init__(self, tolerancia=1e-6, detector=None, estrategia=None):
        self.tolerancia = tolerancia
        self.detector = detector if detector is not None else DetectorSingularidades()
        self.estrategia = estrategia if estrategia is not None else EstrategiaLimiteLateral()

    def evaluar_en_punto(self, funcion, x):
        ok, valor, motivo = self.detector.evaluar_directo(funcion, x)
        if ok:
            return ResultadoEvaluacion(
                x=x,
                estado="ok",
                valor=valor,
                metodo="evaluacion_directa",
                error_estimado=0.0,
                mensaje="Evaluacion directa estable.",
            )

        exito, datos = self.estrategia.aplicar(funcion, self.detector, x, self.tolerancia)
        if not exito or not datos:
            return ResultadoEvaluacion(
                x=x,
                estado="no_evaluable",
                valor=None,
                metodo="limite_lateral",
                error_estimado=None,
                mensaje=f"No fue posible evadir la singularidad ({motivo}).",
            )

        clasificacion, mensaje_clasificacion = self.detector.clasificar_por_laterales(
            datos.get("valor_izq"),
            datos.get("valor_der"),
            datos.get("error_lateral"),
            self.tolerancia,
        )

        if clasificacion == "singularidad_removible":
            return ResultadoEvaluacion(
                x=x,
                estado="limite_usado",
                valor=datos["limite"],
                metodo="limite_lateral",
                error_estimado=datos.get("error_lateral"),
                mensaje=(
                    "Se uso aproximacion por limite lateral con "
                    f"delta={datos.get('delta'):.3E}."
                ),
            )

        if clasificacion == "singularidad_polo":
            return ResultadoEvaluacion(
                x=x,
                estado="singularidad_polo",
                valor=None,
                metodo="limite_lateral",
                error_estimado=datos.get("error_lateral"),
                mensaje=mensaje_clasificacion,
            )

        return ResultadoEvaluacion(
            x=x,
            estado="indeterminada",
            valor=datos.get("limite"),
            metodo="limite_lateral",
            error_estimado=datos.get("error_lateral"),
            mensaje=mensaje_clasificacion,
        )


def mostrar_titulo():
    print("==================================================================================")
    print(" Programacion Numerica - Evaluacion segura con evasion de singularidad - Jose Javier Cuello")
    print("==================================================================================")


def mostrar_menu():
    print("\nMenu principal:")
    print("1. Evaluar un punto")
    print("2. Evaluar varios puntos")
    print("3. Configurar parametros")
    print("4. Salir")


def leer_opcion():
    return input("Elige una opcion (1-4): ").strip()


def mostrar_resultado(resultado):
    print("\nResultado:")
    print(f"x evaluado: {resultado.x}")
    print(f"Estado: {resultado.estado}")
    print(f"Metodo: {resultado.metodo}")

    if resultado.valor is not None:
        print(f"Valor estimado: {resultado.valor:.12g}")
    else:
        print("Valor estimado: no disponible")

    if resultado.error_estimado is not None:
        print(f"Error estimado: {resultado.error_estimado:.3E}")
    else:
        print("Error estimado: no disponible")

    print(f"Detalle: {resultado.mensaje}")


def leer_puntos():
    texto = input("Ingresa los puntos separados por coma (ej: 0, 1, 2.5): ").strip()
    if not texto:
        raise ValueError("No se ingresaron puntos.")

    partes = [parte.strip() for parte in texto.split(",") if parte.strip()]
    if not partes:
        raise ValueError("No se encontraron puntos validos.")

    return [float(parte) for parte in partes]


def main():
    mostrar_titulo()

    expresion = input(
        "Escribe f(x) (ej: (x**2 - 1)/(x - 1), sin(x)/x, tan(x)): "
    ).strip()
    if not expresion:
        print("No se ingreso ninguna funcion. Cerrando modulo.")
        return

    try:
        funcion = FuncionObjetivo(expresion)
    except Exception as error:
        print(f"No se pudo construir la funcion: {error}")
        return

    tolerancia = 1e-6
    delta_inicial = 1e-2
    factor_reduccion = 0.5
    max_intentos = 20

    while True:
        mostrar_menu()
        opcion = leer_opcion()

        if opcion == "1":
            try:
                x = float(input("Ingresa el punto x a evaluar: ").strip())
                evaluador = EvaluadorSeguro(
                    tolerancia=tolerancia,
                    detector=DetectorSingularidades(),
                    estrategia=EstrategiaLimiteLateral(
                        delta_inicial=delta_inicial,
                        factor_reduccion=factor_reduccion,
                        max_intentos=max_intentos,
                    ),
                )
                resultado = evaluador.evaluar_en_punto(funcion, x)
                mostrar_resultado(resultado)
            except Exception as error:
                print(f"No se pudo evaluar el punto: {error}")

        elif opcion == "2":
            try:
                puntos = leer_puntos()
                evaluador = EvaluadorSeguro(
                    tolerancia=tolerancia,
                    detector=DetectorSingularidades(),
                    estrategia=EstrategiaLimiteLateral(
                        delta_inicial=delta_inicial,
                        factor_reduccion=factor_reduccion,
                        max_intentos=max_intentos,
                    ),
                )
                for x in puntos:
                    resultado = evaluador.evaluar_en_punto(funcion, x)
                    mostrar_resultado(resultado)
            except Exception as error:
                print(f"No se pudieron evaluar los puntos: {error}")

        elif opcion == "3":
            try:
                tolerancia_txt = input(
                    f"Nueva tolerancia (Enter para {tolerancia}): "
                ).strip()
                delta_txt = input(
                    f"Nuevo delta inicial (Enter para {delta_inicial}): "
                ).strip()
                factor_txt = input(
                    f"Factor de reduccion (Enter para {factor_reduccion}): "
                ).strip()
                intentos_txt = input(
                    f"Maximo de intentos (Enter para {max_intentos}): "
                ).strip()

                if tolerancia_txt:
                    tolerancia = float(tolerancia_txt)
                if delta_txt:
                    delta_inicial = float(delta_txt)
                if factor_txt:
                    factor_reduccion = float(factor_txt)
                if intentos_txt:
                    max_intentos = int(intentos_txt)

                if tolerancia <= 0:
                    raise ValueError("La tolerancia debe ser mayor que cero.")
                if delta_inicial <= 0:
                    raise ValueError("El delta inicial debe ser mayor que cero.")
                if not (0 < factor_reduccion < 1):
                    raise ValueError("El factor de reduccion debe estar entre 0 y 1.")
                if max_intentos < 1:
                    raise ValueError("El maximo de intentos debe ser al menos 1.")

                print("\nParametros actualizados correctamente.")
                print(f"Tolerancia: {tolerancia}")
                print(f"Delta inicial: {delta_inicial}")
                print(f"Factor de reduccion: {factor_reduccion}")
                print(f"Maximo de intentos: {max_intentos}")
            except Exception as error:
                print(f"No se pudieron actualizar los parametros: {error}")

        elif opcion == "4":
            print("Cerrando modulo de evasion de singularidad. Hasta luego.")
            break
        else:
            print("Opcion invalida. Intenta nuevamente.")


if __name__ == "__main__":
    main()
