from .operaciones_basicas import producto_matricial
from .reduccion_gauss import gauss_jordan
import math

def matriz_identidad(n):
    """Genera una matriz identidad de tamaño n x n."""
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]

def potencia_matriz(A, n):
    """Eleva una matriz A a la potencia n (A^n)."""
    if len(A) != len(A[0]):
        raise ValueError("Error: La matriz debe ser cuadrada para elevarse a una potencia.")
    if n == 0:
        return matriz_identidad(len(A))
    res = A
    for _ in range(1, n):
        res = producto_matricial(res, A)
    return res

def rango_matriz(A):
    """Calcula el rango contando las filas no nulas después de aplicar Gauss-Jordan."""
    _, pivotes, _ = gauss_jordan(A)
    return pivotes

def matriz_triangular_superior(A):
    """Lleva la matriz a su forma triangular superior (Eliminación Gaussiana simple)."""
    M = [fila[:] for fila in A]
    filas, cols = len(M), len(M[0])
    for i in range(min(filas, cols)):
        if M[i][i] == 0:
            continue
        for j in range(i+1, filas):
            factor = M[j][i] / M[i][i]
            for k in range(i, cols):
                M[j][k] -= factor * M[i][k]
    return M

def factorizacion_lu(A):
    """Calcula la factorización L (Lower) y U (Upper) de una matriz."""
    if len(A) != len(A[0]):
        raise ValueError("Error: La matriz debe ser cuadrada para LU.")
    n = len(A)
    L = matriz_identidad(n)
    U = [fila[:] for fila in A]
    
    for i in range(n):
        for j in range(i+1, n):
            if U[i][i] == 0:
                raise ValueError("Se requiere pivoteo (el pivote es 0). LU simple falló.")
            factor = U[j][i] / U[i][i]
            L[j][i] = factor
            for k in range(i, n):
                U[j][k] -= factor * U[i][k]
    return L, U

def matriz_diagonal(A):
    """Extrae solo la diagonal principal y hace ceros el resto."""
    filas = len(A)
    cols = len(A[0])
    return [[A[i][j] if i == j else 0.0 for j in range(cols)] for i in range(filas)]

def multiplicacion_escalar(c, A):
    """Multiplica toda la matriz por un número."""
    return [[c * A[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def factorizacion_cholesky(A):
    """Calcula la matriz L tal que L * L^T = A (Debe ser simétrica y definida positiva)."""
    n = len(A)
    L = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            suma = sum(L[i][k] * L[j][k] for k in range(j))
            if i == j:
                val = A[i][i] - suma
                if val <= 0:
                    raise ValueError("La matriz no es definida positiva (requerido para Cholesky).")
                L[i][j] = math.sqrt(val)
            else:
                L[i][j] = (1.0 / L[j][j]) * (A[i][j] - suma)
    return L