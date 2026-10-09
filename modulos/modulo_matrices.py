"""
Módulo de Álgebra de Matrices (Programa 5).
Contiene operaciones algebraicas, cálculo de determinantes (Cofactores y Triangular),
inversas (Gauss-Jordan y Adjunta) y un verificador de 6 propiedades.
Implementado en Python puro sin librerías externas (solo 'fractions').
"""
from fractions import Fraction

# ==========================================
# 1. VALIDACIONES
# ==========================================
def validar_suma_resta(A, B):
    """Verifica que ambas matrices tengan exactamente la misma dimensión."""
    if len(A) != len(B) or len(A[0]) != len(B[0]):
        raise ValueError("Error: Las matrices deben tener la misma dimensión.")

def validar_multiplicacion(A, B):
    """Verifica que las columnas de A sean iguales a las filas de B."""
    if len(A[0]) != len(B):
        raise ValueError("Error: Columnas de A no coinciden con filas de B.")

def validar_cuadrada(A):
    """Verifica que la matriz sea cuadrada (m = n)."""
    if len(A) != len(A[0]):
        raise ValueError("Error: La matriz debe ser cuadrada.")

# ==========================================
# 2. OPERACIONES BÁSICAS
# ==========================================
def suma(A, B):
    """Suma dos matrices elemento a elemento."""
    validar_suma_resta(A, B)
    return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def resta(A, B):
    """Resta la Matriz B de la Matriz A elemento a elemento."""
    validar_suma_resta(A, B)
    return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def multiplicacion_escalar(c, A):
    """Multiplica cada elemento de la matriz por una constante c."""
    return [[c * A[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def producto_matricial(A, B):
    """Multiplica A y B utilizando el algoritmo de filas por columnas."""
    validar_multiplicacion(A, B)
    C = [[Fraction(0)] * len(B[0]) for _ in range(len(A))]
    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(B)):
                C[i][j] += A[i][k] * B[k][j]
    return C

def transpuesta(A):
    """Intercambia las filas por las columnas de la matriz."""
    return [[A[j][i] for j in range(len(A))] for i in range(len(A[0]))]

# ==========================================
# 3. DETERMINANTES (COFACTORES Y TRIANGULAR)
# ==========================================
def determinante_cofactores(M):
    """Calcula el determinante usando expansión por cofactores (recursividad)."""
    validar_cuadrada(M)
    n = len(M)
    if n == 1:
        return M[0][0]
    if n == 2:
        return M[0][0] * M[1][1] - M[0][1] * M[1][0]
        
    det = Fraction(0)
    for c in range(n):
        submatriz = [fila[:c] + fila[c+1:] for fila in M[1:]]
        signo = Fraction(1) if c % 2 == 0 else Fraction(-1)
        det += signo * M[0][c] * determinante_cofactores(submatriz)
    return det

def determinante_triangular(M):
    """
    Calcula el determinante reduciendo la matriz a forma triangular superior
    y multiplicando los elementos de la diagonal principal.
    """
    validar_cuadrada(M)
    n = len(M)
    aug = [fila[:] for fila in M]
    det = Fraction(1)
    
    for r in range(n):
        # Buscamos un pivote distinto de cero
        if aug[r][r] == Fraction(0):
            for i in range(r + 1, n):
                if aug[i][r] != Fraction(0):
                    aug[r], aug[i] = aug[i], aug[r]
                    det *= Fraction(-1) # Un intercambio de fila invierte el signo del det
                    break
        
        # Si la columna entera es ceros, el determinante es 0
        if aug[r][r] == Fraction(0):
            return Fraction(0)
            
        pivote = aug[r][r]
        for i in range(r + 1, n):
            factor = aug[i][r] / pivote
            for j in range(r, n):
                aug[i][j] -= factor * aug[r][j]
                
    # Producto de la diagonal
    for i in range(n):
        det *= aug[i][i]
    return det

# ==========================================
# 4. INVERSAS (ADJUNTA Y GAUSS-JORDAN)
# ==========================================
def matriz_adjunta(M):
    """Calcula la matriz de cofactores transpuesta."""
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

def inversa_adjunta(A):
    """Calcula la inversa multiplicando 1/det por la Adjunta."""
    det = determinante_cofactores(A)
    if det == Fraction(0):
        raise ValueError("Diagnóstico: Matriz SINGULAR (det=0). Vectores L.D.")
    adj = matriz_adjunta(A)
    return multiplicacion_escalar(Fraction(1) / det, adj)

def inversa_gauss_jordan(A):
    """
    Calcula la inversa llevando [A|I] a [I|A^-1]. 
    Retorna la inversa y el diagnóstico de invertibilidad.
    """
    validar_cuadrada(A)
    n = len(A)
    
    # Construir [A | I]
    aug = [A[i][:] + [Fraction(1) if i == j else Fraction(0) for j in range(n)] for i in range(n)]
    pivotes = 0
    
    # Reducción de filas
    for r in range(n):
        if aug[r][r] == Fraction(0):
            for i in range(r + 1, n):
                if aug[i][r] != Fraction(0):
                    aug[r], aug[i] = aug[i], aug[r]
                    break
                    
        pivot_val = aug[r][r]
        if pivot_val == Fraction(0):
            raise ValueError(f"Diagnóstico: Solo {pivotes} pivotes. Vectores L.D. Matriz SINGULAR (det=0).")
            
        pivotes += 1
        aug[r] = [elem / pivot_val for elem in aug[r]]
        
        for i in range(n):
            if i != r and aug[i][r] != Fraction(0):
                factor = aug[i][r]
                aug[i] = [aug[i][j] - factor * aug[r][j] for j in range(2 * n)]
                
    diagnostico = f"Invertible ({pivotes} pivotes, columnas L.I., det(A) != 0)"
    inversa = [fila[n:] for fila in aug]
    return inversa, diagnostico

# ==========================================
# 5. VERIFICADOR DE LAS 6 PROPIEDADES
# ==========================================
def verificar_propiedades(A, B):
    """
    Calcula ambos miembros de las 6 propiedades requeridas por la rúbrica:
    1. Determinantes coinciden (Cofactores = Triangular)
    2. Identidad: A * A^-1 = I
    3. Transpuesta del Producto: (AB)^T = B^T * A^T
    4. Inversa del Producto: (AB)^-1 = B^-1 * A^-1
    5. Inversa de la Transpuesta: (A^T)^-1 = (A^-1)^T
    6. Determinante de la Inversa: det(A^-1) = 1 / det(A)
    """
    resultados = []
    
    # Prop 1: Determinantes
    try:
        det_cof = determinante_cofactores(A)
        det_tri = determinante_triangular(A)
        resultados.append(("1. det(A) Cofactores == det(A) Triangular", det_cof == det_tri))
    except Exception: resultados.append(("1. det(A) Cofactores == det(A) Triangular", False))

    # Prop 2: A * A^-1 = I
    try:
        inv_A, _ = inversa_gauss_jordan(A)
        identidad_calc = producto_matricial(A, inv_A)
        identidad_real = [[Fraction(1) if i == j else Fraction(0) for j in range(len(A))] for i in range(len(A))]
        resultados.append(("2. A * A^-1 == Identidad", identidad_calc == identidad_real))
    except Exception: resultados.append(("2. A * A^-1 == Identidad", False))

    # Prop 3: (AB)^T = B^T * A^T
    try:
        AB_T = transpuesta(producto_matricial(A, B))
        BT_AT = producto_matricial(transpuesta(B), transpuesta(A))
        resultados.append(("3. (A * B)^T == B^T * A^T", AB_T == BT_AT))
    except Exception: resultados.append(("3. (A * B)^T == B^T * A^T", False))

    # Prop 4: (AB)^-1 = B^-1 * A^-1 (Teorema de la inversa)
    try:
        inv_AB, _ = inversa_gauss_jordan(producto_matricial(A, B))
        inv_A, _ = inversa_gauss_jordan(A)
        inv_B, _ = inversa_gauss_jordan(B)
        Binv_Ainv = producto_matricial(inv_B, inv_A)
        resultados.append(("4. (A * B)^-1 == B^-1 * A^-1", inv_AB == Binv_Ainv))
    except Exception: resultados.append(("4. (A * B)^-1 == B^-1 * A^-1", False))

    # Prop 5: (A^T)^-1 = (A^-1)^T
    try:
        inv_AT, _ = inversa_gauss_jordan(transpuesta(A))
        inv_A_T = transpuesta(inv_A)
        resultados.append(("5. (A^T)^-1 == (A^-1)^T", inv_AT == inv_A_T))
    except Exception: resultados.append(("5. (A^T)^-1 == (A^-1)^T", False))

    # Prop 6: det(A^-1) = 1 / det(A)
    try:
        det_A = determinante_cofactores(A)
        det_invA = determinante_cofactores(inv_A)
        resultados.append(("6. det(A^-1) == 1 / det(A)", det_invA == (Fraction(1) / det_A)))
    except Exception: resultados.append(("6. det(A^-1) == 1 / det(A)", False))

    return resultados