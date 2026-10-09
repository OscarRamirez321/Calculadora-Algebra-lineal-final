from fractions import Fraction
from modulos import utilidades as util

# --- FUNCIONES MATEMÁTICAS PURAS ---

def sumar(A, B):
    if len(A) != len(B) or len(A[0]) != len(B[0]):
        raise ValueError("Las matrices deben tener la misma dimensión para sumarse.")
    return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def restar(A, B):
    if len(A) != len(B) or len(A[0]) != len(B[0]):
        raise ValueError("Las matrices deben tener la misma dimensión para restarse.")
    return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def transpuesta(A):
    return [[A[j][i] for j in range(len(A))] for i in range(len(A[0]))]

def mult_escalar(c, A):
    return [[c * A[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def producto_matricial(A, B):
    if len(A[0]) != len(B):
        raise ValueError("El número de columnas de A debe ser igual a las filas de B.")
    C = [[Fraction(0)] * len(B[0]) for _ in range(len(A))]
    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(B)):
                C[i][j] += A[i][k] * B[k][j]
    return C

def extraer_diagonal(A):
    return [[A[i][j] if i == j else Fraction(0) for j in range(len(A[0]))] for i in range(len(A))]

# --- CONTROLADOR DEL MENÚ ---

def preguntar_guardar_memoria(resultado, memoria):
    """Permite encadenar cálculos guardando el resultado en A o B."""
    print(f"\n{util.Color.YELLOW}¿Querés guardar este resultado para la siguiente operación?{util.Color.END}")
    opc = input("Guardar en (A) / Guardar en (B) / (N)o guardar: ").strip().upper()
    if opc == 'A':
        memoria['A'] = resultado
        util.imprimir_exito("Resultado guardado exitosamente como la nueva Matriz A.")
    elif opc == 'B':
        memoria['B'] = resultado
        util.imprimir_exito("Resultado guardado exitosamente como la nueva Matriz B.")

def ejecutar(memoria):
    util.limpiar_pantalla()
    print(f"{util.Color.CYAN}{util.Color.BOLD}--- SESIÓN 1 y 9: OPERACIONES BÁSICAS Y PROPIEDADES ---{util.Color.END}")
    print("1. Sumar (A + B)")
    print("2. Restar (A - B) o (B - A)")
    print("3. Multiplicar Matrices (A * B) + Demostración de Teorema")
    print("4. Transpuesta (A^T o B^T)")
    print("5. Multiplicar por un Escalar (c * A o c * B)")
    print("6. Matriz Diagonal")
    print(f"{util.Color.RED}0. Regresar al Menú Principal{util.Color.END}")

    sub = input("\nSeleccione la operación >> ")

    if sub == '0':
        return

    try:
        resultado = None
        
        if sub == '1':
            if not memoria['A'] or not memoria['B']:
                raise ValueError("Necesitás cargar ambas matrices (A y B) desde el menú principal.")
            resultado = sumar(memoria['A'], memoria['B'])
            util.imprimir_matriz(resultado, "Resultado A + B")

        elif sub == '2':
            if not memoria['A'] or not memoria['B']:
                raise ValueError("Necesitás cargar ambas matrices (A y B).")
            orden = input("¿Qué querés restar? (1) A - B  (2) B - A : ")
            if orden == '1':
                resultado = restar(memoria['A'], memoria['B'])
                util.imprimir_matriz(resultado, "Resultado A - B")
            elif orden == '2':
                resultado = restar(memoria['B'], memoria['A'])
                util.imprimir_matriz(resultado, "Resultado B - A")

        elif sub == '3':
            if not memoria['A'] or not memoria['B']:
                raise ValueError("Necesitás cargar ambas matrices (A y B).")
            resultado = producto_matricial(memoria['A'], memoria['B'])
            util.imprimir_matriz(resultado, "Resultado A * B")
            
            # --- TEOREMA EN VIVO (SESIÓN 9) ---
            util.imprimir_teorema("9", "Propiedad de la Transpuesta en el Producto: (A*B)^T = B^T * A^T")
            AB_T = transpuesta(resultado)
            BT_AT = producto_matricial(transpuesta(memoria['B']), transpuesta(memoria['A']))
            
            util.imprimir_matriz(AB_T, "(A * B)^T")
            util.imprimir_matriz(BT_AT, "B^T * A^T")
            
            if AB_T == BT_AT:
                util.imprimir_exito("Como podemos observar, ambas matrices son idénticas. Propiedad demostrada.")
            else:
                util.imprimir_error("Las matrices no coinciden.")

        elif sub in ['4', '5', '6']:
            letra = input("¿A cuál matriz querés aplicarle la operación? (A / B): ").strip().upper()
            M = memoria.get(letra)
            if not M:
                raise ValueError(f"La Matriz {letra} está vacía. Cargala primero.")
                
            if sub == '4':
                resultado = transpuesta(M)
                util.imprimir_matriz(resultado, f"Transpuesta de {letra}^T")
                
            elif sub == '5':
                val = input("Ingrese el valor del escalar (ej. 2 o -1/3): ")
                c = Fraction(val)
                resultado = mult_escalar(c, M)
                util.imprimir_matriz(resultado, f"Escalar {c} * {letra}")
                
            elif sub == '6':
                resultado = extraer_diagonal(M)
                util.imprimir_matriz(resultado, f"Diagonal de {letra}")

        if resultado:
            preguntar_guardar_memoria(resultado, memoria)

    except Exception as e:
        util.imprimir_error(str(e))
    
    input(f"\n{util.Color.CYAN}Presiona ENTER para regresar...{util.Color.END}")