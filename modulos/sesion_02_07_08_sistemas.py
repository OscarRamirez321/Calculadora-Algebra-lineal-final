from fractions import Fraction
from modulos import utilidades as util
from modulos.sesion_03_04_gauss import gauss_jordan_paso_a_paso

# --- LÓGICA DE SISTEMAS ---

def construir_aumentada(A, b):
    """Une la matriz de coeficientes A con el vector de resultados b: [A | b]"""
    if len(A) != len(b):
        raise ValueError("El número de filas de A debe coincidir con el número de elementos de b.")
    
    aumentada = []
    for i in range(len(A)):
        aumentada.append(A[i][:] + [b[i][0]])
    return aumentada

def analizar_sistema(A, b, rref):
    """Clasifica el sistema y extrae las soluciones si las hay."""
    filas = len(A)
    cols_variables = len(A[0])
    
    # 1. Comprobar si es Homogéneo o No Homogéneo
    es_homogeneo = all(val[0] == Fraction(0) for val in b)
    print(f"\n{util.Color.YELLOW}--- CLASIFICACIÓN DEL SISTEMA ---{util.Color.END}")
    if es_homogeneo:
        print("Tipo: SISTEMA HOMOGÉNEO (Ax = 0). Siempre tiene al menos la solución trivial.")
    else:
        print("Tipo: SISTEMA NO HOMOGÉNEO (Ax = b).")

    # 2. Buscar inconsistencias (0 = constante no nula)
    inconsistente = False
    for i in range(filas):
        # Si toda la fila de variables es 0 pero el término independiente no lo es
        todo_cero = all(rref[i][j] == Fraction(0) for j in range(cols_variables))
        if todo_cero and rref[i][-1] != Fraction(0):
            inconsistente = True
            break
            
    if inconsistente:
        print(f"{util.Color.RED}❌ SISTEMA INCOMPATIBLE: No tiene solución (las rectas/planos son paralelos o no se cruzan).{util.Color.END}")
        return None

    # 3. Contar pivotes reales en la parte de las variables
    pivotes = 0
    for i in range(filas):
        for j in range(cols_variables):
            if rref[i][j] == Fraction(1):
                # Verificamos que sea el primer elemento no nulo de la fila
                if all(rref[i][k] == Fraction(0) for k in range(j)):
                    pivotes += 1
                    break

    # 4. Veredicto Final
    variables_libres = cols_variables - pivotes
    if variables_libres == 0:
        print(f"{util.Color.GREEN}✅ SISTEMA COMPATIBLE DETERMINADO: Solución Única.{util.Color.END}")
        soluciones = [[rref[i][-1]] for i in range(cols_variables)]
        return soluciones
    else:
        print(f"{util.Color.YELLOW}⚠️ SISTEMA COMPATIBLE INDETERMINADO: Infinitas Soluciones.{util.Color.END}")
        print(f"El sistema tiene {variables_libres} variable(s) libre(s).")
        return None

# --- CONTROLADOR DEL MENÚ ---

def ejecutar(memoria):
    util.limpiar_pantalla()
    print(f"{util.Color.CYAN}{util.Color.BOLD}--- SESIONES 2, 7 y 8: SISTEMAS DE ECUACIONES LINEALES ---{util.Color.END}")
    print("1. Resolver Sistema Ax = b (Requiere Matriz A como coeficientes)")
    print(f"{util.Color.RED}0. Regresar al Menú Principal{util.Color.END}")

    sub = input("\nSeleccione la operación >> ")
    if sub == '0': return

    try:
        if sub == '1':
            M = memoria.get('A')
            if not M:
                raise ValueError("Primero debes cargar la Matriz A (Coeficientes) en el Menú Principal.")
            
            filas_a = len(M)
            print(f"\n{util.Color.BOLD}--- Ingresando Vector b (Términos Independientes) ---{util.Color.END}")
            print(f"El vector debe tener exactamente {filas_a} filas para coincidir con la Matriz A.")
            
            vector_b = []
            for i in range(filas_a):
                val = input(f"Término b[{i+1}]: ")
                vector_b.append([Fraction(val)])
                
            # Mostramos el sistema planteado
            util.imprimir_matriz(M, "Matriz de Coeficientes (A)")
            util.imprimir_matriz(vector_b, "Vector de Resultados (b)")
            
            # Construir y reducir [A|b]
            aumentada = construir_aumentada(M, vector_b)
            rref, _, _, pasos = gauss_jordan_paso_a_paso(aumentada)
            
            print(f"\n{util.Color.CYAN}Reduciendo matriz aumentada por Gauss-Jordan...{util.Color.END}")
            util.imprimir_matriz(rref, "Matriz Aumentada RREF [A | b]")
            
            # Analizamos e interpretamos
            solucion = analizar_sistema(M, vector_b, rref)
            
            if solucion:
                util.imprimir_matriz(solucion, "Solución Exacta del Sistema (Vector x)")
                
                # PREGUNTAR PARA GUARDAR
                print(f"\n{util.Color.YELLOW}¿Querés guardar este vector de solución en la memoria B?{util.Color.END}")
                opc = input("Guardar en (B) / (N)o guardar: ").strip().upper()
                if opc == 'B':
                    memoria['B'] = solucion
                    util.imprimir_exito("Vector guardado como nueva Matriz B.")

    except Exception as e:
        util.imprimir_error(str(e))
    
    input(f"\n{util.Color.CYAN}Presiona ENTER para regresar...{util.Color.END}")