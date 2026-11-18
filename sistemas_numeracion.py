"""
Laboratorio interactivo: Sistemas de Numeración
Curso: Matemáticas para la Informática - ITM

Módulos:
  1. Conversor de bases (con pasos posicionales y divisiones sucesivas)
  2. Suma binaria paso a paso (con acarreos y verificación)
  3. Complemento a dos y detección de Overflow
  4. Estándar IEEE 754 (demostración de precisión y 0.1 + 0.2 != 0.3)
"""

import struct
from decimal import Decimal

DIGITOS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"


# ------------------------------------------------------------ funciones auxiliares
def pedir_entero(mensaje, minimo, maximo):
    while True:
        try:
            val = int(input(mensaje).strip())
            if minimo <= val <= maximo:
                return val
            print(f"  Por favor, ingresa un número entre {minimo} y {maximo}.")
        except ValueError:
            print("  Entrada no válida. Ingresa un número entero.")


def pedir_binario(mensaje):
    while True:
        val = input(mensaje).strip()
        if val and all(c in "01" for c in val):
            return val
        print("  Entrada no válida. Solo se permiten dígitos binarios (0 y 1).")


def de_base(texto, base):
    """Convierte un string en una base dada a decimal, retornando el valor decimal y los pasos posicionales."""
    texto = texto.upper()
    pasos = []
    n = len(texto)
    decimal = 0
    for i, ch in enumerate(texto):
        if ch not in DIGITOS or DIGITOS.index(ch) >= base:
            raise ValueError(f"El dígito '{ch}' no es válido para la base {base}.")
        valor_digito = DIGITOS.index(ch)
        potencia = n - 1 - i
        aporte = valor_digito * (base ** potencia)
        pasos.append((ch, valor_digito, base, potencia, aporte))
        decimal += aporte
    return decimal, pasos


def a_base(decimal, base):
    """Convierte un entero decimal a una base dada usando divisiones sucesivas."""
    if decimal == 0:
        return "0", [(0, base, 0, 0)]
    
    pasos = []
    actual = decimal
    residuos = []
    while actual > 0:
        cociente = actual // base
        residuo = actual % base
        pasos.append((actual, base, cociente, residuo))
        residuos.append(DIGITOS[residuo])
        actual = cociente
    resultado = "".join(reversed(residuos))
    return resultado, pasos


def a_complemento_a_dos(valor, bits):
    """Convierte un entero con signo a su representación en complemento a dos con N bits."""
    minimo = -(2 ** (bits - 1))
    maximo = (2 ** (bits - 1)) - 1
    if not (minimo <= valor <= maximo):
        raise ValueError(f"El valor {valor} no cabe en {bits} bits (rango: {minimo} a {maximo}).")
    
    if valor < 0:
        valor = (1 << bits) + valor
    return format(valor, f"0{bits}b")


def de_complemento_a_dos(bin_str):
    """Convierte una cadena binaria en complemento a dos a su valor decimal con signo."""
    bits = len(bin_str)
    if bin_str[0] == "1":
        return int(bin_str, 2) - (1 << bits)
    return int(bin_str, 2)


def fraccion_a_binario(frac, max_bits=12):
    """Convierte la parte fraccionaria de un decimal a binario mediante multiplicaciones sucesivas por 2."""
    pasos = []
    bits = []
    actual = frac
    for _ in range(max_bits):
        actual *= 2
        bit = int(actual)
        pasos.append((actual, bit))
        bits.append(str(bit))
        actual -= bit
        if actual == 0:
            break
    return "".join(bits), pasos, actual == 0


# ------------------------------------------------------------ 1. conversor
def modulo_conversor():
    print("\n=== CONVERSOR DE BASES ===")
    origen = pedir_entero("Base de origen (2-36): ", 2, 36)
    destino = pedir_entero("Base de destino (2-36): ", 2, 36)
    while True:
        texto = input(f"Número en base {origen}: ").strip()
        try:
            decimal, pasos_pos = de_base(texto, origen)
            break
        except ValueError as e:
            print(f"  {e}")

    if origen != 10:
        print(f"\nPaso 1: a decimal por valor posicional (base {origen})")
        for ch, v, b, p, aporte in pasos_pos:
            print(f"  {ch} x {b}^{p} = {v} x {b ** p} = {aporte}")
        print(f"  Suma = {decimal}")

    if destino != 10:
        resultado, pasos = a_base(decimal, destino)
        print(f"\nPaso 2: de decimal a base {destino} por divisiones sucesivas")
        for q, b, c, r in pasos:
            print(f"  {q} / {b} = {c}, residuo {r} ({DIGITOS[r]})")
        print("  (los residuos se leen de abajo hacia arriba)")
    else:
        resultado = str(decimal)

    print(f"\nResultado: {texto.upper()} (base {origen}) = {resultado} (base {destino})")


# ---------------------------------------------------------- 2. suma binaria
def modulo_suma_binaria():
    print("\n=== SUMA BINARIA PASO A PASO ===")
    a = pedir_binario("Primer número binario:  ")
    b = pedir_binario("Segundo número binario: ")
    n = max(len(a), len(b))
    a, b = a.zfill(n), b.zfill(n)

    acarreo, resultado = 0, []
    print(f"\n{'Posición':>9} | a | b | acarreo in | suma | acarreo out")
    print("-" * 50)
    for i in range(n - 1, -1, -1):
        x, y = int(a[i]), int(b[i])
        total = x + y + acarreo
        bit, nuevo = total % 2, total // 2
        print(f"{n - 1 - i:>9} | {x} | {y} | {acarreo:>10} | {bit:>4} | {nuevo:>11}")
        resultado.append(str(bit))
        acarreo = nuevo
    if acarreo:
        resultado.append("1")
    res = "".join(reversed(resultado))
    print(f"\n  {a}  ({int(a, 2)})\n+ {b}  ({int(b, 2)})\n= {res}  ({int(res, 2)})")


# ------------------------------------------------ 3. complemento a dos
def modulo_complemento_dos():
    print("\n=== COMPLEMENTO A DOS Y OVERFLOW ===")
    bits = pedir_entero("Cantidad de bits (2-16): ", 2, 16)
    minimo, maximo = -(2 ** (bits - 1)), 2 ** (bits - 1) - 1
    print(f"Con {bits} bits el rango con signo es {minimo} a {maximo}.")
    a = pedir_entero("Primer entero:  ", minimo, maximo)
    b = pedir_entero("Segundo entero: ", minimo, maximo)

    ba, bb = a_complemento_a_dos(a, bits), a_complemento_a_dos(b, bits)
    print(f"\n  {a:>6} -> {ba}")
    print(f"  {b:>6} -> {bb}")

    suma_cruda = int(ba, 2) + int(bb, 2)
    suma_bits = format(suma_cruda & (2 ** bits - 1), f"0{bits}b")
    obtenido = de_complemento_a_dos(suma_bits)
    esperado = a + b
    
    # Detección formal de Overflow en complemento a dos:
    overflow = (a > 0 and b > 0 and obtenido < 0) or (a < 0 and b < 0 and obtenido > 0)

    print(f"\n  Suma en hardware ({bits} bits): {suma_bits} -> {obtenido}")
    print(f"  Suma matemática real: {esperado}")
    if overflow:
        print("  *** OVERFLOW: el resultado desborda la capacidad de representación con signo en hardware ***")
    else:
        print("  Sin overflow: el resultado es correcto dentro del rango.")


# ------------------------------------------------------------ 4. IEEE 754
def bits_ieee(x):
    entero = struct.unpack(">I", struct.pack(">f", x))[0]
    b_str = format(entero, "032b")
    return b_str[0], b_str[1:9], b_str[9:]


def modulo_ieee():
    print("\n=== IEEE 754: POR QUE 0.1 + 0.2 != 0.3 ===")
    print("Paso 1: 0.1 en binario fraccionario (multiplicaciones sucesivas por 2)")
    _, pasos, _ = fraccion_a_binario(0.1, 10)
    for valor, bit in pasos:
        print(f"  x2 = {valor:.4f} -> bit {bit}")
    print("  (el patrón binario de la fracción se repite infinitamente)\n")

    while True:
        try:
            x = float(input("Ingresa un decimal para ver su representación float32 (ej. 0.1): "))
            break
        except ValueError:
            print("  Número no válido.")
    
    s, e, m = bits_ieee(x)
    sesgo = 127
    exp_real = int(e, 2) - sesgo
    print(f"\n  float32:  signo={s}  exponente={e}  mantisa={m}")
    print(f"  Exponente sesgado = {int(e, 2)} (sesgo {sesgo} -> exponente real {exp_real})")
    
    almacenado = struct.unpack(">f", struct.pack(">f", x))[0]
    print(f"  Valor realmente guardado en memoria: {Decimal(str(almacenado))}")

    print("\nDemostración clásica con punto flotante:")
    suma = 0.1 + 0.2
    print(f"  0.1 + 0.2        = {suma!r}")
    print(f"  0.1 + 0.2 == 0.3 -> {suma == 0.3}")
    print(f"  Valor decimal exacto de suma: {Decimal(str(suma))}")
    print(f"  Valor decimal exacto de 0.3:  {Decimal('0.3')}")
    print("  Comparación segura recomendada: abs(a - b) < 1e-9 ->", abs(suma - 0.3) < 1e-9)


# --------------------------------------------------------------------- menú
def main():
    opciones = {
        "1": ("Conversor de bases", modulo_conversor),
        "2": ("Suma binaria paso a paso", modulo_suma_binaria),
        "3": ("Complemento a dos y overflow", modulo_complemento_dos),
        "4": ("IEEE 754 (0.1 + 0.2)", modulo_ieee),
    }
    while True:
        print("\n===== LABORATORIO DE SISTEMAS DE NUMERACION =====")
        for k, (nombre, _) in opciones.items():
            print(f"  {k}. {nombre}")
        print("  0. Salir")
        eleccion = input("Elige una opción: ").strip()
        if eleccion == "0":
            print("¡Gracias!")
            break
        if eleccion in opciones:
            try:
                opciones[eleccion][1]()
            except ValueError as e:
                print(f"  Error: {e}")
        else:
            print("  Opción no válida.")


if __name__ == "__main__":
    main()