import sys
from fractions import Fraction
from modulos import utilidades as util
from modulos import sesion_01_09_operaciones as op_basicas
from modulos import sesion_03_04_gauss as gauss
from modulos import sesion_10_11_det_inversa as det_inversa
from modulos import sesion_02_07_08_sistemas as sistemas
from modulos import sesion_05_06_vectores as vectores
from modulos import modulo_matrices as mod_profe

# Memoria global del sistema
memoria = {
    'A': None,
    'B': None
}

def obtener_estado_matriz(matriz):
    if matriz is None:
        return f"{util.Color.RED}Vacía{util.Color.END}"
    filas = len(matriz)
    cols = len(matriz[0])
    return f"{util.Color.GREEN}Cargada ({filas}x{cols}){util.Color.END}"

def mostrar_encabezado():
    util.limpiar_pantalla()
    print(f"{util.Color.GREEN}{util.Color.BOLD}")
    print(r"""
     __  __       _                  _            
    |  \/  | ___ | |_ ___  _ __   __| | ___       
    | |\/| |/ _ \| __/ _ \| '__| / _` |/ _ \      
    | |  | | (_) | || (_) | |   | (_| |  __/      
    |_|  |_|\___/ \__\___/|_|    \__,_|\___|      
    """)
    print(f"       MOTOR DE ÁLGEBRA LINEAL (UAM) {util.Color.END}")
    print(f"{util.Color.CYAN}========================================================={util.Color.END}")
    print(f"{util.Color.BOLD}[ESTADO DE MEMORIA]{util.Color.END}")
    print(f"Matriz A: {obtener_estado_matriz(memoria['A'])}  |  Matriz B: {obtener_estado_matriz(memoria['B'])}")
    print(f"{util.Color.CYAN}========================================================={util.Color.END}")

def ingresar_matriz(nombre):
    print(f"\n{util.Color.BOLD}--- Ingresando Matriz {nombre} ---{util.Color.END}")
    try:
        filas = int(input("Número de filas: "))
        cols = int(input("Número de columnas: "))
        
        matriz = []
        print(f"Ingrese los valores (soporta enteros o fracciones como 1/2):")
        for i in range(filas):
            fila = []
            for j in range(cols):
                valor = input(f"Elemento {util.Color.YELLOW}[{i+1}][{j+1}]{util.Color.END}: ")
                fila.append(Fraction(valor))
            matriz.append(fila)
            
        memoria[nombre] = matriz
        util.imprimir_exito(f"Matriz {nombre} guardada en memoria.")
    except ValueError:
        util.imprimir_error("Entrada inválida. Usa números enteros o fracciones (ej. 3/4).")

def pausa():
    input(f"\n{util.Color.CYAN}Presiona ENTER para continuar...{util.Color.END}")

def main():
    while True:
        mostrar_encabezado()
        print(f"\n{util.Color.BOLD}MENÚ DEL SÍLABO{util.Color.END}")
        print("1. Cargar / Editar Matrices en Memoria (A o B)")
        print("2. Sesión 1 y 9: Operaciones Básicas y Propiedades (+, -, *, Transpuesta)")
        print("3. Sesión 3 y 4: Forma Escalonada y Existencia (Gauss-Jordan y RREF)")
        print("4. Sesión 2, 7 y 8: Sistemas de Ecuaciones Lineales y Aplicaciones")
        print("5. Sesión 5 y 6: Ecuaciones Vectoriales, C.L. e Independencia Lineal")
        print("6. Sesión 10 y 11: Determinantes, Inversas y Propiedades")
        print(f"{util.Color.YELLOW}7. Evaluación Profe: Módulo III (Archivo Único){util.Color.END}") 
        print(f"{util.Color.RED}0. Salir{util.Color.END}")
        
        opc = input(f"\nSeleccione un módulo >> ")
        
        if opc == '0':
            util.limpiar_pantalla()
            print(f"{util.Color.GREEN}Saliendo de la calculadora... ¡Éxito con el profe!{util.Color.END}\n")
            sys.exit()
            
        elif opc == '1':
            letra = input("¿Cuál matriz querés cargar o editar? (A / B): ").strip().upper()
            if letra in ['A', 'B']:
                ingresar_matriz(letra)
                if memoria[letra]:
                    util.imprimir_matriz(memoria[letra], f"Matriz {letra}")
            else:
                util.imprimir_error("Solo podés seleccionar A o B.")
            pausa()
            
        elif opc == '2':
            op_basicas.ejecutar(memoria)
            
        elif opc == '3':
            gauss.ejecutar(memoria)
            
        elif opc == '4':
            sistemas.ejecutar(memoria)
            
        elif opc == '5':
            vectores.ejecutar(memoria)
            
        elif opc == '6':
            det_inversa.ejecutar(memoria)
            
        elif opc == '7':
            util.limpiar_pantalla()
            print(f"{util.Color.CYAN}{util.Color.BOLD}--- EVALUACIÓN: MÓDULO III (modulos/modulo_matrices.py) ---{util.Color.END}")
            print("Demostración de que el archivo único exigido existe y funciona de forma independiente.")
            
            try:
                # Usamos la Matriz A y B de la memoria general para no tener que volver a escribirlas
                A = memoria.get('A')
                B = memoria.get('B')
                
                if not A or not B:
                    raise ValueError("Por favor, cargá la Matriz A y B en la Opción 1 primero.")
                    
                print("\n1. Demostrar Validaciones y Operaciones (A + B, A * B)")
                print("2. Demostrar Determinante e Inversa (Gauss/Adjunta)")
                print("3. Ejecutar Verificador de Propiedades")
                
                sub_profe = input("\nSeleccione qué evaluará el profesor >> ")
                
                if sub_profe == '1':
                    print("\nProbando Suma (A + B):")
                    util.imprimir_matriz(mod_profe.suma(A, B))
                    print("\nProbando Multiplicación (A * B):")
                    util.imprimir_matriz(mod_profe.producto_matricial(A, B))
                    
                elif sub_profe == '2':
                    print(f"\nDeterminante de A (Cofactores): {mod_profe.determinante_cofactores(A)}")
                    print(f"Determinante de A (Triangular): {mod_profe.determinante_triangular(A)}")
                    
                    inv_gj, diag = mod_profe.inversa_gauss_jordan(A)
                    util.imprimir_matriz(inv_gj, "Inversa por Gauss-Jordan")
                    print(f"{util.Color.YELLOW}{diag}{util.Color.END}")
                    
                    util.imprimir_matriz(mod_profe.inversa_adjunta(A), "Inversa por Adjunta")
                    
                elif sub_profe == '3':
                    print("\nCorriendo Verificador de las 6 Propiedades (Rúbrica)...")
                    resultados = mod_profe.verificar_propiedades(A, B)
                    for prop, estado in resultados:
                        if estado:
                            util.imprimir_exito(f"VERIFICADO: {prop}")
                        else:
                            util.imprimir_error(f"FALLÓ o NO APLICABLE: {prop}")
                        
            except Exception as e:
                util.imprimir_error(str(e))
            
            pausa()

if __name__ == "__main__":
    main()