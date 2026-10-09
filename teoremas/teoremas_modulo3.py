"""Teoremas clave del Módulo III (álgebra de matrices) para la opción 0 del menú.
Contiene el texto que se muestra en pantalla: Tarea 4, Sesión 10 (inversa),
Sesión 11 (determinantes) y Teorema de la Matriz Invertible.
Elaborado por: [Integrantes del grupo: completar nombres].
"""

# Cada elemento es (título, líneas). La interfaz decide cómo dibujarlos.
TEOREMAS_MODULO_3 = [
    ("Álgebra de matrices (Tarea 4)", [
        "Sean A, B, C del mismo tamaño y r, s escalares:",
        "  a) A + B = B + A             d) r(A + B) = rA + rB",
        "  b) (A + B) + C = A + (B + C) e) (r + s)A = rA + sA",
        "  c) A + 0 = A                 f) r(sA) = (rs)A",
        "Con tamaños compatibles para el producto:",
        "  A(BC) = (AB)C   A(B + C) = AB + AC   (B + C)A = BA + CA",
        "  r(AB) = (rA)B = A(rB)   I·A = A = A·I",
        "Advertencia: en general AB ≠ BA (el producto no es conmutativo).",
    ]),
    ("Propiedades de la transpuesta", [
        "  a) (Aᵀ)ᵀ = A              c) (rA)ᵀ = r·Aᵀ",
        "  b) (A + B)ᵀ = Aᵀ + Bᵀ     d) (AB)ᵀ = BᵀAᵀ  (el orden se invierte)",
    ]),
    ("Teorema de la inversa (Sesión 10)", [
        "  a) Si A es invertible, A⁻¹ es invertible y (A⁻¹)⁻¹ = A.",
        "  b) Si A y B son n×n invertibles, AB es invertible y (AB)⁻¹ = B⁻¹A⁻¹.",
        "  c) Si A es invertible, Aᵀ es invertible y (Aᵀ)⁻¹ = (A⁻¹)ᵀ.",
    ]),
    ("Determinantes (Sesión 11)", [
        "  • Expansión por cofactores: det(A) = Σ aᵢⱼ·Cᵢⱼ, con Cᵢⱼ = (-1)^(i+j)·det(Mᵢⱼ).",
        "  • Si A' resulta de A por: intercambio de dos filas → det(A') = -det(A)",
        "                            reemplazo Fi → Fi + k·Fj → det(A') = det(A)",
        "                            multiplicar una fila por k → det(A') = k·det(A)",
        "  • Si A es triangular, det(A) es el producto de su diagonal.",
        "  • det(A⁻¹) = 1 / det(A).",
    ]),
    ("Teorema de la Matriz Invertible (caracterizaciones con asterisco)", [
        "Para A de n×n, las siguientes afirmaciones son equivalentes:",
        "  (a) A es invertible.",
        "  (c*) A tiene n posiciones pivote.",
        "  (e*) Las columnas de A son linealmente independientes.",
        "  (h*) Las columnas de A generan ℝⁿ.",
        "Además: A es invertible ⇔ det(A) ≠ 0,  y entonces",
        "  A⁻¹ = (1 / det(A)) · adj(A),  con adj(A) = (matriz de cofactores)ᵀ.",
    ]),
]
