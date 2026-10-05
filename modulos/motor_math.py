from fractions import Fraction


def imprimir_matriz(matriz, mensaje=""):
    """Imprime cualquier matriz de forma normal."""

    if mensaje:
        print(f"\n{mensaje}")

    for fila in matriz:
        fila_str = [f"{str(val):>8}" for val in fila]
        print(f"  [ {' '.join(fila_str)} ]")

    print()


def imprimir_matriz_aumentada(matriz, mensaje=""):
    """Imprime una matriz aumentada separando la última columna."""

    if mensaje:
        print(f"\n{mensaje}")

    for fila in matriz:
        fila_str = [f"{str(val):>8}" for val in fila[:-1]]
        termino_ind = f"| {str(fila[-1]):>8}"

        print(
            f"  [ {' '.join(fila_str)} {termino_ind} ]"
        )

    print()


def gauss_jordan(m, n, A, silencioso=False):
    """
    Ejecuta Gauss-Jordan sobre una matriz aumentada.
    Devuelve la matriz reducida y las columnas pivote.
    """

    if not silencioso:
        imprimir_matriz_aumentada(
            A,
            "--- Matriz Aumentada Inicial ---"
        )

    fila_actual = 0
    col_actual = 0
    columnas_pivote = []

    while fila_actual < m and col_actual < n:

        idx_pivote = fila_actual

        while (
            idx_pivote < m
            and A[idx_pivote][col_actual] == 0
        ):
            idx_pivote += 1

        if idx_pivote == m:
            col_actual += 1
            continue

        if idx_pivote != fila_actual:

            A[fila_actual], A[idx_pivote] = (
                A[idx_pivote],
                A[fila_actual]
            )

            if not silencioso:
                imprimir_matriz_aumentada(
                    A,
                    f"Intercambio: Fila {fila_actual + 1} "
                    f"con {idx_pivote + 1}"
                )

        pivote = A[fila_actual][col_actual]

        # Convertir el pivote en 1
        for j in range(col_actual, n + 1):
            A[fila_actual][j] /= pivote

        columnas_pivote.append(col_actual)

        # Hacer ceros arriba y abajo del pivote
        for i in range(m):

            if (
                i != fila_actual
                and A[i][col_actual] != 0
            ):

                factor = A[i][col_actual]

                for j in range(col_actual, n + 1):
                    A[i][j] -= (
                        factor * A[fila_actual][j]
                    )

        fila_actual += 1
        col_actual += 1

    return A, columnas_pivote


def multiplicar_matriz_vector(A, v):
    """Multiplica una matriz A por un vector v."""

    m = len(A)
    n = len(A[0])

    resultado = []

    for i in range(m):

        suma = Fraction(0)

        for j in range(n):
            suma += A[i][j] * v[j]

        resultado.append(suma)

    return resultado


def sumar_matrices(A, B):
    """Suma dos matrices del mismo tamaño."""

    filas = len(A)
    columnas = len(A[0])

    resultado = []

    for i in range(filas):

        fila = []

        for j in range(columnas):
            fila.append(A[i][j] + B[i][j])

        resultado.append(fila)

    return resultado


def restar_matrices(A, B):
    """Resta dos matrices del mismo tamaño."""

    filas = len(A)
    columnas = len(A[0])

    resultado = []

    for i in range(filas):

        fila = []

        for j in range(columnas):
            fila.append(A[i][j] - B[i][j])

        resultado.append(fila)

    return resultado


def multiplicar_matrices(A, B):
    """
    Multiplica dos matrices.
    Las columnas de A deben coincidir
    con las filas de B.
    """

    filas_A = len(A)
    columnas_A = len(A[0])

    filas_B = len(B)
    columnas_B = len(B[0])

    if columnas_A != filas_B:
        raise ValueError(
            "No se pueden multiplicar las matrices: "
            "las dimensiones no son compatibles."
        )

    resultado = []

    for i in range(filas_A):

        fila = []

        for j in range(columnas_B):

            suma = Fraction(0)

            for k in range(columnas_A):
                suma += A[i][k] * B[k][j]

            fila.append(suma)

        resultado.append(fila)

    return resultado


def multiplicar_matriz_escalar(A, c):
    """Multiplica una matriz por un escalar."""

    resultado = []

    for fila in A:

        nueva_fila = []

        for valor in fila:
            nueva_fila.append(c * valor)

        resultado.append(nueva_fila)

    return resultado


def traspuesta(A):
    """Calcula la matriz traspuesta de A."""

    filas = len(A)
    columnas = len(A[0])

    resultado = []

    for j in range(columnas):

        fila = []

        for i in range(filas):
            fila.append(A[i][j])

        resultado.append(fila)

    return resultado


def matriz_identidad(n):
    """Crea una matriz identidad de tamaño n x n."""

    identidad = []

    for i in range(n):

        fila = []

        for j in range(n):

            if i == j:
                fila.append(Fraction(1))
            else:
                fila.append(Fraction(0))

        identidad.append(fila)

    return identidad


def determinante(A):
    """
    Calcula el determinante de una matriz cuadrada
    mediante eliminación de Gauss.
    """

    n = len(A)

    if n == 0:
        return Fraction(1)

    for fila in A:
        if len(fila) != n:
            raise ValueError(
                "El determinante solo existe "
                "para matrices cuadradas."
            )

    M = [
        [Fraction(valor) for valor in fila]
        for fila in A
    ]

    det = Fraction(1)

    for col in range(n):

        fila_pivote = col

        while (
            fila_pivote < n
            and M[fila_pivote][col] == 0
        ):
            fila_pivote += 1

        if fila_pivote == n:
            return Fraction(0)

        # Si intercambiamos filas, cambia el signo
        if fila_pivote != col:

            M[col], M[fila_pivote] = (
                M[fila_pivote],
                M[col]
            )

            det *= -1

        pivote = M[col][col]

        det *= pivote

        # Hacer ceros debajo del pivote
        for i in range(col + 1, n):

            if M[i][col] != 0:

                factor = M[i][col] / pivote

                for j in range(col, n):
                    M[i][j] -= (
                        factor * M[col][j]
                    )

    return det


def inversa(A):
    """
    Calcula la matriz inversa mediante Gauss-Jordan.
    Devuelve None si la matriz no es invertible.
    """

    n = len(A)

    for fila in A:
        if len(fila) != n:
            raise ValueError(
                "La inversa solo existe para "
                "matrices cuadradas."
            )

    # Crear [A | I]
    aumentada = []

    identidad = matriz_identidad(n)

    for i in range(n):

        fila = []

        for valor in A[i]:
            fila.append(Fraction(valor))

        for valor in identidad[i]:
            fila.append(valor)

        aumentada.append(fila)

    # Gauss-Jordan manual para [A | I]
    fila_actual = 0
    col_actual = 0

    while (
        fila_actual < n
        and col_actual < n
    ):

        idx_pivote = fila_actual

        while (
            idx_pivote < n
            and aumentada[idx_pivote][col_actual] == 0
        ):
            idx_pivote += 1

        if idx_pivote == n:
            col_actual += 1
            continue

        if idx_pivote != fila_actual:
            aumentada[fila_actual], aumentada[idx_pivote] = (
                aumentada[idx_pivote],
                aumentada[fila_actual]
            )

        pivote = aumentada[fila_actual][col_actual]

        # Normalizar fila
        for j in range(2 * n):
            aumentada[fila_actual][j] /= pivote

        # Eliminar columna
        for i in range(n):

            if i != fila_actual:

                factor = aumentada[i][col_actual]

                if factor != 0:

                    for j in range(2 * n):
                        aumentada[i][j] -= (
                            factor
                            * aumentada[fila_actual][j]
                        )

        fila_actual += 1
        col_actual += 1

    # Si no quedaron pivotes en todas las columnas,
    # la matriz no es invertible.
    for i in range(n):

        for j in range(n):

            esperado = Fraction(1) if i == j else Fraction(0)

            if aumentada[i][j] != esperado:
                return None

    # Extraer la parte derecha
    resultado = []

    for i in range(n):

        fila = []

        for j in range(n, 2 * n):
            fila.append(aumentada[i][j])

        resultado.append(fila)

    return resultado


def potencia_matriz(A, exponente):
    """
    Calcula A^n mediante multiplicación de matrices.
    """

    n = len(A)

    for fila in A:
        if len(fila) != n:
            raise ValueError(
                "Las potencias de matrices "
                "requieren una matriz cuadrada."
            )

    if exponente < 0:
        inversa_A = inversa(A)

        if inversa_A is None:
            raise ValueError(
                "No se puede calcular una potencia negativa "
                "porque la matriz no es invertible."
            )

        return potencia_matriz(
            inversa_A,
            -exponente
        )

    resultado = matriz_identidad(n)

    base = [
        [Fraction(valor) for valor in fila]
        for fila in A
    ]

    # Exponenciación rápida
    while exponente > 0:

        if exponente % 2 == 1:
            resultado = multiplicar_matrices(
                resultado,
                base
            )

        base = multiplicar_matrices(
            base,
            base
        )

        exponente //= 2

    return resultado