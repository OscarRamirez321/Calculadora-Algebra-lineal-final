import streamlit as st
from modulos import operaciones_basicas as op
from modulos import determinantes_inversas as det_inv
from modulos import reduccion_gauss as gauss
from modulos import operaciones_avanzadas as adv

st.set_page_config(page_title="Calculadora de Matrices", layout="wide")

def renderizar_matriz(matriz, titulo="Resultado"):
    st.markdown(f"**{titulo}**")
    latex_str = "\\begin{pmatrix}\n"
    for fila in matriz:
        latex_str += " & ".join([f"{x:.3f}".rstrip('0').rstrip('.') if isinstance(x, float) else str(x) for x in fila]) + " \\\\\n"
    latex_str += "\\end{pmatrix}"
    st.latex(latex_str)

st.title("🧮 Calculadora de Matrices Pro")
st.markdown("---")

# DISEÑO EN 3 COLUMNAS: Izquierda (A), Centro (A y B), Derecha (B)
col_A, col_Mid, col_B = st.columns([2, 1, 2])

# ==========================================
# COLUMNA IZQUIERDA: SOLO MATRIZ A
# ==========================================
with col_A:
    st.subheader("Matriz A")
    c1, c2 = st.columns(2)
    filas_a = c1.number_input("Filas", 1, 5, 3, key="fa")
    cols_a = c2.number_input("Columnas", 1, 5, 3, key="ca")
    
    matriz_A = []
    for i in range(filas_a):
        cols = st.columns(cols_a)
        fila_datos = []
        for j in range(cols_a):
            fila_datos.append(cols[j].number_input(f"A[{i+1},{j+1}]", value=0.0, step=1.0, key=f"a_{i}_{j}"))
        matriz_A.append(fila_datos)

    st.markdown("---")
    # Botones que solo afectan a la Matriz A
    b1, b2 = st.columns(2)
    if b1.button("Determinante (A)"):
        try: st.info(f"**Determinante:** {det_inv.determinante_cofactores(matriz_A)}")
        except Exception as e: st.error(e)
        
    if b2.button("Matriz Inversa (A)"):
        try: renderizar_matriz(det_inv.inversa_gauss_jordan(matriz_A), "A^{-1}")
        except Exception as e: st.error(e)
        
    b3, b4 = st.columns(2)
    if b3.button("Matriz Transpuesta (A)"):
        renderizar_matriz(op.transpuesta(matriz_A), "A^T")
        
    if b4.button("Rango (A)"):
        st.info(f"**Rango:** {adv.rango_matriz(matriz_A)}")

    b5, b6 = st.columns(2)
    escalar_A = b5.number_input("Multiplicar por:", value=2.0, key="esc_a")
    if b5.button("Multiplicar A"):
        renderizar_matriz(adv.multiplicacion_escalar(escalar_A, matriz_A), f"{escalar_A} \\cdot A")

    if b6.button("Matriz Diagonal (A)"):
        renderizar_matriz(adv.matriz_diagonal(matriz_A), "Diagonal(A)")

    b7, b8 = st.columns(2)
    if b7.button("Matriz Triangular (A)"):
        try: renderizar_matriz(adv.matriz_triangular_superior(matriz_A), "Triangular(A)")
        except Exception as e: st.error(e)

    if b8.button("Fact. Cholesky (A)"):
        try: renderizar_matriz(adv.factorizacion_cholesky(matriz_A), "L (Cholesky)")
        except Exception as e: st.error(e)


# ==========================================
# COLUMNA CENTRAL: OPERACIONES CON A Y B
# ==========================================
with col_Mid:
    st.markdown("<br>"*5, unsafe_allow_html=True) # Espaciado
    if st.button("A × B", use_container_width=True):
        try: renderizar_matriz(op.producto_matricial(matriz_A, matriz_B), "A \\cdot B")
        except Exception as e: st.error("A y B no compatibles.")
        
    if st.button("A + B", use_container_width=True):
        try: renderizar_matriz(op.suma(matriz_A, matriz_B), "A + B")
        except Exception as e: st.error("Deben tener igual dimensión.")
        
    if st.button("A - B", use_container_width=True):
        try: renderizar_matriz(op.resta(matriz_A, matriz_B), "A - B")
        except Exception as e: st.error("Deben tener igual dimensión.")


# ==========================================
# COLUMNA DERECHA: SOLO MATRIZ B
# ==========================================
with col_B:
    st.subheader("Matriz B")
    c3, c4 = st.columns(2)
    filas_b = c3.number_input("Filas", 1, 5, 3, key="fb")
    cols_b = c4.number_input("Columnas", 1, 5, 3, key="cb")
    
    matriz_B = []
    for i in range(filas_b):
        cols = st.columns(cols_b)
        fila_datos = []
        for j in range(cols_b):
            fila_datos.append(cols[j].number_input(f"B[{i+1},{j+1}]", value=0.0, step=1.0, key=f"b_{i}_{j}"))
        matriz_B.append(fila_datos)

    st.markdown("---")
    # Botones que solo afectan a la Matriz B
    b1_b, b2_b = st.columns(2)
    if b1_b.button("Determinante (B)"):
        try: st.info(f"**Determinante:** {det_inv.determinante_cofactores(matriz_B)}")
        except Exception as e: st.error(e)
        
    if b2_b.button("Matriz Inversa (B)"):
        try: renderizar_matriz(det_inv.inversa_gauss_jordan(matriz_B), "B^{-1}")
        except Exception as e: st.error(e)
        
    b3_b, b4_b = st.columns(2)
    if b3_b.button("Matriz Transpuesta (B)"):
        renderizar_matriz(op.transpuesta(matriz_B), "B^T")
        
    if b4_b.button("Rango (B)"):
        st.info(f"**Rango:** {adv.rango_matriz(matriz_B)}")

    b5_b, b6_b = st.columns(2)
    escalar_B = b5_b.number_input("Multiplicar por:", value=2.0, key="esc_b")
    if b5_b.button("Multiplicar B"):
        renderizar_matriz(adv.multiplicacion_escalar(escalar_B, matriz_B), f"{escalar_B} \\cdot B")

    if b6_b.button("Matriz Diagonal (B)"):
        renderizar_matriz(adv.matriz_diagonal(matriz_B), "Diagonal(B)")

    b7_b, b8_b = st.columns(2)
    if b7_b.button("Matriz Triangular (B)"):
        try: renderizar_matriz(adv.matriz_triangular_superior(matriz_B), "Triangular(B)")
        except Exception as e: st.error(e)

    if b8_b.button("Fact. Cholesky (B)"):
        try: renderizar_matriz(adv.factorizacion_cholesky(matriz_B), "L (Cholesky)")
        except Exception as e: st.error(e)