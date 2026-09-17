# 07_Datos/m1 — Corrección M1: el panel y el detector evaluaron textos distintos

Esta carpeta documenta y corrige un problema detectado en la revisión del
manuscrito: las etiquetas del panel de expertos se asignaron a una redacción
de los requisitos (T_A) y el detector se ejecutó sobre otra (T_B, ERS v2.0).
Todo lo que hay aquí se genera por programa a partir de los datos brutos y del
historial de git. Nada se copia a mano.

| Símbolo | Redacción | Archivo |
|---|---|---|
| **T_A** | Texto evaluado por los expertos el 31-08-2026 | `corpus_TA_rf.json` |
| **T_B** | ERS v2.0, sobre el que corre el detector desde el 14-09-2026 | `../scripts/rf27.json` |

---

## Fase 0 — Evidencia congelada

- Etiqueta git `m1-estado-inicial` sobre el commit `7fe1439`.
- `hashes_estado_inicial.sha256`: SHA-256 de los 9 archivos implicados
  (plantillas, etiquetas, corpus, detector, clasificaciones, rúbrica, panel).

Las plantillas de `../datos_crudos/` no se modifican en ninguna fase.

---

## Fase 1 — Reconstrucción de T_A

Ejecutar desde la raíz del repositorio, en este orden:

```bash
python 07_Datos/m1/m1_01_extraer_TA.py
python 07_Datos/m1/m1_02_reconstruir_clave.py
python 07_Datos/m1/m1_03_cronologia_corpus.py
```

| Script | Produce | SHA-256 |
|---|---|---|
| `m1_01_extraer_TA.py` | `corpus_TA_items.json` | `9d466819b5848c8bc23aa2e5ba239121fb037e75c741a8b40f58664b7139d21a` |
| | `marcas_TA_items.csv` | `f308638ac08e3ca9f609c3ecc065a4ab371ea53fcc6d7aa8331fc5b04fe5b6c8` |
| `m1_02_reconstruir_clave.py` | `clave_items_rf.csv` | `7e541cf4cc9e43e61372316ba43d58c51ef4c3fa76401e93b06d9815bee684ed` |
| | `corpus_TA_rf.json` | `4d45a04acbdcb0c3a15f1ebbe3871d5e4e9b4ee0e2889a9d7f2f9bac6dc3a1f6` |
| `m1_03_cronologia_corpus.py` | `cronologia_corpus.csv` | `61f4310ea2d5c53dfcc2b1e71963a55d2f1c2d35123dee51995d5c47ae71967a` |

Los tres scripts se ejecutaron dos veces, en sesiones distintas, con hashes
idénticos.

### 1.1 Extracción de T_A

Las tres plantillas contienen los mismos 27 textos en el mismo orden, con fecha
de evaluación 2026-08-31. Ítems marcados como ambiguos: 6 (experto 1),
3 (experto 2) y 6 (experto 3).

### 1.2 Clave ítem → RF (reconstruida)

**La clave original de aleatorización no se conservó.** La clave de
`clave_items_rf.csv` es reconstruida y así debe declararse.

- Método: cada ítem se asigna al requisito de T_B con mayor similitud textual
  (`difflib.SequenceMatcher`, `autojunk=False`). Sin intervención manual.
- La clave es biyectiva (27 ítems ↔ 27 RF distintos).
- Las 81 marcas de las plantillas, reordenadas con la clave, coinciden con
  `../datos_procesados/etiquetas_expertos.csv`.
- **Limitación:** esa validación solo discrimina en los 3 RF con patrón de
  marcas único (RF-08, RF-20, RF-22). En los otros 24 la evidencia es la
  similitud textual.

#### Revisión humana de las asignaciones señaladas

El script señala las asignaciones con similitud < 0,60 o margen < 0,10 sobre
el segundo candidato. Revisadas y confirmadas por Gleiston C. Guerrero-Ulloa
el 2026-09-17, sobre la clave con SHA-256 `7e541cf4…`:

| Ítem → RF | Similitud | Segundo candidato (margen) | Motivo de la confirmación |
|---|---|---|---|
| 01 → RF-17 | 0,56 | RF-04 (0,11) | Ambos textos tratan de asociar coordenadas geográficas de la granja de origen al perfil del proveedor. La v2.0 elimina "aproximadas" y añade la validación de rango y precisión. RF-04 trata del pesaje |
| 07 → RF-06 | 0,50 | RF-12 (0,01) | Ambos textos tratan de registrar los cortes obtenidos al despostar un animal y su peso individual. La v2.0 añade la validación de merma. RF-12 trata del conteo físico de inventario |

### 1.3 Cronología de las redacciones

`cronologia_corpus.csv` cuenta, para cada versión relevante del corpus y del
ERS en el historial de git, cuántos requisitos coinciden literalmente con T_A
y con T_B. Las versiones del ERS se leen con `../scripts/extraer_rf_desde_tex.py`.
Extracto (el CSV incluye además `77fad51` y `456d109`, ambos iguales a T_B); la
fila del 31-08 no procede del historial, sino de las plantillas:

| Fecha (UTC-5) | Commit | Versión | RF | = T_A | = T_B |
|---|---|---|---|---|---|
| 2026-08-02 21:36 | `87f2fc2` | `rf25.json` (día del registro OSF) | 25 | 25 | 4 |
| 2026-08-02 23:37 | `b921494` | ERS 2A v1.0 | 25 | 25 | 4 |
| 2026-08-31 | — | Evaluación del panel (plantillas) | 27 | 27 | 6 |
| 2026-09-01 13:43 | `a2fea20` | `rf27.json` creado | 27 | 27 | 6 |
| 2026-09-01 17:46 | `446a828` | ERS 2B v2.0 | 27 | 6 | 27 |
| 2026-09-03 17:39 | `899f9a7` | `rf27.json` movido a `07_Datos` | 27 | 27 | 6 |
| 2026-09-14 15:57 | `c9e90f0` | `rf27.json` sustituido por v2.0 | 27 | 6 | 27 |

Hechos que se desprenden de la tabla:

1. T_A es la redacción de la ERS 2A registrada el 02-08-2026 (25 RF), más RF-26
   y RF-27, cuya redacción no cambió en la v2.0.
2. Hasta el 14-09-2026 las etiquetas del panel y el corpus del detector usaban
   el mismo texto (T_A). La desalineación se introdujo en el commit `c9e90f0`.
3. El manuscrito afirma que el corpus se mantuvo a mano "hasta el 3 de
   septiembre". El corpus cambió el **14 de septiembre**; el 03-09 solo se movió
   de carpeta.
4. El mensaje del commit `a2fea20` ("27 RF verbatim del ERS v2.0") no es
   exacto: el archivo contiene T_A, y la redacción v2.0 aparece en el
   repositorio cuatro horas después (`446a828`).

---

## Fase 2 — Tabla S1: diferencias entre T_A y T_B

```bash
python 07_Datos/m1/m1_04_tabla_S1.py
```

| Produce | SHA-256 |
|---|---|
| `tabla_S1_diferencias_TA_TB.csv` | `8ff423318036ad2580415370c02fd345faeafa8b4f2f660feeea1dcac5f7069b` |
| `codificacion_S1_plantilla.csv` | `324681f687e3278f265dd3fc89076e581b5437a19b6a39dd4c2fe2410c0c5054` |

- 6 RF idénticos (RF-03, RF-07, RF-10, RF-14, RF-26, RF-27) y 21 con cambios.
  De estos, 4 solo añaden texto (RF-09, RF-11, RF-15, RF-22) y 17 eliminan o
  sustituyen palabras.
- Recorriendo las 22 versiones del ERS en el historial, la redacción T_B de
  los 21 RF que cambian aparece por primera vez en el commit `446a828`
  (2026-09-01 17:46 UTC-5), después de la evaluación del panel.

### Codificación del tipo de cambio

El tipo de cambio de cada RF es un juicio humano. Lo codifican dos personas
por separado, según `codificacion_S1/libro_codigos_S1.md`, en cuatro
dimensiones binarias: `L` (léxico impreciso), `R` (restricción añadida),
`G` (agente) y `C` (cosmético o referencial). El libro de códigos y la
plantilla se congelan con commit **antes** de que empiece la codificación.

Para facilitar la tarea, cada persona codificadora recibe
`codificacion_S1/herramienta_codificacion_S1.html`, generada con:

```bash
python 07_Datos/m1/m1_05_herramienta_codificacion.py
```

Es un único archivo HTML que funciona sin conexión:
- muestra cada RF con T_A y T_B lado a lado y los cambios resaltados;
- presenta L, R, G y C como casillas, con la definición completa;
- guarda el avance en el navegador;
- al terminar descarga `hoja_codificador_A.csv` o `hoja_codificador_B.csv`
  y muestra su SHA-256.

Los textos, las definiciones y las reglas se toman literalmente de la Tabla S1,
la plantilla y el libro de códigos. La hoja descargada tiene exactamente el
formato de `codificacion_S1_plantilla.csv`, así que se puede usar la herramienta
o editar la plantilla a mano con el mismo resultado.

#### Hojas recibidas

| Hoja | SHA-256 | L | R | G | C |
|---|---|---|---|---|---|
| `codificacion_S1/hoja_codificador_A.csv` | `aaa44384…` | 4 | 19 | 1 | 11 |
| `codificacion_S1/hoja_codificador_B.csv` | `de6a0e04…` | 4 | 19 | 1 | 9 |
| `codificacion_S1/hoja_codificador_C.csv` | `4f6c55c4…` | 2 | 19 | 1 | 12 |

Las tres se registran sin abrirlas ni modificarlas. Verificación de formato: 21
filas en el orden de la plantilla, solo valores 0 y 1, al menos una marca por
fila y columnas de origen intactas.

Procedimiento realmente seguido, que se desvía del previsto en el libro de
códigos en dos puntos:

- **Tres personas codificadoras, no dos.** Las tres son ajenas al proyecto:
  no participaron en la especificación, ni en el panel de expertos, ni en el
  análisis. En el repositorio se identifican solo como A, B y C.
- **Herramienta en lugar de edición manual** de la plantilla
  (`herramienta_codificacion_S1.html`), que produce el mismo formato.

Trabajaron de forma independiente. Consultaron el significado de algunos
términos, pero no consultaron ninguna decisión de codificación. Las tres
hojas traen comentario en los 21 requisitos, más extensos de lo previsto para
un campo pensado para dudas puntuales.

**Regla de consenso, fijada antes de calcular nada:** para cada requisito y
cada dimensión, el valor de consenso es la mayoría simple (≥ 2 de 3). La
concordancia se informa por dimensión (acuerdo bruto, κ de Cohen por pares y
κ de Fleiss), y las discrepancias se documentan sin modificar las hojas
originales.

#### Concordancia y consenso

```bash
python 07_Datos/m1/m1_06_acuerdo_codificacion.py
```

| Produce | SHA-256 |
|---|---|
| `codificacion_S1/codificacion_S1_consenso.csv` | `ab418320…` |
| `codificacion_S1/discrepancias_S1.csv` | `b64f79f7…` |
| `codificacion_S1/acuerdo_S1.json` | `5dab613e…` |

| Dim. | Marcas A/B/C | Unánime | PABAK | κ de Fleiss | κ de Cohen (A-B, A-C, B-C) | Consenso |
|---|---|---|---|---|---|---|
| L | 4/4/2 | 0,8095 | 0,6190 | 0,5245 | 0,3824 · 0,6182 · 0,6182 | 2 |
| R | 19/19/19 | 1,0000 | 1,0000 | 1,0000 | 1,0000 · 1,0000 · 1,0000 | 19 |
| G | 1/1/1 | 1,0000 | 1,0000 | 1,0000 | 1,0000 · 1,0000 · 1,0000 | 1 |
| C | 11/9/12 | 0,7143 | 0,4286 | 0,6190 | 0,6216 · 0,7123 · 0,5333 | 12 |

De las 84 decisiones (21 RF × 4 dimensiones), 74 son unánimes y 10 se resuelven
por mayoría; 15 de los 21 RF son unánimes en las cuatro dimensiones. Las
discrepancias se concentran en L y C, y ninguna afecta a R ni a G.

Lectura de los valores de consenso:

- **L = 1 solo en RF-08 y RF-17**, con acuerdo unánime de las tres personas. Son
  los dos requisitos en los que la v2.0 elimina una expresión vaga
  («próximo a vencer» y «aproximadas»), y ambos están entre los cuatro que el
  panel de expertos marcó como ambiguos.
- **G = 1 solo en RF-19**, donde la v2.0 elimina el agente explícito
  («a la propietaria o al administrador general»).
- **R = 1 en 19 de 21**: el cambio dominante es añadir umbrales, condiciones y
  reglas.

**Estado:** Fase 2 completa.

---

## Desviaciones del registro detectadas en esta fase

- **Orden de presentación.** El registro OSF indica que el orden de los
  requisitos se aleatoriza *para cada evaluador* con una semilla fija. Las tres
  plantillas tienen el mismo orden, y ni la semilla ni la clave se conservaron.
- **Corpus del detector.** Desde el 14-09-2026 el detector se ejecuta sobre T_B,
  un texto que el panel no evaluó.
