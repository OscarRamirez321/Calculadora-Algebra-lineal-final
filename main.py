import sys
from fractions import Fraction

from modulos import utilidades as util
from modulos import operaciones_basicas as op
from modulos import reduccion_gauss as gauss
from modulos import determinantes_inversas as det_inv
from modulos import verificador as verif
from modulos import operaciones_avanzadas as adv
from modulos import sistemas_ecuaciones as sis

# Variable global para guardar la memoria de la calculadora
ultimo_resultado = None

def mostrar_logo():
    util.limpiar_pantalla()
    logo = f"""{util.Color.GREEN}{util.Color.BOLD}
     _____       _            _           _                 
    / ____|     | |          | |         | |                
   | |     __ _ | | ___ _   _| | __ _  __| | ___  _ __ __ _ 
   | |    / _` || |/ __| | | | |/ _` |/ _` |/ _ \| '__/ _` |
   | |___| (_| || | (__| |_| | | (_| | (_| | (_) | | | (_| |
    \_____\__,_||_|\___|\__,_|_|\__,_|\__,_|\___/|_|  \__,_|
    {util.Color.END}"""
    print(logo)
    print(f"{util.Color.CYAN}" + "=" * 60 + f"{util.Color.END}")
    print(f"{util.Color.BOLD} CALCULADORA MODULAR DE ÁLGEBRA MATRICIAL (VERSIÓN PRO) {util.Color.END}")
    print(f"{util.Color.CYAN}" + "=" * 60 + f"{util.Color.END}")

def ingresar_matriz(nombre, una_columna=False):
    global ultimo_resultado
    
    # Si hay una matriz guardada en memoria, te pregunta si la querés usar
    if ultimo_resultado is not None:
        usar_mem = input(f"\n¿Querés usar el ÚLTIMO RESULTADO en memoria para la Matriz {nombre}? (s/n): ").strip().lower()
        if usar_mem == 's':
            print(f"{util.Color.GREEN}✔ Matriz {nombre} cargada desde la memoria.{util.Color.END}")
            return ultimo_resultado

    # Si elegís 'n' o no hay memoria, te pide los datos normales
    print(f"\n{util.Color.BOLD}--- Ingresando {nombre} ---{util.Color.END}")
    filas = int(input("Número de filas: "))
    columnas = 1 if una_columna else int(input("Número de columnas: "))
    
    matriz = []
    print(f"Ingrese los valores (puede usar enteros o fracciones como 1/2):")
    for i in range(filas):
        fila = []
        for j in range(columnas):
            valor = input(f"Elemento {util.Color.YELLOW}[{i+1}][{j+1}]{util.Color.END}: ")
            fila.append(Fraction(valor))
        matriz.append(fila)

    return matriz

def pausa():
    input(f"\n{util.Color.CYAN}Presiona ENTER para continuar...{util.Color.END}")

def main():
    global ultimo_resultado
    while True:
        mostrar_logo()
        print(f"\n{util.Color.BOLD}MENÚ PRINCIPAL{util.Color.END}")
        print("1. Operaciones Básicas (+, -, *, Transpuesta)")
        print("2. Determinantes e Inversas")
        print("3. Reducción Gauss-Jordan")
        print("4. Herramientas Avanzadas (Rango, Potencia, LU, Triangular)")
        print("5. Resolver Sistemas de Ecuaciones (Ax = b)")
        print("6. Verificador de Propiedades")
        print(f"{util.Color.RED}0. Salir{util.Color.END}")
        
        opc = input(f"\nSelecciona un módulo {util.Color.YELLOW}>>{util.Color.END} ")
        
        if opc == '0':
            util.limpiar_pantalla()
            print(f"{util.Color.GREEN}Saliendo del sistema... ¡Éxito en la defensa!{util.Color.END}\n")
            break
            
        util.limpiar_pantalla()
        
        if opc == '1':
            print(f"{util.Color.CYAN}--- Módulo de Operaciones Básicas ---{util.Color.END}")
            print("1. Suma | 2. Resta | 3. Multiplicación | 4. Transpuesta")
            sub = input(f"Elige la operación {util.Color.YELLOW}>>{util.Color.END} ")
            
            try:
                A = ingresar_matriz("Matriz A")
                if sub in ['1', '2', '3']:
                    B = ingresar_matriz("Matriz B")
                    
                if sub == '1':
                    res = op.suma(A, B)
                    util.imprimir_matriz(res, "Suma: A + B")
                    ultimo_resultado = res
                elif sub == '2':
                    res = op.resta(A, B)
                    util.imprimir_matriz(res, "Resta: A - B")
                    ultimo_resultado = res
                elif sub == '3':
                    res = op.producto_matricial(A, B)
                    util.imprimir_matriz(res, "Producto: A * B")
                    ultimo_resultado = res
                elif sub == '4':
                    res = op.transpuesta(A)
                    util.imprimir_matriz(res, "Transpuesta de A")
                    ultimo_resultado = res
                    
                print(f"{util.Color.GREEN}✔ Resultado guardado en memoria.{util.Color.END}")
            except Exception as e: util.imprimir_error(e)
            pausa()
                
        elif opc == '2':
            print(f"{util.Color.CYAN}--- Módulo de Determinantes e Inversas ---{util.Color.END}")
            A = ingresar_matriz("Matriz Cuadrada A")
            try:
                det = det_inv.determinante_cofactores(A)
                util.imprimir_exito(f"Determinante calculado: {det}")
                if det != 0:
                    inv = det_inv.inversa_gauss_jordan(A)
                    util.imprimir_matriz(inv, "Matriz Inversa")
                    ultimo_resultado = inv
                    print(f"{util.Color.GREEN}✔ Matriz inversa guardada en memoria.{util.Color.END}")
                else:
                    util.imprimir_error("La matriz es singular (det = 0). No tiene inversa.")
            except Exception as e: util.imprimir_error(e)
            pausa()
                
        elif opc == '3':
            print(f"{util.Color.CYAN}--- Módulo de Reducción Gauss-Jordan ---{util.Color.END}")
            A = ingresar_matriz("Matriz A")
            try:
                rref, piv, lib = gauss.gauss_jordan(A)
                util.imprimir_matriz(rref, "Matriz RREF")
                ultimo_resultado = rref
                print(f"Pivotes: {util.Color.YELLOW}{piv}{util.Color.END} | Variables Libres: {util.Color.YELLOW}{lib}{util.Color.END}")
                print(f"{util.Color.GREEN}✔ Matriz RREF guardada en memoria.{util.Color.END}")
            except Exception as e: util.imprimir_error(e)
            pausa()

        elif opc == '4':
            print(f"{util.Color.CYAN}--- Herramientas Avanzadas ---{util.Color.END}")
            print("1. Rango | 2. Potencia | 3. Triangular | 4. LU")
            sub_opc = input(f"Elige la herramienta {util.Color.YELLOW}>>{util.Color.END} ")
            
            try:
                A = ingresar_matriz("Matriz A")
                if sub_opc == '1':
                    util.imprimir_exito(f"El Rango de la matriz es: {adv.rango_matriz(A)}")
                elif sub_opc == '2':
                    pot = int(input("Elevar a la potencia: "))
                    res = adv.potencia_matriz(A, pot)
                    util.imprimir_matriz(res, f"A^{pot}")
                    ultimo_resultado = res
                    print(f"{util.Color.GREEN}✔ Resultado guardado en memoria.{util.Color.END}")
                elif sub_opc == '3':
                    res = adv.matriz_triangular_superior(A)
                    util.imprimir_matriz(res, "Matriz Triangular Superior")
                    ultimo_resultado = res
                    print(f"{util.Color.GREEN}✔ Resultado guardado en memoria.{util.Color.END}")
                elif sub_opc == '4':
                    L, U = adv.factorizacion_lu(A)
                    util.imprimir_matriz(L, "Matriz L (Inferior)")
                    util.imprimir_matriz(U, "Matriz U (Superior)")
                    print(f"{util.Color.YELLOW}Nota: No se guardó en memoria al ser dos matrices separadas.{util.Color.END}")
            except Exception as e: util.imprimir_error(e)
            pausa()

        elif opc == '5':
            print(f"{util.Color.CYAN}--- Resolución de Sistemas (Ax = b) ---{util.Color.END}")
            try:
                A = ingresar_matriz("Matriz de Coeficientes (A)")
                b = ingresar_matriz("Vector de Resultados (b)", una_columna=True)
                sol, msg = sis.resolver_sistema_ax_b(A, b)
                if sol:
                    util.imprimir_exito(msg)
                    util.imprimir_matriz(sol, "Solución (Valores)")
                else:
                    util.imprimir_error(msg)
            except Exception as e: util.imprimir_error(e)
            pausa()
            
        elif opc == '6':
            print(f"{util.Color.CYAN}--- Verificador de Propiedades ---{util.Color.END}")
            try:
                A = ingresar_matriz("Matriz A")
                B = ingresar_matriz("Matriz B")
                verif.verificador_propiedades(A, B)
            except Exception as e: util.imprimir_error(e)
            pausa()

if __name__ == "__main__":
    main()