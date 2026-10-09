import os
from fractions import Fraction

# Códigos ANSI para colores nativos en la terminal de Mac
class Color:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

def limpiar_pantalla():
    """Limpia la consola para mantener el menú limpio."""
    os.system('clear' if os.name != 'nt' else 'cls')

def imprimir_matriz(matriz, nombre="Matriz"):
    """Imprime la matriz alineada, soportando fracciones."""
    if not matriz:
        print(f"{Color.RED}La matriz está vacía.{Color.END}")
        return

    print(f"\n{Color.CYAN}{Color.BOLD}--- {nombre} ---{Color.END}")
    for fila in matriz:
        # Convierte las fracciones a string limpio (ej. '1/2' o '3')
        fila_str = []
        for x in fila:
            if isinstance(x, Fraction):
                fila_str.append(f"{Color.YELLOW}{str(x):>6}{Color.END}")
            else:
                fila_str.append(f"{Color.YELLOW}{x:>6}{Color.END}")
                
        print(f"{Color.CYAN}|{Color.END} {'  '.join(fila_str)} {Color.CYAN}|{Color.END}")
    print(f"{Color.CYAN}" + "-" * (len(nombre) + 8) + f"{Color.END}\n")

def imprimir_exito(mensaje):
    print(f"{Color.GREEN}{Color.BOLD}✔ {mensaje}{Color.END}")

def imprimir_error(mensaje):
    print(f"{Color.RED}{Color.BOLD}✖ ERROR: {mensaje}{Color.END}")
    
def imprimir_teorema(sesion, mensaje):
    """Imprime el recuadro automático de demostración de teoremas."""
    print(f"\n{Color.CYAN}========================================{Color.END}")
    print(f"{Color.BOLD} VERIFICACIÓN AUTOMÁTICA (Sesión {sesion}) {Color.END}")
    print(f"{Color.CYAN}========================================{Color.END}")
    print(f"{mensaje}")