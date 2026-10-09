"""Memoria de matrices A y B compartida por todas las sesiones de la Calculadora.
Permite cargar una vez y reutilizar o encadenar resultados entre módulos, como
en la versión original del proyecto. Separa el almacén (lógica) del asistente (consola).
Elaborado por: [Integrantes del grupo: completar nombres].
"""
from .interfaz import Consola, Entrada
from .modulo_matrices import ErrorMatriz, LectorMatrices


class MemoriaMatrices:
    """Almacén con dos casillas, 'A' y 'B', que guardan objetos Matriz."""

    NOMBRES = ("A", "B")

    def __init__(self):
        """Inicia ambas casillas vacías."""
        self._matrices = {nombre: None for nombre in self.NOMBRES}

    def guardar(self, nombre, matriz):
        """Guarda una matriz en la casilla indicada."""
        self._matrices[nombre] = matriz

    def obtener(self, nombre):
        """Devuelve la matriz guardada, o None si la casilla está vacía."""
        return self._matrices[nombre]

    def describir(self, nombre):
        """Devuelve 'Vacía' o 'Cargada (m×n)' para mostrar el estado."""
        matriz = self._matrices[nombre]
        if matriz is None:
            return "Vacía"
        return f"Cargada ({matriz.filas}×{matriz.columnas})"


class AsistenteMemoria:
    """Interfaz de consola sobre la memoria: cargar, elegir, usar y guardar matrices."""

    def __init__(self, memoria):
        """Recibe la MemoriaMatrices que va a manejar."""
        self.memoria = memoria

    def pedir_letra(self, mensaje="¿A cuál matriz querés aplicar la operación? (A / B): "):
        """Pide 'A' o 'B' y devuelve la letra en mayúscula."""
        return Entrada.opcion(mensaje, ["a", "b"]).upper()

    def requerir(self, nombre):
        """Devuelve la matriz de la casilla o lanza ErrorMatriz si está vacía."""
        matriz = self.memoria.obtener(nombre)
        if matriz is None:
            raise ErrorMatriz(f"La Matriz {nombre} está vacía. Cargala primero en la opción 1 del menú.")
        return matriz

    def cargar(self, nombre):
        """Lee una matriz nueva desde el teclado y la guarda en la casilla."""
        Consola.seccion(f"Ingresando Matriz {nombre}")
        self.memoria.guardar(nombre, LectorMatrices.leer(nombre))
        Consola.exito(f"Matriz {nombre} guardada en memoria.")
        Consola.matriz(self.memoria.obtener(nombre).datos, f"Matriz {nombre}")

    def ofrecer_usar(self, nombre, cuadrada=False):
        """Si hay una matriz utilizable en memoria, pregunta si usarla; devuelve Matriz o None."""
        matriz = self.memoria.obtener(nombre)
        if matriz is None or (cuadrada and not matriz.es_cuadrada()):
            return None
        Consola.matriz(matriz.datos, f"Matriz {nombre} en memoria")
        return matriz if Entrada.si_no(f"  ¿Usar la matriz {nombre} de memoria?") else None

    def ofrecer_guardar(self, matriz, descripcion="este resultado"):
        """Pregunta si guardar `matriz` en A, en B o en ninguna; permite encadenar cálculos."""
        Consola.aviso(f"¿Querés guardar {descripcion} para la siguiente operación?")
        eleccion = Entrada.opcion("  Guardar en (A) / (B) / (N)o guardar: ", ["a", "b", "n"])
        if eleccion != "n":
            self.memoria.guardar(eleccion.upper(), matriz)
            Consola.exito(f"Guardado como la nueva Matriz {eleccion.upper()}.")
