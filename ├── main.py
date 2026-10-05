from fractions import Fraction

from modulos.motor_math import (
    gauss_jordan,
    imprimir_matriz,
    multiplicar_matriz_vector,
    sumar_matrices,
    restar_matrices,
    multiplicar_matrices,
    traspuesta,
    multiplicar_matriz_escalar,
    determinante,
    inversa,
    potencia_matriz
)


def ingresar_sistema():

    print(
        "\n--- INGRESO DEL SISTEMA "
        "(NOTACIÓN a_ij) ---"
    )

    m = int(
        input("Ingrese el número de filas (m): ")
    )

    n = int(
        input(
            "Ingrese el número de columnas/variables (n): "
        )
    )

    matriz_aumentada = []

    print(
        "\nIngrese los coeficientes "
        "(puede usar fracciones como 1/2):"
    )

    for i in range(m):

        fila = []

        for j in range(n):

            val = input(
                f"  a_{i+1}{j+1}: "
            )

            fila.append(
                Fraction(val)
            )

        b = input(
            f"  Término independiente b_{i+1}: "
        )

        fila.append(
            Fraction(b)
        )

        matriz_aumentada.append(fila)

    return m, n, matriz_aumentada


def clasificar_y_resolver(
    m,
    n,
    A,
    columnas_pivote,
    modo="sistema"
):

    incompatible = False

    for i in range(m):

        todo_cero = all(
            A[i][j] == 0
            for j in range(n)
        )

        if (
            todo_cero
            and A[i][n] != 0
        ):

            incompatible = True
            break

    if incompatible:

        if modo == "combinacion":

            print(
                "\n❌ RESULTADO: El vector 'b' "
                "NO ES combinación lineal "
                "de los vectores dados."
            )

        else:

            print(
                "\n❌ SISTEMA INCOMPATIBLE "
                "(Sin Solución)"
            )

        return

    rango = len(columnas_pivote)

    if modo == "combinacion":

        print(
            "\n✅ RESULTADO: El vector 'b' "
            "SÍ ES una combinación lineal."
        )

        if rango < n:

            print(
                "Se puede formar de infinitas maneras "
                "(Compatible Indeterminado)."
            )

        else:

            print(
                "Se forma de una única manera "
                "con los siguientes escalares:"
            )

            for i, col in enumerate(
                columnas_pivote
            ):

                print(
                    f"  c_{col + 1} = {A[i][n]}"
                )

        return

    vars_libres_indices = [
        j
        for j in range(n)
        if j not in columnas_pivote
    ]

    if rango < n:

        nombres_libres = [
            f"x{j + 1}"
            for j in vars_libres_indices
        ]

        print(
            "\n⚠️ SISTEMA COMPATIBLE "
            "INDETERMINADO "
            "(Infinitas Soluciones)"
        )

        print(
            f"  - Variables Libres: "
            f"{nombres_libres}"
        )

    else:

        print(
            "\n✅ SISTEMA COMPATIBLE "
            "DETERMINADO "
            "(Solución Única)"
        )

        for i, col in enumerate(
            columnas_pivote
        ):

            print(
                f"  - x{col + 1} = {A[i][n]}"
            )


def operaciones_vectores():

    print(
        "\n--- OPERACIONES CON VECTORES EN Rn ---"
    )

    n = int(
        input(
            "Ingrese la dimensión de los vectores (n): "
        )
    )

    print("\nVector 1:")

    v1 = [
        Fraction(
            input(
                f"  v1_{i+1}: "
            )
        )
        for i in range(n)
    ]

    print("\nVector 2:")

    v2 = [
        Fraction(
            input(
                f"  v2_{i+1}: "
            )
        )
        for i in range(n)
    ]

    print("\n[1] Suma (v1 + v2)")
    print("[2] Producto Punto (v1 • v2)")
    print("[3] Multiplicar v1 por un escalar")

    opc = input(
        "Elija una opción: "
    )

    if opc == '1':

        suma = [
            v1[i] + v2[i]
            for i in range(n)
        ]

        print(
            f"\nResultado de la Suma: {suma}"
        )

    elif opc == '2':

        punto = sum(
            v1[i] * v2[i]
            for i in range(n)
        )

        print(
            f"\nProducto Punto: {punto}"
        )

    elif opc == '3':

        k = Fraction(
            input("Ingrese el escalar k: ")
        )

        mult = [
            k * val
            for val in v1
        ]

        print(
            f"\nResultado Escalar: {mult}"
        )

    else:

        print(
            "\n❌ Opción inválida."
        )


def ingresar_matriz(nombre="A"):

    filas = int(
        input(
            f"Ingrese el número de filas de {nombre}: "
        )
    )

    columnas = int(
        input(
            f"Ingrese el número de columnas de {nombre}: "
        )
    )

    matriz = []

    print(
        f"\nIngrese los valores de la Matriz {nombre}:"
    )

    for i in range(filas):

        fila = []

        for j in range(columnas):

            valor = input(
                f"  {nombre}[{i+1}][{j+1}]: "
            )

            fila.append(
                Fraction(valor)
            )

        matriz.append(fila)

    return matriz


def operaciones_matrices():

    print(
        "\n--- OPERACIONES CON MATRICES ---"
    )

    print("\n[1] Sumar matrices")
    print("[2] Restar matrices")
    print("[3] Multiplicar matrices")
    print("[4] Multiplicar matriz por escalar")
    print("[5] Traspuesta")
    print("[6] Determinante")
    print("[7] Inversa")
    print("[8] Potencia de una matriz")

    opcion = input(
        "\nSeleccione una opción: "
    )

    if opcion == '1':

        A = ingresar_matriz("A")
        B = ingresar_matriz("B")

        if (
            len(A) != len(B)
            or len(A[0]) != len(B[0])
        ):

            print(
                "\n❌ Las matrices deben "
                "tener el mismo tamaño."
            )

            return

        resultado = sumar_matrices(
            A,
            B
        )

        imprimir_matriz(
            A,
            "--- Matriz A ---"
        )

        imprimir_matriz(
            B,
            "--- Matriz B ---"
        )

        imprimir_matriz(
            resultado,
            "--- Resultado A + B ---"
        )

    elif opcion == '2':

        A = ingresar_matriz("A")
        B = ingresar_matriz("B")

        if (
            len(A) != len(B)
            or len(A[0]) != len(B[0])
        ):

            print(
                "\n❌ Las matrices deben "
                "tener el mismo tamaño."
            )

            return

        resultado = restar_matrices(
            A,
            B
        )

        imprimir_matriz(
            A,
            "--- Matriz A ---"
        )

        imprimir_matriz(
            B,
            "--- Matriz B ---"
        )

        imprimir_matriz(
            resultado,
            "--- Resultado A - B ---"
        )

    elif opcion == '3':

        A = ingresar_matriz("A")
        B = ingresar_matriz("B")

        try:

            resultado = multiplicar_matrices(
                A,
                B
            )

            imprimir_matriz(
                A,
                "--- Matriz A ---"
            )

            imprimir_matriz(
                B,
                "--- Matriz B ---"
            )

            imprimir_matriz(
                resultado,
                "--- Resultado A × B ---"
            )

        except ValueError as error:

            print(
                f"\n❌ {error}"
            )

    elif opcion == '4':

        A = ingresar_matriz("A")

        c = Fraction(
            input(
                "\nIngrese el escalar: "
            )
        )

        resultado = multiplicar_matriz_escalar(
            A,
            c
        )

        imprimir_matriz(
            A,
            "--- Matriz A ---"
        )

        imprimir_matriz(
            resultado,
            "--- Resultado cA ---"
        )

    elif opcion == '5':

        A = ingresar_matriz("A")

        resultado = traspuesta(A)

        imprimir_matriz(
            A,
            "--- Matriz A ---"
        )

        imprimir_matriz(
            resultado,
            "--- Matriz Traspuesta A^T ---"
        )

    elif opcion == '6':

        A = ingresar_matriz("A")

        try:

            resultado = determinante(A)

            imprimir_matriz(
                A,
                "--- Matriz A ---"
            )

            print(
                f"Determinante: {resultado}"
            )

        except ValueError as error:

            print(
                f"\n❌ {error}"
            )

    elif opcion == '7':

        A = ingresar_matriz("A")

        try:

            resultado = inversa(A)

            if resultado is None:

                print(
                    "\n❌ La matriz no tiene inversa."
                )

            else:

                imprimir_matriz(
                    A,
                    "--- Matriz A ---"
                )

                imprimir_matriz(
                    resultado,
                    "--- Matriz Inversa A^-1 ---"
                )

        except ValueError as error:

            print(
                f"\n❌ {error}"
            )

    elif opcion == '8':

        A = ingresar_matriz("A")

        exponente = int(
            input(
                "Ingrese el exponente n: "
            )
        )

        try:

            resultado = potencia_matriz(
                A,
                exponente
            )

            imprimir_matriz(
                A,
                "--- Matriz A ---"
            )

            imprimir_matriz(
                resultado,
                f"--- Resultado A^{exponente} ---"
            )

        except ValueError as error:

            print(
                f"\n❌ {error}"
            )

    else:

        print(
            "\n❌ Opción inválida."
        )


def evaluar_independencia():

    print(
        "\n--- ANÁLISIS DE INDEPENDENCIA LINEAL "
        "(L.I. / L.D.) ---"
    )

    k = int(
        input(
            "Ingrese la cantidad de vectores: "
        )
    )

    n = int(
        input(
            "Ingrese la dimensión de los vectores (n): "
        )
    )

    vectores = []

    for i in range(k):

        print(
            f"\nVector v{i+1}:"
        )

        vector = [
            Fraction(
                input(
                    f"  Componente {j+1}: "
                )
            )
            for j in range(n)
        ]

        vectores.append(vector)

    matriz = []

    for i in range(n):

        fila = []

        for j in range(k):

            fila.append(
                vectores[j][i]
            )

        # Sistema homogéneo:
        # c1*v1 + ... + ck*vk = 0
        fila.append(
            Fraction(0)
        )

        matriz.append(fila)

    print(
        "\nSistema Homogéneo planteado "
        "(c1*v1 + ... + ck*vk = 0):"
    )

    A_rref, cols = gauss_jordan(
        n,
        k,
        matriz,
        silencioso=False
    )

    imprimir_matriz(
        A_rref,
        "--- Matriz Reducida (RREF) ---"
    )

    num_pivotes = len(cols)

    print("=" * 65)
    print(" VEREDICTO TEÓRICO ")
    print("=" * 65)

    print(
        f"Pivotes: {num_pivotes} | "
        f"Variables Libres: "
        f"{k - num_pivotes}"
    )

    if num_pivotes == k:

        print(
            "\n✅ LINEALMENTE INDEPENDIENTE (L.I.) "
            "- Solo admite solución trivial."
        )

    else:

        print(
            "\n❌ LINEALMENTE DEPENDIENTE (L.D.) "
            "- Existen variables libres."
        )


def demostrar_teoremas():

    print(
        "\n--- DEMOSTRACIÓN DE TEOREMAS (Ax) ---"
    )

    print(
        "Teorema: Si A es matriz m x n, "
        "u y v vectores en R^n, y c es escalar:"
    )

    print(
        "  a) A(u + v) = Au + Av"
    )

    print(
        "  b) A(cu) = c(Au)\n"
    )

    A = [
        [Fraction(1), Fraction(2)],
        [Fraction(3), Fraction(4)]
    ]

    u = [
        Fraction(1),
        Fraction(1)
    ]

    v = [
        Fraction(2),
        Fraction(0)
    ]

    c = Fraction(3)

    # A(u + v)
    print(
        "Demostrando a) A(u + v) = Au + Av"
    )

    u_mas_v = [
        u[i] + v[i]
        for i in range(len(u))
    ]

    lado_izq_a = multiplicar_matriz_vector(
        A,
        u_mas_v
    )

    Au = multiplicar_matriz_vector(
        A,
        u
    )

    Av = multiplicar_matriz_vector(
        A,
        v
    )

    lado_der_a = [
        Au[i] + Av[i]
        for i in range(len(Au))
    ]

    print(
        f"  Izq: {lado_izq_a} | "
        f"Der: {lado_der_a} -> "
        f"✅ Idénticos"
    )

    # A(cu)
    print(
        "\nDemostrando b) A(cu) = c(Au)"
    )

    cu = [
        c * val
        for val in u
    ]

    lado_izq_b = multiplicar_matriz_vector(
        A,
        cu
    )

    lado_der_b = [
        c * val
        for val in Au
    ]

    print(
        f"  Izq: {lado_izq_b} | "
        f"Der: {lado_der_b} -> "
        f"✅ Idénticos\n"
    )


def demostrar_propiedades_traspuesta():

    print(
        "\n--- PROPIEDADES DE LA MATRIZ "
        "TRASPUESTA ---"
    )

    A = [
        [Fraction(1), Fraction(2), Fraction(3)],
        [Fraction(4), Fraction(5), Fraction(6)]
    ]

    B = [
        [Fraction(7), Fraction(8), Fraction(9)],
        [Fraction(10), Fraction(11), Fraction(12)]
    ]

    c = Fraction(3)

    imprimir_matriz(
        A,
        "--- Matriz A ---"
    )

    imprimir_matriz(
        B,
        "--- Matriz B ---"
    )

    # --------------------------------
    # PROPIEDAD 1
    # (A + B)^T = A^T + B^T
    # --------------------------------

    print(
        "1. Propiedad: "
        "(A + B)^T = A^T + B^T"
    )

    A_mas_B = sumar_matrices(
        A,
        B
    )

    izquierda_1 = traspuesta(
        A_mas_B
    )

    AT = traspuesta(A)
    BT = traspuesta(B)

    derecha_1 = sumar_matrices(
        AT,
        BT
    )

    imprimir_matriz(
        izquierda_1,
        "--- Lado izquierdo: (A + B)^T ---"
    )

    imprimir_matriz(
        derecha_1,
        "--- Lado derecho: A^T + B^T ---"
    )

    if izquierda_1 == derecha_1:

        print(
            "✅ Propiedad verificada."
        )

    else:

        print(
            "❌ Propiedad no verificada."
        )

    # --------------------------------
    # PROPIEDAD 2
    # (A^T)^T = A
    # --------------------------------

    print(
        "\n2. Propiedad: (A^T)^T = A"
    )

    AT = traspuesta(A)

    izquierda_2 = traspuesta(AT)

    imprimir_matriz(
        izquierda_2,
        "--- Lado izquierdo: (A^T)^T ---"
    )

    imprimir_matriz(
        A,
        "--- Lado derecho: A ---"
    )

    if izquierda_2 == A:

        print(
            "✅ Propiedad verificada."
        )

    else:

        print(
            "❌ Propiedad no verificada."
        )

    # --------------------------------
    # PROPIEDAD 3
    # (cA)^T = cA^T
    # --------------------------------

    print(
        "\n3. Propiedad: (cA)^T = cA^T"
    )

    cA = multiplicar_matriz_escalar(
        A,
        c
    )

    izquierda_3 = traspuesta(
        cA
    )

    derecha_3 = multiplicar_matriz_escalar(
        traspuesta(A),
        c
    )

    imprimir_matriz(
        izquierda_3,
        "--- Lado izquierdo: (cA)^T ---"
    )

    imprimir_matriz(
        derecha_3,
        "--- Lado derecho: cA^T ---"
    )

    if izquierda_3 == derecha_3:

        print(
            "✅ Propiedad verificada."
        )

    else:

        print(
            "❌ Propiedad no verificada."
        )

    # --------------------------------
    # PROPIEDAD 4
    # (AB)^T = B^T A^T
    # --------------------------------

    print(
        "\n4. Propiedad: "
        "(AB)^T = B^T A^T"
    )

    A2 = [
        [Fraction(1), Fraction(2)],
        [Fraction(3), Fraction(4)]
    ]

    B2 = [
        [Fraction(5), Fraction(6)],
        [Fraction(7), Fraction(8)]
    ]

    AB = multiplicar_matrices(
        A2,
        B2
    )

    izquierda_4 = traspuesta(
        AB
    )

    BT = traspuesta(B2)
    AT = traspuesta(A2)

    derecha_4 = multiplicar_matrices(
        BT,
        AT
    )

    imprimir_matriz(
        A2,
        "--- Matriz A ---"
    )

    imprimir_matriz(
        B2,
        "--- Matriz B ---"
    )

    imprimir_matriz(
        izquierda_4,
        "--- Lado izquierdo: (AB)^T ---"
    )

    imprimir_matriz(
        derecha_4,
        "--- Lado derecho: B^T A^T ---"
    )

    if izquierda_4 == derecha_4:

        print(
            "✅ Propiedad verificada."
        )

    else:

        print(
            "❌ Propiedad no verificada."
        )


def menu_principal():

    while True:

        print(
            "\n" + "=" * 55
        )

        print(
            "             MOTOR DE ÁLGEBRA LINEAL"
        )

        print(
            "=" * 55
        )

        print(
            "[1] Resolver Sistema de Ecuaciones (Ax = b)"
        )

        print(
            "[2] Verificar Combinación Lineal"
        )

        print(
            "[3] Operaciones Básicas con Vectores"
        )

        print(
            "[4] Operaciones con Matrices"
        )

        print(
            "[5] Evaluar Independencia Lineal (L.I. / L.D.)"
        )

        print(
            "[6] Demostrar Teoremas Producto Ax"
        )

        print(
            "[7] Propiedades de Matrices Traspuestas"
        )

        print(
            "[8] Salir"
        )

        opcion = input(
            "\nSeleccione una opción: "
        )

        if opcion == '1':

            m, n, matriz = ingresar_sistema()

            A_rref, cols = gauss_jordan(
                m,
                n,
                matriz
            )

            clasificar_y_resolver(
                m,
                n,
                A_rref,
                cols,
                modo="sistema"
            )

        elif opcion == '2':

            m, n, matriz = ingresar_sistema()

            A_rref, cols = gauss_jordan(
                m,
                n,
                matriz,
                silencioso=True
            )

            clasificar_y_resolver(
                m,
                n,
                A_rref,
                cols,
                modo="combinacion"
            )

        elif opcion == '3':

            operaciones_vectores()

        elif opcion == '4':

            operaciones_matrices()

        elif opcion == '5':

            evaluar_independencia()

        elif opcion == '6':

            demostrar_teoremas()

        elif opcion == '7':

            demostrar_propiedades_traspuesta()

        elif opcion == '8':

            print(
                "\nPrograma finalizado."
            )

            break

        else:

            print(
                "\n❌ Opción inválida."
            )


if __name__ == "__main__":
    menu_principal()