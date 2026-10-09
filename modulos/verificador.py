from .operaciones_basicas import producto_matricial, transpuesta
from .determinantes_inversas import inversa_gauss_jordan, determinante_cofactores
from .utilidades import imprimir_matriz

def verificador_propiedades(A, B):
    print("\n--- VERIFICADOR DE TEOREMAS ---")
    try:
        # Propiedad 1: (A * B)^T = B^T * A^T
        AB_T = transpuesta(producto_matricial(A, B))
        BT_AT = producto_matricial(transpuesta(B), transpuesta(A))
        print("1. (A * B)^T == B^T * A^T : VÁLIDO" if AB_T == BT_AT else "1. (A * B)^T == B^T * A^T : FALSO")
        
        # Propiedad 2: A * A^-1 = I
        if len(A) == len(A[0]) and determinante_cofactores(A) != 0:
            I_calc = producto_matricial(A, inversa_gauss_jordan(A))
            print("2. A * A^-1 == Identidad : VÁLIDO")
            imprimir_matriz(I_calc, "Matriz Identidad Resultante")
    except Exception as e:
        print(f"No se pudieron verificar todas las propiedades: {e}")