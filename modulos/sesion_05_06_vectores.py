from fractions import Fraction
from modulos import utilidades as util
from modulos.sesion_03_04_gauss import gauss_jordan_paso_a_paso
from modulos.sesion_02_07_08_sistemas import construir_aumentada

# --- CONTROLADOR DEL MENÚ ---

def ejecutar(memoria):
    util.limpiar_pantalla()
    print(f"{util.Color.CYAN}{util.Color.BOLD}--- SESIÓN 5 y 6: VECTORES Y COMBINACIÓN LINEAL ---{util.Color.END}")
    print(f"{util.Color.YELLOW}Nota: Las columnas de la Matriz A serán tratadas como tu conjunto de vectores (v1, v2, ..., vk).{util.Color.END}")
    print("1. Evaluar Independencia Lineal (Sistema Homogéneo Ax = 0)")
    print("2. Verificar si un vector 'b' es Combinación Lineal (Ax = b)")
    print(f"{util.Color.RED}0. Regresar al Menú Principal{util.Color.END}")

    sub = input("\nSeleccione la operación >> ")
    if sub == '0': return

    try:
        M = memoria.get('A')
        if not M:
            raise ValueError("Primero debes cargar la Matriz A en el Menú Principal (sus columnas serán los vectores).")

        filas_a = len(M)
        cols_a = len(M[0]) # Cantidad de vectores

        if sub == '1':
            print(f"\n{util.Color.BOLD}Planteando sistema homogéneo (c1*v1 + c2*v2 + ... + ck*vk = 0)...{util.Color.END}")
            
            # Construir vector de ceros
            b_ceros = [[Fraction(0)] for _ in range(filas_a)]
            aumentada = construir_aumentada(M, b_ceros)
            
            # Reducir matriz
            rref, pivotes, libres, _ = gauss_jordan_paso_a_paso(aumentada)
            util.imprimir_matriz(rref, "Matriz Reducida (RREF)")
            
            print(f"Vectores analizados (Columnas): {cols_a}")
            print(f"Pivotes encontrados: {util.Color.YELLOW}{pivotes}{util.Color.END}")
            
            if libres == 0:
                print(f"\n{util.Color.GREEN}✅ Veredicto: LINEALMENTE INDEPENDIENTES (L.I.){util.Color.END}")
                print("La única forma de obtener el vector cero es con escalares c = 0 (Solución trivial).")
            else:
                print(f"\n{util.Color.RED}❌ Veredicto: LINEALMENTE DEPENDIENTES (L.D.){util.Color.END}")
                print(f"Hay {libres} variable(s) libre(s). Existen infinitas combinaciones que dan el vector cero.")

        elif sub == '2':
            print(f"\n{util.Color.BOLD}--- Ingresando Vector 'b' a verificar ---{util.Color.END}")
            print(f"El vector debe tener {filas_a} componentes (igual que los vectores de A).")
            
            vector_b = []
            for i in range(filas_a):
                val = input(f"Componente b[{i+1}]: ")
                vector_b.append([Fraction(val)])
                
            aumentada = construir_aumentada(M, vector_b)
            rref, pivotes, libres, _ = gauss_jordan_paso_a_paso(aumentada)
            
            util.imprimir_matriz(rref, "Matriz Reducida [Vectores | b]")
            
            # Analizar inconsistencia para ver si es Combinación Lineal
            inconsistente = False
            for i in range(filas_a):
                todo_cero = all(rref[i][j] == Fraction(0) for j in range(cols_a))
                if todo_cero and rref[i][-1] != Fraction(0):
                    inconsistente = True
                    break
                    
            if inconsistente:
                print(f"\n{util.Color.RED}❌ RESULTADO: El vector 'b' NO ES combinación lineal de los vectores dados.{util.Color.END}")
                print("El sistema es incompatible (No existen escalares que formen a 'b').")
            else:
                print(f"\n{util.Color.GREEN}✅ RESULTADO: El vector 'b' SÍ ES una combinación lineal.{util.Color.END}")
                if libres == 0:
                    print("El vector 'b' se forma de una ÚNICA MANERA con los siguientes escalares:")
                    for i in range(cols_a):
                        print(f"  c_{i+1} = {rref[i][-1]}")
                else:
                    print("El vector 'b' se puede armar de INFINITAS MANERAS (Sistema compatible indeterminado).")

    except Exception as e:
        util.imprimir_error(str(e))
    
    input(f"\n{util.Color.CYAN}Presiona ENTER para regresar...{util.Color.END}")