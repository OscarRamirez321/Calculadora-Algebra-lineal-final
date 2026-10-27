"""Sesiones 1 y 9: operaciones básicas y propiedades de matrices.
Suma, resta, producto, transpuesta, escalar y diagonal sobre las matrices en memoria,
con la demostración en vivo de (AB)ᵀ = BᵀAᵀ.
Elaborado por: [Integrantes del grupo: completar nombres].
"""
from .interfaz import Consola, Entrada
from .modulo_matrices import ErrorMatriz


class MenuOperaciones:
    """Menú de la Sesión 1 y 9; trabaja con las matrices A y B de la memoria."""

    def __init__(self, asistente):
        """Recibe el AsistenteMemoria con el que lee y guarda matrices."""
        self.memoria = asistente
        self.acciones = {
            "1": self._sumar, "2": self._restar, "3": self._producto,
            "4": self._transpuesta, "5": self._escalar, "6": self._diagonal,
        }

    def ejecutar(self):
        """Muestra el menú de la sesión y ejecuta una operación."""
        Consola.limpiar()
        Consola.encabezado("SESIÓN 1 Y 9 · OPERACIONES BÁSICAS Y PROPIEDADES")
        Consola.opcion("1", "Sumar (A + B)")
        Consola.opcion("2", "Restar (A - B) o (B - A)")
        Consola.opcion("3", "Multiplicar matrices (A · B) + demostración de teorema")
        Consola.opcion("4", "Transpuesta (Aᵀ o Bᵀ)")
        Consola.opcion("5", "Multiplicar por un escalar (c·A o c·B)")
        Consola.opcion("6", "Matriz diagonal")
        Consola.opcion("0", "Regresar al menú principal")
        opcion = Entrada.opcion("\n  Seleccione la operación: ", list(self.acciones) + ["0"])
        if opcion == "0":
            return
        try:
            resultado = self.acciones[opcion]()
            self.memoria.ofrecer_guardar(resultado)
        except ErrorMatriz as error:
            Consola.error(str(error))
        Consola.pausar()

    def _sumar(self):
        """Suma A + B de la memoria."""
        a, b = self.memoria.requerir("A"), self.memoria.requerir("B")
        resultado = a.sumar(b)
        Consola.matriz(resultado.datos, "Resultado A + B")
        return resultado

    def _restar(self):
        """Resta A - B o B - A según elija el usuario."""
        a, b = self.memoria.requerir("A"), self.memoria.requerir("B")
        if Entrada.opcion("  ¿Qué restar? (1) A - B  (2) B - A: ", ["1", "2"]) == "1":
            resultado = a.restar(b)
            Consola.matriz(resultado.datos, "Resultado A - B")
        else:
            resultado = b.restar(a)
            Consola.matriz(resultado.datos, "Resultado B - A")
        return resultado

    def _producto(self):
        """Multiplica A·B y demuestra (AB)ᵀ = BᵀAᵀ con las mismas matrices."""
        a, b = self.memoria.requerir("A"), self.memoria.requerir("B")
        producto = a.producto(b)
        Consola.matriz(producto.datos, "Resultado A · B")
        Consola.encabezado("VERIFICACIÓN AUTOMÁTICA · SESIÓN 9")
        print("  Propiedad de la transpuesta en el producto: (A·B)ᵀ = Bᵀ · Aᵀ")
        izquierda = producto.transpuesta()
        derecha = b.transpuesta().producto(a.transpuesta())
        Consola.matriz(izquierda.datos, "(A · B)ᵀ")
        Consola.matriz(derecha.datos, "Bᵀ · Aᵀ")
        if izquierda == derecha:
            Consola.exito("Ambas matrices son idénticas. Propiedad demostrada.")
        else:
            Consola.error("Las matrices no coinciden.")
        return producto

    def _transpuesta(self):
        """Transpone la matriz elegida."""
        letra = self.memoria.pedir_letra()
        resultado = self.memoria.requerir(letra).transpuesta()
        Consola.matriz(resultado.datos, f"Transpuesta {letra}ᵀ")
        return resultado

    def _escalar(self):
        """Multiplica la matriz elegida por un escalar."""
        letra = self.memoria.pedir_letra()
        matriz = self.memoria.requerir(letra)
        c = Entrada.fraccion("  Valor del escalar (ej. 2 o -1/3): ")
        resultado = matriz.por_escalar(c)
        Consola.matriz(resultado.datos, f"Escalar ({c})·{letra}")
        return resultado

    def _diagonal(self):
        """Extrae la diagonal de la matriz elegida."""
        letra = self.memoria.pedir_letra()
        resultado = self.memoria.requerir(letra).diagonal()
        Consola.matriz(resultado.datos, f"Diagonal de {letra}")
        return resultado
