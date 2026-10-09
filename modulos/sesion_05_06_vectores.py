"""Sesiones 5 y 6: ecuaciones vectoriales, combinación lineal e independencia lineal.
Las columnas de la Matriz A de la memoria son el conjunto de vectores. Incluye operaciones
en ℝⁿ y comprobaciones numéricas del teorema del producto Ax y de la transpuesta.
Elaborado por: [Integrantes del grupo: completar nombres].
"""
from fractions import Fraction

from teoremas.teoremas_vectores import CRITERIO_INDEPENDENCIA, TEOREMA_PRODUCTO_AX
from .interfaz import Consola, Entrada
from .modulo_matrices import ErrorMatriz, Matriz, ResultadoPropiedad
from .reduccion import ReductorFilas
from .sesion_02_07_08_sistemas import SistemaLineal


class OperacionesVector:
    """Operaciones básicas en ℝⁿ; los vectores son listas de Fractions."""

    @staticmethod
    def sumar(u, v):
        """Devuelve u + v componente a componente."""
        return [a + b for a, b in zip(u, v)]

    @staticmethod
    def producto_punto(u, v):
        """Devuelve el producto punto u • v."""
        return sum(a * b for a, b in zip(u, v))

    @staticmethod
    def por_escalar(k, v):
        """Devuelve k·v."""
        return [k * componente for componente in v]


class IndependenciaLineal:
    """Decide si v1, ..., vk son L.I. resolviendo c1·v1 + ... + ck·vk = 0."""

    def __init__(self, vectores):
        """Recibe una lista de vectores (listas de Fractions) de la misma dimensión."""
        self.vectores = vectores

    def analizar(self):
        """Devuelve (ResultadoReduccion, es_independiente) del sistema homogéneo."""
        k = len(self.vectores)
        # Los vectores van como columnas; la columna de ceros es el lado derecho homogéneo
        aumentada = [[v[i] for v in self.vectores] + [Fraction(0)]
                     for i in range(len(self.vectores[0]))]
        reduccion = ReductorFilas(aumentada, k).reducir()
        return reduccion, len(reduccion.columnas_pivote) == k


class DemostradorPropiedades:
    """Comprobaciones numéricas con ejemplos fijos, listas para mostrar en pantalla."""

    @staticmethod
    def teorema_producto_ax():
        """Comprueba A(u + v) = Au + Av y A(cu) = c(Au); devuelve dos ResultadoPropiedad."""
        a = Matriz([[1, 2], [3, 4]])
        u, v, c = [Fraction(1), Fraction(1)], [Fraction(2), Fraction(0)], Fraction(3)
        suma_izq = a.por_vector(OperacionesVector.sumar(u, v))
        suma_der = OperacionesVector.sumar(a.por_vector(u), a.por_vector(v))
        esc_izq = a.por_vector(OperacionesVector.por_escalar(c, u))
        esc_der = OperacionesVector.por_escalar(c, a.por_vector(u))
        return [
            ResultadoPropiedad(1, "A(u + v) = Au + Av", "A(u + v)", suma_izq, "Au + Av",
                               suma_der, suma_izq == suma_der, [("A", a)]),
            ResultadoPropiedad(2, "A(cu) = c(Au)", "A(cu)", esc_izq, "c(Au)",
                               esc_der, esc_izq == esc_der, [("c", c)]),
        ]

    @staticmethod
    def propiedades_traspuesta():
        """Comprueba las cuatro propiedades de la transpuesta con matrices de ejemplo."""
        a = Matriz([[1, 2, 3], [4, 5, 6]])
        b = Matriz([[7, 8, 9], [10, 11, 12]])
        c = Fraction(3)
        cuadrada_a = Matriz([[1, 2], [3, 4]])
        cuadrada_b = Matriz([[5, 6], [7, 8]])
        pares = [
            ("(A + B)ᵀ = Aᵀ + Bᵀ", "(A + B)ᵀ", a.sumar(b).transpuesta(),
             "Aᵀ + Bᵀ", a.transpuesta().sumar(b.transpuesta()), [("A", a), ("B", b)]),
            ("(Aᵀ)ᵀ = A", "(Aᵀ)ᵀ", a.transpuesta().transpuesta(), "A", a, [("A", a)]),
            ("(cA)ᵀ = c·Aᵀ", "(cA)ᵀ", a.por_escalar(c).transpuesta(),
             "c·Aᵀ", a.transpuesta().por_escalar(c), [("A", a), ("c", c)]),
            ("(AB)ᵀ = BᵀAᵀ", "(AB)ᵀ", cuadrada_a.producto(cuadrada_b).transpuesta(),
             "BᵀAᵀ", cuadrada_b.transpuesta().producto(cuadrada_a.transpuesta()),
             [("A", cuadrada_a), ("B", cuadrada_b)]),
        ]
        return [
            ResultadoPropiedad(i, enunciado, exp_izq, izq, exp_der, der, izq == der, aux)
            for i, (enunciado, exp_izq, izq, exp_der, der, aux) in enumerate(pares, start=1)
        ]




class MenuVectores:
    """Menú de las Sesiones 5 y 6: independencia, combinación lineal y vectores en ℝⁿ."""

    def __init__(self, asistente):
        """Recibe el AsistenteMemoria con el que lee las matrices."""
        self.memoria = asistente
        self.acciones = {
            "1": self._independencia, "2": self._combinacion, "3": self._operaciones,
            "4": self._teorema_ax, "5": self._traspuesta,
        }

    def ejecutar(self):
        """Muestra el menú de la sesión y ejecuta la opción elegida."""
        Consola.limpiar()
        Consola.encabezado("SESIÓN 5 Y 6 · VECTORES, C.L. E INDEPENDENCIA")
        Consola.info("Las columnas de la Matriz A son su conjunto de vectores v1, v2, ..., vk.")
        Consola.opcion("1", "Evaluar independencia lineal (sistema homogéneo Ax = 0)")
        Consola.opcion("2", "Verificar si un vector b es combinación lineal (Ax = b)")
        Consola.opcion("3", "Operaciones con vectores (suma, producto punto, escalar)")
        Consola.opcion("4", "Demostrar teoremas del producto Ax")
        Consola.opcion("5", "Propiedades de la matriz transpuesta")
        Consola.opcion("0", "Regresar al menú principal")
        opcion = Entrada.opcion("\n  Seleccione la operación: ", list(self.acciones) + ["0"])
        if opcion == "0":
            return
        try:
            self.acciones[opcion]()
        except ErrorMatriz as error:
            Consola.error(str(error))
        Consola.pausar()

    def _independencia(self):
        """Opción 1: decide si las columnas de A son L.I. o L.D."""
        a = self.memoria.requerir("A")
        for linea in CRITERIO_INDEPENDENCIA:
            Consola.info(linea)
        reduccion, es_independiente = IndependenciaLineal(a.columnas_como_vectores()).analizar()
        k, pivotes = a.columnas, len(reduccion.columnas_pivote)
        Consola.matriz(reduccion.filas, "Forma reducida del sistema homogéneo", columna_separadora=k)
        print(f"\n  Vectores analizados (columnas): {k} | Pivotes: {pivotes} | Variables libres: {k - pivotes}")
        if es_independiente:
            Consola.exito("LINEALMENTE INDEPENDIENTES (L.I.): solo existe la solución trivial c = 0.")
        else:
            Consola.error(f"LINEALMENTE DEPENDIENTES (L.D.): {k - pivotes} variable(s) libre(s), "
                          "hay infinitas combinaciones que dan el vector cero.")

    def _combinacion(self):
        """Opción 2: indica si b es combinación lineal de las columnas de A."""
        a = self.memoria.requerir("A")
        b = Entrada.fila(f"  Vector b ({a.filas} componentes): ", a.filas)
        sistema = SistemaLineal.desde_matriz(a, b)
        reduccion = sistema.reducir()
        Consola.matriz(reduccion.filas, "Matriz reducida [vectores | b]", columna_separadora=a.columnas)
        diagnostico = sistema.diagnosticar(reduccion)
        if diagnostico.tipo == "incompatible":
            Consola.error("b NO es combinación lineal de los vectores dados (sistema incompatible).")
        elif diagnostico.tipo == "indeterminado":
            Consola.exito("b SÍ es combinación lineal, de INFINITAS maneras (sistema indeterminado).")
        else:
            Consola.exito("b SÍ es combinación lineal, de una ÚNICA manera:")
            for columna, valor in diagnostico.solucion.items():
                print(f"  c{columna + 1} = {valor}")

    @staticmethod
    def _operaciones():
        """Opción 3: suma, producto punto o escalar sobre dos vectores."""
        Consola.seccion("Operaciones con vectores en ℝⁿ")
        n = Entrada.entero_positivo("  Dimensión de los vectores (n): ")
        u = Entrada.fila(f"    Vector 1 ({n} componentes): ", n)
        v = Entrada.fila(f"    Vector 2 ({n} componentes): ", n)
        Consola.opcion("1", "Suma (v1 + v2)")
        Consola.opcion("2", "Producto punto (v1 • v2)")
        Consola.opcion("3", "Multiplicar v1 por un escalar")
        opcion = Entrada.opcion("  Operación: ", ["1", "2", "3"])
        if opcion == "1":
            Consola.valor(OperacionesVector.sumar(u, v), "v1 + v2")
        elif opcion == "2":
            Consola.valor(OperacionesVector.producto_punto(u, v), "v1 • v2")
        else:
            k = Entrada.fraccion("  Escalar k: ")
            Consola.valor(OperacionesVector.por_escalar(k, u), f"({k})·v1")

    @staticmethod
    def _teorema_ax():
        """Opción 4: muestra el teorema y su comprobación numérica."""
        Consola.seccion("Teorema del producto Ax")
        for linea in TEOREMA_PRODUCTO_AX:
            print(f"  {linea}")
        for resultado in DemostradorPropiedades.teorema_producto_ax():
            Consola.propiedad(resultado)

    @staticmethod
    def _traspuesta():
        """Opción 5: comprueba las propiedades de la transpuesta."""
        Consola.seccion("Propiedades de la matriz transpuesta")
        for resultado in DemostradorPropiedades.propiedades_traspuesta():
            Consola.propiedad(resultado)
