"""Utilidades de consola compartidas por todos los módulos de la Calculadora.
Centralizan colores, formato de matrices y lectura validada de datos, para que
ningún módulo repita código de entrada/salida.
Elaborado por: [Integrantes del grupo: completar nombres].
"""
import os
import sys
from fractions import Fraction


class Estilo:
    """Códigos ANSI de color; se desactivan si la salida no es una terminal."""

    RESET = "\033[0m"
    NEGRITA = "\033[1m"
    TENUE = "\033[2m"
    ROJO = "\033[91m"
    VERDE = "\033[92m"
    AMARILLO = "\033[93m"
    AZUL = "\033[94m"
    MAGENTA = "\033[95m"
    CIAN = "\033[96m"

    @staticmethod
    def activo():
        """Devuelve True si conviene usar colores (terminal y sin NO_COLOR)."""
        return sys.stdout.isatty() and "NO_COLOR" not in os.environ

    @classmethod
    def pintar(cls, texto, *estilos):
        """Devuelve el texto envuelto en los códigos de estilo indicados."""
        if not cls.activo() or not estilos:
            return texto
        return "".join(estilos) + texto + cls.RESET


class Consola:
    """Mensajes con formato: encabezados, avisos, matrices y pausas."""

    ANCHO = 66

    @staticmethod
    def preparar_terminal():
        """Activa UTF-8 y los colores ANSI (en Windows hay que pedirlo)."""
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass
        if os.name == "nt":
            os.system("")  # Llamada vacía: habilita secuencias ANSI en cmd

    @staticmethod
    def limpiar():
        """Limpia la pantalla si hay una terminal real (no ensucia redirecciones)."""
        if sys.stdout.isatty():
            os.system("cls" if os.name == "nt" else "clear")

    @classmethod
    def logo(cls, texto, color=Estilo.CIAN):
        """Imprime un logotipo ASCII en el color indicado."""
        print()
        print(Estilo.pintar(texto.strip("\n"), color, Estilo.NEGRITA))

    @classmethod
    def encabezado(cls, titulo, color=Estilo.CIAN):
        """Imprime un título dentro de un recuadro doble."""
        borde = "═" * (cls.ANCHO - 2)
        print()
        print(Estilo.pintar(f"╔{borde}╗", color))
        print(Estilo.pintar(f"║{titulo.center(cls.ANCHO - 2)}║", color, Estilo.NEGRITA))
        print(Estilo.pintar(f"╚{borde}╝", color))

    @classmethod
    def seccion(cls, titulo):
        """Imprime un subtítulo con una línea decorativa."""
        relleno = "─" * max(2, cls.ANCHO - len(titulo) - 4)
        print()
        print(Estilo.pintar(f"── {titulo} {relleno}", Estilo.AZUL, Estilo.NEGRITA))

    @staticmethod
    def opcion(clave, texto):
        """Imprime una opción de menú con su clave resaltada."""
        print(f"  {Estilo.pintar(f'[{clave}]', Estilo.AMARILLO, Estilo.NEGRITA)} {texto}")

    @staticmethod
    def info(texto):
        """Imprime un mensaje informativo."""
        print(Estilo.pintar(f"  {texto}", Estilo.TENUE))

    @staticmethod
    def exito(texto):
        """Imprime un mensaje de éxito."""
        print(Estilo.pintar(f"  ✔ {texto}", Estilo.VERDE, Estilo.NEGRITA))

    @staticmethod
    def error(texto):
        """Imprime un mensaje de error."""
        print(Estilo.pintar(f"  ✘ {texto}", Estilo.ROJO, Estilo.NEGRITA))

    @staticmethod
    def aviso(texto):
        """Imprime una advertencia."""
        print(Estilo.pintar(f"  ⚠ {texto}", Estilo.AMARILLO))

    @staticmethod
    def pausar():
        """Espera Enter para que el usuario alcance a leer el resultado."""
        input(Estilo.pintar("\n  Presione Enter para continuar...", Estilo.TENUE))

    @classmethod
    def lineas_matriz(cls, datos, columna_separadora=None):
        """Devuelve las líneas de una matriz con columnas alineadas y corchetes.
        Si se da columna_separadora, dibuja una barra antes de esa columna."""
        celdas = [[str(valor) for valor in fila] for fila in datos]
        anchos = [max(len(fila[j]) for fila in celdas) for j in range(len(celdas[0]))]
        filas = []
        for fila in celdas:
            partes = []
            for j, texto in enumerate(fila):
                if j == columna_separadora:
                    partes.append("│")
                partes.append(texto.rjust(anchos[j]))
            filas.append(" ".join(partes))
        return cls._poner_corchetes(filas)

    @staticmethod
    def _poner_corchetes(filas):
        """Rodea las filas con corchetes de una pieza (┌ ┐ │ └ ┘)."""
        if len(filas) == 1:
            return [f"  [ {filas[0]} ]"]
        ultima = len(filas) - 1
        lineas = []
        for i, fila in enumerate(filas):
            izquierda = "┌" if i == 0 else "└" if i == ultima else "│"
            derecha = "┐" if i == 0 else "┘" if i == ultima else "│"
            lineas.append(f"  {izquierda} {fila} {derecha}")
        return lineas

    @classmethod
    def matriz(cls, datos, titulo=None, columna_separadora=None):
        """Imprime una matriz (lista de filas) con su título y dimensiones.
        Las matrices aumentadas no muestran dimensiones: la barra ya las separa."""
        if titulo:
            dimension = ""
            if columna_separadora is None:
                dimension = f"  ({len(datos)} × {len(datos[0])})"
            print(Estilo.pintar(f"\n  {titulo}{dimension}", Estilo.NEGRITA))
        for linea in cls.lineas_matriz(datos, columna_separadora):
            print(Estilo.pintar(linea, Estilo.CIAN))

    @classmethod
    def valor(cls, valor, titulo):
        """Imprime una matriz (objeto con .datos), una lista o un número."""
        if hasattr(valor, "datos"):
            cls.matriz(valor.datos, titulo)
        elif isinstance(valor, list):
            texto = ", ".join(str(elemento) for elemento in valor)
            print(Estilo.pintar(f"\n  {titulo} = ", Estilo.NEGRITA) + f"[{texto}]")
        else:
            print(Estilo.pintar(f"\n  {titulo} = ", Estilo.NEGRITA) + str(valor))

    @classmethod
    def propiedad(cls, resultado):
        """Imprime una propiedad comprobada: ambos miembros y el veredicto.
        Recibe un objeto con numero, enunciado, miembros y se_cumple."""
        cls.seccion(f"Propiedad {resultado.numero}: {resultado.enunciado}")
        for titulo, valor in resultado.auxiliares:
            cls.valor(valor, titulo)
        cls.valor(resultado.lado_izquierdo, resultado.expresion_izquierda)
        cls.valor(resultado.lado_derecho, resultado.expresion_derecha)
        if resultado.se_cumple:
            cls.exito("Se cumple")
        else:
            cls.error("No se cumple")


class Entrada:
    """Lectura desde teclado: cada dato se valida y se vuelve a pedir si falla."""

    @staticmethod
    def texto_a_fraccion(texto):
        """Convierte '3', '-1/2' o '0,75' en Fraction; lanza ValueError si no es válido."""
        limpio = texto.strip().replace(",", ".")  # Acepta coma decimal (0,5)
        try:
            return Fraction(limpio)
        except ZeroDivisionError:
            raise ValueError(f"'{texto}': el denominador no puede ser 0") from None
        except ValueError:
            raise ValueError(f"'{texto}' no es un número válido") from None

    @classmethod
    def fraccion(cls, mensaje):
        """Pide un número (entero, decimal o fracción) hasta recibir uno válido."""
        while True:
            try:
                return cls.texto_a_fraccion(input(mensaje))
            except ValueError as error:
                Consola.error(f"{error}. Intente de nuevo.")

    @staticmethod
    def entero_positivo(mensaje, maximo=None):
        """Pide un entero >= 1 (y <= maximo si se indica) hasta recibir uno válido."""
        while True:
            texto = input(mensaje).strip()
            if texto.isdigit() and int(texto) >= 1 and (maximo is None or int(texto) <= maximo):
                return int(texto)
            limite = f" y como máximo {maximo}" if maximo else ""
            Consola.error(f"'{texto}' no es válido: debe ser un entero positivo{limite}.")

    @classmethod
    def fila(cls, mensaje, cantidad):
        """Pide una fila de `cantidad` números separados por espacios."""
        while True:
            partes = input(mensaje).split()
            if len(partes) != cantidad:
                Consola.error(f"Se esperaban {cantidad} valores y se recibieron {len(partes)}.")
                continue
            try:
                return [cls.texto_a_fraccion(parte) for parte in partes]
            except ValueError as error:
                Consola.error(f"{error}. Ingrese la fila completa otra vez.")

    @staticmethod
    def si_no(mensaje):
        """Pregunta s/n y devuelve True para 's' (cualquier otra respuesta se repite)."""
        while True:
            respuesta = input(f"{mensaje} (s/n): ").strip().lower()
            if respuesta in ("s", "n"):
                return respuesta == "s"
            Consola.error("Responda 's' o 'n'.")

    @staticmethod
    def opcion(mensaje, validas):
        """Pide una opción de menú dentro de `validas` (sin distinguir mayúsculas)."""
        while True:
            eleccion = input(mensaje).strip().lower()
            if eleccion in validas:
                return eleccion
            Consola.error("Opción inválida. Elija una de las que aparecen en el menú.")
