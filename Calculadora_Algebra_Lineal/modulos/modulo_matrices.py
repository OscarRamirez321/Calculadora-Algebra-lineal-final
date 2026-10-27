"""Módulo III de la Calculadora: álgebra de matrices.
Implementa operaciones básicas, determinantes (cofactores, Sarrus y reducción),
inversa (Gauss-Jordan y adjunta) y verificador de propiedades, sin librerías externas.
Las clases de cálculo no imprimen ni piden datos; solo la parte de interfaz usa la consola.
Elaborado por: [Integrantes del grupo: completar nombres].
"""
import operator
from dataclasses import dataclass, field, replace
from fractions import Fraction

from teoremas.teoremas_modulo3 import TEOREMAS_MODULO_3
from .interfaz import Consola, Entrada, Estilo
from .reduccion import PasoReduccion, ReductorFilas

LOGO_MODULO_3 = r"""
  #   #  ###  ####  #   # #      ###      ##### ##### #####
  ## ## #   # #   # #   # #     #   #       #     #     #
  # # # #   # #   # #   # #     #   #       #     #     #
  #   # #   # #   # #   # #     #   #       #     #     #
  #   #  ###  ####   ###  #####  ###      ##### ##### #####
  ---------  A L G E B R A   D E   M A T R I C E S  ---------
"""


# ======================================================================
#  LÓGICA: validación, matrices, determinantes, inversas y propiedades
# ======================================================================


class ErrorMatriz(ValueError):
    """Operación imposible: dimensiones incompatibles o matriz inadecuada."""


class Validador:
    """Condiciones previas de cada operación; se comprueban antes de calcular."""

    @staticmethod
    def misma_dimension(dim_a, dim_b, verbo):
        """Exige que A y B tengan el mismo tamaño (suma y resta)."""
        if dim_a != dim_b:
            raise ErrorMatriz(
                f"No se puede {verbo}: A es {dim_a[0]}×{dim_a[1]} y B es {dim_b[0]}×{dim_b[1]}")

    @staticmethod
    def producto_posible(dim_a, dim_b):
        """Exige columnas de A == filas de B para poder multiplicar."""
        if dim_a[1] != dim_b[0]:
            raise ErrorMatriz(
                f"No se puede multiplicar: Columnas de A [{dim_a[1]}] ≠ Filas de B [{dim_b[0]}]")

    @staticmethod
    def cuadrada(dimension, operacion):
        """Exige matriz cuadrada (determinante, inversa)."""
        if dimension[0] != dimension[1]:
            raise ErrorMatriz(
                f"No se puede calcular {operacion}: la matriz es "
                f"{dimension[0]}×{dimension[1]} y no es cuadrada")


class Matriz:
    """Matriz rectangular de Fractions con las operaciones del álgebra matricial."""

    def __init__(self, filas):
        """Construye desde una lista de filas; usa Fraction para no perder exactitud."""
        datos = [[Fraction(valor) for valor in fila] for fila in filas]
        if not datos or not datos[0] or any(len(fila) != len(datos[0]) for fila in datos):
            raise ErrorMatriz("Todas las filas deben tener la misma cantidad de elementos")
        self.datos = datos

    @classmethod
    def identidad(cls, n):
        """Devuelve la matriz identidad de orden n."""
        return cls([[1 if i == j else 0 for j in range(n)] for i in range(n)])

    @property
    def filas(self):
        """Cantidad de filas (m)."""
        return len(self.datos)

    @property
    def columnas(self):
        """Cantidad de columnas (n)."""
        return len(self.datos[0])

    @property
    def dimension(self):
        """Tupla (m, n)."""
        return (self.filas, self.columnas)

    def __eq__(self, otra):
        """Dos matrices son iguales si ambas son Matriz y tienen los mismos elementos."""
        return isinstance(otra, Matriz) and self.datos == otra.datos

    def __repr__(self):
        """Texto con las filas, útil al depurar."""
        return f"Matriz({[[str(v) for v in fila] for fila in self.datos]})"

    def _combinar(self, otra, funcion):
        """Aplica `funcion` a cada par de elementos en la misma posición."""
        resultado = []
        for i in range(self.filas):
            fila = []
            for j in range(self.columnas):
                fila.append(funcion(self.datos[i][j], otra.datos[i][j]))
            resultado.append(fila)
        return Matriz(resultado)

    def sumar(self, otra):
        """Devuelve A + B; ambas deben tener el mismo tamaño."""
        Validador.misma_dimension(self.dimension, otra.dimension, "sumar")
        return self._combinar(otra, operator.add)

    def restar(self, otra):
        """Devuelve A - B; ambas deben tener el mismo tamaño."""
        Validador.misma_dimension(self.dimension, otra.dimension, "restar")
        return self._combinar(otra, operator.sub)

    def por_escalar(self, k):
        """Devuelve k·A multiplicando cada elemento por k."""
        return Matriz([[k * valor for valor in fila] for fila in self.datos])

    def producto(self, otra):
        """Devuelve A·B (m×p). Requiere columnas de A == filas de B."""
        Validador.producto_posible(self.dimension, otra.dimension)
        resultado = []
        for i in range(self.filas):
            fila = []
            for j in range(otra.columnas):
                # Elemento (i, j) = fila i de A por columna j de B
                fila.append(sum(self.datos[i][k] * otra.datos[k][j] for k in range(self.columnas)))
            resultado.append(fila)
        return Matriz(resultado)

    def transpuesta(self):
        """Devuelve Aᵀ: las filas de A pasan a ser columnas."""
        return Matriz([[self.datos[i][j] for i in range(self.filas)] for j in range(self.columnas)])

    def por_vector(self, vector):
        """Devuelve A·v como lista; v debe tener tantos elementos como columnas tiene A."""
        if len(vector) != self.columnas:
            raise ErrorMatriz(
                f"No se puede multiplicar: Columnas de A [{self.columnas}] ≠ Elementos de v [{len(vector)}]")
        return [sum(a * x for a, x in zip(fila, vector)) for fila in self.datos]

    def menor(self, fila, columna):
        """Devuelve la submatriz que resulta de quitar una fila y una columna."""
        return Matriz([
            valores[:columna] + valores[columna + 1:]
            for i, valores in enumerate(self.datos) if i != fila
        ])

    def diagonal(self):
        """Devuelve una copia que conserva la diagonal y pone ceros en el resto."""
        return Matriz([[valor if i == j else 0 for j, valor in enumerate(fila)]
                       for i, fila in enumerate(self.datos)])

    def columnas_como_vectores(self):
        """Devuelve las columnas de A como lista de vectores (listas de Fractions)."""
        return [[fila[j] for fila in self.datos] for j in range(self.columnas)]

    def es_identidad(self):
        """Indica si la matriz es la identidad (exacto, gracias a Fraction)."""
        return self.es_cuadrada() and self == Matriz.identidad(self.filas)

    def es_cuadrada(self):
        """Indica si la matriz tiene tantas filas como columnas."""
        return self.filas == self.columnas

    def con_filas_intercambiadas(self, i, j):
        """Devuelve una copia con las filas i y j intercambiadas."""
        datos = [fila[:] for fila in self.datos]
        datos[i], datos[j] = datos[j], datos[i]
        return Matriz(datos)

    def con_fila_reemplazada(self, i, j, k):
        """Devuelve una copia con Fi → Fi + k·Fj."""
        datos = [fila[:] for fila in self.datos]
        datos[i] = [a + k * b for a, b in zip(datos[i], datos[j])]
        return Matriz(datos)

    def con_fila_escalada(self, i, k):
        """Devuelve una copia con Fi → k·Fi."""
        datos = [fila[:] for fila in self.datos]
        datos[i] = [k * valor for valor in datos[i]]
        return Matriz(datos)


@dataclass
class ReduccionTriangular:
    """Resultado de triangular una matriz: forma U, intercambios y determinante."""
    triangular: Matriz
    intercambios: int
    producto_diagonal: Fraction
    determinante: Fraction
    pasos: list = field(default_factory=list)


@dataclass
class ResultadoSarrus:
    """Productos de las diagonales de la regla de Sarrus y su resultado."""
    productos_positivos: list
    productos_negativos: list
    valor: Fraction


class Determinante:
    """Tres formas de calcular det(A): cofactores, Sarrus y reducción triangular."""

    # Los cofactores cuestan cerca de n! multiplicaciones: pasado este orden se vuelven inviables
    LIMITE_COFACTORES = 8

    @staticmethod
    def _exigir_orden_razonable(n):
        """Rechaza los órdenes donde la expansión por cofactores tardaría demasiado."""
        if n > Determinante.LIMITE_COFACTORES:
            raise ErrorMatriz(
                f"Cofactores no disponible para n = {n} (máximo {Determinante.LIMITE_COFACTORES}): "
                "requiere cerca de n! multiplicaciones. Use la reducción triangular.")

    @staticmethod
    def _expandir_primera_fila(filas):
        """Expansión recursiva por la primera fila, trabajando con listas simples."""
        if len(filas) == 1:
            return filas[0][0]
        total = Fraction(0)
        for j, elemento in enumerate(filas[0]):
            menor = [fila[:j] + fila[j + 1:] for fila in filas[1:]]
            # El signo (-1)**j sigue el patrón de cofactores: alterna según la posición de la columna
            total += (-1) ** j * elemento * Determinante._expandir_primera_fila(menor)
        return total

    @staticmethod
    def por_cofactores(matriz):
        """Devuelve det(A) por expansión de cofactores (cualquier orden n <= 8)."""
        Validador.cuadrada(matriz.dimension, "el determinante")
        Determinante._exigir_orden_razonable(matriz.filas)
        return Determinante._expandir_primera_fila(matriz.datos)

    @staticmethod
    def cofactor(matriz, i, j):
        """Devuelve C_ij = (-1)^(i+j) · det(menor_ij); en una 1×1 vale 1 por convención."""
        Validador.cuadrada(matriz.dimension, "el cofactor")
        if matriz.filas == 1:
            return Fraction(1)
        Determinante._exigir_orden_razonable(matriz.filas)
        menor = matriz.menor(i, j)
        return (-1) ** (i + j) * Determinante.por_cofactores(menor)

    @staticmethod
    def terminos_primera_fila(matriz):
        """Devuelve [(a_1j, C_1j), ...]: los términos de la expansión por la primera fila."""
        return [
            (matriz.datos[0][j], Determinante.cofactor(matriz, 0, j))
            for j in range(matriz.columnas)
        ]

    @staticmethod
    def por_sarrus(matriz):
        """Devuelve el cálculo de Sarrus; solo existe para matrices 3×3."""
        if matriz.dimension != (3, 3):
            raise ErrorMatriz("La regla de Sarrus solo se aplica a matrices 3×3")
        a = matriz.datos
        positivos, negativos = [], []
        for desplazamiento in range(3):
            # Las diagonales que bajan a la derecha suman; las que suben restan
            positivos.append(a[0][desplazamiento] * a[1][(1 + desplazamiento) % 3]
                             * a[2][(2 + desplazamiento) % 3])
            negativos.append(a[0][(2 + desplazamiento) % 3] * a[1][(1 + desplazamiento) % 3]
                             * a[2][desplazamiento])
        return ResultadoSarrus(positivos, negativos, sum(positivos) - sum(negativos))

    @staticmethod
    def por_reduccion(matriz):
        """Triangula A con intercambios y reemplazos de fila y devuelve el determinante.
        Los reemplazos no cambian det(A), así que no hay factores de escala que corregir."""
        Validador.cuadrada(matriz.dimension, "el determinante")
        filas = [fila[:] for fila in matriz.datos]
        n = len(filas)
        intercambios = 0
        pasos = [PasoReduccion("Matriz original", [fila[:] for fila in filas])]
        for columna in range(n):
            fila_pivote = next((i for i in range(columna, n) if filas[i][columna] != 0), None)
            if fila_pivote is None:
                continue  # Diagonal en 0: el producto, y por tanto det(A), será 0
            if fila_pivote != columna:
                filas[columna], filas[fila_pivote] = filas[fila_pivote], filas[columna]
                intercambios += 1  # Cada intercambio de filas cambia el signo del determinante
                pasos.append(PasoReduccion(f"Intercambio F{columna + 1} ↔ F{fila_pivote + 1}",
                                           [fila[:] for fila in filas], None, columna))
            Determinante._eliminar_debajo(filas, columna, pasos)
        producto = Fraction(1)
        for i in range(n):
            producto *= filas[i][i]
        return ReduccionTriangular(Matriz(filas), intercambios, producto,
                                   (-1) ** intercambios * producto, pasos)

    @staticmethod
    def _eliminar_debajo(filas, columna, pasos):
        """Hace ceros bajo el pivote con Fi → Fi - factor·F_pivote y registra cada paso."""
        for i in range(columna + 1, len(filas)):
            factor = filas[i][columna] / filas[columna][columna]
            if factor == 0:
                continue
            filas[i] = [a - factor * b for a, b in zip(filas[i], filas[columna])]
            operador = "−" if factor > 0 else "+"
            pasos.append(PasoReduccion(
                f"Hacer cero: F{i + 1} → F{i + 1} {operador} {abs(factor)}·F{columna + 1}",
                [fila[:] for fila in filas], (columna, columna), i))

    @staticmethod
    def calcular(matriz):
        """Devuelve det(A) con el método eficiente (reducción triangular)."""
        return Determinante.por_reduccion(matriz).determinante


@dataclass
class ResultadoGaussJordan:
    """Inversa (None si es singular), pivotes hallados y proceso sobre [A|I]."""
    inversa: object
    num_pivotes: int
    aumentada_final: list
    pasos: list


class InversaGaussJordan:
    """Inversa por reducción de [A | I] hasta [I | A⁻¹]."""

    @staticmethod
    def calcular(matriz):
        """Reduce [A|I]; si A no tiene n pivotes es singular y no se arma la inversa."""
        Validador.cuadrada(matriz.dimension, "la inversa")
        n = matriz.filas
        identidad = Matriz.identidad(n).datos
        aumentada = [fila_a + fila_i for fila_a, fila_i in zip(matriz.datos, identidad)]
        # Solo las columnas de A pueden ser pivote: las de I siempre tendrían pivote y falsearían el conteo
        reduccion = ReductorFilas(aumentada, n).reducir()
        num_pivotes = len(reduccion.columnas_pivote)
        inversa = None
        if num_pivotes == n:
            inversa = Matriz([fila[n:] for fila in reduccion.filas])
        return ResultadoGaussJordan(inversa, num_pivotes, reduccion.filas, reduccion.pasos)


@dataclass
class ResultadoAdjunta:
    """Datos de la inversa por adjunta; cofactores, adjunta e inversa son None si det = 0."""
    determinante: Fraction
    cofactores: object
    adjunta: object
    inversa: object


class InversaAdjunta:
    """Inversa con la fórmula A⁻¹ = (1/det(A)) · adj(A)."""

    @staticmethod
    def matriz_cofactores(matriz):
        """Devuelve la matriz cuyo elemento (i, j) es el cofactor C_ij."""
        n = matriz.filas
        return Matriz([[Determinante.cofactor(matriz, i, j) for j in range(n)] for i in range(n)])

    @staticmethod
    def calcular(matriz):
        """Calcula cofactores, adj(A) = cofactoresᵀ e inversa, solo si det(A) ≠ 0."""
        Validador.cuadrada(matriz.dimension, "la inversa")
        determinante = Determinante.calcular(matriz)
        if determinante == 0:
            return ResultadoAdjunta(determinante, None, None, None)
        cofactores = InversaAdjunta.matriz_cofactores(matriz)
        adjunta = cofactores.transpuesta()
        inversa = adjunta.por_escalar(Fraction(1) / determinante)
        return ResultadoAdjunta(determinante, cofactores, adjunta, inversa)


@dataclass
class ResultadoPropiedad:
    """Una igualdad comprobada: ambos miembros y si coinciden."""
    numero: int
    enunciado: str
    expresion_izquierda: str
    lado_izquierdo: object
    expresion_derecha: str
    lado_derecho: object
    se_cumple: bool
    auxiliares: list = field(default_factory=list)  # Pares (título, valor) de apoyo
    categoria: str = ""

    @property
    def diagnostico(self):
        """Devuelve el veredicto en texto: 'Se cumple' o 'No se cumple'."""
        return "Se cumple" if self.se_cumple else "No se cumple"


class VerificadorPropiedades:
    """Comprueba las propiedades de las Sesiones 10 y 11 reutilizando las clases anteriores."""

    def __init__(self, a, b, exigir_invertibles=True):
        """Exige A y B cuadradas del mismo orden; por defecto también invertibles."""
        Validador.misma_dimension(a.dimension, b.dimension, "verificar propiedades")
        for nombre, matriz in (("A", a), ("B", b)):
            Validador.cuadrada(matriz.dimension, "las propiedades de la inversa")
            if exigir_invertibles and Determinante.calcular(matriz) == 0:
                raise ErrorMatriz(f"La matriz {nombre} es singular (det = 0): no tiene inversa")
        self.a = a
        self.b = b

    @staticmethod
    def _inversa(matriz):
        """Inversa por Gauss-Jordan, la misma función de la opción 7 del menú."""
        return InversaGaussJordan.calcular(matriz).inversa

    def propiedad_1(self):
        """Comprueba (A⁻¹)⁻¹ = A y devuelve un ResultadoPropiedad."""
        izquierda = self._inversa(self._inversa(self.a))
        return ResultadoPropiedad(1, "(A⁻¹)⁻¹ = A", "(A⁻¹)⁻¹", izquierda, "A", self.a,
                                  izquierda == self.a)

    def propiedad_2(self):
        """Comprueba (AB)⁻¹ = B⁻¹A⁻¹ y devuelve un ResultadoPropiedad."""
        izquierda = self._inversa(self.a.producto(self.b))
        derecha = self._inversa(self.b).producto(self._inversa(self.a))
        return ResultadoPropiedad(2, "(AB)⁻¹ = B⁻¹A⁻¹", "(AB)⁻¹", izquierda, "B⁻¹A⁻¹", derecha,
                                  izquierda == derecha)

    def propiedad_3(self):
        """Comprueba (Aᵀ)⁻¹ = (A⁻¹)ᵀ y devuelve un ResultadoPropiedad."""
        izquierda = self._inversa(self.a.transpuesta())
        derecha = self._inversa(self.a).transpuesta()
        return ResultadoPropiedad(3, "(Aᵀ)⁻¹ = (A⁻¹)ᵀ", "(Aᵀ)⁻¹", izquierda, "(A⁻¹)ᵀ", derecha,
                                  izquierda == derecha)

    def propiedad_4(self):
        """Comprueba det(A⁻¹) = 1/det(A) y devuelve un ResultadoPropiedad."""
        izquierda = Determinante.calcular(self._inversa(self.a))
        derecha = Fraction(1) / Determinante.calcular(self.a)
        return ResultadoPropiedad(4, "det(A⁻¹) = 1/det(A)", "det(A⁻¹)", izquierda, "1/det(A)",
                                  derecha, izquierda == derecha)

    def propiedad_5(self, operacion, fila_i, fila_j, k):
        """Comprueba cómo una operación de fila cambia el determinante y devuelve el resultado.
        operacion: 'intercambio', 'reemplazo' (Fi → Fi + k·Fj) o 'escala' (Fi → k·Fi)."""
        self._validar_operacion_fila(operacion, fila_i, fila_j, k)
        determinante_a = Determinante.calcular(self.a)
        nueva, esperado, expresion, enunciado = self._operacion_y_efecto(
            operacion, fila_i, fila_j, k, determinante_a)
        izquierda = Determinante.calcular(nueva)
        auxiliares = [("A' (después de la operación)", nueva), ("det(A)", determinante_a)]
        return ResultadoPropiedad(5, f"Operación de fila: {enunciado}", "det(A')", izquierda, expresion, esperado,
                                  izquierda == esperado, auxiliares)

    def _validar_operacion_fila(self, operacion, i, j, k):
        """Rechaza filas fuera de rango, i = j (intercambio o reemplazo) y k = 0 (escala)."""
        n = self.a.filas
        if not 0 <= i < n or (operacion != "escala" and not 0 <= j < n):
            raise ErrorMatriz(f"Las filas deben estar entre 1 y {n}")
        if operacion != "escala" and i == j:
            raise ErrorMatriz("La fila j debe ser distinta de la fila i")
        if operacion == "escala" and k == 0:
            raise ErrorMatriz("k debe ser distinto de 0 al multiplicar una fila")

    def _operacion_y_efecto(self, operacion, i, j, k, determinante_a):
        """Devuelve (A', valor esperado de det(A'), su expresión, enunciado) para la operación."""
        if operacion == "intercambio":
            return (self.a.con_filas_intercambiadas(i, j), -determinante_a, "-det(A)",
                    f"F{i + 1} ↔ F{j + 1} da -det(A)")
        if operacion == "reemplazo":
            return (self.a.con_fila_reemplazada(i, j, k), determinante_a, "det(A)",
                    f"F{i + 1} → F{i + 1} + ({k})·F{j + 1} da det(A)")
        return (self.a.con_fila_escalada(i, k), k * determinante_a, f"({k})·det(A)",
                f"F{i + 1} → ({k})·F{i + 1} da k·det(A)")

    def propiedad_6(self):
        """Compara det(A) por cofactores con el de la forma triangular (corregido por el signo)."""
        reduccion = Determinante.por_reduccion(self.a)
        izquierda = Determinante.por_cofactores(self.a)
        auxiliares = [
            ("Forma triangular U", reduccion.triangular),
            ("Intercambios de fila", reduccion.intercambios),
            ("Producto de la diagonal de U", reduccion.producto_diagonal),
        ]
        return ResultadoPropiedad(
            6, "det(A) = (-1)^intercambios · producto de la diagonal de U",
            "det(A) por cofactores", izquierda, "det(A) por reducción triangular",
            reduccion.determinante, izquierda == reduccion.determinante, auxiliares)


class VerificadorCompleto:
    """Evalúa ambos miembros de cada propiedad del Programa 6 con las funciones del sistema."""

    def __init__(self, a, b, c, k):
        """Exige A, B y C cuadradas del mismo orden; k es el escalar de las propiedades con k."""
        for matriz in (a, b, c):
            Validador.cuadrada(matriz.dimension, "las propiedades")
        Validador.misma_dimension(a.dimension, b.dimension, "verificar propiedades")
        Validador.misma_dimension(a.dimension, c.dimension, "verificar propiedades")
        self.a, self.b, self.c, self.k = a, b, c, k
        self.base = VerificadorPropiedades(a, b, exigir_invertibles=False)
        self.omitidas = []

    @staticmethod
    def _igualdad(enunciado, expresion_izquierda, izquierda, expresion_derecha, derecha, auxiliares=None):
        """Crea el ResultadoPropiedad de una igualdad; número y categoría se asignan en evaluar."""
        return ResultadoPropiedad(0, enunciado, expresion_izquierda, izquierda, expresion_derecha,
                                  derecha, izquierda == derecha, auxiliares or [])

    def operaciones_y_transposicion(self):
        """Propiedades de la transpuesta y del producto: AB se calcula una sola vez."""
        a, b, c, k = self.a, self.b, self.c, self.k
        ab = a.producto(b)
        return [
            self._igualdad("(Aᵀ)ᵀ = A", "(Aᵀ)ᵀ", a.transpuesta().transpuesta(), "A", a),
            self._igualdad("(A + B)ᵀ = Aᵀ + Bᵀ", "(A + B)ᵀ", a.sumar(b).transpuesta(),
                           "Aᵀ + Bᵀ", a.transpuesta().sumar(b.transpuesta())),
            self._igualdad("(kA)ᵀ = k·Aᵀ", "(kA)ᵀ", a.por_escalar(k).transpuesta(),
                           "k·Aᵀ", a.transpuesta().por_escalar(k), [("k", k)]),
            self._igualdad("(AB)ᵀ = BᵀAᵀ", "(AB)ᵀ", ab.transpuesta(), "BᵀAᵀ",
                           b.transpuesta().producto(a.transpuesta()), [("AB", ab)]),
            self._igualdad("A(B + C) = AB + AC", "A(B + C)", a.producto(b.sumar(c)),
                           "AB + AC", ab.sumar(a.producto(c))),
            self._igualdad("(AB)C = A(BC)", "(AB)C", ab.producto(c), "A(BC)", a.producto(b.producto(c))),
        ]

    def inversas(self):
        """Propiedades de la inversa; se omiten con una nota si A o B son singulares."""
        if Determinante.calcular(self.a) == 0 or Determinante.calcular(self.b) == 0:
            self.omitidas.append("Propiedades de la inversa: A y B deben tener det(A) ≠ 0 y det(B) ≠ 0.")
            return []
        base = self.base
        return [base.propiedad_1(), base.propiedad_2(), base.propiedad_3(), self._a_por_inversa()]

    def _a_por_inversa(self):
        """Comprueba A·A⁻¹ = I y, de paso, A⁻¹·A = I."""
        inversa = InversaGaussJordan.calcular(self.a).inversa
        identidad = Matriz.identidad(self.a.filas)
        derecha_a_izquierda = inversa.producto(self.a)
        producto = self.a.producto(inversa)
        cumple = producto == identidad and derecha_a_izquierda == identidad
        return ResultadoPropiedad(0, "A · A⁻¹ = I", "A · A⁻¹", producto, "I", identidad, cumple,
                                  [("A⁻¹", inversa), ("A⁻¹ · A", derecha_a_izquierda)])

    def determinantes(self, operacion_fila):
        """Propiedades de det; operacion_fila = (operación, i, j, k) para el efecto de fila."""
        a, b, k = self.a, self.b, self.k
        det_a = Determinante.calcular(a)
        lista = [
            self._igualdad("det(Aᵀ) = det(A)", "det(Aᵀ)", Determinante.calcular(a.transpuesta()),
                           "det(A)", det_a),
            self._igualdad("det(AB) = det(A)·det(B)", "det(AB)", Determinante.calcular(a.producto(b)),
                           "det(A)·det(B)", det_a * Determinante.calcular(b)),
        ]
        lista += self._det_inversa(det_a)
        lista.append(self._igualdad(
            f"det(kA) = kⁿ·det(A), con n = {a.filas}", "det(kA)", Determinante.calcular(a.por_escalar(k)),
            "kⁿ·det(A)", k ** a.filas * det_a, [("k", k)]))
        return lista + [self.base.propiedad_5(*operacion_fila), self.base.propiedad_6()]

    def _det_inversa(self, det_a):
        """det(A⁻¹) = 1/det(A) solo existe si A es invertible; si no, se anota la omisión."""
        if det_a == 0:
            self.omitidas.append("det(A⁻¹) = 1/det(A): se omite porque det(A) = 0.")
            return []
        return [self.base.propiedad_4()]

    def evaluar(self, operacion_fila):
        """Devuelve todas las propiedades numeradas y con su categoría, en el orden del PDF."""
        grupos = (("Operaciones y transposición", self.operaciones_y_transposicion),
                  ("Matriz inversa", self.inversas),
                  ("Determinantes", lambda: self.determinantes(operacion_fila)))
        resultados = []
        for categoria, calcular in grupos:
            for propiedad in calcular():
                resultados.append(replace(propiedad, numero=len(resultados) + 1, categoria=categoria))
        return resultados


# ======================================================================
#  INTERFAZ: único lugar del módulo que usa print() e input()
# ======================================================================


class LectorMatrices:
    """Lee matrices desde el teclado: dimensiones y elementos fila por fila."""

    @staticmethod
    def pedir_dimension(nombre, cuadrada=False):
        """Pide m y n (o solo n si la matriz debe ser cuadrada) y devuelve (m, n)."""
        if cuadrada:
            n = Entrada.entero_positivo(f"  Orden n de {nombre} (matriz n × n): ")
            return (n, n)
        m = Entrada.entero_positivo(f"  Número de filas de {nombre} (m): ")
        n = Entrada.entero_positivo(f"  Número de columnas de {nombre} (n): ")
        return (m, n)

    @staticmethod
    def pedir_elementos(nombre, dimension):
        """Pide los elementos fila por fila y devuelve la Matriz."""
        filas, columnas = dimension
        Consola.info(f"Ingrese {nombre} fila por fila: {columnas} valores separados por espacio.")
        Consola.info("Acepta enteros, decimales y fracciones (ej. 3, 0.5, -1/2).")
        return Matriz([Entrada.fila(f"    {nombre} fila {i + 1}: ", columnas) for i in range(filas)])

    @classmethod
    def leer(cls, nombre, cuadrada=False):
        """Pide dimensiones y elementos de una matriz completa."""
        return cls.pedir_elementos(nombre, cls.pedir_dimension(nombre, cuadrada))


class MenuMatrices:
    """Menú del Módulo III: pide datos, llama a la lógica y muestra los resultados.
    Si recibe una memoria (AsistenteMemoria) permite reutilizar y guardar A y B."""

    OPCIONES = [
        ("1", "Suma"), ("2", "Resta"), ("3", "Multiplicación por escalar"),
        ("4", "Producto matricial"), ("5", "Transposición"), ("6", "Determinante"),
        ("7", "Inversa por Gauss-Jordan"), ("8", "Inversa por matriz adjunta"),
        ("9", "Verificador de propiedades (completo)"), ("0", "Ver Teoremas Clave del Módulo"),
    ]
    PASOS_COMPLETOS_HASTA_ORDEN = 3  # Con órdenes mayores solo se muestra inicio y fin

    def __init__(self, memoria=None):
        """Asocia cada tecla del menú con el método que la atiende."""
        self.memoria = memoria
        self.acciones = {
            "1": self._suma, "2": self._resta, "3": self._escalar, "4": self._producto,
            "5": self._transposicion, "6": self._determinante,
            "7": self._inversa_gauss_jordan, "8": self._inversa_adjunta,
            "9": self._verificador, "0": self._teoremas,
        }

    def ejecutar(self):
        """Muestra el logo y atiende el menú hasta que el usuario vuelve atrás."""
        Consola.limpiar()
        Consola.logo(LOGO_MODULO_3)
        while True:
            self._mostrar_menu()
            opcion = Entrada.opcion("\n  Seleccione una opción: ", list(self.acciones) + ["s"])
            if opcion == "s":
                return
            try:
                self.acciones[opcion]()
            except ErrorMatriz as error:
                Consola.error(str(error))
            Consola.pausar()

    def _mostrar_menu(self):
        """Dibuja las opciones del módulo."""
        Consola.encabezado("MÓDULO III · ÁLGEBRA DE MATRICES")
        for clave, texto in self.OPCIONES:
            Consola.opcion(clave, texto)
        Consola.opcion("S", "Volver al menú principal")

    # ---------- memoria y lectura ----------

    def _de_memoria(self, nombre, cuadrada=False):
        """Devuelve la matriz guardada en memoria si el usuario quiere usarla; si no, None."""
        if self.memoria is None:
            return None
        return self.memoria.ofrecer_usar(nombre, cuadrada)

    def _ofrecer_guardar(self, matriz):
        """Ofrece guardar un resultado en A o B para encadenar cálculos."""
        if self.memoria is not None:
            self.memoria.ofrecer_guardar(matriz)

    def _leer_matriz(self, nombre, cuadrada=False):
        """Obtiene una matriz de la memoria o del teclado."""
        return self._de_memoria(nombre, cuadrada) or LectorMatrices.leer(nombre, cuadrada)

    def _leer_dos_matrices(self, validar):
        """Obtiene A y B; `validar` revisa las dimensiones antes de pedir los elementos."""
        fuentes = [self._de_memoria(nombre) for nombre in ("A", "B")]
        dimensiones = [
            fuente.dimension if fuente else LectorMatrices.pedir_dimension(nombre)
            for fuente, nombre in zip(fuentes, ("A", "B"))
        ]
        validar(*dimensiones)  # Falla pronto: evita teclear matrices inútiles
        return tuple(
            fuente or LectorMatrices.pedir_elementos(nombre, dimension)
            for fuente, nombre, dimension in zip(fuentes, ("A", "B"), dimensiones)
        )

    # ---------- operaciones básicas ----------

    def _suma(self):
        """Opción 1: A + B."""
        self._sumar_o_restar("Suma A + B", "sumar", Matriz.sumar)

    def _resta(self):
        """Opción 2: A - B."""
        self._sumar_o_restar("Resta A - B", "restar", Matriz.restar)

    def _sumar_o_restar(self, titulo, verbo, operacion):
        """Flujo común de suma y resta: ambas exigen el mismo tamaño."""
        Consola.seccion(titulo)
        a, b = self._leer_dos_matrices(lambda da, db: Validador.misma_dimension(da, db, verbo))
        Consola.matriz(a.datos, "Matriz A")
        Consola.matriz(b.datos, "Matriz B")
        resultado = operacion(a, b)
        Consola.matriz(resultado.datos, f"Resultado ({titulo})")
        self._ofrecer_guardar(resultado)

    def _escalar(self):
        """Opción 3: k·A."""
        Consola.seccion("Multiplicación por escalar k·A")
        a = self._leer_matriz("A")
        k = Entrada.fraccion("  Escalar k: ")
        Consola.matriz(a.datos, "Matriz A")
        resultado = a.por_escalar(k)
        Consola.matriz(resultado.datos, f"Resultado ({k})·A")
        self._ofrecer_guardar(resultado)

    def _producto(self):
        """Opción 4: A·B, con aviso si el producto no conmuta."""
        Consola.seccion("Producto matricial A·B")
        a, b = self._leer_dos_matrices(Validador.producto_posible)
        Consola.matriz(a.datos, "Matriz A")
        Consola.matriz(b.datos, "Matriz B")
        producto = a.producto(b)
        Consola.matriz(producto.datos, "Resultado A·B")
        self._comparar_con_producto_inverso(a, b, producto)
        self._ofrecer_guardar(producto)

    @staticmethod
    def _comparar_con_producto_inverso(a, b, producto):
        """Si B·A existe, lo muestra: el producto no es conmutativo en general."""
        if b.columnas != a.filas:
            return
        inverso = b.producto(a)
        Consola.matriz(inverso.datos, "Además, B·A también existe")
        if inverso == producto:
            Consola.aviso("En este caso AB = BA, pero no ocurre en general.")
        else:
            Consola.aviso("AB ≠ BA: el producto de matrices no es conmutativo.")

    def _transposicion(self):
        """Opción 5: Aᵀ."""
        Consola.seccion("Transposición Aᵀ")
        a = self._leer_matriz("A")
        Consola.matriz(a.datos, "Matriz A")
        resultado = a.transpuesta()
        Consola.matriz(resultado.datos, "Resultado Aᵀ")
        self._ofrecer_guardar(resultado)

    # ---------- determinante ----------

    def _determinante(self):
        """Opción 6: pide A y muestra det(A) por los tres métodos."""
        Consola.seccion("Determinante")
        self.mostrar_determinante(self._leer_matriz("A", cuadrada=True))

    def mostrar_determinante(self, a):
        """Muestra det(A) por cofactores, Sarrus (3×3) y reducción triangular."""
        Validador.cuadrada(a.dimension, "el determinante")
        Consola.matriz(a.datos, "Matriz A")
        valores = [self._mostrar_cofactores(a), self._mostrar_sarrus(a), self._mostrar_reduccion(a)]
        calculados = [valor for valor in valores if valor is not None]
        Consola.seccion("Comparación de métodos")
        if len(set(calculados)) == 1:
            Consola.exito(f"Los {len(calculados)} métodos coinciden: det(A) = {calculados[0]}")
        else:
            Consola.error(f"Los métodos NO coinciden: {calculados}")
        self._diagnostico(Determinante.calcular(a), a.filas)

    @staticmethod
    def _mostrar_cofactores(a):
        """Muestra la expansión por la primera fila; devuelve det(A) o None si n es muy grande."""
        Consola.seccion("Método 1: expansión por cofactores (primera fila)")
        try:
            terminos = Determinante.terminos_primera_fila(a)
        except ErrorMatriz as error:
            Consola.aviso(str(error))
            return None
        suma = " + ".join(f"({elemento})·({cofactor})" for elemento, cofactor in terminos)
        valor = sum(elemento * cofactor for elemento, cofactor in terminos)
        print(f"  det(A) = {suma}\n  det(A) = {valor}")
        return valor

    @staticmethod
    def _mostrar_sarrus(a):
        """Muestra Sarrus si A es 3×3; devuelve det(A) o None."""
        if a.dimension != (3, 3):
            return None
        Consola.seccion("Método 2: regla de Sarrus (solo 3×3)")
        sarrus = Determinante.por_sarrus(a)
        positivos = " + ".join(str(p) for p in sarrus.productos_positivos)
        negativos = " + ".join(str(p) for p in sarrus.productos_negativos)
        print(f"  Diagonales que suman:  {positivos}")
        print(f"  Diagonales que restan: {negativos}")
        print(f"  det(A) = ({sum(sarrus.productos_positivos)}) - ({sum(sarrus.productos_negativos)}) = {sarrus.valor}")
        return sarrus.valor

    @staticmethod
    def _mostrar_reduccion(a):
        """Muestra la reducción triangular y devuelve det(A)."""
        Consola.seccion("Método 3: reducción a forma triangular")
        reduccion = Determinante.por_reduccion(a)
        Consola.matriz(reduccion.triangular.datos, "Forma triangular U")
        print(f"\n  Intercambios de fila: {reduccion.intercambios} → signo (-1)^{reduccion.intercambios}")
        print(f"  Producto de la diagonal: {reduccion.producto_diagonal}")
        print(f"  det(A) = {reduccion.determinante}")
        return reduccion.determinante

    @staticmethod
    def _diagnostico(determinante, n):
        """Imprime si la matriz es invertible o singular según det(A)."""
        Consola.seccion("Diagnóstico")
        if determinante != 0:
            Consola.exito(f"La matriz es invertible: det(A) ≠ 0, tiene {n} posiciones pivote, "
                          "sus columnas son L.I. y generan ℝⁿ")
        else:
            Consola.error("La matriz es singular (no tiene inversa): det(A) = 0")

    # ---------- inversas ----------

    def _inversa_gauss_jordan(self):
        """Opción 7: pide A y calcula A⁻¹ reduciendo [A | I]."""
        Consola.seccion("Inversa por Gauss-Jordan")
        self.mostrar_inversa_gauss_jordan(self._leer_matriz("A", cuadrada=True))

    def mostrar_inversa_gauss_jordan(self, a, guardar=True):
        """Muestra el proceso [A|I] → [I|A⁻¹], la comprobación y el diagnóstico."""
        Validador.cuadrada(a.dimension, "la inversa")
        Consola.matriz(a.datos, "Matriz A")
        print(f"\n  det(A) = {Determinante.calcular(a)}")
        resultado = InversaGaussJordan.calcular(a)
        n = a.filas
        self._mostrar_proceso(resultado.pasos, n)
        if resultado.inversa is None:
            Consola.aviso(f"Posiciones pivote: {resultado.num_pivotes} de {n}. Se detiene: no hay inversa.")
            self._diagnostico(Fraction(0), n)
            return
        Consola.matriz(resultado.aumentada_final, "Proceso final [I | A⁻¹]", columna_separadora=n)
        Consola.matriz(resultado.inversa.datos, "Inversa A⁻¹")
        self._comprobar_inversa(a, resultado.inversa)
        self._diagnostico(Determinante.calcular(a), n)
        if guardar:
            self._ofrecer_guardar(resultado.inversa)

    def _mostrar_proceso(self, pasos, orden):
        """Imprime los pasos de [A|I]: todos si n es chico, si no solo el inicio."""
        mostrar = pasos if orden <= self.PASOS_COMPLETOS_HASTA_ORDEN else pasos[:1]
        for numero, paso in enumerate(mostrar):
            Consola.matriz(paso.filas, f"Paso {numero}: {paso.descripcion}", columna_separadora=orden)
        if len(mostrar) < len(pasos):
            Consola.info(f"(Se omiten {len(pasos) - 1} pasos; n > {self.PASOS_COMPLETOS_HASTA_ORDEN}.)")

    @staticmethod
    def _comprobar_inversa(a, inversa):
        """Verifica A·A⁻¹ = I y A⁻¹·A = I usando el producto propio de Matriz."""
        for nombre, producto in (("A · A⁻¹", a.producto(inversa)), ("A⁻¹ · A", inversa.producto(a))):
            Consola.matriz(producto.datos, f"Comprobación {nombre}")
            if producto.es_identidad():
                Consola.exito(f"{nombre} = I (exacto, con fracciones)")
            else:
                Consola.error(f"{nombre} ≠ I: revise el cálculo")

    def _inversa_adjunta(self):
        """Opción 8: pide A y calcula A⁻¹ = (1/det(A)) · adj(A)."""
        Consola.seccion("Inversa por matriz adjunta")
        self.mostrar_inversa_adjunta(self._leer_matriz("A", cuadrada=True))

    def mostrar_inversa_adjunta(self, a, guardar=True):
        """Muestra cofactores, adj(A), la inversa y su comparación con Gauss-Jordan."""
        Validador.cuadrada(a.dimension, "la inversa")
        Consola.matriz(a.datos, "Matriz A")
        resultado = InversaAdjunta.calcular(a)
        print(f"\n  det(A) = {resultado.determinante}")
        if resultado.inversa is None:
            self._diagnostico(resultado.determinante, a.filas)
            return
        Consola.matriz(resultado.cofactores.datos, "Matriz de cofactores")
        Consola.matriz(resultado.adjunta.datos, "adj(A) = (cofactores)ᵀ")
        Consola.matriz(resultado.inversa.datos, f"A⁻¹ = 1/({resultado.determinante}) · adj(A)")
        self._comprobar_inversa(a, resultado.inversa)
        self._comparar_con_gauss_jordan(a, resultado.inversa)
        self._diagnostico(resultado.determinante, a.filas)
        if guardar:
            self._ofrecer_guardar(resultado.inversa)

    @staticmethod
    def _comparar_con_gauss_jordan(a, inversa_adjunta):
        """Ambos métodos deben producir la misma inversa."""
        if InversaGaussJordan.calcular(a).inversa == inversa_adjunta:
            Consola.exito("Coincide con la inversa obtenida por Gauss-Jordan")
        else:
            Consola.error("No coincide con la inversa de Gauss-Jordan")

    # ---------- verificador y teoremas ----------

    def _verificador(self):
        """Opción 9: evalúa todas las propiedades con A, B y C cuadradas del mismo orden."""
        Consola.seccion("Verificador de propiedades (A, B y C cuadradas del mismo orden)")
        a, b = self._de_memoria("A", True), self._de_memoria("B", True)
        if a is None and b is None:
            orden = Entrada.entero_positivo(
                f"  Orden n (máximo {Determinante.LIMITE_COFACTORES}, por la propiedad de triangulares): ",
                Determinante.LIMITE_COFACTORES)
        else:
            orden = (a or b).filas
        a = a or LectorMatrices.pedir_elementos("A", (orden, orden))
        b = b or LectorMatrices.pedir_elementos("B", (orden, orden))
        c = LectorMatrices.pedir_elementos("C", (orden, orden))
        k = Entrada.fraccion("  Escalar k: ")
        verificador = VerificadorCompleto(a, b, c, k)
        self._mostrar_propiedades(verificador, (a, b, c), self._pedir_operacion_fila(orden))

    @staticmethod
    def _mostrar_propiedades(verificador, matrices, operacion_fila):
        """Imprime A, B, C y cada propiedad agrupada por categoría, con su diagnóstico."""
        for nombre, matriz in zip("ABC", matrices):
            Consola.matriz(matriz.datos, f"Matriz {nombre}")
        categoria = None
        for propiedad in verificador.evaluar(operacion_fila):
            if propiedad.categoria != categoria:
                categoria = propiedad.categoria
                Consola.encabezado(categoria.upper(), Estilo.MAGENTA)
            Consola.propiedad(propiedad)
        for nota in verificador.omitidas:
            Consola.aviso(nota)

    @staticmethod
    def _pedir_operacion_fila(n):
        """Pide la operación de fila, las filas y k; devuelve (operación, i, j, k)."""
        Consola.seccion("Efecto de una operación de fila sobre det(A): elija la operación")
        Consola.opcion("1", "Intercambio Fi ↔ Fj")
        Consola.opcion("2", "Reemplazo Fi → Fi + k·Fj")
        Consola.opcion("3", "Multiplicar una fila por k")
        eleccion = Entrada.opcion("  Operación: ", ["1", "2", "3"])
        operacion = {"1": "intercambio", "2": "reemplazo", "3": "escala"}[eleccion]
        i = Entrada.entero_positivo("  Fila i: ", n) - 1
        j, k = i, None
        if operacion != "escala":
            j = MenuMatrices._pedir_fila_distinta(i, n)
        if operacion != "intercambio":
            k = MenuMatrices._pedir_k(distinto_de_cero=(operacion == "escala"))
        return operacion, i, j, k

    @staticmethod
    def _pedir_fila_distinta(i, n):
        """Pide una fila j distinta de i (con j = i el reemplazo o intercambio no tiene sentido)."""
        while True:
            j = Entrada.entero_positivo("  Fila j: ", n) - 1
            if j != i:
                return j
            Consola.error("La fila j debe ser distinta de la fila i.")

    @staticmethod
    def _pedir_k(distinto_de_cero):
        """Pide k; al escalar una fila, k = 0 no es una operación de fila válida."""
        while True:
            k = Entrada.fraccion("  Valor de k: ")
            if k != 0 or not distinto_de_cero:
                return k
            Consola.error("k debe ser distinto de 0 al multiplicar una fila.")

    @staticmethod
    def _teoremas():
        """Opción 0: muestra los teoremas clave del módulo."""
        Consola.encabezado("TEOREMAS CLAVE · MÓDULO III", Estilo.MAGENTA)
        for titulo, lineas in TEOREMAS_MODULO_3:
            Consola.seccion(titulo)
            for linea in lineas:
                print(f"  {linea}")
