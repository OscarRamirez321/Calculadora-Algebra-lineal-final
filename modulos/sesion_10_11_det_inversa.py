"""Sesiones 10 y 11: determinantes, inversas y sus propiedades.
Aplica a las matrices de la memoria los mismos cálculos del Módulo III: determinante por
tres métodos, inversa por adjunta y por Gauss-Jordan, y el teorema A·A⁻¹ = I.
Elaborado por: [Integrantes del grupo: completar nombres].
"""
from .interfaz import Consola, Entrada
from .modulo_matrices import ErrorMatriz, MenuMatrices


class MenuDetInversa:
    """Menú de las Sesiones 10 y 11; reutiliza la presentación de MenuMatrices."""

    def __init__(self, asistente):
        """Recibe el AsistenteMemoria y prepara la interfaz de matrices compartida."""
        self.memoria = asistente
        self.presentador = MenuMatrices(asistente)

    def ejecutar(self):
        """Muestra el menú y calcula con la matriz elegida de la memoria."""
        Consola.limpiar()
        Consola.encabezado("SESIÓN 10 Y 11 · DETERMINANTES E INVERSAS")
        Consola.opcion("1", "Calcular determinante (cofactores, Sarrus y triangular)")
        Consola.opcion("2", "Calcular inversa (adjunta vs Gauss-Jordan) y teorema A·A⁻¹ = I")
        Consola.opcion("0", "Regresar al menú principal")
        opcion = Entrada.opcion("\n  Seleccione la operación: ", ["1", "2", "0"])
        if opcion == "0":
            return
        try:
            letra = self.memoria.pedir_letra()
            matriz = self.memoria.requerir(letra)
            self._calcular(opcion, matriz)
        except ErrorMatriz as error:
            Consola.error(str(error))
        Consola.pausar()

    def _calcular(self, opcion, matriz):
        """Ejecuta la opción 1 (determinante) o la 2 (ambas inversas)."""
        if opcion == "1":
            self.presentador.mostrar_determinante(matriz)
            return
        Consola.seccion("Inversa por matriz adjunta")
        self.presentador.mostrar_inversa_adjunta(matriz, guardar=False)
        Consola.seccion("Inversa por Gauss-Jordan")
        self.presentador.mostrar_inversa_gauss_jordan(matriz)
