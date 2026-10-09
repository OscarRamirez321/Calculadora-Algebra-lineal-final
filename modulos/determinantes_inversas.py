from .operaciones_basicas import multiplicacion_escalar, transpuesta
from .reduccion_gauss import gauss_jordan

def determinante_cofactores(M):
    """Determinante por expansión de cofactores."""
    if len(M) != len(M[0]): raise ValueError("La matriz debe ser cuadrada.")
    n = len(M)
    if n == 1: return M[0][0]
    if n == 2: return M[0][0] * M[1][1] - M[0][1] * M[1][0]
        
    det = 0
    for c in range(n):
        submatriz = [fila[:c] + fila[c+1:] for fila in M[1:]]
        det += ((-1) ** c) * M[0][c] * determinante_cofactores(submatriz)
    return det

def matriz_adjunta(M):
    n = len(M)
    cofactores = []
    for i in range(n):
        fila_cofactores = []
        for j in range(n):
            submatriz = [fila[:j] + fila[j+1:] for r, fila in enumerate(M) if r != i]
            fila_cofactores.append(((-1) ** (i + j)) * determinante_cofactores(submatriz))
        cofactores.append(fila_cofactores)
    return transpuesta(cofactores)

def inversa_adjunta(M):
    det = determinante_cofactores(M)
    if det == 0: raise ValueError("Matriz singular (det=0). No tiene inversa.")
    return multiplicacion_escalar(1/det, matriz_adjunta(M))

def inversa_gauss_jordan(M):
    n = len(M)
    aumentada = [M[i][:] + [1 if i == j else 0 for j in range(n)] for i in range(n)]
    rref, pivotes, _ = gauss_jordan(aumentada)
    if pivotes < n: raise ValueError("La matriz no es invertible.")
    return [fila[n:] for fila in rref]