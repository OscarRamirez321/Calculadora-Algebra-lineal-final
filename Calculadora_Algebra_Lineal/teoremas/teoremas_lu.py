"""Teoremas clave de la Factorización LU para la opción 0 del módulo LU.
Texto que se muestra en pantalla: existencia, multiplicadores, doble sustitución y
relación con el determinante. Unidad: Módulo III, Álgebra Lineal (MTM0120).
Elaborado por: [Integrantes del grupo: completar nombres].
"""

# Cada elemento es (título, líneas). La interfaz decide cómo dibujarlos.
TEOREMAS_LU = [
    ("Existencia de la factorización A = LU", [
        "Si A (m × n) se reduce a forma escalonada U usando solo operaciones de",
        "reemplazo de fila Fi ← Fi − l·Fj (sin intercambios), entonces A = LU.",
        "L es triangular inferior m × m con unos en la diagonal; U es m × n escalonada.",
        "Si algún pivote es 0 y hace falta intercambiar filas, se necesita PA = LU.",
    ]),
    ("Multiplicadores de L", [
        "l = (elemento a eliminar) / (pivote). Cada l se guarda en la posición (i, j) de L.",
        "Las operaciones de fila que llevan A a U son las mismas que llevan L a I.",
        "Por eso L registra ordenadamente toda la eliminación.",
    ]),
    ("Resolver Ax = b con la factorización", [
        "Como A = LU, el sistema Ax = b equivale a L(Ux) = b. Se hace en dos etapas:",
        "  1. Sustitución hacia adelante: resolver Ly = b para hallar y.",
        "  2. Sustitución hacia atrás:    resolver Ux = y para hallar x.",
        "Comprobación: A·x = b.",
    ]),
    ("Unicidad y determinante", [
        "Si A es invertible y admite LU, la factorización con unos en la diagonal de L es única.",
        "Sin intercambios de fila: det(A) = det(L)·det(U) = producto de la diagonal de U.",
        "Si U tiene un 0 en la diagonal, A es singular y Ax = b no tiene solución única.",
    ]),
]
