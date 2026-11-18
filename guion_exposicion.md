# Guion de exposición: ¿Por qué 0.1 + 0.2 ≠ 0.3?
**Sistemas de numeración dentro del computador**
Curso: Matemáticas para la Informática, ITM · Duración objetivo: 12 minutos · Modalidad: virtual, individual

**Enfoque:** desarrollo de un programa interactivo (Python) + diapositivas breves.
**Idea central:** el computador solo entiende bits, y la forma en que representamos los números con bits explica comportamientos que parecen "errores" (overflow, decimales imprecisos).

---

## Estructura por minutos

| Min | Bloque | Qué haces | Recurso |
|---|---|---|---|
| 0:00 – 1:00 | Gancho | Abres Python y escribes `0.1 + 0.2`. Preguntas: "¿Por qué da 0.30000000000000004?" | Terminal en vivo |
| 1:00 – 3:00 | Sistemas posicionales | Valor posicional, base 10 vs base 2 vs base 16. Un solo ejemplo: 45 = 101101₂ = 2D₁₆ | Diapositiva 2–3 |
| 3:00 – 5:30 | Conversión de bases | Demo del módulo 1 con 45 (decimal → binario) y luego un hexadecimal, por ejemplo `2D` → decimal | Programa, opción 1 |
| 5:30 – 7:00 | Suma binaria | Módulo 2 con 1011 + 0110. Explica el acarreo como en la suma decimal | Programa, opción 2 |
| 7:00 – 9:00 | Complemento a dos y overflow | Módulo 3 con 4 bits: 7 + 3 da -6. Pregunta al público: "¿qué pasaría en un contador de vidas de un videojuego?" | Programa, opción 3 |
| 9:00 – 11:30 | IEEE 754 (resolver el gancho) | Módulo 4: 0.1 en binario es periódico (0.000110011…), así que no cabe exacto en 32 o 64 bits | Programa, opción 4 |
| 11:30 – 12:00 | Cierre | Aplicaciones reales y conclusión | Diapositiva final |

---

## Diapositivas sugeridas (máximo 6, pocas palabras, muchas imágenes)

1. **Portada:** título, tu nombre, curso, ITM.
2. **Gancho:** captura de `0.1 + 0.2 = 0.30000000000000004`.
3. **Sistemas posicionales:** tabla con 45 en bases 2, 10 y 16 y los pesos de cada posición.
4. **Complemento a dos:** tabla de 4 bits (de -8 a 7) y el esquema circular que muestra el "salto" del overflow.
5. **IEEE 754:** esquema de los campos signo / exponente / mantisa de float32 (1 + 8 + 23 bits).
6. **Aplicaciones y conclusión:** ver abajo.

## Aplicaciones reales para el cierre

- **Dinero:** por eso los sistemas financieros no usan `float` sino enteros (centavos) o `Decimal`.
- **Overflow:** errores clásicos como el del Ariane 5 (1996), donde una conversión numérica fuera de rango contribuyó a la pérdida del cohete. Verifícalo en una fuente antes de citarlo.
- **Hexadecimal:** colores en la web (`#FF5733`), direcciones de memoria y direcciones MAC.
- **Comparar decimales en código:** usar una tolerancia (`abs(a - b) < 1e-9`) en lugar de `==`.

## Conclusión (frase para decir)

> "El computador no se equivoca: hace aritmética exacta sobre una representación finita. Entender el sistema de numeración nos dice cuándo confiar en el resultado y cuándo no."

---

## Preguntas probables y cómo responderlas

**¿Por qué el complemento a dos y no signo-magnitud?**
Porque la suma funciona igual con y sin signo (mismo circuito sumador) y solo existe un cero.

**¿Cómo se detecta el overflow en complemento a dos?**
Si se suman dos números del mismo signo y el resultado tiene signo distinto.

**¿Por qué 0.5 sí es exacto y 0.1 no?**
Porque 0.5 = 2⁻¹ es suma de potencias de 2. 0.1 tiene denominador 10 = 2·5, y el factor 5 no se puede expresar con potencias de 2, así que la expansión binaria es periódica.

**¿Cuál es la diferencia entre float32 y float64?**
float32 usa 1 + 8 + 23 bits (unas 7 cifras decimales); float64 usa 1 + 11 + 52 bits (unas 15 a 16).

**¿Cómo se conecta esto con el álgebra booleana?**
El sumador binario se construye con compuertas: la suma de un bit es un XOR y el acarreo es un AND. Es lo que hace el hardware que ejecuta tu programa.

---

## Checklist antes de exponer

- [ ] Ejecutar `python sistemas_numeracion.py` el día anterior y el mismo día.
- [ ] Tener la terminal con letra grande (se debe leer al compartir pantalla).
- [ ] Ensayar con cronómetro: 12 minutos, sin leer las diapositivas.
- [ ] Tener a mano los ejemplos de entrada: `10 → 2 → 45`, `1011 + 0110`, `4 bits: 7 y 3`, `0.1`.
- [ ] Probar compartir pantalla y audio en la plataforma que use el curso.

## Cómo alinearlo con la rúbrica

| Criterio | Cómo lo cubres |
|---|---|
| Dominio del tema (25) | Explicas valor posicional, complemento a dos e IEEE 754 con ejemplos calculados a mano y en el programa |
| Aplicación y profundidad (20) | Overflow y el caso de los decimales con aplicaciones reales |
| Creatividad e innovación (20) | Programa interactivo propio que muestra los pasos, no solo el resultado |
| Claridad (15) | Estructura por minutos y gancho inicial |
| Material de apoyo (10) | 6 diapositivas visuales + programa |
| Participación (10) | Preguntas probables preparadas y una pregunta al público en el minuto 7 |
