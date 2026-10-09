import os

# Códigos ANSI para darle color a la terminal
class Color:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

def limpiar_pantalla():
    """Limpia la consola para que parezca una app real y no texto infinito."""
    os.system('clear' if os.name != 'nt' else 'cls')

def imprimir_matriz(matriz, nombre="Matriz"):
    """Imprime la matriz con bordes y colores alineados."""
    print(f"\n{Color.CYAN}{Color.BOLD}=== {nombre} ==={Color.END}")
    for fila in matriz:
        # Formatea los números para que queden alineados con 3 decimales
        fila_str = "  ".join(f"{Color.YELLOW}{x:7.3f}{Color.END}" if isinstance(x, float) else f"{Color.YELLOW}{x:7}{Color.END}" for x in fila)
        # Pone las barras laterales de la matriz
        print(f"{Color.CYAN}|{Color.END} {fila_str} {Color.CYAN}|{Color.END}")
    print(f"{Color.CYAN}" + "=" * (len(nombre) + 8) + f"{Color.END}\n")

def imprimir_exito(mensaje):
    print(f"{Color.GREEN}{Color.BOLD}✔ {mensaje}{Color.END}")

def imprimir_error(mensaje):
    print(f"{Color.RED}{Color.BOLD}✖ ERROR: {mensaje}{Color.END}")