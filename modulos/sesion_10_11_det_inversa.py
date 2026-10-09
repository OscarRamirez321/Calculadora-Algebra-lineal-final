from fractions import Fraction
from modulos import utilidades as util
# Importamos las funciones puras que ya hicimos para reutilizarlas
from modulos.sesion_01_09_operaciones import producto_matricial, transpuesta, mult_escalar
from modulos.sesion_03_04_gauss import gauss_jordan_paso_a_paso

# --- FUNCIONES MATEMÁTICAS PURAS ---

def determinante_cofactores(M):
    """Calcula el determinante por recursividad (Expansión de Cofactores)."""
    n = len(M)
    if n != len(M[0]):
        raise ValueError("La matriz debe ser cuadrada para calcular su determinante.")
    
    if n == 1:
        return M[0][0]
    if n == 2:
        return M[0][0] * M[1][1] - M[0][1] * M[1][0]
        
    det = Fraction(0)
    for c in range(n):
        # Crear submatriz eliminando la fila 0 y la columna c
        submatriz = [fila[:c] + fila[c+1:] for fila in M[1:]]
        # Alternar el signo (+, -, +, -)
        signo = Fraction(1) if c % 2 == 0 else Fraction(-1)
        det += signo * M[0][c] * determinante_cofactores(submatriz)
    return det

def matriz_adjunta(M):
    """Calcula la matriz adjunta (Transpuesta de la matriz de cofactores)."""
    n = len(M)
    cofactores = []
    for i in range(n):
        fila_cofactores = []
        for j in range(n):
            submatriz = [fila[:j] + fila[j+1:] for r, fila in enumerate(M) if r != i]
            signo = Fraction(1) if (i + j) % 2 == 0 else Fraction(-1)
            fila_cofactores.append(signo * determinante_cofactores(submatriz))
        cofactores.append(fila_cofactores)
    return transpuesta(cofactores)

def inversa_adjunta(M):
    """Fórmula: A^-1 = (1 / det) * Adjunta(A)"""
    det = determinante_cofactores(M)
    if det == Fraction(0):
        raise ValueError("La matriz es SINGULAR (det = 0). No tiene inversa.")
    adj = matriz_adjunta(M)
    return mult_escalar(Fraction(1) / det, adj)

def inversa_gauss(M):
    """Fórmula: Llevar [A | I] a [I | A^-1] por reducción de filas."""
    n = len(M)
    if determinante_cofactores(M) == Fraction(0):
        raise ValueError("La matriz es SINGULAR (det = 0). No tiene inversa.")
        
    # Construimos la matriz aumentada [A | Identidad]
    aumentada = []
    for i in range(n):
        fila = M[i][:] + [Fraction(1) if i == j else Fraction(0) for j in range(n)]
        aumentada.append(fila)
        
    # Usamos nuestra función silenciando los pasos visuales
    rref, pivotes, libres, _ = gauss_jordan_paso_a_paso(aumentada)
    
    # Extraemos la mitad derecha, que ahora es la inversa
    inversa = [fila[n:] for fila in rref]
    return inversa


# --- CONTROLADOR DEL MENÚ ---

def ejecutar(memoria):
    util.limpiar_pantalla()
    print(f"{util.Color.CYAN}{util.Color.BOLD}--- SESIÓN 10 y 11: DETERMINANTES E INVERSAS ---{util.Color.END}")
    print("1. Calcular Determinante (Expansión por Cofactores)")
    print("2. Calcular Inversa (Método Adjunta vs Gauss-Jordan) y Teorema")
    print(f"{util.Color.RED}0. Regresar al Menú Principal{util.Color.END}")

    sub = input("\nSeleccione la operación >> ")
    if sub == '0': return

    try:
        letra = input("¿A cuál matriz querés aplicarle la operación? (A / B): ").strip().upper()
        M = memoria.get(letra)
        if not M:
            raise ValueError(f"La Matriz {letra} está vacía. Cargala primero en el menú.")

        if sub == '1':
            det = determinante_cofactores(M)
            util.imprimir_exito(f"El Determinante de la Matriz {letra} es: {det}")
            
            # Teorema Sesión 11
            print(f"\n{util.Color.YELLOW}Análisis de Invertibilidad:{util.Color.END}")
            if det != Fraction(0):
                print(f"{util.Color.GREEN}Como el det != 0, la matriz es INVERTIBLE (No Singular).{util.Color.END}")
            else:
                print(f"{util.Color.RED}Como el det == 0, la matriz es SINGULAR (No Invertible).{util.Color.END}")

        elif sub == '2':
            # Comprueba si tiene inversa primero
            det = determinante_cofactores(M)
            if det == Fraction(0):
                raise ValueError("El determinante es 0. Esta matriz NO tiene inversa.")

            # Método 1: Adjunta
            inv_adj = inversa_adjunta(M)
            util.imprimir_matriz(inv_adj, f"Inversa por ADJUNTA ({letra}^-1)")

            # Método 2: Gauss-Jordan
            inv_gj = inversa_gauss(M)
            util.imprimir_matriz(inv_gj, f"Inversa por GAUSS-JORDAN ({letra}^-1)")

            # TEOREMA EN VIVO (SESIÓN 10)
            util.imprimir_teorema("10", f"Propiedad: La Matriz multiplicada por su Inversa da la Identidad ({letra} * {letra}^-1 = I)")
            identidad = producto_matricial(M, inv_adj)
            util.imprimir_matriz(identidad, "Resultado de la Multiplicación")
            util.imprimir_exito("Podemos observar que la diagonal son 1s puros. Propiedad demostrada.")

            # Preguntar si guardamos
            print(f"\n{util.Color.YELLOW}¿Querés guardar esta Matriz Inversa para usarla luego?{util.Color.END}")
            opc = input("Guardar en (A) / Guardar en (B) / (N)o guardar: ").strip().upper()
            if opc == 'A':
                memoria['A'] = inv_adj
                util.imprimir_exito("Matriz Inversa guardada como nueva Matriz A.")
            elif opc == 'B':
                memoria['B'] = inv_adj
                util.imprimir_exito("Matriz Inversa guardada como nueva Matriz B.")

    except Exception as e:
        util.imprimir_error(str(e))
    
    input(f"\n{util.Color.CYAN}Presiona ENTER para regresar...{util.Color.END}")