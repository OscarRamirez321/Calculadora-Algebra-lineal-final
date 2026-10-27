"""Servicio que conecta la interfaz web con las clases de cálculo del proyecto.
Recibe datos en JSON (celdas como texto), llama a Matriz, Determinante, ReductorFilas, etc.
y devuelve resultados serializables; todo el álgebra se ejecuta en Python, no en el navegador.
Elaborado por: [Integrantes del grupo: completar nombres].
"""
from fractions import Fraction

from .interfaz import Entrada
from .modulo_lu import (
    FactorizacionLU, MENSAJE_PERMUTACION, ErrorPermutacion, ResolverSistemaLU, VerificadorLU)
from .modulo_matrices import (
    Determinante, ErrorMatriz, InversaAdjunta, InversaGaussJordan, Matriz, Validador,
    VerificadorCompleto, VerificadorPropiedades)
from .reduccion import ReductorFilas
from .sesion_02_07_08_sistemas import MenuSistemas, SistemaLineal
from .sesion_05_06_vectores import IndependenciaLineal, OperacionesVector


class Serializador:
    """Convierte Matriz, Fraction y pasos de reducción a tipos que JSON entiende."""

    @staticmethod
    def filas(objeto):
        """Devuelve una matriz (Matriz o lista de filas) como lista de listas de texto."""
        datos = objeto.datos if hasattr(objeto, "datos") else objeto
        return [[str(valor) for valor in fila] for fila in datos]

    @classmethod
    def valor(cls, objeto):
        """Devuelve una matriz como filas de texto y cualquier otro valor como texto."""
        if hasattr(objeto, "datos"):
            return cls.filas(objeto)
        return str(objeto)

    @classmethod
    def pasos(cls, pasos):
        """Devuelve los pasos de una reducción con su pivote y fila resaltados."""
        return [{"desc": p.descripcion, "rows": cls.filas(p.filas),
                 "pivot": list(p.pivote) if p.pivote else None, "row": p.fila} for p in pasos]


class Lector:
    """Convierte los datos que llegan de la página en Matriz y Fraction, con mensajes claros."""

    @staticmethod
    def matriz(filas, nombre):
        """Convierte las celdas de texto en una Matriz; avisa cuál tiene celdas inválidas."""
        try:
            return Matriz([[Entrada.texto_a_fraccion(celda) for celda in fila] for fila in filas])
        except ValueError:
            raise ErrorMatriz(
                f"La Matriz {nombre} tiene celdas vacías o inválidas. Revise las celdas en rojo.") from None

    @staticmethod
    def numero(texto):
        """Convierte un texto en Fraction; lanza ErrorMatriz si no es un número."""
        try:
            return Entrada.texto_a_fraccion(str(texto))
        except ValueError as error:
            raise ErrorMatriz(str(error)) from None

    @classmethod
    def vector(cls, textos):
        """Convierte una lista de textos (o un texto con espacios) en lista de Fractions."""
        partes = textos.split() if isinstance(textos, str) else textos
        return [cls.numero(parte) for parte in partes]


class ServicioAlgebra:
    """Una acción por operación de la interfaz; cada una recibe y devuelve un diccionario."""

    def __init__(self):
        """Registra las acciones disponibles."""
        self.acciones = {
            "operacion": self.operacion, "gauss": self.gauss, "sistema": self.sistema,
            "independencia": self.independencia, "vectores": self.vectores,
            "determinante": self.determinante, "inversa_gj": self.inversa_gauss_jordan,
            "inversa_adj": self.inversa_adjunta, "verificador": self.verificador,
            "autocomprobacion": self.autocomprobacion, "lu": self.factorizacion_lu,
        }

    def ejecutar(self, accion, datos):
        """Ejecuta una acción; los errores de validación vuelven como {'error': mensaje}."""
        if accion not in self.acciones:
            return {"error": f"Acción desconocida: {accion}"}
        try:
            return self.acciones[accion](datos)
        except ErrorMatriz as error:
            return {"error": str(error)}
        except (KeyError, IndexError, TypeError, ValueError) as error:
            return {"error": f"Datos incompletos o inválidos ({error})"}

    # ---------- Sesión 1 y 9 ----------

    OPERANDOS = {"tA": "A", "dA": "A", "cA": "A", "tB": "B", "dB": "B", "cB": "B"}

    def operacion(self, d):
        """Suma, resta, producto, transpuesta, diagonal o escalar de las matrices dadas."""
        op = d["op"]
        necesarias = self.OPERANDOS.get(op, "AB")
        a = Lector.matriz(d["A"], "A") if "A" in necesarias else None
        b = Lector.matriz(d["B"], "B") if "B" in necesarias else None
        if op == "mul":
            return self._producto(a, b)
        c = Lector.numero(d.get("c", "1")) if op in ("cA", "cB") else None
        calculos = {
            "add": lambda: a.sumar(b), "sub": lambda: a.restar(b), "subr": lambda: b.restar(a),
            "tA": a.transpuesta if a else None, "tB": b.transpuesta if b else None,
            "dA": a.diagonal if a else None, "dB": b.diagonal if b else None,
            "cA": lambda: a.por_escalar(c), "cB": lambda: b.por_escalar(c),
        }
        resultado = calculos[op]()
        return {"A": Serializador.filas(a) if a else None, "B": Serializador.filas(b) if b else None,
                "R": Serializador.filas(resultado), "c": str(c) if c is not None else None}

    def _producto(self, a, b):
        """A·B con la demostración (AB)ᵀ = BᵀAᵀ y, si existe, B·A."""
        producto = a.producto(b)
        izquierda = producto.transpuesta()
        derecha = b.transpuesta().producto(a.transpuesta())
        inverso = b.producto(a) if b.columnas == a.filas else None
        return {"A": Serializador.filas(a), "B": Serializador.filas(b), "R": Serializador.filas(producto),
                "lhs": Serializador.filas(izquierda), "rhs": Serializador.filas(derecha),
                "ok": izquierda == derecha,
                "BA": Serializador.filas(inverso) if inverso else None,
                "conmuta": inverso == producto if inverso else None}

    # ---------- Sesión 3 y 4 ----------

    def gauss(self, d):
        """Reduce la matriz a RREF y analiza pivotes y variables libres."""
        matriz = Lector.matriz(d["M"], "elegida")
        reduccion = ReductorFilas(matriz.datos).reducir()
        pivotes = len(reduccion.columnas_pivote)
        return {"pasos": Serializador.pasos(reduccion.pasos), "rref": Serializador.filas(reduccion.filas),
                "columnas": matriz.columnas, "pivotes": pivotes, "libres": matriz.columnas - pivotes}

    # ---------- Sesión 2, 7, 8, 5 y 6 ----------

    def sistema(self, d):
        """Clasifica y resuelve Ax = b (o Ax = 0 si se pide el homogéneo)."""
        a = Lector.matriz(d["A"], "A")
        b = [Fraction(0)] * a.filas if d.get("homogeneo") else Lector.vector(d["b"])
        sistema = SistemaLineal.desde_matriz(a, b)
        reduccion = sistema.reducir()
        diagnostico = sistema.diagnosticar(reduccion)
        parametrica = []
        if diagnostico.tipo == "indeterminado":
            for variable, (constante, coef) in sistema.forma_parametrica(reduccion, diagnostico).items():
                parametrica.append(f"x{variable + 1} = {MenuSistemas._expresion(constante, coef)}")
        return {"tipo": diagnostico.tipo, "homogeneo": sistema.es_homogeneo(), "n": sistema.num_variables,
                "pasos": Serializador.pasos(reduccion.pasos),
                "libres": [j + 1 for j in diagnostico.variables_libres],
                "solucion": [[c + 1, str(v)] for c, v in diagnostico.solucion.items()],
                "parametrica": parametrica}

    def independencia(self, d):
        """Decide si las columnas de A son linealmente independientes."""
        a = Lector.matriz(d["A"], "A")
        reduccion, es_independiente = IndependenciaLineal(a.columnas_como_vectores()).analizar()
        return {"pasos": Serializador.pasos(reduccion.pasos), "k": a.columnas,
                "pivotes": len(reduccion.columnas_pivote), "li": es_independiente}

    def vectores(self, d):
        """Suma, producto punto o escalar entre dos vectores de ℝⁿ."""
        u, v = Lector.vector(d["u"]), Lector.vector(d["v"])
        if d["op"] != "k" and len(u) != len(v):
            raise ErrorMatriz("Los vectores deben tener la misma dimensión")
        if d["op"] == "s":
            texto = "v₁ + v₂ = [" + ", ".join(str(x) for x in OperacionesVector.sumar(u, v)) + "]"
        elif d["op"] == "p":
            texto = f"v₁ • v₂ = {OperacionesVector.producto_punto(u, v)}"
        else:
            k = Lector.numero(d["k"])
            texto = f"({k})·v₁ = [" + ", ".join(str(x) for x in OperacionesVector.por_escalar(k, u)) + "]"
        return {"texto": texto}

    # ---------- Sesión 10 y 11 ----------

    def determinante(self, d):
        """det(A) por cofactores, Sarrus (3×3) y reducción triangular."""
        a = Lector.matriz(d["A"], "elegida")
        Validador.cuadrada(a.dimension, "el determinante")
        reduccion = Determinante.por_reduccion(a)
        return {"n": a.filas, "A": Serializador.filas(a), "cofactores": self._cofactores(a),
                "sarrus": self._sarrus(a),
                "triangular": {"U": Serializador.filas(reduccion.triangular), "swaps": reduccion.intercambios,
                               "prod": str(reduccion.producto_diagonal), "det": str(reduccion.determinante),
                               "pasos": Serializador.pasos(reduccion.pasos)}}

    @staticmethod
    def _cofactores(a):
        """Términos de la expansión por la primera fila, o un aviso si n es muy grande."""
        try:
            terminos = Determinante.terminos_primera_fila(a)
        except ErrorMatriz as error:
            return {"aviso": str(error)}
        return {"terminos": [[str(x), str(c)] for x, c in terminos],
                "valor": str(sum(x * c for x, c in terminos))}

    @staticmethod
    def _sarrus(a):
        """Diagonales de Sarrus si A es 3×3; None en otro caso."""
        if a.dimension != (3, 3):
            return None
        s = Determinante.por_sarrus(a)
        return {"pos": [str(p) for p in s.productos_positivos],
                "neg": [str(p) for p in s.productos_negativos], "val": str(s.valor)}

    def inversa_gauss_jordan(self, d):
        """A⁻¹ reduciendo [A | I], con la comprobación A·A⁻¹ = I."""
        a = Lector.matriz(d["A"], "elegida")
        r = InversaGaussJordan.calcular(a)
        salida = {"n": a.filas, "A": Serializador.filas(a), "det": str(Determinante.calcular(a)),
                  "pasos": Serializador.pasos(r.pasos), "pivotes": r.num_pivotes, "inversa": None}
        if r.inversa is not None:
            producto = a.producto(r.inversa)
            salida.update(inversa=Serializador.filas(r.inversa), final=Serializador.filas(r.aumentada_final),
                          producto=Serializador.filas(producto), identidad=producto.es_identidad(),
                          producto2=Serializador.filas(r.inversa.producto(a)),
                          identidad2=r.inversa.producto(a).es_identidad())
        return salida

    def inversa_adjunta(self, d):
        """A⁻¹ = (1/det)·adj(A), comparada con la de Gauss-Jordan."""
        a = Lector.matriz(d["A"], "elegida")
        r = InversaAdjunta.calcular(a)
        salida = {"n": a.filas, "A": Serializador.filas(a), "det": str(r.determinante), "inversa": None}
        if r.inversa is not None:
            producto = a.producto(r.inversa)
            salida.update(cof=Serializador.filas(r.cofactores), adj=Serializador.filas(r.adjunta),
                          inversa=Serializador.filas(r.inversa), producto=Serializador.filas(producto),
                          identidad=producto.es_identidad(),
                          producto2=Serializador.filas(r.inversa.producto(a)),
                          identidad2=r.inversa.producto(a).es_identidad(),
                          coincide=InversaGaussJordan.calcular(a).inversa == r.inversa)
        return salida

    # ---------- Módulo III ----------

    def verificador(self, d):
        """Todas las propiedades del Programa 6; la de efecto de fila usa la operación elegida."""
        a, b, c = (Lector.matriz(d[n], n) for n in "ABC")
        p = d["p5"]
        k = Lector.numero(p["k"]) if p["op"] != "intercambio" else None
        verificador = VerificadorCompleto(a, b, c, Lector.numero(d["k"]))
        propiedades = verificador.evaluar((p["op"], int(p["i"]), int(p["j"]), k))
        return {"A": Serializador.filas(a), "B": Serializador.filas(b), "C": Serializador.filas(c),
                "props": [self._propiedad(x) for x in propiedades], "omitidas": verificador.omitidas}

    # ---------- Programa 6: factorización LU ----------

    def factorizacion_lu(self, d):
        """A = LU con sus pasos; si A es cuadrada también resuelve Ly = b y Ux = y."""
        a = Lector.matriz(d["A"], "A")
        b = Lector.vector(d["b"])
        if len(b) != a.filas:
            raise ErrorMatriz(f"El vector b debe tener {a.filas} componentes (una por fila de A)")
        r = FactorizacionLU(a).calcular()
        salida = {"A": Serializador.filas(a), "L": Serializador.filas(r.matriz_L),
                  "U": Serializador.filas(r.matriz_U), "cuadrada": a.es_cuadrada(),
                  "pasos": [{"desc": p.descripcion, "rows": Serializador.filas(p.filas_u),
                             "L": Serializador.filas(p.filas_l), "pivot": list(p.pivote) if p.pivote else None,
                             "row": p.fila} for p in r.pasos],
                  "producto": Serializador.filas(r.matriz_L.producto(r.matriz_U)),
                  "fact_ok": VerificadorLU.factorizacion_correcta(a, r)}
        if a.es_cuadrada():
            salida.update(self._solucion_lu(a, r, b))
        return salida

    @staticmethod
    def _solucion_lu(a, r, b):
        """Parte del resultado LU con y, x, los pasos de ambas sustituciones y la comprobación."""
        s = ResolverSistemaLU.resolver(r.matriz_L, r.matriz_U, b)
        return {"b": [str(v) for v in b], "y": [str(v) for v in s.vector_y], "x": [str(v) for v in s.vector_x],
                "pasos_y": Serializador.pasos(s.pasos_y), "pasos_x": Serializador.pasos(s.pasos_x),
                "ax": [str(v) for v in a.por_vector(s.vector_x)],
                "sol_ok": VerificadorLU.solucion_correcta(a, s.vector_x, b)}

    @staticmethod
    def _propiedad(r):
        """Serializa un ResultadoPropiedad."""
        return {"n": r.numero, "t": r.enunciado, "l": r.expresion_izquierda,
                "lv": Serializador.valor(r.lado_izquierdo), "r": r.expresion_derecha,
                "rv": Serializador.valor(r.lado_derecho), "ok": r.se_cumple, "cat": r.categoria,
                "aux": [[titulo, Serializador.valor(valor)] for titulo, valor in r.auxiliares]}

    def autocomprobacion(self, d):
        """Ejecuta los casos de prueba del enunciado y devuelve [[nombre, pasó]]."""
        casos = CasosDePrueba()
        resultados = []
        for nombre, prueba in casos.lista():
            try:
                resultados.append([nombre, bool(prueba())])
            except Exception as error:  # Un caso que falla no debe tapar a los demás
                resultados.append([f"{nombre} ({error})", False])
        return {"casos": resultados}


class CasosDePrueba:
    """Casos de prueba del Programa 5 ejecutados con las clases reales del proyecto."""

    @staticmethod
    def _m(filas):
        """Atajo: Matriz desde filas de texto o números."""
        return Matriz([[Entrada.texto_a_fraccion(str(x)) for x in fila] for fila in filas])

    def lista(self):
        """Devuelve [(nombre, función)] con cada caso del enunciado."""
        return (self._casos_producto_y_determinante() + self._casos_inversas_y_propiedades()
                + self._casos_lu())

    def _casos_producto_y_determinante(self):
        """Casos del producto matricial, el error de dimensiones y el determinante."""
        m = self._m
        a23, c32 = m([[1, 2, 3], [4, 5, 6]]), m([[1, 0], [2, 1], [0, 3]])
        a3 = m([[1, 2, 3], [0, 1, 4], [5, 6, 0]])
        return [
            ("A·C = [[5,11],[14,23]] y C·A es 3×3",
             lambda: a23.producto(c32) == m([[5, 11], [14, 23]]) and c32.producto(a23).dimension == (3, 3)),
            ("2×3 por 2×3: «Columnas de A [3] ≠ Filas de B [2]»", lambda: self._mensaje(a23, a23)),
            ("det = 1 por cofactores, Sarrus y triangular",
             lambda: {Determinante.por_cofactores(a3), Determinante.por_sarrus(a3).valor,
                      Determinante.por_reduccion(a3).determinante} == {1}),
        ]

    def _casos_inversas_y_propiedades(self):
        """Casos de inversa por ambos métodos, matriz singular y verificador."""
        m = self._m
        a3, i3 = m([[1, 2, 3], [0, 1, 4], [5, 6, 0]]), m([[-24, 18, 5], [20, -15, -4], [-5, 4, 1]])
        a2, b2 = m([[1, 2], [3, 4]]), m([[0, 1], [1, 1]])
        singular = m([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        return [
            ("A⁻¹ = [[−24,18,5],[20,−15,−4],[−5,4,1]] por ambos métodos",
             lambda: InversaGaussJordan.calcular(a3).inversa == i3 and InversaAdjunta.calcular(a3).inversa == i3),
            ("adj(A) = [[4,−2],[−3,1]] y A⁻¹ = [[−2,1],[3/2,−1/2]]",
             lambda: InversaAdjunta.calcular(a2).adjunta == m([[4, -2], [-3, 1]])
             and InversaAdjunta.calcular(a2).inversa == m([[-2, 1], ["3/2", "-1/2"]])),
            ("Singular: det = 0, solo 2 pivotes, sin inversa",
             lambda: Determinante.calcular(singular) == 0
             and InversaGaussJordan.calcular(singular).num_pivotes == 2
             and InversaGaussJordan.calcular(singular).inversa is None),
            ("Verificador: det(A) = −2, det(A⁻¹) = −1/2 y las propiedades 1–4 y 6",
             lambda: self._verificador(a2, b2)),
            ("(AB)⁻¹ = [[7/2,−3/2],[−2,1]]",
             lambda: VerificadorPropiedades(a2, b2).propiedad_2().lado_izquierdo == m([["7/2", "-3/2"], [-2, 1]])),
            ("Propiedad 5: intercambio → 2, F2→F2−3F1 → −2, F1×3 → −6", lambda: self._propiedad_5(a2, b2)),
            ("Propiedad 6 con diagonal 1, 1, 1",
             lambda: VerificadorPropiedades(a3, a3).propiedad_6().se_cumple
             and [Determinante.por_reduccion(a3).triangular.datos[i][i] for i in range(3)] == [1, 1, 1]),
        ]

    def _casos_lu(self):
        """Casos del Programa 6: factorización, doble sustitución, permutación y verificador."""
        m = self._m
        a2, a3 = m([[2, 1], [6, 8]]), m([[2, 1, 1], [4, -6, 0], [-2, 7, 2]])
        return [
            ("LU de [[2,1],[6,8]]: L = [[1,0],[3,1]], U = [[2,1],[0,5]]",
             lambda: self._lu(a2) == ([[1, 0], [3, 1]], [[2, 1], [0, 5]])),
            ("Ax = b con A 3×3 y b = (5, −2, 9): y = (5, −12, 2) y x = (1, 1, 2)",
             lambda: self._sistema_lu(a3, [5, -2, 9]) == ([5, -12, 2], [1, 1, 2])),
            ("Pivote 0 con intercambio: mensaje de pivoteo parcial",
             lambda: self._permutacion(m([[0, 1], [1, 0]]))),
            ("Verificador completo: las 16 propiedades se cumplen",
             lambda: self._verificador_completo(m([[1, 2], [3, 4]]), m([[0, 1], [1, 1]]), m([[2, 0], [1, 3]]))),
        ]

    @staticmethod
    def _lu(a):
        """Devuelve (L, U) como listas de enteros para compararlas con el ejemplo."""
        r = FactorizacionLU(a).calcular()
        return [[int(v) for v in f] for f in r.matriz_L.datos], [[int(v) for v in f] for f in r.matriz_U.datos]

    @staticmethod
    def _sistema_lu(a, b):
        """Devuelve (y, x) del sistema Ax = b resuelto con LU."""
        r = FactorizacionLU(a).calcular()
        s = ResolverSistemaLU.resolver(r.matriz_L, r.matriz_U, b)
        return [int(v) for v in s.vector_y], [int(v) for v in s.vector_x]

    @staticmethod
    def _permutacion(a):
        """Comprueba el mensaje exacto cuando hace falta pivoteo parcial."""
        try:
            FactorizacionLU(a).calcular()
        except ErrorPermutacion as error:
            return str(error) == MENSAJE_PERMUTACION
        return False

    @staticmethod
    def _verificador_completo(a, b, c):
        """Las 16 propiedades dan 'Se cumple' con matrices invertibles de orden 2."""
        v = VerificadorCompleto(a, b, c, Fraction(3))
        resultado = v.evaluar(("reemplazo", 1, 0, Fraction(-3)))
        return len(resultado) == 16 and all(p.se_cumple for p in resultado)

    @staticmethod
    def _mensaje(a, b):
        """Comprueba el mensaje exacto de error del producto incompatible."""
        try:
            a.producto(b)
        except ErrorMatriz as error:
            return str(error) == "No se puede multiplicar: Columnas de A [3] ≠ Filas de B [2]"
        return False

    @staticmethod
    def _verificador(a, b):
        """Las propiedades 1–4 y 6 se cumplen y los valores clave coinciden con el PDF."""
        v = VerificadorPropiedades(a, b)
        todas = [v.propiedad_1(), v.propiedad_2(), v.propiedad_3(), v.propiedad_4(), v.propiedad_6()]
        return (all(p.se_cumple for p in todas) and Determinante.calcular(a) == -2
                and v.propiedad_4().lado_izquierdo == Fraction(-1, 2))

    @staticmethod
    def _propiedad_5(a, b):
        """Los tres determinantes del enunciado: 2, −2 y −6."""
        v = VerificadorPropiedades(a, b)
        return [v.propiedad_5("intercambio", 0, 1, None).lado_izquierdo,
                v.propiedad_5("reemplazo", 1, 0, Fraction(-3)).lado_izquierdo,
                v.propiedad_5("escala", 0, 0, Fraction(3)).lado_izquierdo] == [2, -2, -6]
