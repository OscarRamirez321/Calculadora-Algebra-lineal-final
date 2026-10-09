"""Sesiones 2, 7 y 8: sistemas de ecuaciones lineales Ax = b.
Clasifica el sistema (homogéneo o no, compatible o no), da la solución única o la
forma paramétrica y sigue el proceso de Gauss-Jordan sobre [A | b].
Elaborado por: [Integrantes del grupo: completar nombres].
"""
from dataclasses import dataclass
from fractions import Fraction

from .interfaz import Consola, Entrada
from .modulo_matrices import ErrorMatriz, Matriz
from .reduccion import ReductorFilas


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

    @classmethod
    def desde_matriz(cls, coeficientes, terminos_independientes):
        """Arma [A | b] a partir de una Matriz A y la lista de términos b."""
        if coeficientes.filas != len(terminos_independientes):
            raise ErrorMatriz(
                f"A tiene {coeficientes.filas} filas y b tiene {len(terminos_independientes)} términos")
        return cls([fila + [b] for fila, b in zip(coeficientes.datos, terminos_independientes)])

    def es_homogeneo(self):
        """Indica si todos los términos independientes son cero (Ax = 0)."""
        return all(fila[-1] == 0 for fila in self.aumentada)

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

    def forma_parametrica(self, reduccion, diagnostico):
        """Devuelve {variable: (constante, {libre: coeficiente})} de un sistema indeterminado.
        De la fila de un pivote x_p = b - Σ a_pj·x_j, por eso los coeficientes cambian de signo."""
        n = self.num_variables
        expresiones = {}
        for fila, columna in zip(reduccion.filas, reduccion.columnas_pivote):
            coeficientes = {j: -fila[j] for j in diagnostico.variables_libres if fila[j] != 0}
            expresiones[columna] = (fila[n], coeficientes)
        for j in diagnostico.variables_libres:
            expresiones[j] = (Fraction(0), {j: Fraction(1)})
        return dict(sorted(expresiones.items()))


class MenuSistemas:
    """Menú de las Sesiones 2, 7 y 8: resolver sistemas con A de la memoria o nuevos."""

    def __init__(self, asistente):
        """Recibe el AsistenteMemoria con el que lee y guarda matrices."""
        self.memoria = asistente

    def ejecutar(self):
        """Muestra el menú y resuelve el sistema elegido."""
        Consola.limpiar()
        Consola.encabezado("SESIONES 2, 7 Y 8 · SISTEMAS DE ECUACIONES LINEALES")
        Consola.opcion("1", "Resolver Ax = b (usa la Matriz A de la memoria como coeficientes)")
        Consola.opcion("2", "Ingresar un sistema nuevo completo [A | b]")
        Consola.opcion("0", "Regresar al menú principal")
        opcion = Entrada.opcion("\n  Seleccione la operación: ", ["1", "2", "0"])
        if opcion == "0":
            return
        try:
            sistema = self._sistema_de_memoria() if opcion == "1" else self._sistema_nuevo()
            self._resolver(sistema)
        except ErrorMatriz as error:
            Consola.error(str(error))
        Consola.pausar()

    def _sistema_de_memoria(self):
        """Toma A de la memoria y pide el vector b."""
        a = self.memoria.requerir("A")
        Consola.matriz(a.datos, "Matriz de coeficientes (A)")
        b = Entrada.fila(f"  Vector b ({a.filas} términos independientes): ", a.filas)
        return SistemaLineal.desde_matriz(a, b)

    @staticmethod
    def _sistema_nuevo():
        """Pide m, n y cada ecuación completa (coeficientes y b)."""
        m = Entrada.entero_positivo("  Número de ecuaciones (m): ")
        n = Entrada.entero_positivo("  Número de variables (n): ")
        Consola.info(f"Escriba cada ecuación: {n} coeficientes y luego el término independiente b.")
        return SistemaLineal([Entrada.fila(f"    Ecuación {i + 1}: ", n + 1) for i in range(m)])

    def _resolver(self, sistema):
        """Clasifica, reduce, muestra el proceso y la solución del sistema."""
        tipo = "HOMOGÉNEO (Ax = 0): siempre admite la solución trivial" if sistema.es_homogeneo() \
            else "NO HOMOGÉNEO (Ax = b)"
        Consola.seccion("Clasificación del sistema")
        print(f"  Tipo: SISTEMA {tipo}")
        reduccion = sistema.reducir()
        self._mostrar_proceso(reduccion, sistema.num_variables)
        diagnostico = sistema.diagnosticar(reduccion)
        Consola.seccion("Resultado")
        self._mostrar_diagnostico(sistema, reduccion, diagnostico)

    @staticmethod
    def _mostrar_proceso(reduccion, num_variables):
        """Muestra la matriz aumentada original y su forma reducida [A | b]."""
        Consola.matriz(reduccion.pasos[0].filas, "Matriz aumentada [A | b]", num_variables)
        Consola.matriz(reduccion.filas, "Forma reducida RREF [A | b]", num_variables)
        if Entrada.si_no("  ¿Ver el paso a paso?"):
            for numero, paso in enumerate(reduccion.pasos[1:], start=1):
                Consola.matriz(paso.filas, f"Paso {numero}: {paso.descripcion}", num_variables)

    def _mostrar_diagnostico(self, sistema, reduccion, diagnostico):
        """Imprime el veredicto y la solución (única o paramétrica)."""
        if diagnostico.tipo == "incompatible":
            Consola.error("SISTEMA INCOMPATIBLE: no tiene solución (aparece una fila 0 = c con c ≠ 0).")
        elif diagnostico.tipo == "indeterminado":
            nombres = ", ".join(f"x{j + 1}" for j in diagnostico.variables_libres)
            Consola.aviso(f"SISTEMA COMPATIBLE INDETERMINADO: infinitas soluciones. Variables libres: {nombres}")
            for variable, (constante, coeficientes) in sistema.forma_parametrica(reduccion, diagnostico).items():
                print(f"  x{variable + 1} = {self._expresion(constante, coeficientes)}")
        else:
            Consola.exito("SISTEMA COMPATIBLE DETERMINADO: solución única.")
            for columna, valor in diagnostico.solucion.items():
                print(f"  x{columna + 1} = {valor}")
            self.memoria.ofrecer_guardar(
                Matriz([[valor] for valor in diagnostico.solucion.values()]), "el vector solución")

    @staticmethod
    def _expresion(constante, coeficientes):
        """Escribe 'c + a·x2 − b·x3' (los parámetros se llaman como la variable libre)."""
        partes = [str(constante)] if constante != 0 or not coeficientes else []
        for libre, coeficiente in coeficientes.items():
            signo = "-" if coeficiente < 0 else "+"
            termino = f"{abs(coeficiente)}·x{libre + 1}" if abs(coeficiente) != 1 else f"x{libre + 1}"
            partes.append(f"{signo} {termino}" if partes else (f"-{termino}" if signo == "-" else termino))
        return " ".join(partes)
