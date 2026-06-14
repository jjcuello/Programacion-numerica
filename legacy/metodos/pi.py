import math
import time
from decimal import Decimal, localcontext


PI_REFERENCIA = Decimal("3.14159265358979323846264338327950288419716939937510")


class AnalizadorPi:
    def __init__(self, tolerancia=1e-10, max_iteraciones=50000, decimales=12):
        self.tolerancia = tolerancia
        self.max_iteraciones = max_iteraciones
        self.decimales = decimales

    def _referencia_pi(self):
        return PI_REFERENCIA

    def _error_absoluto(self, aproximacion):
        referencia = self._referencia_pi()
        aproximacion_decimal = Decimal(str(aproximacion))
        return abs(aproximacion_decimal - referencia)

    def _aproximacion_leibniz_n(self, n):
        suma = 0.0
        for k in range(n):
            suma += ((-1.0) ** k) / (2 * k + 1)
        return Decimal(str(4.0 * suma))

    def metodo_leibniz(self):
        inicio = time.perf_counter()
        suma = 0.0
        aproximacion_anterior = None

        for k in range(self.max_iteraciones):
            termino = ((-1.0) ** k) / (2 * k + 1)
            suma += termino
            aproximacion = 4.0 * suma

            if aproximacion_anterior is not None:
                if abs(aproximacion - aproximacion_anterior) < self.tolerancia:
                    fin = time.perf_counter()
                    return {
                        "metodo": "Leibniz",
                        "aproximacion": Decimal(str(aproximacion)),
                        "iteraciones": k + 1,
                        "tiempo": fin - inicio,
                        "error": self._error_absoluto(aproximacion),
                    }

            aproximacion_anterior = aproximacion

        fin = time.perf_counter()
        return {
            "metodo": "Leibniz",
            "aproximacion": Decimal(str(aproximacion_anterior)),
            "iteraciones": self.max_iteraciones,
            "tiempo": fin - inicio,
            "error": self._error_absoluto(aproximacion_anterior),
        }

    def metodo_nilakantha(self):
        inicio = time.perf_counter()
        aproximacion = 3.0
        aproximacion_anterior = None
        signo = 1.0
        n = 2

        for i in range(self.max_iteraciones):
            termino = 4.0 / (n * (n + 1) * (n + 2))
            aproximacion += signo * termino

            if aproximacion_anterior is not None:
                if abs(aproximacion - aproximacion_anterior) < self.tolerancia:
                    fin = time.perf_counter()
                    return {
                        "metodo": "Nilakantha",
                        "aproximacion": Decimal(str(aproximacion)),
                        "iteraciones": i + 1,
                        "tiempo": fin - inicio,
                        "error": self._error_absoluto(aproximacion),
                    }

            aproximacion_anterior = aproximacion
            signo *= -1.0
            n += 2

        fin = time.perf_counter()
        return {
            "metodo": "Nilakantha",
            "aproximacion": Decimal(str(aproximacion_anterior)),
            "iteraciones": self.max_iteraciones,
            "tiempo": fin - inicio,
            "error": self._error_absoluto(aproximacion_anterior),
        }

    def metodo_archimedes(self):
        inicio = time.perf_counter()
        lados = 6
        aproximacion_anterior = None

        for i in range(self.max_iteraciones):
            aproximacion = lados * math.sin(math.pi / lados)

            if aproximacion_anterior is not None:
                if abs(aproximacion - aproximacion_anterior) < self.tolerancia:
                    fin = time.perf_counter()
                    return {
                        "metodo": "Arquimedes (inscrito)",
                        "aproximacion": Decimal(str(aproximacion)),
                        "iteraciones": i + 1,
                        "tiempo": fin - inicio,
                        "error": self._error_absoluto(aproximacion),
                        "lados": lados,
                    }

            aproximacion_anterior = aproximacion
            lados *= 2

        fin = time.perf_counter()
        return {
            "metodo": "Arquimedes (inscrito)",
            "aproximacion": Decimal(str(aproximacion_anterior)),
            "iteraciones": self.max_iteraciones,
            "tiempo": fin - inicio,
            "error": self._error_absoluto(aproximacion_anterior),
            "lados": lados // 2,
        }

    def metodo_ramanujan(self):
        inicio = time.perf_counter()
        precision_decimal = max(50, self.decimales + 25)
        tolerancia_decimal = Decimal(str(self.tolerancia))
        suma = Decimal(0)
        aproximacion_anterior = None

        with localcontext() as contexto:
            contexto.prec = precision_decimal

            for k in range(self.max_iteraciones):
                numerador = Decimal(math.factorial(4 * k)) * Decimal(1103 + 26390 * k)
                denominador = (
                    (Decimal(math.factorial(k)) ** 4)
                    * (Decimal(396) ** (4 * k))
                )
                suma += numerador / denominador

                inverso_pi = (Decimal(2) * Decimal(2).sqrt() / Decimal(9801)) * suma
                aproximacion = Decimal(1) / inverso_pi

                if aproximacion_anterior is not None:
                    if abs(aproximacion - aproximacion_anterior) < tolerancia_decimal:
                        fin = time.perf_counter()
                        return {
                            "metodo": "Ramanujan",
                            "aproximacion": +aproximacion,
                            "iteraciones": k + 1,
                            "tiempo": fin - inicio,
                            "error": self._error_absoluto(aproximacion),
                        }

                aproximacion_anterior = aproximacion

            fin = time.perf_counter()
            return {
                "metodo": "Ramanujan",
                "aproximacion": +aproximacion_anterior,
                "iteraciones": self.max_iteraciones,
                "tiempo": fin - inicio,
                "error": self._error_absoluto(aproximacion_anterior),
            }

    def metodo_chudnovsky(self):
        inicio = time.perf_counter()
        precision_decimal = max(60, self.decimales + 30)
        tolerancia_decimal = Decimal(str(self.tolerancia))
        suma = Decimal(0)
        aproximacion_anterior = None

        with localcontext() as contexto:
            contexto.prec = precision_decimal
            constante = Decimal(426880) * Decimal(10005).sqrt()

            for k in range(self.max_iteraciones):
                numerador = (
                    Decimal((-1) ** k)
                    * Decimal(math.factorial(6 * k))
                    * Decimal(13591409 + 545140134 * k)
                )
                denominador = (
                    Decimal(math.factorial(3 * k))
                    * (Decimal(math.factorial(k)) ** 3)
                    * (Decimal(640320) ** (3 * k))
                )
                suma += numerador / denominador
                aproximacion = constante / suma

                if aproximacion_anterior is not None:
                    if abs(aproximacion - aproximacion_anterior) < tolerancia_decimal:
                        fin = time.perf_counter()
                        return {
                            "metodo": "Chudnovsky",
                            "aproximacion": +aproximacion,
                            "iteraciones": k + 1,
                            "tiempo": fin - inicio,
                            "error": self._error_absoluto(aproximacion),
                        }

                aproximacion_anterior = aproximacion

            fin = time.perf_counter()
            return {
                "metodo": "Chudnovsky",
                "aproximacion": +aproximacion_anterior,
                "iteraciones": self.max_iteraciones,
                "tiempo": fin - inicio,
                "error": self._error_absoluto(aproximacion_anterior),
            }

    def resumen_leibniz_10000(self, decimales):
        n = 10000
        aproximacion = self._aproximacion_leibniz_n(n)
        referencia = self._referencia_pi()
        aproximacion_txt = formatear_decimal(aproximacion, decimales)
        referencia_txt = formatear_decimal(referencia, decimales)
        decimales_correctos = contar_decimales_correctos(aproximacion_txt, referencia_txt)
        error = abs(aproximacion - referencia)
        return {
            "iteraciones": n,
            "aproximacion": aproximacion,
            "error": error,
            "decimales_correctos": decimales_correctos,
        }

    def ejecutar_todos(self):
        return [
            self.metodo_leibniz(),
            self.metodo_nilakantha(),
            self.metodo_archimedes(),
            self.metodo_ramanujan(),
            self.metodo_chudnovsky(),
        ]


class DemostracionPi:
    def __init__(self, max_iteraciones=10000, decimales=15):
        self.max_iteraciones = max_iteraciones
        self.decimales = decimales
        self.referencia = math.pi

    def aproximacion(self, n):
        suma = 0.0
        for k in range(n):
            suma += ((-1.0) ** k) / (2 * k + 1)
        return 4.0 * suma

    def generar_iteraciones(self):
        suma = 0.0
        for n in range(1, self.max_iteraciones + 1):
            k = n - 1
            suma += ((-1.0) ** k) / (2 * k + 1)
            aproximacion_actual = 4.0 * suma
            error_actual = abs(aproximacion_actual - self.referencia)
            yield n, aproximacion_actual, error_actual

    def imprimir_formula_objetivo(self):
        valor_pi_20 = format(Decimal(str(math.pi)), ".20f")
        print("\nFormula objetivo fija:")
        print(f"pi = 4 * sum((-1)^k/(2k+1), k=0..inf) = {valor_pi_20}")

    def ejecutar(self, mostrar_cada=1, delay_ms=0):
        print("\nDemostracion incremental de pi")
        self.imprimir_formula_objetivo()
        print("\nn        | Aproximacion de pi    | Error absoluto")
        print("-" * 60)

        ultimo_n = 0
        ultima_aproximacion = 0.0
        ultimo_error = 0.0

        for n, aproximacion_actual, error_actual in self.generar_iteraciones():
            ultimo_n = n
            ultima_aproximacion = aproximacion_actual
            ultimo_error = error_actual

            if mostrar_cada == 1 or n % mostrar_cada == 0 or n == self.max_iteraciones:
                print(
                    f"{n:<8d} | {aproximacion_actual:<20.{self.decimales}f} | "
                    f"{error_actual:.3E}"
                )
                if delay_ms > 0:
                    time.sleep(delay_ms / 1000.0)

        print("\nResumen final:")
        print(f"Iteraciones ejecutadas: {ultimo_n}")
        print(f"Ultima aproximacion:    {ultima_aproximacion:.{self.decimales}f}")
        print(f"Error final:            {ultimo_error:.3E}")

    def ejecutar_en_vivo(self, mostrar_cada=1, delay_ms=80):
        print("\nDemostracion incremental de pi (vista en vivo)")
        self.imprimir_formula_objetivo()
        print("\nLa linea de resultado se actualiza sobre si misma:")

        ultimo_n = 0
        ultima_aproximacion = 0.0
        ultimo_error = 0.0

        for n, aproximacion_actual, error_actual in self.generar_iteraciones():
            ultimo_n = n
            ultima_aproximacion = aproximacion_actual
            ultimo_error = error_actual

            if mostrar_cada == 1 or n % mostrar_cada == 0 or n == self.max_iteraciones:
                linea = (
                    f"n={n:<8d} | pi ~= {aproximacion_actual:.{self.decimales}f} | "
                    f"error = {error_actual:.3E}"
                )
                print(f"\r{linea}", end="", flush=True)
                if delay_ms > 0:
                    time.sleep(delay_ms / 1000.0)

        print()
        print("\nResumen final:")
        print(f"Iteraciones ejecutadas: {ultimo_n}")
        print(f"Ultima aproximacion:    {ultima_aproximacion:.{self.decimales}f}")
        print(f"Error final:            {ultimo_error:.3E}")


def mostrar_titulo():
    print("==================================================================================")
    print(" Programacion Numerica - Analisis del Numero Pi - Jose Javier Cuello")
    print("==================================================================================")


def mostrar_menu():
    print("\nMenu principal:")
    print("1. Comparar metodos de calculo de pi")
    print("2. Ejecutar un metodo individual")
    print("3. Configurar parametros")
    print("4. Salir")


def leer_opcion():
    return input("Elige una opcion (1-4): ").strip()


def mostrar_formulas_pi():
    print("\nFormulas utilizadas en este modulo:")
    print("- Leibniz:    pi = 4 * sum((-1)^k/(2k+1), k=0..inf)")
    print("- Nilakantha: pi = 3 + 4/(2*3*4) - 4/(4*5*6) + 4/(6*7*8) - ...")
    print("- Arquimedes: pi ~= n * sin(pi/n)  (poligono inscrito)")
    print("- Ramanujan:  1/pi = (2*sqrt(2)/9801) * sum((4k)!*(1103+26390k)/(k!^4*396^(4k)))")
    print("- Chudnovsky: pi = 426880*sqrt(10005) / sum((-1)^k*(6k)!*(13591409+545140134k)/((3k)!*(k!)^3*640320^(3k)))")


def mostrar_formula_metodo(nombre):
    print("\nFormula del metodo seleccionado:")
    if nombre == "Leibniz":
        print("pi = 4 * sum((-1)^k/(2k+1), k=0..inf)")
    elif nombre == "Nilakantha":
        print("pi = 3 + 4/(2*3*4) - 4/(4*5*6) + 4/(6*7*8) - ...")
    elif nombre == "Arquimedes":
        print("pi ~= n * sin(pi/n), con n creciendo por duplicacion")
    elif nombre == "Ramanujan":
        print("1/pi = (2*sqrt(2)/9801) * sum((4k)!*(1103+26390k)/(k!^4*396^(4k)))")
    elif nombre == "Chudnovsky":
        print("pi = 426880*sqrt(10005) / sum((-1)^k*(6k)!*(13591409+545140134k)/((3k)!*(k!)^3*640320^(3k)))")


def formatear_decimal(valor, decimales):
    if isinstance(valor, Decimal):
        return format(valor, f".{decimales}f")
    visibles = min(decimales, 16)
    return f"{float(valor):.{visibles}f}"


def contar_decimales_correctos(aproximacion_txt, referencia_txt):
    aproximacion_decimales = aproximacion_txt.split(".")[-1]
    referencia_decimales = referencia_txt.split(".")[-1]

    contador = 0
    for digito_aprox, digito_ref in zip(aproximacion_decimales, referencia_decimales):
        if digito_aprox == digito_ref:
            contador += 1
        else:
            break
    return contador


def enriquecer_resultado(resultado, decimales, referencia_pi):
    aproximacion_txt = formatear_decimal(resultado["aproximacion"], decimales)
    referencia_txt = formatear_decimal(referencia_pi, decimales)

    resultado["decimales"] = decimales
    resultado["referencia_pi"] = referencia_pi
    resultado["decimales_correctos"] = contar_decimales_correctos(aproximacion_txt, referencia_txt)
    return resultado


def imprimir_resultado(resultado):
    referencia_txt = formatear_decimal(resultado["referencia_pi"], resultado["decimales"])
    aproximacion_txt = formatear_decimal(resultado["aproximacion"], resultado["decimales"])

    print("\nResultado:")
    print(f"Metodo: {resultado['metodo']}")
    print(f"Valor de referencia pi: {referencia_txt}")
    print(f"Aproximacion de pi:     {aproximacion_txt}")
    print(f"Decimales correctos:    {resultado['decimales_correctos']}")
    print(f"Iteraciones: {resultado['iteraciones']}")
    if "lados" in resultado:
        print(f"Lados del poligono: {resultado['lados']}")
    print(f"Error absoluto: {resultado['error']:.3E}")
    print(f"Tiempo: {resultado['tiempo']:.6f} s")


def imprimir_tabla(resultados):
    if not resultados:
        print("No hay resultados para mostrar.")
        return

    decimales = resultados[0]["decimales"]
    referencia_txt = formatear_decimal(resultados[0]["referencia_pi"], decimales)
    print(f"\nValor de referencia de pi ({decimales} decimales): {referencia_txt}")
    print("\nComparacion de metodos:")
    print("Metodo                   | Aproximacion         | Iteraciones | Error abs      | Dec. ok | Tiempo (s)")
    print("-" * 105)
    for item in resultados:
        aproximacion = formatear_decimal(item["aproximacion"], decimales)
        print(
            f"{item['metodo']:<24} | "
            f"{aproximacion:<19} | "
            f"{item['iteraciones']:<11d} | "
            f"{item['error']:<14.3E} | "
            f"{item['decimales_correctos']:<7d} | "
            f"{item['tiempo']:<.6f}"
        )


def solicitar_decimales(decimales_actuales):
    texto = input(
        f"Cantidad de decimales a calcular (1-50, Enter para {decimales_actuales}): "
    ).strip()

    if not texto:
        return decimales_actuales

    valor = int(texto)
    if valor < 1 or valor > 50:
        raise ValueError("Los decimales deben estar entre 1 y 50.")
    return valor


def ejecutar_metodo_individual(analizador, decimales):
    print("\nMetodos disponibles:")
    print("1. Leibniz")
    print("2. Nilakantha")
    print("3. Arquimedes (poligono inscrito)")
    print("4. Ramanujan")
    print("5. Chudnovsky")
    opcion = input("Elige una opcion (1-5): ").strip()

    referencia_pi = analizador._referencia_pi()

    if opcion == "1":
        mostrar_formula_metodo("Leibniz")
        resultado = enriquecer_resultado(analizador.metodo_leibniz(), decimales, referencia_pi)
        resumen = analizador.resumen_leibniz_10000(decimales)
        print("\nObservacion pedagogica (Leibniz):")
        decimales_fraccionarios = resumen["decimales_correctos"]
        cifras_totales = decimales_fraccionarios + 1
        print(
            f"Con {resumen['iteraciones']} iteraciones, Leibniz alcanza solo "
            f"{decimales_fraccionarios} decimales correctos despues del punto "
            f"({cifras_totales} cifras correctas contando la parte entera)."
        )
        print(f"Aproximacion: {formatear_decimal(resumen['aproximacion'], decimales)}")
        print(f"Error absoluto: {resumen['error']:.3E}")
    elif opcion == "2":
        mostrar_formula_metodo("Nilakantha")
        resultado = enriquecer_resultado(analizador.metodo_nilakantha(), decimales, referencia_pi)
    elif opcion == "3":
        mostrar_formula_metodo("Arquimedes")
        resultado = enriquecer_resultado(analizador.metodo_archimedes(), decimales, referencia_pi)
    elif opcion == "4":
        mostrar_formula_metodo("Ramanujan")
        resultado = enriquecer_resultado(analizador.metodo_ramanujan(), decimales, referencia_pi)
    elif opcion == "5":
        mostrar_formula_metodo("Chudnovsky")
        resultado = enriquecer_resultado(analizador.metodo_chudnovsky(), decimales, referencia_pi)
    else:
        print("Opcion invalida. Intenta nuevamente.")
        return

    imprimir_resultado(resultado)


def demostracion_pi():
    print("\nDemostracion Pi")
    print("Se calcula incrementalmente con la serie de Leibniz.")

    print("\nModo de ejecucion:")
    print("1. Demo (con delay para visualizar cambios)")
    print("2. Rapido (sin delay)")
    print("3. En vivo (resultado sobre el resultado)")
    modo = input("Elige una opcion (1-3, Enter para 1): ").strip()
    modo = modo if modo in {"1", "2", "3"} else "1"

    max_iter_txt = input("Maximo de iteraciones (Enter para 10000): ").strip()

    if modo == "1":
        mostrar_default = 1
    elif modo == "2":
        mostrar_default = 100
    else:
        mostrar_default = 1

    mostrar_cada_txt = input(
        f"Mostrar cada cuantas iteraciones (Enter para {mostrar_default}): "
    ).strip()

    if modo == "1":
        delay_default = 80
    elif modo == "2":
        delay_default = 0
    else:
        delay_default = 50

    delay_txt = input(
        f"Delay en milisegundos por fila mostrada (Enter para {delay_default}): "
    ).strip()

    max_iteraciones = int(max_iter_txt) if max_iter_txt else 10000
    mostrar_cada = int(mostrar_cada_txt) if mostrar_cada_txt else mostrar_default
    delay_ms = int(delay_txt) if delay_txt else delay_default

    if max_iteraciones < 1:
        raise ValueError("El maximo de iteraciones debe ser mayor o igual a 1.")
    if mostrar_cada < 1:
        raise ValueError("El valor de muestreo debe ser mayor o igual a 1.")
    if delay_ms < 0:
        raise ValueError("El delay no puede ser negativo.")

    demostrador = DemostracionPi(max_iteraciones=max_iteraciones, decimales=15)
    if modo == "3":
        demostrador.ejecutar_en_vivo(mostrar_cada=mostrar_cada, delay_ms=delay_ms)
    else:
        demostrador.ejecutar(mostrar_cada=mostrar_cada, delay_ms=delay_ms)


def main():
    mostrar_titulo()

    tolerancia = 1e-10
    max_iteraciones = 50000
    decimales = 12

    while True:
        mostrar_menu()
        opcion = leer_opcion()

        if opcion == "1":
            try:
                decimales = solicitar_decimales(decimales)
                analizador = AnalizadorPi(tolerancia, max_iteraciones, decimales)
                mostrar_formulas_pi()
                referencia_pi = analizador._referencia_pi()
                resultados = [
                    enriquecer_resultado(item, decimales, referencia_pi)
                    for item in analizador.ejecutar_todos()
                ]
                imprimir_tabla(resultados)
                resumen = analizador.resumen_leibniz_10000(decimales)
                print("\nObservacion pedagogica de Leibniz:")
                decimales_fraccionarios = resumen["decimales_correctos"]
                cifras_totales = decimales_fraccionarios + 1
                print(
                    f"Con {resumen['iteraciones']} iteraciones, Leibniz alcanza solo "
                    f"{decimales_fraccionarios} decimales correctos despues del punto "
                    f"({cifras_totales} cifras correctas contando la parte entera)."
                )
                print(f"Aproximacion: {formatear_decimal(resumen['aproximacion'], decimales)}")
                print(f"Error absoluto: {resumen['error']:.3E}")
            except Exception as error:
                print(f"Error en comparacion de metodos: {error}")

        elif opcion == "2":
            try:
                decimales = solicitar_decimales(decimales)
                analizador = AnalizadorPi(tolerancia, max_iteraciones, decimales)
                ejecutar_metodo_individual(analizador, decimales)
            except Exception as error:
                print(f"Error al ejecutar el metodo: {error}")

        elif opcion == "3":
            try:
                tolerancia_txt = input("Nueva tolerancia (Enter para mantener): ").strip()
                max_iter_txt = input("Maximo de iteraciones (Enter para mantener): ").strip()
                decimales = solicitar_decimales(decimales)

                if tolerancia_txt:
                    tolerancia = float(tolerancia_txt)
                if max_iter_txt:
                    max_iteraciones = int(max_iter_txt)

                print("\nParametros actualizados correctamente.")
                print(f"Tolerancia: {tolerancia}")
                print(f"Maximo iteraciones: {max_iteraciones}")
                print(f"Decimales solicitados: {decimales}")
            except Exception as error:
                print(f"No se pudieron actualizar los parametros: {error}")

        elif opcion == "4":
            print("Cerrando modulo de Pi. Hasta luego.")
            break
        else:
            print("Opcion invalida. Intenta nuevamente.")


if __name__ == "__main__":
    main()
