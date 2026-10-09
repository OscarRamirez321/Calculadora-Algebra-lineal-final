from .reduccion_gauss import gauss_jordan

def resolver_sistema_ax_b(A, b):
    """
    Resuelve el sistema Ax = b creando la matriz aumentada [A|b].
    Ideal para problemas reales de ingeniería.
    """
    if len(A) != len(b):
        raise ValueError("Error: El vector 'b' debe tener la misma cantidad de filas que 'A'.")
    
    # Crear matriz aumentada [A | b]
    aumentada = [A[i] + [b[i][0]] for i in range(len(A))]
    
    rref, pivotes, libres = gauss_jordan(aumentada)
    cols_variables = len(A[0])
    
    if libres > 0 or pivotes < cols_variables:
        return None, "El sistema tiene infinitas soluciones (variables libres) o es inconsistente."
    
    # Extraer la última columna (que ahora tiene las respuestas)
    soluciones = [[fila[-1]] for fila in rref[:cols_variables]]
    return soluciones, "Solución única encontrada con éxito."