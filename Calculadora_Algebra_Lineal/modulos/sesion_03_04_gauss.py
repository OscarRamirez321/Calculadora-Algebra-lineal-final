"""Sesiones 3 y 4: forma escalonada reducida (RREF) y existencia de soluciones.
Reduce por Gauss-Jordan la matriz elegida, muestra el proceso paso a paso y analiza
pivotes y variables libres para decidir independencia lineal.
Elaborado por: [Integrantes del grupo: completar nombres].
"""
from .interfaz import Consola, Entrada, Estilo
from .modulo_matrices import ErrorMatriz, Matriz
from .reduccion import ReductorFilas


class MenuGauss:
    """Menú de las Sesiones 3 y 4 sobre una matriz de la memoria."""

    def __init__(self, asistente):
        """Recibe el AsistenteMemoria con el que lee y guarda matrices."""
        self.memoria = asistente

    def ejecutar(self):
        """Muestra el menú, reduce la matriz elegida y analiza el resultado."""
        Consola.limpiar()
        Consola.encabezado("SESIÓN 3 Y 4 · FORMA ESCALONADA Y EXISTENCIA")
        Consola.opcion("1", "Reducción Gauss-Jordan (paso a paso detallado)")
        Consola.opcion("2", "Análisis rápido (RREF directo, pivotes y L.I. / L.D.)")
        Consola.opcion("0", "Regresar al menú principal")
        opcion = Entrada.opcion("\n  Seleccione la operación: ", ["1", "2", "0"])
        if opcion == "0":
            return
        try:
            letra = self.memoria.pedir_letra("¿A cuál matriz querés aplicar Gauss-Jordan? (A / B): ")
            matriz = self.memoria.requerir(letra)
            self._reducir_y_analizar(matriz, letra, paso_a_paso=(opcion == "1"))
        except ErrorMatriz as error:
            Consola.error(str(error))
        Consola.pausar()

    def _reducir_y_analizar(self, matriz, letra, paso_a_paso):
        """Reduce la matriz, muestra el proceso pedido y el teorema de unicidad."""
        reduccion = ReductorFilas(matriz.datos).reducir()
        if paso_a_paso:
            self._mostrar_pasos(reduccion.pasos)
        else:
            Consola.matriz(reduccion.filas, f"Matriz RREF de {letra}")
        self._teorema_unicidad(matriz, reduccion)
        self.memoria.ofrecer_guardar(Matriz(reduccion.filas), "la matriz reducida (RREF)")

    @staticmethod
    def _mostrar_pasos(pasos):
        """Muestra cada paso y espera Enter, para poder seguirlos con calma."""
        Consola.seccion("Iniciando reducción por filas")
        for numero, paso in enumerate(pasos):
            Consola.matriz(paso.filas, f"Paso {numero}: {paso.descripcion}")
            if numero < len(pasos) - 1:
                input(Estilo.pintar("  [Enter para ver el siguiente paso...]", Estilo.TENUE))
        Consola.exito("Reducción a forma escalonada reducida (RREF) completada.")

    @staticmethod
    def _teorema_unicidad(matriz, reduccion):
        """Sesión 4: pivotes y variables libres deciden si las columnas son L.I."""
        pivotes = len(reduccion.columnas_pivote)
        libres = matriz.columnas - pivotes
        Consola.encabezado("VERIFICACIÓN AUTOMÁTICA · SESIÓN 4", Estilo.MAGENTA)
        print("  Análisis de unicidad e independencia lineal")
        print(f"  Columnas (variables): {matriz.columnas} | Pivotes: {pivotes} | Variables libres: {libres}")
        if libres == 0:
            Consola.exito("VECTORES LINEALMENTE INDEPENDIENTES (L.I.): solución única.")
        else:
            Consola.error("VECTORES LINEALMENTE DEPENDIENTES (L.D.): hay variables libres, infinitas soluciones.")
