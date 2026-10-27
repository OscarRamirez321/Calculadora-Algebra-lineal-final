import sys

from modulos.interfaz import Consola, Entrada, Estilo
from modulos.memoria import AsistenteMemoria, MemoriaMatrices
from modulos.modulo_lu import MenuLU
from modulos.modulo_matrices import MenuMatrices
from modulos.sesion_01_09_operaciones import MenuOperaciones
from modulos.sesion_02_07_08_sistemas import MenuSistemas
from modulos.sesion_03_04_gauss import MenuGauss
from modulos.sesion_05_06_vectores import MenuVectores
from modulos.servidor_web import ServidorWeb
from modulos.sesion_10_11_det_inversa import MenuDetInversa

LOGO_PRINCIPAL = r"""
   ###  #      #### ##### ####  ####   ###      #     ##### #   # #####  ###  #
  #   # #     #     #     #   # #   # #   #     #       #   ##  # #     #   # #
  ##### #     #  ## ####  ####  ####  #####     #       #   # # # ####  ##### #
  #   # #     #   # #     #   # #  #  #   #     #       #   #  ## #     #   # #
  #   # #####  #### ##### ####  #   # #   #     ##### ##### #   # ##### #   # #####
"""


class CalculadoraAlgebraLineal:
    """Menú principal: cada opción abre una sesión del sílabo."""

    def __init__(self):
        """Crea la memoria compartida y registra las sesiones (clave -> (nombre, menú))."""
        self.memoria = MemoriaMatrices()
        self.asistente = AsistenteMemoria(self.memoria)
        self.sesiones = {
            "2": ("Sesión 1 y 9: Operaciones básicas y propiedades", MenuOperaciones(self.asistente)),
            "3": ("Sesión 3 y 4: Forma escalonada y existencia (Gauss-Jordan)", MenuGauss(self.asistente)),
            "4": ("Sesión 2, 7 y 8: Sistemas de ecuaciones lineales", MenuSistemas(self.asistente)),
            "5": ("Sesión 5 y 6: Vectores, C.L. e independencia lineal", MenuVectores(self.asistente)),
            "6": ("Sesión 10 y 11: Determinantes, inversas y propiedades", MenuDetInversa(self.asistente)),
            "7": ("Módulo III: Álgebra de matrices (Programa 5)", MenuMatrices(self.asistente)),
            "8": ("Factorización LU y solución Ax = b (Programa 6)", MenuLU(self.asistente)),
        }

    def ejecutar(self):
        """Atiende el menú principal hasta que el usuario elige salir."""
        Consola.preparar_terminal()
        while True:
            self._mostrar_menu()
            opcion = Entrada.opcion("\n  Seleccione un módulo: ", ["0", "1"] + list(self.sesiones))
            if opcion == "0":
                print("\n  Saliendo de la calculadora... ¡Éxito con el profe!")
                return
            if opcion == "1":
                self._cargar_matriz()
            else:
                self.sesiones[opcion][1].ejecutar()

    def _mostrar_menu(self):
        """Dibuja el logo, el estado de la memoria y las opciones."""
        Consola.limpiar()
        Consola.logo(LOGO_PRINCIPAL)
        Consola.encabezado("MOTOR DE ÁLGEBRA LINEAL")
        for nombre in self.memoria.NOMBRES:
            estado = self.memoria.describir(nombre)
            color = Estilo.ROJO if estado == "Vacía" else Estilo.VERDE
            print(f"  Matriz {nombre}: {Estilo.pintar(estado, color, Estilo.NEGRITA)}")
        print()
        Consola.opcion("1", "Cargar / editar matrices en memoria (A o B)")
        for clave, (nombre, _) in self.sesiones.items():
            Consola.opcion(clave, nombre)
        Consola.opcion("0", "Salir")

    def _cargar_matriz(self):
        """Opción 1: pide la letra y lee la matriz nueva."""
        letra = self.asistente.pedir_letra("  ¿Cuál matriz querés cargar o editar? (A / B): ")
        self.asistente.cargar(letra)
        Consola.pausar()


if __name__ == "__main__":
    try:
        if "--consola" in sys.argv:
            CalculadoraAlgebraLineal().ejecutar()
        else:
            ServidorWeb().iniciar()
    except (KeyboardInterrupt, EOFError):
        print("\n\n  Programa interrumpido por el usuario.")
