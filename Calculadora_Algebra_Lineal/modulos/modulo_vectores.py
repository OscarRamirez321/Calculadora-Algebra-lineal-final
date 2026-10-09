"""Módulo II de la Calculadora: vectores y producto matriz-vector.
Implementa operaciones en ℝⁿ y comprueba con ejemplos los teoremas del producto Ax
y las propiedades de la transpuesta usando la clase Matriz del Módulo III.
Elaborado por: [Integrantes del grupo: completar nombres].
"""
from fractions import Fraction

from teoremas.teoremas_vectores import TEOREMA_PRODUCTO_AX
from .interfaz import Consola, Entrada
from .modulo_matrices import Matriz, ResultadoPropiedad

LOGO_MODULO_2 = r"""
  #   #  ###  ####  #   # #      ###      ##### #####
  ## ## #   # #   # #   # #     #   #       #     #
  # # # #   # #   # #   # #     #   #       #     #
  #   # #   # #   # #   # #     #   #       #     #
  #   #  ###  ####   ###  #####  ###      ##### #####
  -------------  V E C T O R E S  E N  R n  -------------
"""


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
    """Menú del Módulo II: vectores, teorema del producto Ax y transpuesta."""

    def ejecutar(self):
        """Muestra el logo y atiende el menú hasta que el usuario vuelve atrás."""
        Consola.logo(LOGO_MODULO_2)
        acciones = {"1": self._operaciones, "2": self._teorema_ax, "3": self._traspuesta}
        while True:
            Consola.encabezado("MÓDULO II · VECTORES")
            Consola.opcion("1", "Operaciones con vectores")
            Consola.opcion("2", "Demostrar teoremas del producto Ax")
            Consola.opcion("3", "Propiedades de la matriz transpuesta")
            Consola.opcion("S", "Volver al menú principal")
            opcion = Entrada.opcion("\n  Seleccione una opción: ", list(acciones) + ["s"])
            if opcion == "s":
                return
            acciones[opcion]()
            Consola.pausar()

    @staticmethod
    def _operaciones():
        """Opción 1: suma, producto punto o escalar sobre dos vectores."""
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
        """Opción 2: muestra el teorema y su comprobación numérica."""
        Consola.seccion("Teorema del producto Ax")
        for linea in TEOREMA_PRODUCTO_AX:
            print(f"  {linea}")
        for resultado in DemostradorPropiedades.teorema_producto_ax():
            Consola.propiedad(resultado)

    @staticmethod
    def _traspuesta():
        """Opción 3: comprueba las propiedades de la transpuesta."""
        Consola.seccion("Propiedades de la matriz transpuesta")
        for resultado in DemostradorPropiedades.propiedades_traspuesta():
            Consola.propiedad(resultado)
