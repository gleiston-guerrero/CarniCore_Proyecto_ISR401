# Libro de códigos — Tipo de cambio entre T_A y T_B (Tabla S1)

## 1. Propósito y unidad de análisis

Este libro define cómo clasificar **qué tipo de cambio** sufrió cada requisito
funcional entre la redacción que evaluó el panel de expertos (T_A, 31-08-2026) y
la redacción del ERS v2.0 (T_B). Lo aplican **dos personas codificadoras, de
forma independiente y sin consultarse**.

- **Unidad de análisis:** cada uno de los 21 RF cuya redacción cambia.
- **Material:** `../tabla_S1_diferencias_TA_TB.csv` (columnas `texto_TA`,
  `texto_TB`, `palabras_eliminadas`, `palabras_anadidas`) y la hoja de
  codificación propia.
- **Qué NO se juzga:** si el requisito es ambiguo, si la v2.0 es mejor o peor, o
  qué haría el detector. Solo qué cambió en el texto.

## 2. Esquema: cuatro dimensiones binarias

Un mismo cambio puede tener varias dimensiones a la vez. Para **cada RF** se
escribe `1` (presente) o `0` (ausente) en **cada una** de las cuatro columnas.
Cada RF debe tener al menos un `1`.

| Columna | Dimensión |
|---|---|
| `L` | Léxico impreciso |
| `R` | Restricción añadida |
| `G` | Agente |
| `C` | Cosmético o referencial |

## 3. Definiciones operacionales

### L — Léxico impreciso

**Definición:** T_B elimina o sustituye una palabra o expresión de T_A cuyo
referente no puede verificarse sin información adicional.

**Incluye:** cuantificadores o adjetivos vagos ("aproximado", "suficiente",
"varios"), expresiones temporales o de grado sin valor ("pronto", "próximo a",
"en su momento"), y ejemplos que sustituyen a una regla ("por ejemplo, …").

**Excluye:** eliminar palabras con referente preciso. Añadir una precisión
**sin** retirar ninguna expresión vaga es `R`, no `L`.

**Ejemplo ancla (ficticio):** T_A "responder en un tiempo razonable" → T_B
"responder en menos de 3 segundos": `L = 1` y `R = 1`.

### R — Restricción añadida

**Definición:** T_B añade una condición, umbral, rango, regla de validación,
límite de tiempo o comportamiento ante un caso que T_A no establecía.

**Incluye:** valores numéricos nuevos, condiciones "cuando…/si…", reglas de
negocio, comportamientos ante error, estado intermedio o modo excepcional,
requisitos de rendimiento y nuevos datos obligatorios en la salida.

**Excluye:** reformular una restricción que ya existía sin cambiar su contenido
(eso es `C`).

**Ejemplo ancla (ficticio):** T_A "registrar el pedido" → T_B "registrar el
pedido; si el cliente no tiene crédito, el sistema lo rechaza": `R = 1`.

### G — Agente

**Definición:** cambia **quién** ejecuta o puede ejecutar una acción del
requisito, o si ese actor queda explícito.

**Incluye:** eliminar o añadir un actor ("el administrador", "la propietaria"),
restringir la acción a ciertos roles, e introducir una construcción pasiva o
impersonal sin agente ("se registra", "no se incluyen", "sea aprobada") donde
T_A no la tenía.

**Excluye:** mencionar un rol solo como dato almacenado (p. ej. "asignar uno de
los roles definidos") sin que ese rol ejecute la acción.

**Ejemplo ancla (ficticio):** T_A "el supervisor aprueba la orden" → T_B "la
orden se aprueba antes del envío": `G = 1`.

### C — Cosmético o referencial

**Definición:** cambio de redacción que no altera qué debe hacer el sistema.

**Incluye:** sinónimos o reordenación, eliminar o añadir aclaraciones entre
paréntesis que no restringen nada, cambios de puntuación, y añadir o cambiar
referencias cruzadas (RF-xx, RFC-xx, CU-xx) o menciones de trazabilidad
documental.

**Excluye:** cualquier cambio que añada o retire una obligación verificable.

**Ejemplo ancla (ficticio):** T_A "emitir un comprobante (recibo)" → T_B
"emitir un comprobante": `C = 1`.

## 4. Reglas de aplicación

1. Leer `texto_TA` y `texto_TB` completos. Las columnas de palabras
   eliminadas y añadidas son una ayuda, no el criterio.
2. Decidir cada dimensión por separado. No existe un código "principal".
3. En caso de duda entre `C` y `R`, preguntarse: *¿T_B permite rechazar una
   implementación que T_A aceptaba?* Si sí, `R = 1`.
4. Usar `comentario` solo para dudas reales. No discutirlas con la otra persona
   hasta que ambas hojas estén entregadas y registradas.
5. No consultar la hoja de la otra persona, este informe de revisión, ni los
   resultados del detector o del panel.

## 5. Procedimiento

1. Cada persona copia `../codificacion_S1_plantilla.csv` a
   `hoja_codificador_A.csv` o `hoja_codificador_B.csv`, en esta carpeta.
2. Completa las columnas `L`, `R`, `G` y `C` con 0 o 1 en los 21 RF.
3. Entrega su hoja. Se calcula su SHA-256 y se hace commit **antes** de abrir la
   otra hoja.
4. Con ambas hojas registradas se calcula la concordancia por dimensión (acuerdo
   bruto y κ de Cohen). Las discrepancias se resuelven después por consenso y
   se documentan; las hojas originales no se modifican.
