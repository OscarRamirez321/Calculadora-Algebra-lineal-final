"""Módulo de Factorización LU (A = LU) y solución de sistemas Ax = b por doble sustitución.
Reduce A con operaciones de reemplazo de fila, registra los multiplicadores en L y
resuelve Ly = b y Ux = y. Reutiliza Matriz y ReductorFilas; solo MenuLU usa la consola.
Elaborado por: [Integrantes del grupo: completar nombres].
"""
from dataclasses import dataclass
from fractions import Fraction

from teoremas.teoremas_lu import TEOREMAS_LU
from .interfaz import Consola, Entrada, Estilo
from .modulo_matrices import ErrorMatriz, LectorMatrices, Matriz, Validador
from .reduccion import ReductorFilas

LOGO_MODULO_LU = r"""
  #      #   #
  #      #   #
  #      #   #
  #      #   #
  #####   ###
  ------  F A C T O R I Z A C I Ó N   L U  ------
"""

MENSAJE_PERMUTACION = ("La matriz no admite Factorización LU sin permutación "
                       "(requiere pivoteo parcial PA = LU)")


class ErrorPermutacion(ErrorMatriz):
    """Un pivote es cero y haría falta intercambiar filas: no hay A = LU directa."""


@dataclass
class PasoLU:
    """Descripción de una operación de fila y las filas de U y L tras aplicarla."""
    descripcion: str
    filas_u: list
    filas_l: list
    pivote: object = None  # (fila, columna) del pivote en uso
    fila: object = None  # índice de la fila de U que cambió


@dataclass
class ResultadoLU:
    """Factores L y U, multiplicadores (i, j, l) y pasos registrados."""
    matriz_L: Matriz
    matriz_U: Matriz
    multiplicadores: list
    pasos: list


@dataclass
class ResultadoSistema:
    """Vectores y, x y los pasos de ambas sustituciones."""
    vector_y: list
    vector_x: list
    pasos_y: list
    pasos_x: list


class FactorizacionLU:
    """Obtiene U y L de una matriz A (m × n) usando solo reemplazos de fila."""

    def __init__(self, matriz_a):
        """Parte de U = A y L = I (m × m)."""
        self.filas_u = [fila[:] for fila in matriz_a.datos]
        self.filas_l = [[Fraction(int(i == j)) for j in range(matriz_a.filas)]
                        for i in range(matriz_a.filas)]
        self.multiplicadores = []
        self.pasos = []
        self._registrar("Matriz original: U = A y L = I")

    def calcular(self):
        """Devuelve un ResultadoLU; lanza ErrorPermutacion si se necesita intercambiar filas."""
        fila_pivote = 0
        for columna in range(len(self.filas_u[0])):
            if fila_pivote == len(self.filas_u):
                break
            if self.filas_u[fila_pivote][columna] == 0:
                self._exigir_sin_permutacion(fila_pivote, columna)
                continue  # Columna sin pivote: no hay nada que eliminar debajo
            self._eliminar_debajo(fila_pivote, columna)
            fila_pivote += 1
        return ResultadoLU(Matriz(self.filas_l), Matriz(self.filas_u), self.multiplicadores, self.pasos)

    def _exigir_sin_permutacion(self, fila_pivote, columna):
        """Un pivote 0 con valores no nulos debajo exigiría un intercambio de filas."""
        if any(self.filas_u[i][columna] != 0 for i in range(fila_pivote + 1, len(self.filas_u))):
            raise ErrorPermutacion(MENSAJE_PERMUTACION)

    def _eliminar_debajo(self, fila_pivote, columna):
        """Hace ceros debajo del pivote con Fi ← Fi − l·Fj y guarda cada l en L."""
        pivote = self.filas_u[fila_pivote][columna]
        for i in range(fila_pivote + 1, len(self.filas_u)):
            elemento_a_eliminar = self.filas_u[i][columna]
            if elemento_a_eliminar == 0:
                continue
            multiplicador_l = elemento_a_eliminar / pivote
            # Se registra el multiplicador en L antes de alterar la fila en U
            self.filas_l[i][fila_pivote] = multiplicador_l
            self.filas_u[i] = [valor - multiplicador_l * valor_pivote
                               for valor, valor_pivote in zip(self.filas_u[i], self.filas_u[fila_pivote])]
            self.multiplicadores.append((i, fila_pivote, multiplicador_l))
            self._registrar(f"F{i + 1} ← F{i + 1} − ({multiplicador_l})·F{fila_pivote + 1}",
                            (fila_pivote, columna), i)

    def _registrar(self, descripcion, pivote=None, fila=None):
        """Guarda una copia de U y L para mostrar el proceso después."""
        self.pasos.append(PasoLU(descripcion, [f[:] for f in self.filas_u],
                                 [f[:] for f in self.filas_l], pivote, fila))


class ResolverSistemaLU:
    """Resuelve Ax = b con la doble sustitución Ly = b y Ux = y."""

    @staticmethod
    def _sustituir(matriz_triangular, vector):
        """Reduce [T | v] con ReductorFilas y devuelve (solución, pasos)."""
        n = matriz_triangular.filas
        aumentada = [fila + [vector[i]] for i, fila in enumerate(matriz_triangular.datos)]
        reduccion = ReductorFilas(aumentada, n).reducir()
        return [fila[n] for fila in reduccion.filas], reduccion.pasos

    @classmethod
    def resolver(cls, matriz_L, matriz_U, vector_b):
        """Devuelve un ResultadoSistema; exige A cuadrada y sin pivotes nulos en U."""
        Validador.cuadrada(matriz_U.dimension, "la solución por sustitución")
        if any(matriz_U.datos[i][i] == 0 for i in range(matriz_U.filas)):
            raise ErrorMatriz("El sistema no tiene solución única: U tiene un 0 en la diagonal (A es singular)")
        vector_y, pasos_y = cls._sustituir(matriz_L, vector_b)
        vector_x, pasos_x = cls._sustituir(matriz_U, vector_y)
        return ResultadoSistema(vector_y, vector_x, pasos_y, pasos_x)


class VerificadorLU:
    """Comprobaciones finales: L·U == A y A·x == b, con exactitud de Fraction."""

    @staticmethod
    def factorizacion_correcta(matriz_a, resultado):
        """Devuelve True si L·U == A (usa el producto de Matriz)."""
        return resultado.matriz_L.producto(resultado.matriz_U) == matriz_a

    @staticmethod
    def solucion_correcta(matriz_a, vector_x, vector_b):
        """Devuelve True si A·x == b."""
        return matriz_a.por_vector(vector_x) == list(vector_b)


class MenuLU:
    """Menú del módulo LU: lee A y b, llama a la lógica y muestra el resultado."""

    PASOS_COMPLETOS_HASTA_ORDEN = 3  # Con tamaños mayores solo se muestra el final

    def __init__(self, asistente=None):
        """Recibe el AsistenteMemoria para reutilizar A guardada (opcional)."""
        self.asistente = asistente

    def ejecutar(self):
        """Muestra el logo y atiende el menú hasta que el usuario vuelve atrás."""
        Consola.limpiar()
        Consola.logo(LOGO_MODULO_LU)
        acciones = {"1": self._factorizar_y_resolver, "0": self._teoremas}
        while True:
            Consola.encabezado("FACTORIZACIÓN LU Y SOLUCIÓN Ax = b")
            Consola.opcion("1", "Factorización LU y solución Ax = b")
            Consola.opcion("0", "Ver Teoremas Clave del Módulo")
            Consola.opcion("S", "Volver al menú principal")
            opcion = Entrada.opcion("\n  Seleccione una opción: ", list(acciones) + ["s"])
            if opcion == "s":
                return
            try:
                acciones[opcion]()
            except ErrorMatriz as error:
                Consola.error(str(error))
            Consola.pausar()

    def _leer_a(self):
        """Obtiene A de la memoria (si el usuario quiere) o del teclado."""
        guardada = self.asistente.ofrecer_usar("A") if self.asistente else None
        return guardada or LectorMatrices.leer("A")

    def _factorizar_y_resolver(self):
        """Pide A y b, muestra L y U, verifica L·U == A y resuelve si A es cuadrada."""
        Consola.seccion("Factorización A = LU")
        matriz_a = self._leer_a()
        vector_b = Entrada.fila(f"    Vector b ({matriz_a.filas} componentes): ", matriz_a.filas)
        resultado = FactorizacionLU(matriz_a).calcular()
        self._mostrar_factorizacion(matriz_a, resultado)
        if matriz_a.es_cuadrada():
            self._mostrar_solucion(matriz_a, resultado, vector_b)
        else:
            Consola.aviso("Ax = b se resuelve con LU solo si A es cuadrada (n × n).")

    def _mostrar_factorizacion(self, matriz_a, resultado):
        """Muestra los pasos, L, U y el veredicto de L·U == A."""
        Consola.matriz(matriz_a.datos, "Matriz A")
        pasos = resultado.pasos
        if max(matriz_a.dimension) > self.PASOS_COMPLETOS_HASTA_ORDEN:
            pasos = pasos[:1]
        for numero, paso in enumerate(pasos):
            Consola.matriz(paso.filas_u, f"Paso {numero}: {paso.descripcion} (U)")
        Consola.matriz(resultado.matriz_L.datos, "Matriz L")
        Consola.matriz(resultado.matriz_U.datos, "Matriz U")
        if VerificadorLU.factorizacion_correcta(matriz_a, resultado):
            Consola.exito("La factorización es correcta (L · U == A)")
        else:
            Consola.error("La factorización es incorrecta (L · U ≠ A)")

    @staticmethod
    def _mostrar_solucion(matriz_a, resultado, vector_b):
        """Resuelve Ly = b y Ux = y, muestra y, x y la comprobación A·x == b."""
        solucion = ResolverSistemaLU.resolver(resultado.matriz_L, resultado.matriz_U, vector_b)
        Consola.seccion("Solución por doble sustitución")
        Consola.valor(solucion.vector_y, "Vector intermedio y (de Ly = b)")
        Consola.valor(solucion.vector_x, "Vector solución x (de Ux = y)")
        if VerificadorLU.solucion_correcta(matriz_a, solucion.vector_x, vector_b):
            Consola.exito("Comprobación exitosa: A · x == b")
        else:
            Consola.error("Comprobación fallida: A · x ≠ b")

    @staticmethod
    def _teoremas():
        """Opción 0: muestra los teoremas clave del módulo."""
        Consola.encabezado("TEOREMAS CLAVE · FACTORIZACIÓN LU", Estilo.MAGENTA)
        for titulo, lineas in TEOREMAS_LU:
            Consola.seccion(titulo)
            for linea in lineas:
                print(f"  {linea}")
