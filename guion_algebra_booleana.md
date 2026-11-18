# Guion de exposición: De la lógica a la suma, cómo un computador calcula con compuertas
**Álgebra booleana y circuitos lógicos**
Curso: Matemáticas para la Informática, ITM · Duración objetivo: 12 minutos · Modalidad: virtual, individual

**Enfoque:** programa interactivo en Python (`algebra_booleana.py`) + simulación opcional del mismo circuito en Logisim.
**Idea central:** toda la aritmética de un computador sale de tres operaciones (AND, OR, NOT). Con álgebra booleana podemos simplificar un circuito sin cambiar lo que hace, y eso significa menos compuertas, menos costo y menos energía.

---

## Estructura por minutos

| Min | Bloque | Qué haces | Recurso |
|---|---|---|---|
| 0:00 – 1:30 | Gancho | Preguntas: "¿Cómo suma un computador si solo entiende 0 y 1?" Anuncias que al final verás un sumador hecho solo con compuertas | Diapositiva 1–2 |
| 1:30 – 3:00 | Fundamentos | AND, OR, NOT y XOR con sus tablas de verdad; analogía con interruptores | Diapositiva 3 |
| 3:00 – 5:00 | Tabla de verdad (demo) | Opción 1 con `(A & B) \| (~A & C)`. Muestras Σm y la forma canónica | Programa, opción 1 |
| 5:00 – 7:30 | Simplificación (demo principal) | Opción 2 con la expresión por defecto: de 19 compuertas pasa a 2 (`F = C + A·B`). Explicas que el programa agrupa minterminos que difieren en un bit | Programa, opción 2 |
| 7:30 – 8:30 | Leyes y equivalencia | Opción 4 (verifica 11 leyes) y luego opción 3 con De Morgan. Pides al público una expresión para probar | Programa, opciones 3–4 |
| 8:30 – 11:00 | El sumador | Opción 5: sumador completo, tabla y suma de 4 bits (11 + 6 = 17) mostrando las compuertas de cada etapa | Programa, opción 5 |
| 11:00 – 12:00 | Cierre | Conectas: la ALU del procesador es esto a gran escala. Conclusión | Diapositiva final |

---

## Diapositivas sugeridas (máximo 5)

1. **Portada:** título, tu nombre, curso, ITM.
2. **Pregunta gancho:** "¿Cómo suma un computador?" con un dibujo de dos bits entrando y dos saliendo.
3. **Compuertas básicas:** símbolo + tabla de verdad de AND, OR, NOT, XOR en una sola imagen.
4. **Sumador completo:** diagrama con 2 XOR, 2 AND y 1 OR (el mismo que simula el programa).
5. **Aplicaciones y conclusión:** ver abajo.

## Aplicaciones reales para el cierre

- **ALU del procesador:** cadenas de sumadores completos como el de la demo.
- **Optimización de circuitos:** simplificar expresiones reduce compuertas, área de chip y consumo (FPGA, ASIC).
- **Programación:** condiciones `if` complejas se simplifican con las mismas leyes (De Morgan es muy usada).
- **Bases de datos y búsquedas:** los filtros `AND / OR / NOT` son álgebra booleana pura.
- **Verificación de equivalencia:** comprobar que un diseño optimizado hace lo mismo que el original, como hace la opción 3.

## Frase de cierre

> "Con solo tres operaciones lógicas se construye toda la aritmética de un computador, y el álgebra booleana nos permite hacerlo con el menor número de compuertas posible."

---

## Opcional (suma puntos en creatividad): replicarlo en Logisim

El programa imprime la expresión en sintaxis Logisim (por ejemplo `C | (A & B)`). Para llevarla al simulador:

1. Abre Logisim Evolution → menú **Window → Combinational Analysis**.
2. En la pestaña **Expression**, escribe la expresión simplificada y pulsa **Enter**.
3. Usa **Build Circuit** para generar el circuito automáticamente.
4. En la ventana principal, activa y desactiva las entradas y muestra que la salida coincide con la tabla de verdad del programa.

Si te falta tiempo, deja esto como "trabajo futuro" en la última diapositiva.

---

## Preguntas probables y cómo responderlas

**¿Qué es un minitermino?**
Un producto (AND) en el que aparecen todas las variables, directas o negadas; corresponde a una fila de la tabla de verdad donde F vale 1.

**¿Cómo funciona Quine-McCluskey?**
Se escriben los minterminos en binario, se combinan los que difieren en un solo bit (ese bit pasa a `-`), se repite hasta que no se pueda combinar más y se eligen los implicantes primos que cubren todos los minterminos.

**¿Por qué no usar mapas de Karnaugh?**
Karnaugh es visual y práctico hasta 4 variables; Quine-McCluskey es algorítmico y por eso se puede programar y escalar.

**¿Por qué el XOR es tan importante en el sumador?**
Porque la suma de dos bits sin acarreo es exactamente XOR (1+1 = 0 con acarreo 1), y el acarreo es AND.

**¿Qué pasa con la suma de 4 bits cuando el resultado no cabe?**
El último acarreo (Cout de la etapa 3) indica desbordamiento sin signo; en la demo se muestra como el quinto bit del resultado.

**¿Cómo se relaciona con la ley de De Morgan en programación?**
`not (a and b)` equivale a `(not a) or (not b)`; se usa para simplificar condiciones.

---

## Checklist antes de exponer

- [ ] Ejecutar `python algebra_booleana.py` el día anterior y el mismo día.
- [ ] Terminal con letra grande para compartir pantalla.
- [ ] Ensayar con cronómetro: 12 minutos, sin leer las diapositivas.
- [ ] Tener a mano las entradas de la demo: Enter (por defecto) en las opciones 1 y 2; `~(A & B)` y `~A | ~B` en la opción 3; 11 y 6 en la opción 5.
- [ ] Preparar una expresión propia para la parte del público (por ejemplo `A ^ B ^ C`).
- [ ] Probar compartir pantalla y audio en la plataforma del curso.

## Cómo alinearlo con la rúbrica

| Criterio | Cómo lo cubres |
|---|---|
| Dominio del tema (25) | Compuertas, formas canónicas, leyes, simplificación y su relación con el sumador |
| Aplicación y profundidad (20) | Sumador de 4 bits y reducción de 19 a 2 compuertas |
| Creatividad e innovación (20) | Programa propio con parser, Quine-McCluskey y verificación automática; opcional Logisim |
| Claridad (15) | Estructura por minutos y gancho que se resuelve al final |
| Material de apoyo (10) | 5 diapositivas visuales + programa (+ Logisim) |
| Participación (10) | Expresión propuesta por el público y preguntas preparadas |
