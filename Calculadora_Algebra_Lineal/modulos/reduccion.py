"""Motor de reducción por filas (Gauss-Jordan) reutilizado por varios módulos.
Implementa el método de eliminación de la Sesión de sistemas lineales: lleva una
matriz a su forma escalonada reducida y registra cada paso sin imprimir nada.
Elaborado por: [Integrantes del grupo: completar nombres].
"""
from dataclasses import dataclass
from fractions import Fraction


@dataclass
class PasoReduccion:
    """Descripción, foto de la matriz tras el paso y, si aplica, pivote y fila afectada."""
    descripcion: str
    filas: list
    pivote: object = None  # (fila, columna) del pivote en uso
    fila: object = None  # índice de la fila que cambió


@dataclass
class ResultadoReduccion:
    """Matriz reducida, columnas pivote, intercambios hechos y pasos registrados."""
    filas: list
    columnas_pivote: list
    intercambios: int
    pasos: list


class ReductorFilas:
    """Reduce una matriz a forma escalonada reducida con operaciones de fila."""

    def __init__(self, filas, columnas_a_reducir=None):
        """Recibe las filas y cuántas columnas (desde la izquierda) pueden ser pivote.
        Las demás (p. ej. b o la identidad en [A|I]) solo acompañan las operaciones."""
        self.filas = [[Fraction(valor) for valor in fila] for fila in filas]
        self.columnas_a_reducir = columnas_a_reducir or len(self.filas[0])
        self.columnas_pivote = []
        self.intercambios = 0
        self.pasos = []
        self._registrar("Matriz original")

    def reducir(self):
        """Ejecuta Gauss-Jordan y devuelve un ResultadoReduccion."""
        fila_actual = 0
        for columna in range(self.columnas_a_reducir):
            if fila_actual == len(self.filas):
                break
            fila_pivote = self._buscar_fila_pivote(fila_actual, columna)
            if fila_pivote is None:
                continue  # Columna sin pivote: la variable es libre
            self._intercambiar(fila_actual, fila_pivote)
            self._normalizar(fila_actual, columna)
            self._eliminar_columna(fila_actual, columna)
            self.columnas_pivote.append(columna)
            fila_actual += 1
        return ResultadoReduccion(self.filas, self.columnas_pivote, self.intercambios, self.pasos)

    def _buscar_fila_pivote(self, desde_fila, columna):
        """Devuelve la primera fila (>= desde_fila) con entrada no nula en la columna."""
        for i in range(desde_fila, len(self.filas)):
            if self.filas[i][columna] != 0:
                return i
        return None

    def _intercambiar(self, fila_actual, fila_pivote):
        """Intercambia filas si el pivote es 0: sin pivote no se puede eliminar la columna."""
        if fila_actual == fila_pivote:
            return
        self.filas[fila_actual], self.filas[fila_pivote] = (
            self.filas[fila_pivote], self.filas[fila_actual])
        self.intercambios += 1
        self._registrar(f"Intercambio F{fila_actual + 1} ↔ F{fila_pivote + 1}", None, fila_actual)

    def _normalizar(self, fila, columna):
        """Divide la fila entre su pivote para que el pivote valga 1."""
        pivote = self.filas[fila][columna]
        if pivote == 1:
            return
        self.filas[fila] = [valor / pivote for valor in self.filas[fila]]
        self._registrar(f"Normalizar pivote: F{fila + 1} ÷ ({pivote})", (fila, columna), fila)

    def _eliminar_columna(self, fila_pivote, columna):
        """Hace ceros arriba y abajo del pivote (por eso es Gauss-Jordan y no solo Gauss)."""
        for i in range(len(self.filas)):
            factor = self.filas[i][columna]
            if i != fila_pivote and factor != 0:
                self.filas[i] = [
                    actual - factor * pivote
                    for actual, pivote in zip(self.filas[i], self.filas[fila_pivote])
                ]
                operador = "−" if factor > 0 else "+"
                self._registrar(
                    f"Hacer cero: F{i + 1} → F{i + 1} {operador} {abs(factor)}·F{fila_pivote + 1}",
                    (fila_pivote, columna), i)

    def _registrar(self, descripcion, pivote=None, fila=None):
        """Guarda una copia de la matriz (y qué se resaltó) para mostrar el proceso después."""
        self.pasos.append(PasoReduccion(descripcion, [valores[:] for valores in self.filas], pivote, fila))
