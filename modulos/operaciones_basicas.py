def suma(A, B):
    """Suma dos matrices. Deben tener dimensiones exactas."""
    if len(A) != len(B) or len(A[0]) != len(B[0]):
        raise ValueError("Error: Para sumar matrices, deben tener la misma dimensión.")
    return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def resta(A, B):
    """Resta dos matrices."""
    if len(A) != len(B) or len(A[0]) != len(B[0]):
        raise ValueError("Error: Para restar matrices, deben tener la misma dimensión.")
    return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def multiplicacion_escalar(c, A):
    """Multiplica una matriz por un número escalar."""
    return [[c * A[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def producto_matricial(A, B):
    """Multiplica A(mxn) * B(nxp). Valida compatibilidad."""
    if len(A[0]) != len(B):
        raise ValueError("Error: Las columnas de A deben ser iguales a las filas de B.")
    
    C = [[0] * len(B[0]) for _ in range(len(A))]
    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(B)):
                C[i][j] += A[i][k] * B[k][j]
    return C

def transpuesta(A):
    """Convierte filas en columnas."""
    return [[A[j][i] for j in range(len(A))] for i in range(len(A[0]))]
