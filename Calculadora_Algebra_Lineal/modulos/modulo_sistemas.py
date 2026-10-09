"""Módulo I de la Calculadora: sistemas de ecuaciones lineales.
Resuelve Ax = b por Gauss-Jordan, verifica combinaciones lineales y decide si un
conjunto de vectores es linealmente independiente (L.I.) o dependiente (L.D.).
Elaborado por: [Integrantes del grupo: completar nombres].
"""
from dataclasses import dataclass
from fractions import Fraction

from teoremas.teoremas_vectores import CRITERIO_INDEPENDENCIA
from .interfaz import Consola, Entrada
from .reduccion import ReductorFilas

LOGO_MODULO_1 = r"""
  #   #  ###  ####  #   # #      ###      #####
  ## ## #   # #   # #   # #     #   #       #
  # # # #   # #   # #   # #     #   #       #
  #   # #   # #   # #   # #     #   #       #
  #   #  ###  ####   ###  #####  ###      #####
  ---------  S I S T E M A S   L I N E A L E S  ---------
"""


@dataclass
class DiagnosticoSistema:
    """Clasificación de un sistema: tipo, variables libres y solución única."""
    tipo: str  # "incompatible", "determinado" o "indeterminado"
    variables_libres: list
    solucion: dict  # índice de variable -> valor (solo si es determinado)


class SistemaLineal:
    """Sistema Ax = b representado por su matriz aumentada [A | b]."""

    def __init__(self, aumentada):
        """Recibe las filas de [A | b]; la última columna es b."""
        self.aumentada = aumentada
        self.num_variables = len(aumentada[0]) - 1

    def reducir(self):
        """Lleva [A | b] a forma escalonada reducida y devuelve un ResultadoReduccion."""
        # b no puede ser columna pivote: un pivote ahí significaría 0 = 1 (sin solución)
        return ReductorFilas(self.aumentada, self.num_variables).reducir()

    def diagnosticar(self, reduccion):
        """Clasifica el sistema ya reducido y devuelve un DiagnosticoSistema."""
        n = self.num_variables
        if self._tiene_fila_imposible(reduccion.filas):
            return DiagnosticoSistema("incompatible", [], {})
        pivotes = reduccion.columnas_pivote
        libres = [j for j in range(n) if j not in pivotes]
        if libres:
            return DiagnosticoSistema("indeterminado", libres, {})
        solucion = {columna: reduccion.filas[i][n] for i, columna in enumerate(pivotes)}
        return DiagnosticoSistema("determinado", [], solucion)

    def _tiene_fila_imposible(self, filas):
        """Detecta filas del tipo [0 ... 0 | c] con c ≠ 0, que equivalen a 0 = c."""
        n = self.num_variables
        return any(all(fila[j] == 0 for j in range(n)) and fila[n] != 0 for fila in filas)


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


class MenuSistemas:
    """Menú del Módulo I: lee los datos, llama a la lógica y muestra resultados."""

    def ejecutar(self):
        """Muestra el logo y atiende el menú hasta que el usuario vuelve atrás."""
        Consola.logo(LOGO_MODULO_1)
        acciones = {"1": self._resolver, "2": self._combinacion, "3": self._independencia}
        while True:
            Consola.encabezado("MÓDULO I · SISTEMAS LINEALES")
            Consola.opcion("1", "Resolver sistema Ax = b")
            Consola.opcion("2", "Verificar combinación lineal")
            Consola.opcion("3", "Evaluar independencia lineal (L.I. / L.D.)")
            Consola.opcion("S", "Volver al menú principal")
            opcion = Entrada.opcion("\n  Seleccione una opción: ", list(acciones) + ["s"])
            if opcion == "s":
                return
            acciones[opcion]()
            Consola.pausar()

    @staticmethod
    def _leer_sistema():
        """Pide m, n y los coeficientes; devuelve el SistemaLineal."""
        m = Entrada.entero_positivo("  Número de ecuaciones (m): ")
        n = Entrada.entero_positivo("  Número de variables (n): ")
        Consola.info(f"Escriba cada ecuación: {n} coeficientes y luego el término independiente b.")
        filas = [Entrada.fila(f"    Ecuación {i + 1}: ", n + 1) for i in range(m)]
        return SistemaLineal(filas)

    @staticmethod
    def _mostrar_proceso(reduccion, num_variables):
        """Imprime cada paso de la reducción sobre la matriz aumentada."""
        for paso in reduccion.pasos:
            Consola.matriz(paso.filas, paso.descripcion, columna_separadora=num_variables)

    def _resolver(self):
        """Opción 1: resuelve Ax = b y clasifica el sistema."""
        Consola.seccion("Resolver sistema Ax = b")
        sistema = self._leer_sistema()
        reduccion = sistema.reducir()
        self._mostrar_proceso(reduccion, sistema.num_variables)
        diagnostico = sistema.diagnosticar(reduccion)
        Consola.seccion("Resultado")
        if diagnostico.tipo == "incompatible":
            Consola.error("SISTEMA INCOMPATIBLE (sin solución)")
        elif diagnostico.tipo == "indeterminado":
            nombres = [f"x{j + 1}" for j in diagnostico.variables_libres]
            Consola.aviso("SISTEMA COMPATIBLE INDETERMINADO (infinitas soluciones)")
            print(f"  Variables libres: {nombres}")
        else:
            Consola.exito("SISTEMA COMPATIBLE DETERMINADO (solución única)")
            for columna, valor in diagnostico.solucion.items():
                print(f"  x{columna + 1} = {valor}")

    def _combinacion(self):
        """Opción 2: indica si b es combinación lineal de las columnas de A."""
        Consola.seccion("Combinación lineal: ¿b = c1·v1 + ... + cn·vn?")
        Consola.info("Las columnas de A son los vectores v1, ..., vn.")
        sistema = self._leer_sistema()
        reduccion = sistema.reducir()
        diagnostico = sistema.diagnosticar(reduccion)
        Consola.seccion("Resultado")
        if diagnostico.tipo == "incompatible":
            Consola.error("b NO es combinación lineal de los vectores dados")
        elif diagnostico.tipo == "indeterminado":
            Consola.exito("b SÍ es combinación lineal, de infinitas maneras")
        else:
            Consola.exito("b SÍ es combinación lineal, de una única manera:")
            for columna, valor in diagnostico.solucion.items():
                print(f"  c{columna + 1} = {valor}")

    def _independencia(self):
        """Opción 3: evalúa si un conjunto de vectores es L.I. o L.D."""
        Consola.seccion("Independencia lineal")
        for linea in CRITERIO_INDEPENDENCIA:
            Consola.info(linea)
        k = Entrada.entero_positivo("  Cantidad de vectores (k): ")
        n = Entrada.entero_positivo("  Dimensión de los vectores (n): ")
        vectores = [Entrada.fila(f"    v{i + 1} ({n} componentes): ", n) for i in range(k)]
        reduccion, es_independiente = IndependenciaLineal(vectores).analizar()
        Consola.matriz(reduccion.filas, "Forma reducida del sistema homogéneo", columna_separadora=k)
        print(f"\n  Pivotes: {len(reduccion.columnas_pivote)} | Variables libres: {k - len(reduccion.columnas_pivote)}")
        if es_independiente:
            Consola.exito("LINEALMENTE INDEPENDIENTES (L.I.): solo existe la solución trivial")
        else:
            Consola.error("LINEALMENTE DEPENDIENTES (L.D.): hay variables libres")
