"""
Simulador de álgebra booleana y circuitos lógicos
Curso: Matemáticas para la Informática - ITM

Módulos:
  1. Tabla de verdad de una expresión (formas canónicas Σm y ΠM)
  2. Simplificación con el método de Quine-McCluskey
  3. Comprobador de equivalencia entre dos expresiones
  4. Verificador de leyes del álgebra booleana (De Morgan, absorción, ...)
  5. Sumador completo y sumador de 4 bits construidos con compuertas

Sintaxis de las expresiones (variables de una letra o nombre corto):
  NOT:  ~A   !A   NOT A
  AND:  A & B   A * B   A . B   A AND B
  OR :  A | B   A + B   A OR B
  XOR:  A ^ B   A XOR B
  Precedencia: NOT > AND > XOR > OR. Se pueden usar paréntesis.
"""

import itertools
import re

MAX_VARIABLES = 6


# ------------------------------------------------------------------- parser
class ErrorSintaxis(ValueError):
    pass


PALABRAS = {"AND": "AND", "OR": "OR", "NOT": "NOT", "XOR": "XOR"}
SIMBOLOS = {
    "~": "NOT", "!": "NOT",
    "&": "AND", "*": "AND", ".": "AND",
    "|": "OR", "+": "OR",
    "^": "XOR",
    "(": "LP", ")": "RP",
}


def tokenizar(texto):
    tokens = []
    for t in re.findall(r"[A-Za-z_]\w*|\S", texto):
        if re.match(r"[A-Za-z_]", t):
            if t.upper() in PALABRAS:
                tokens.append((PALABRAS[t.upper()], t))
            else:
                tokens.append(("VAR", t))
        elif t in SIMBOLOS:
            tokens.append((SIMBOLOS[t], t))
        else:
            raise ErrorSintaxis(f"Símbolo no reconocido: '{t}'")
    return tokens


class Parser:
    def __init__(self, tokens):
        self.t = tokens
        self.i = 0

    def peek(self):
        return self.t[self.i][0] if self.i < len(self.t) else None

    def tomar(self):
        tok = self.t[self.i]
        self.i += 1
        return tok

    def parse(self):
        if not self.t:
            raise ErrorSintaxis("La expresión está vacía")
        nodo = self.o()
        if self.i != len(self.t):
            raise ErrorSintaxis(f"Texto inesperado cerca de '{self.t[self.i][1]}'")
        return nodo

    def o(self):
        n = self.x()
        while self.peek() == "OR":
            self.tomar()
            n = ("OR", n, self.x())
        return n

    def x(self):
        n = self.y()
        while self.peek() == "XOR":
            self.tomar()
            n = ("XOR", n, self.y())
        return n

    def y(self):
        n = self.neg()
        while self.peek() == "AND":
            self.tomar()
            n = ("AND", n, self.neg())
        return n

    def neg(self):
        if self.peek() == "NOT":
            self.tomar()
            return ("NOT", self.neg())
        return self.atomo()

    def atomo(self):
        p = self.peek()
        if p == "VAR":
            return ("VAR", self.tomar()[1])
        if p == "LP":
            self.tomar()
            n = self.o()
            if self.peek() != "RP":
                raise ErrorSintaxis("Falta cerrar un paréntesis")
            self.tomar()
            return n
        raise ErrorSintaxis("Se esperaba una variable o un paréntesis")


def parsear(texto):
    return Parser(tokenizar(texto)).parse()


def variables_de(ast):
    if ast[0] == "VAR":
        return {ast[1]}
    return set().union(*(variables_de(h) for h in ast[1:]))


def evaluar(ast, env):
    op = ast[0]
    if op == "VAR":
        return env[ast[1]]
    if op == "NOT":
        return 1 - evaluar(ast[1], env)
    a, b = evaluar(ast[1], env), evaluar(ast[2], env)
    if op == "AND":
        return a & b
    if op == "OR":
        return a | b
    return a ^ b  # XOR


def a_texto(ast):
    """Expresión completamente parentizada en sintaxis tipo Logisim."""
    op = ast[0]
    if op == "VAR":
        return ast[1]
    if op == "NOT":
        return "~" + a_texto(ast[1])
    simbolo = {"AND": "&", "OR": "|", "XOR": "^"}[op]
    return f"({a_texto(ast[1])} {simbolo} {a_texto(ast[2])})"


def filas(variables):
    """Todas las combinaciones; la primera variable es el bit más significativo."""
    for combo in itertools.product((0, 1), repeat=len(variables)):
        yield combo, dict(zip(variables, combo))


def minterminos_de(ast, variables):
    return [i for i, (_, env) in enumerate(filas(variables)) if evaluar(ast, env)]


# ------------------------------------------------------- Quine-McCluskey
def combinar(a, b):
    """Combina dos implicantes si difieren en un solo bit (ambos sin '-')."""
    dif = [i for i in range(len(a)) if a[i] != b[i]]
    if len(dif) == 1 and a[dif[0]] != "-" and b[dif[0]] != "-":
        d = dif[0]
        return a[:d] + "-" + a[d + 1:]
    return None


def cubre(patron, m, n):
    bits = format(m, f"0{n}b")
    return all(p == "-" or p == b for p, b in zip(patron, bits))


def quine_mccluskey(minterminos, n):
    """Devuelve (rondas, primos, cobertura_elegida)."""
    actuales = {format(m, f"0{n}b") for m in minterminos}
    primos, rondas = set(), []
    while actuales:
        rondas.append(sorted(actuales, key=lambda p: (p.count("1"), p)))
        usados, nuevos = set(), set()
        for a, b in itertools.combinations(sorted(actuales), 2):
            c = combinar(a, b)
            if c:
                nuevos.add(c)
                usados.update((a, b))
        primos |= actuales - usados
        actuales = nuevos

    primos = sorted(primos)
    por_cubrir = set(minterminos)
    elegidos = []
    # primos esenciales
    for m in sorted(minterminos):
        candidatos = [p for p in primos if cubre(p, m, n)]
        if len(candidatos) == 1 and candidatos[0] not in elegidos:
            elegidos.append(candidatos[0])
    for p in elegidos:
        por_cubrir -= {m for m in minterminos if cubre(p, m, n)}
    # el resto, de forma voraz
    while por_cubrir:
        mejor = max(
            (p for p in primos if p not in elegidos),
            key=lambda p: sum(cubre(p, m, n) for m in por_cubrir),
        )
        elegidos.append(mejor)
        por_cubrir -= {m for m in minterminos if cubre(mejor, m, n)}
    return rondas, primos, elegidos


def patron_a_texto(patron, variables):
    partes = []
    for p, v in zip(patron, variables):
        if p == "1":
            partes.append(v)
        elif p == "0":
            partes.append(v + "'")
    return "·".join(partes) if partes else "1"


def patron_a_logisim(patron, variables):
    partes = []
    for p, v in zip(patron, variables):
        if p == "1":
            partes.append(v)
        elif p == "0":
            partes.append("~" + v)
    if not partes:
        return "1"
    return partes[0] if len(partes) == 1 else "(" + " & ".join(partes) + ")"


# ------------------------------------------------------------- entrada
def pedir_expresion(mensaje, ejemplo):
    while True:
        texto = input(f"{mensaje} [Enter = {ejemplo}]: ").strip() or ejemplo
        try:
            ast = parsear(texto)
            vs = sorted(variables_de(ast))
            if len(vs) > MAX_VARIABLES:
                print(f"  Máximo {MAX_VARIABLES} variables.")
                continue
            return texto, ast, vs
        except ErrorSintaxis as e:
            print(f"  Error de sintaxis: {e}")


def imprimir_tabla(ast, vs, titulo="F"):
    print("  " + " ".join(vs) + " | " + titulo)
    print("  " + "-" * (2 * len(vs)) + "+---")
    for combo, env in filas(vs):
        print("  " + " ".join(str(b) for b in combo) + " | " + str(evaluar(ast, env)))


# ------------------------------------------------------ 1. tabla de verdad
def modulo_tabla():
    print("\n=== TABLA DE VERDAD ===")
    texto, ast, vs = pedir_expresion("Expresión", "(A & B) | (~A & C)")
    print(f"\nVariables: {', '.join(vs)}   |   Forma Logisim: {a_texto(ast)}\n")
    imprimir_tabla(ast, vs)
    n = len(vs)
    unos = minterminos_de(ast, vs)
    ceros = [i for i in range(2 ** n) if i not in unos]
    print(f"\n  Suma de minterminos   F = Σm({', '.join(map(str, unos))})")
    print(f"  Producto de maxterminos F = ΠM({', '.join(map(str, ceros))})")
    if unos:
        canon = " + ".join(
            "·".join(v if bit == "1" else v + "'" for v, bit in zip(vs, format(m, f"0{n}b")))
            for m in unos
        )
        print(f"  Forma canónica SOP: {canon}")


# --------------------------------------------------- 2. simplificación
def modulo_simplificar():
    print("\n=== SIMPLIFICACIÓN (Quine-McCluskey) ===")
    texto, ast, vs = pedir_expresion("Expresión", "(~A & ~B & C) | (~A & B & C) | (A & ~B & C) | (A & B & C) | (A & B & ~C)")
    n = len(vs)
    unos = minterminos_de(ast, vs)
    print(f"\n  Variables: {', '.join(vs)}   Minterminos: {unos}")
    if not unos:
        print("  F = 0 (contradicción)")
        return
    if len(unos) == 2 ** n:
        print("  F = 1 (tautología)")
        return

    rondas, primos, elegidos = quine_mccluskey(unos, n)
    for i, r in enumerate(rondas, 1):
        print(f"\n  Ronda {i} (implicantes ordenados por cantidad de unos):")
        print("    " + "  ".join(r))
    print("\n  Implicantes primos:")
    for p in primos:
        cubiertos = [m for m in unos if cubre(p, m, n)]
        marca = "  <- elegido" if p in elegidos else ""
        print(f"    {p}  = {patron_a_texto(p, vs):<10} cubre {cubiertos}{marca}")

    simple = " + ".join(patron_a_texto(p, vs) for p in elegidos)
    logisim = " | ".join(patron_a_logisim(p, vs) for p in elegidos)
    print(f"\n  Expresión simplificada: F = {simple}")
    print(f"  En sintaxis Logisim:    {logisim}")

    # verificación automática
    ast2 = parsear(logisim)
    ok = minterminos_de(ast2, vs) == unos
    print(f"  Verificación (misma tabla de verdad que la original): {'CORRECTA' if ok else 'ERROR'}")

    # ahorro
    comp_original = text_len_compuertas(ast)
    comp_simple = text_len_compuertas(ast2)
    print(f"  Compuertas: original {comp_original} -> simplificada {comp_simple}")


def text_len_compuertas(ast):
    if ast[0] == "VAR":
        return 0
    return 1 + sum(text_len_compuertas(h) for h in ast[1:])


# ----------------------------------------------------- 3. equivalencia
def comparar(ast1, ast2):
    vs = sorted(variables_de(ast1) | variables_de(ast2))
    for combo, env in filas(vs):
        if evaluar(ast1, env) != evaluar(ast2, env):
            return False, dict(zip(vs, combo))
    return True, None


def modulo_equivalencia():
    print("\n=== COMPROBADOR DE EQUIVALENCIA ===")
    t1, a1, _ = pedir_expresion("Expresión 1", "~(A & B)")
    t2, a2, _ = pedir_expresion("Expresión 2", "~A | ~B")
    ok, contra = comparar(a1, a2)
    if ok:
        print(f"\n  EQUIVALENTES: {t1}  ==  {t2}")
    else:
        detalle = ", ".join(f"{k}={v}" for k, v in contra.items())
        print(f"\n  NO son equivalentes. Contraejemplo: {detalle}")
        print(f"    {t1} = {evaluar(a1, contra)}   |   {t2} = {evaluar(a2, contra)}")


# ---------------------------------------------------------- 4. leyes
LEYES = [
    ("De Morgan (1)", "~(A & B)", "~A | ~B"),
    ("De Morgan (2)", "~(A | B)", "~A & ~B"),
    ("Doble negación", "~~A", "A"),
    ("Absorción (1)", "A | (A & B)", "A"),
    ("Absorción (2)", "A & (A | B)", "A"),
    ("Distributiva (1)", "A & (B | C)", "(A & B) | (A & C)"),
    ("Distributiva (2)", "A | (B & C)", "(A | B) & (A | C)"),
    ("Consenso", "(A & B) | (~A & C) | (B & C)", "(A & B) | (~A & C)"),
    ("Definición de XOR", "A ^ B", "(A & ~B) | (~A & B)"),
    ("Idempotencia", "A | A", "A"),
    ("Complemento", "A | ~A", "1"),
]


def modulo_leyes():
    print("\n=== VERIFICADOR DE LEYES DEL ÁLGEBRA BOOLEANA ===")
    print("Cada ley se comprueba revisando TODAS las filas de la tabla de verdad.\n")
    for nombre, izq, der in LEYES:
        if der == "1":
            ok = all(evaluar(parsear(izq), env) == 1 for _, env in filas(sorted(variables_de(parsear(izq)))))
        else:
            ok, _ = comparar(parsear(izq), parsear(der))
        print(f"  [{'OK' if ok else 'FALLA'}] {nombre:<18} {izq}  ==  {der}")


# ----------------------------------------------------------- 5. sumador
def sumador_completo(a, b, cin, traza=False):
    x1 = a ^ b            # XOR
    suma = x1 ^ cin       # XOR
    a1 = a & b            # AND
    a2 = x1 & cin         # AND
    cout = a1 | a2        # OR
    if traza:
        return suma, cout, dict(x1=x1, a1=a1, a2=a2)
    return suma, cout


def modulo_sumador():
    print("\n=== SUMADOR CON COMPUERTAS ===")
    print("Sumador completo (1 bit):")
    print("  S    = A XOR B XOR Cin")
    print("  Cout = (A AND B) OR (Cin AND (A XOR B))\n")
    print("  A B Cin | S Cout")
    print("  --------+-------")
    for a, b, c in itertools.product((0, 1), repeat=3):
        s, co = sumador_completo(a, b, c)
        print(f"  {a} {b}  {c}  | {s}  {co}")

    print("\nSumador de 4 bits (cuatro sumadores completos encadenados):")
    while True:
        try:
            x = int(input("  Primer número (0-15) [Enter = 11]: ").strip() or "11")
            y = int(input("  Segundo número (0-15) [Enter = 6]: ").strip() or "6")
            if 0 <= x <= 15 and 0 <= y <= 15:
                break
        except ValueError:
            pass
        print("  Ingresa enteros entre 0 y 15.")

    bx, by = format(x, "04b"), format(y, "04b")
    print(f"\n  {x} = {bx}    {y} = {by}\n")
    print("  Etapa | A B Cin | XOR(A,B) AND(A,B) AND(Cin,XOR) | S Cout")
    cin, bits = 0, []
    for etapa, i in enumerate(range(3, -1, -1)):
        a, b = int(bx[i]), int(by[i])
        s, cout, t = sumador_completo(a, b, cin, traza=True)
        print(f"    {etapa}   | {a} {b}  {cin}  |    {t['x1']}         {t['a1']}           {t['a2']}       | {s}  {cout}")
        bits.append(str(s))
        cin = cout
    resultado = str(cin) + "".join(reversed(bits))
    print(f"\n  Resultado: {resultado}  = {int(resultado, 2)}  (esperado: {x + y})")
    print("  " + ("Correcto." if int(resultado, 2) == x + y else "ERROR"))


# ------------------------------------------------------------------ menú
def main():
    opciones = {
        "1": ("Tabla de verdad y formas canónicas", modulo_tabla),
        "2": ("Simplificar una expresión (Quine-McCluskey)", modulo_simplificar),
        "3": ("Comprobar equivalencia de dos expresiones", modulo_equivalencia),
        "4": ("Verificar leyes del álgebra booleana", modulo_leyes),
        "5": ("Sumador de 4 bits con compuertas", modulo_sumador),
    }
    while True:
        print("\n===== SIMULADOR DE ALGEBRA BOOLEANA =====")
        for k, (nombre, _) in opciones.items():
            print(f"  {k}. {nombre}")
        print("  0. Salir")
        eleccion = input("Elige una opción: ").strip()
        if eleccion == "0":
            print("¡Gracias!")
            break
        if eleccion in opciones:
            opciones[eleccion][1]()
        else:
            print("  Opción no válida.")


if __name__ == "__main__":
    main()
