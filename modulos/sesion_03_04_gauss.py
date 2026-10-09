from fractions import Fraction
from modulos import utilidades as util

# --- FUNCIONES MATEMÁTICAS PURAS ---

def gauss_jordan_paso_a_paso(matriz):
    """Lleva la matriz a su forma RREF guardando el historial de operaciones."""
    # Hacemos una copia profunda para no modificar la original
    M = [[val for val in fila] for fila in matriz]
    filas = len(M)
    cols = len(M[0])
    pivotes = 0
    r = 0
    pasos = [] # Aquí guardamos el chisme de cada paso

    pasos.append(("Matriz Original", [f[:] for f in M]))

    for c in range(cols):
        if r >= filas: break
        
        # 1. Buscar el pivote
        pivot_row = r
        while pivot_row < filas and M[pivot_row][c] == Fraction(0):
            pivot_row += 1
            
        if pivot_row == filas: continue # No hay pivote en esta columna
            
        # 2. Intercambio de filas si el pivote está más abajo
        if pivot_row != r:
            M[r], M[pivot_row] = M[pivot_row], M[r]
            pasos.append((f"Intercambio: Fila {r+1} <-> Fila {pivot_row+1}", [f[:] for f in M]))
        
        # 3. Normalizar el pivote para que sea 1
        pivot_val = M[r][c]
        if pivot_val != Fraction(1):
            M[r] = [elem / pivot_val for elem in M[r]]
            pasos.append((f"Normalizar Pivote: Fila {r+1} dividida entre {pivot_val}", [f[:] for f in M]))
        
        # 4. Hacer ceros en el resto de la columna (arriba y abajo)
        for i in range(filas):
            if i != r and M[i][c] != Fraction(0):
                factor = M[i][c]
                M[i] = [M[i][j] - factor * M[r][j] for j in range(cols)]
                pasos.append((f"Hacer Cero: Fila {i+1} -> Fila {i+1} - ({factor}) * Fila {r+1}", [f[:] for f in M]))
                
        r += 1
        pivotes += 1
        
    variables_libres = cols - pivotes
    return M, pivotes, variables_libres, pasos


# --- CONTROLADOR DEL MENÚ ---

def ejecutar(memoria):
    util.limpiar_pantalla()
    print(f"{util.Color.CYAN}{util.Color.BOLD}--- SESIÓN 3 y 4: FORMA ESCALONADA Y EXISTENCIA ---{util.Color.END}")
    print("1. Reducción Gauss-Jordan (Paso a Paso detallado)")
    print("2. Análisis Rápido (RREF directo, Pivotes y L.I. / L.D.)")
    print(f"{util.Color.RED}0. Regresar al Menú Principal{util.Color.END}")

    sub = input("\nSeleccione la operación >> ")

    if sub == '0':
        return

    try:
        letra = input("¿A cuál matriz querés aplicarle Gauss-Jordan? (A / B): ").strip().upper()
        M = memoria.get(letra)
        
        if not M:
            raise ValueError(f"La Matriz {letra} está vacía. Cargala primero en la Opción 1.")

        rref, pivotes, libres, pasos = gauss_jordan_paso_a_paso(M)

        if sub == '1':
            print(f"\n{util.Color.YELLOW}--- INICIANDO REDUCCIÓN POR FILAS ---{util.Color.END}")
            for i, (descripcion, estado_matriz) in enumerate(pasos):
                # Imprimimos la operación que se hizo y cómo quedó la matriz
                util.imprimir_matriz(estado_matriz, f"Paso {i}: {descripcion}")
                if i < len(pasos) - 1:
                    input(f"{util.Color.CYAN}[Enter para ver el siguiente paso...]{util.Color.END}")
            
            util.imprimir_exito("Reducción a Forma Escalonada Reducida (RREF) completada.")

        elif sub == '2':
            # Solo muestra el final y el análisis de la Sesión 4
            util.imprimir_matriz(rref, f"Matriz RREF de {letra}")

        # --- TEOREMA EN VIVO (SESIÓN 4 - Condición de Existencia y Unicidad) ---
        util.imprimir_teorema("4", "Análisis de Unicidad e Independencia Lineal")
        print(f"Número de Columnas (Variables): {len(M[0])}")
        print(f"Número de Pivotes hallados: {util.Color.YELLOW}{pivotes}{util.Color.END}")
        print(f"Variables Libres: {util.Color.YELLOW}{libres}{util.Color.END}")
        
        if libres == 0:
            print(f"\n{util.Color.GREEN}✅ Veredicto: VECTORES LINEALMENTE INDEPENDIENTES (L.I.){util.Color.END}")
            print("El sistema tiene SOLUCIÓN ÚNICA (trivial si es homogéneo).")
        else:
            print(f"\n{util.Color.RED}❌ Veredicto: VECTORES LINEALMENTE DEPENDIENTES (L.D.){util.Color.END}")
            print("Existen variables libres, por lo tanto hay INFINITAS SOLUCIONES.")

        # Preguntar si guardamos la RREF
        print(f"\n{util.Color.YELLOW}¿Querés guardar la matriz reducida (RREF) en memoria?{util.Color.END}")
        opc = input("Guardar en (A) / Guardar en (B) / (N)o guardar: ").strip().upper()
        if opc == 'A':
            memoria['A'] = rref
            util.imprimir_exito("Matriz reducida guardada como nueva Matriz A.")
        elif opc == 'B':
            memoria['B'] = rref
            util.imprimir_exito("Matriz reducida guardada como nueva Matriz B.")

    except Exception as e:
        util.imprimir_error(str(e))
    
    input(f"\n{util.Color.CYAN}Presiona ENTER para regresar...{util.Color.END}")