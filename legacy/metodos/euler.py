import math
import time
from decimal import Decimal, localcontext

import numpy as np


class AnalizadorEuler:
    def __init__(
        self,
        tolerancia=1e-10,
        max_iteraciones=50000,
        precision="float64",
        decimales=15,
    ):
        self.tolerancia = tolerancia
        self.max_iteraciones = max_iteraciones
        self.precision = precision
        self.decimales = decimales

    def _usar_decimal(self):
        return self.precision == "decimal"

    def _cast(self, valor):
        if self._usar_decimal():
            return Decimal(str(valor))
        if self.precision == "float32":
            return np.float32(valor)
        return float(valor)

    def _referencia_euler(self):
        if self._usar_decimal():
            with localcontext() as contexto:
                contexto.prec = max(50, self.decimales + 20)
                return Decimal(1).exp()
        return Decimal(str(math.e))

    def _error_absoluto(self, aproximacion):
        referencia = self._referencia_euler()
        aproximacion_decimal = Decimal(str(aproximacion))
        return abs(aproximacion_decimal - referencia)

    def _tolerancia_efectiva(self):
        if self._usar_decimal():
            tolerancia_por_decimales = Decimal(10) ** Decimal(-(self.decimales + 2))
            tolerancia_usuario = Decimal(str(self.tolerancia))
            return min(tolerancia_usuario, tolerancia_por_decimales)

        tolerancia_por_decimales = 10 ** (-(min(self.decimales, 16) + 2))
        return min(float(self.tolerancia), tolerancia_por_decimales)

    def metodo_taylor(self):
        inicio = time.perf_counter()
        tolerancia_efectiva = self._tolerancia_efectiva()

        if self._usar_decimal():
            with localcontext() as contexto:
                contexto.prec = max(50, self.decimales + 20)
                suma = Decimal(1)
                termino = Decimal(1)

                for k in range(1, self.max_iteraciones + 1):
                    termino = termino / Decimal(k)
                    suma_nueva = suma + termino

                    if abs(suma_nueva - suma) < tolerancia_efectiva:
                        fin = time.perf_counter()
                        return {
                            "metodo": "Taylor",
                            "aproximacion": suma_nueva,
                            "iteraciones": k,
                            "tiempo": fin - inicio,
                            "error": self._error_absoluto(suma_nueva),
                        }

                    suma = suma_nueva

                fin = time.perf_counter()
                return {
                    "metodo": "Taylor",
                    "aproximacion": suma,
                    "iteraciones": self.max_iteraciones,
                    "tiempo": fin - inicio,
                    "error": self._error_absoluto(suma),
                }

        suma = self._cast(1.0)
        termino = self._cast(1.0)
        for k in range(1, self.max_iteraciones + 1):
            termino = self._cast(termino / self._cast(k))
            suma_nueva = self._cast(suma + termino)

            if abs(float(suma_nueva) - float(suma)) < tolerancia_efectiva:
                fin = time.perf_counter()
                return {
                    "metodo": "Taylor",
                    "aproximacion": Decimal(str(float(suma_nueva))),
                    "iteraciones": k,
                    "tiempo": fin - inicio,
                    "error": self._error_absoluto(suma_nueva),
                }

            suma = suma_nueva

        fin = time.perf_counter()
        return {
            "metodo": "Taylor",
            "aproximacion": Decimal(str(float(suma))),
            "iteraciones": self.max_iteraciones,
            "tiempo": fin - inicio,
            "error": self._error_absoluto(suma),
        }

    def metodo_limite(self):
        inicio = time.perf_counter()
        tolerancia_efectiva = self._tolerancia_efectiva()

        if self._usar_decimal():
            with localcontext() as contexto:
                contexto.prec = max(50, self.decimales + 20)
                aproximacion_anterior = Decimal(0)

                for n in range(1, self.max_iteraciones + 1):
                    base = Decimal(1) + (Decimal(1) / Decimal(n))
                    aproximacion = base**n

                    if n > 1 and abs(aproximacion - aproximacion_anterior) < tolerancia_efectiva:
                        fin = time.perf_counter()
                        return {
                            "metodo": "Limite (1+1/n)^n",
                            "aproximacion": aproximacion,
                            "iteraciones": n,
                            "tiempo": fin - inicio,
                            "error": self._error_absoluto(aproximacion),
                        }

                    aproximacion_anterior = aproximacion

                fin = time.perf_counter()
                return {
                    "metodo": "Limite (1+1/n)^n",
                    "aproximacion": aproximacion_anterior,
                    "iteraciones": self.max_iteraciones,
                    "tiempo": fin - inicio,
                    "error": self._error_absoluto(aproximacion_anterior),
                }

        aproximacion_anterior = self._cast(0.0)

        for n in range(1, self.max_iteraciones + 1):
            base = self._cast(1.0 + 1.0 / n)
            aproximacion = self._cast(base**n)

            if n > 1 and abs(float(aproximacion) - float(aproximacion_anterior)) < tolerancia_efectiva:
                fin = time.perf_counter()
                return {
                    "metodo": "Limite (1+1/n)^n",
                    "aproximacion": Decimal(str(float(aproximacion))),
                    "iteraciones": n,
                    "tiempo": fin - inicio,
                    "error": self._error_absoluto(aproximacion),
                }

            aproximacion_anterior = aproximacion

        fin = time.perf_counter()
        return {
            "metodo": "Limite (1+1/n)^n",
            "aproximacion": Decimal(str(float(aproximacion_anterior))),
            "iteraciones": self.max_iteraciones,
            "tiempo": fin - inicio,
            "error": self._error_absoluto(aproximacion_anterior),
        }

    def _coeficiente_fraccion_continua(self, indice):
        if indice == 0:
            return 2
        if indice % 3 == 2:
            return 2 * ((indice + 1) // 3)
        return 1

    def _aproximacion_fraccion_continua(self, profundidad):
        if self._usar_decimal():
            with localcontext() as contexto:
                contexto.prec = max(50, self.decimales + 20)
                valor = Decimal(self._coeficiente_fraccion_continua(profundidad))
                for i in range(profundidad - 1, -1, -1):
                    coeficiente = Decimal(self._coeficiente_fraccion_continua(i))
                    valor = coeficiente + (Decimal(1) / valor)
                return valor

        valor = self._cast(self._coeficiente_fraccion_continua(profundidad))
        for i in range(profundidad - 1, -1, -1):
            coeficiente = self._cast(self._coeficiente_fraccion_continua(i))
            valor = self._cast(coeficiente + self._cast(1.0) / valor)
        return Decimal(str(float(valor)))

    def metodo_fraccion_continua(self):
        inicio = time.perf_counter()
        tolerancia_efectiva = self._tolerancia_efectiva()
        aproximacion_anterior = self._aproximacion_fraccion_continua(0)

        for profundidad in range(1, self.max_iteraciones + 1):
            aproximacion = self._aproximacion_fraccion_continua(profundidad)

            diferencia = abs(aproximacion - aproximacion_anterior)
            if diferencia < tolerancia_efectiva:
                fin = time.perf_counter()
                return {
                    "metodo": "Fraccion continua",
                    "aproximacion": aproximacion,
                    "iteraciones": profundidad,
                    "tiempo": fin - inicio,
                    "error": self._error_absoluto(aproximacion),
                }

            aproximacion_anterior = aproximacion

        fin = time.perf_counter()
        return {
            "metodo": "Fraccion continua",
            "aproximacion": aproximacion_anterior,
            "iteraciones": self.max_iteraciones,
            "tiempo": fin - inicio,
            "error": self._error_absoluto(aproximacion_anterior),
        }

    def metodo_newton(self):
        inicio = time.perf_counter()
        tolerancia_efectiva = self._tolerancia_efectiva()

        if self._usar_decimal():
            with localcontext() as contexto:
                contexto.prec = max(50, self.decimales + 20)
                x = Decimal("2.5")

                for i in range(1, self.max_iteraciones + 1):
                    fx = x.ln() - Decimal(1)
                    dfx = Decimal(1) / x
                    x_nuevo = x - (fx / dfx)

                    if abs(x_nuevo - x) < tolerancia_efectiva:
                        fin = time.perf_counter()
                        return {
                            "metodo": "Newton sobre ln(x)-1",
                            "aproximacion": x_nuevo,
                            "iteraciones": i,
                            "tiempo": fin - inicio,
                            "error": self._error_absoluto(x_nuevo),
                        }

                    x = x_nuevo

                fin = time.perf_counter()
                return {
                    "metodo": "Newton sobre ln(x)-1",
                    "aproximacion": x,
                    "iteraciones": self.max_iteraciones,
                    "tiempo": fin - inicio,
                    "error": self._error_absoluto(x),
                }

        x = self._cast(2.5)

        for i in range(1, self.max_iteraciones + 1):
            fx = self._cast(math.log(float(x)) - 1.0)
            dfx = self._cast(1.0 / float(x))
            x_nuevo = self._cast(float(x) - float(fx) / float(dfx))

            if abs(float(x_nuevo) - float(x)) < tolerancia_efectiva:
                fin = time.perf_counter()
                return {
                    "metodo": "Newton sobre ln(x)-1",
                    "aproximacion": Decimal(str(float(x_nuevo))),
                    "iteraciones": i,
                    "tiempo": fin - inicio,
                    "error": self._error_absoluto(x_nuevo),
                }

            x = x_nuevo

        fin = time.perf_counter()
        return {
            "metodo": "Newton sobre ln(x)-1",
            "aproximacion": Decimal(str(float(x))),
            "iteraciones": self.max_iteraciones,
            "tiempo": fin - inicio,
            "error": self._error_absoluto(x),
        }

    def ejecutar_todos(self):
        return [
            self.metodo_taylor(),
            self.metodo_limite(),
            self.metodo_fraccion_continua(),
            self.metodo_newton(),
        ]


def mostrar_titulo():
    print("==================================================================================")
    print(" Programacion Numerica - Analisis del Numero de Euler (e) - Jose Javier Cuello")
    print("==================================================================================")


def mostrar_menu():
    print("\nMenu principal:")
    print("1. Comparar los 4 metodos de generacion de e")
    print("2. Ejecutar un metodo individual")
    print("3. Configurar parametros")
    print("4. Salir")


def leer_opcion():
    opcion = input("Elige una opcion (1-4): ").strip()
    return opcion


def formatear_decimal(valor, decimales, precision):
    if precision == "decimal":
        with localcontext() as contexto:
            contexto.prec = max(50, decimales + 20)
            return format(valor, f".{decimales}f")

    visibles = min(decimales, 16)
    return f"{float(valor):.{visibles}f}"


def vista_corta_decimal(valor, decimales, precision, prefijo=18, sufijo=18):
    texto = formatear_decimal(valor, decimales, precision)
    if "." not in texto:
        return texto

    parte_entera, parte_decimal = texto.split(".", maxsplit=1)
    if len(parte_decimal) <= prefijo + sufijo + 3:
        return texto

    return f"{parte_entera}.{parte_decimal[:prefijo]}...{parte_decimal[-sufijo:]}"


def formatear_por_bloques(texto_decimal, tam_bloque=10, bloques_por_linea=5):
    if "." not in texto_decimal:
        return texto_decimal

    parte_entera, parte_decimal = texto_decimal.split(".", maxsplit=1)
    bloques = [
        parte_decimal[i : i + tam_bloque]
        for i in range(0, len(parte_decimal), tam_bloque)
    ]

    lineas = []
    for i in range(0, len(bloques), bloques_por_linea):
        grupo = " ".join(bloques[i : i + bloques_por_linea])
        if i == 0:
            lineas.append(f" {parte_entera}.{grupo}")
        else:
            lineas.append(f"   {grupo}")

    return "\n".join(lineas)


def imprimir_resultado(resultado):
    referencia_txt_completa = formatear_decimal(
        resultado["referencia_euler"], resultado["decimales"], resultado["precision"]
    )
    aproximacion_txt_completa = formatear_decimal(
        resultado["aproximacion"], resultado["decimales"], resultado["precision"]
    )
    referencia_txt = vista_corta_decimal(
        resultado["referencia_euler"], resultado["decimales"], resultado["precision"]
    )
    aproximacion_txt = vista_corta_decimal(
        resultado["aproximacion"], resultado["decimales"], resultado["precision"]
    )

    print("\nResultado:")
    print(f"Metodo: {resultado['metodo']}")
    print(f"Valor de referencia e: {referencia_txt}")
    print(f"Aproximacion de e:     {aproximacion_txt}")
    if resultado["decimales"] > 40:
        print("\nReferencia completa (bloques):")
        print(formatear_por_bloques(referencia_txt_completa))
        print("\nAproximacion completa (bloques):")
        print(formatear_por_bloques(aproximacion_txt_completa))
    print(f"Decimales solicitados: {resultado['decimales']}")
    print(f"Decimales correctos:   {resultado['decimales_correctos']}")
    print(f"Iteraciones: {resultado['iteraciones']}")
    print(f"Error absoluto: {resultado['error']:.3E}")
    print(f"Tiempo: {resultado['tiempo']:.6f} s")


def imprimir_tabla(resultados):
    if not resultados:
        print("No hay resultados para mostrar.")
        return

    decimales = resultados[0]["decimales"]
    precision = resultados[0]["precision"]
    referencia_txt_completa = formatear_decimal(
        resultados[0]["referencia_euler"], decimales, precision
    )
    referencia_txt = vista_corta_decimal(
        resultados[0]["referencia_euler"], decimales, precision
    )
    print(f"\nValor de referencia de e ({decimales} decimales, vista corta): {referencia_txt}")
    if decimales > 16:
        print("\n\nValor de referencia de e completo (50 decimales por linea):")
        print(formatear_por_bloques(referencia_txt_completa))
    print("\nComparacion de metodos:")
    print("Metodo                      | Aproximacion (vista corta) | Iteraciones | Error abs      | Dec. ok | Tiempo (s)")
    print("-" * 117)
    for item in resultados:
        aproximacion = vista_corta_decimal(item["aproximacion"], decimales, precision)
        print(
            f"{item['metodo']:<27} | "
            f"{aproximacion:<24} | "
            f"{item['iteraciones']:<11d} | "
            f"{item['error']:<14.3E} | "
            f"{item['decimales_correctos']:<7d} | "
            f"{item['tiempo']:<.6f}"
        )


def enriquecer_resultado(resultado, decimales, precision, referencia_euler):
    aproximacion_txt = formatear_decimal(resultado["aproximacion"], decimales, precision)
    referencia_txt = formatear_decimal(referencia_euler, decimales, precision)

    resultado["decimales"] = decimales
    resultado["precision"] = precision
    resultado["referencia_euler"] = referencia_euler
    resultado["decimales_correctos"] = contar_decimales_correctos(aproximacion_txt, referencia_txt)
    resultado["coincide_objetivo"] = aproximacion_txt == referencia_txt
    return resultado


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


def seleccionar_precision():
    print("\nTipo numerico disponible:")
    print("1. float64 (double precision)")
    print("2. float32")
    print("3. Decimal (alta precision)")
    opcion = input("Elige una opcion (1-3, Enter para 1): ").strip()
    if opcion == "2":
        return "float32"
    if opcion == "3":
        return "decimal"
    return "float64"


def solicitar_decimales(decimales_actuales):
    texto = input(
        f"Cantidad de decimales a calcular (1-200, Enter para {decimales_actuales}): "
    ).strip()

    if not texto:
        return decimales_actuales

    valor = int(texto)
    if valor < 1 or valor > 200:
        raise ValueError("Los decimales deben estar entre 1 y 200.")
    return valor


def ajustar_precision_para_decimales(precision, decimales):
    if decimales > 16 and precision in {"float64", "float32"}:
        print("Para mas de 16 decimales se cambia automaticamente a precision Decimal.")
        return "decimal"
    return precision


def ejecutar_metodo_individual(analizador, decimales):
    print("\nMetodos disponibles:")
    print("1. Serie de Taylor")
    print("2. Limite (1 + 1/n)^n")
    print("3. Fraccion continua")
    print("4. Newton (ln(x) - 1 = 0)")
    opcion = input("Elige una opcion (1-4): ").strip()

    referencia_euler = analizador._referencia_euler()

    if opcion == "1":
        resultado = enriquecer_resultado(
            analizador.metodo_taylor(), decimales, analizador.precision, referencia_euler
        )
    elif opcion == "2":
        resultado = enriquecer_resultado(
            analizador.metodo_limite(), decimales, analizador.precision, referencia_euler
        )
    elif opcion == "3":
        resultado = enriquecer_resultado(
            analizador.metodo_fraccion_continua(), decimales, analizador.precision, referencia_euler
        )
    elif opcion == "4":
        resultado = enriquecer_resultado(
            analizador.metodo_newton(), decimales, analizador.precision, referencia_euler
        )
    else:
        print("Opcion invalida. Intenta nuevamente.")
        return

    imprimir_resultado(resultado)


class DemostracionEuler:
    def __init__(self, max_iteraciones=10000, decimales=15):
        self.max_iteraciones = max_iteraciones
        self.decimales = decimales
        self.referencia = math.e

    def aproximacion(self, n):
        return (1.0 + 1.0 / n) ** n

    def generar_iteraciones(self):
        for n in range(1, self.max_iteraciones + 1):
            aproximacion_actual = self.aproximacion(n)
            error_actual = abs(aproximacion_actual - self.referencia)
            yield n, aproximacion_actual, error_actual

    def imprimir_formula_objetivo(self):
        with localcontext() as contexto:
            contexto.prec = 40
            valor_e_20 = format(Decimal(1).exp(), ".20f")
        print("\nFormula objetivo fija:")
        print(f"lim_{{x->inf}} (1 + 1/x)^x = e = {valor_e_20}")

    def ejecutar(self, mostrar_cada=1, delay_ms=0):
        print("\nDemostracion incremental de e")
        self.imprimir_formula_objetivo()
        print("\nn        | (1 + 1/n)^n        | Error absoluto")
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
        print("\nDemostracion incremental de e (vista en vivo)")
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
                    f"n={n:<8d} | (1 + 1/n)^n = {aproximacion_actual:.{self.decimales}f} | "
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


def demostracion_euler():
    print("\nDemostracion Euler")
    print("Se calcula incrementalmente (1 + 1/n)^n desde n=1 hasta n grande.")

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

    demostrador = DemostracionEuler(max_iteraciones=max_iteraciones, decimales=15)
    if modo == "3":
        demostrador.ejecutar_en_vivo(mostrar_cada=mostrar_cada, delay_ms=delay_ms)
    else:
        demostrador.ejecutar(mostrar_cada=mostrar_cada, delay_ms=delay_ms)


def main():
    mostrar_titulo()

    tolerancia = 1e-10
    max_iteraciones = 50000
    precision = "float64"
    decimales = 12

    while True:
        mostrar_menu()
        opcion = leer_opcion()

        if opcion == "1":
            try:
                decimales = solicitar_decimales(decimales)
                precision_efectiva = ajustar_precision_para_decimales(precision, decimales)
                analizador = AnalizadorEuler(tolerancia, max_iteraciones, precision, decimales)
                analizador.precision = precision_efectiva
                referencia_euler = analizador._referencia_euler()
                resultados = [
                    enriquecer_resultado(item, decimales, analizador.precision, referencia_euler)
                    for item in analizador.ejecutar_todos()
                ]
                imprimir_tabla(resultados)
            except Exception as error:
                print(f"Error en comparacion de metodos: {error}")

        elif opcion == "2":
            try:
                decimales = solicitar_decimales(decimales)
                precision_efectiva = ajustar_precision_para_decimales(precision, decimales)
                analizador = AnalizadorEuler(tolerancia, max_iteraciones, precision_efectiva, decimales)
                ejecutar_metodo_individual(analizador, decimales)
            except Exception as error:
                print(f"Error al ejecutar el metodo: {error}")

        elif opcion == "3":
            try:
                tolerancia_txt = input("Nueva tolerancia (Enter para mantener): ").strip()
                max_iter_txt = input("Maximo de iteraciones (Enter para mantener): ").strip()
                precision = seleccionar_precision()
                decimales = solicitar_decimales(decimales)
                precision = ajustar_precision_para_decimales(precision, decimales)

                if tolerancia_txt:
                    tolerancia = float(tolerancia_txt)
                if max_iter_txt:
                    max_iteraciones = int(max_iter_txt)

                print("\nParametros actualizados correctamente.")
                print(f"Tolerancia: {tolerancia}")
                print(f"Maximo iteraciones: {max_iteraciones}")
                print(f"Precision: {precision}")
                print(f"Decimales solicitados: {decimales}")
            except Exception as error:
                print(f"No se pudieron actualizar los parametros: {error}")

        elif opcion == "4":
            print("Cerrando modulo de Euler. Hasta luego.")
            break
        else:
            print("Opcion invalida. Intenta nuevamente.")


if __name__ == "__main__":
    main()