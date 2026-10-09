def gauss_jordan(matriz):
    """Versión silenciosa usada internamente por otros módulos (Inversas, Rangos, etc)."""
    M = [fila[:] for fila in matriz]
    filas, cols = len(M), len(M[0])
    pivotes, r = 0, 0 
    
    for c in range(cols):
        if r >= filas: break
        
        pivot_row = r
        while pivot_row < filas and abs(M[pivot_row][c]) < 1e-10:
            pivot_row += 1
            
        if pivot_row == filas: continue
            
        # Intercambio
        M[r], M[pivot_row] = M[pivot_row], M[r]
        
        # Normalizar a 1
        pivot_val = M[r][c]
        M[r] = [elem / pivot_val for elem in M[r]]
        
        # Hacer ceros el resto de la columna
        for i in range(filas):
            if i != r:
                factor = M[i][c]
                M[i] = [M[i][j] - factor * M[r][j] for j in range(cols)]
                
        r += 1
        pivotes += 1
        
    return M, pivotes, cols - pivotes


def gauss_jordan_paso_a_paso(matriz):
    """Versión locuaz que guarda el historial de pasos para la interfaz gráfica visual."""
    M = [fila[:] for fila in matriz]
    filas, cols = len(M), len(M[0])
    pivotes, r = 0, 0
    pasos = [] 

    pasos.append(("Matriz Original", [f[:] for f in M]))

    for c in range(cols):
        if r >= filas: break
        
        pivot_row = r
        while pivot_row < filas and abs(M[pivot_row][c]) < 1e-10:
            pivot_row += 1
            
        if pivot_row == filas: continue
            
        # 1er Paso: Intercambio de filas
        if pivot_row != r:
            M[r], M[pivot_row] = M[pivot_row], M[r]
            pasos.append((f"Intercambio de Fila {r+1} con Fila {pivot_row+1}", [f[:] for f in M]))
        
        # 2do Paso: Convertir pivote en 1
        pivot_val = M[r][c]
        if pivot_val != 1:
            M[r] = [elem / pivot_val for elem in M[r]]
            pasos.append((f"Fila {r+1} dividida entre {pivot_val:.2f} (Crear pivote)", [f[:] for f in M]))
        
        # 3er Paso: Hacer ceros arriba y abajo
        for i in range(filas):
            if i != r and abs(M[i][c]) > 1e-10:
                factor = M[i][c]
                M[i] = [M[i][j] - factor * M[r][j] for j in range(cols)]
                pasos.append((f"A la Fila {i+1} se le resta {factor:.2f} * Fila {r+1}", [f[:] for f in M]))
                
        r += 1
        pivotes += 1
        
    return M, pivotes, cols - pivotes, pasos