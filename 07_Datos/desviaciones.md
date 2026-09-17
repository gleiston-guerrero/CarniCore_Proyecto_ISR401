# Desviaciones respecto del protocolo pre-registrado

**Protocolo de referencia:** `06_Experimento/protocolo.pdf`, versión 1.0, 2 de agosto de 2026
**Registro OSF:** `https://osf.io/yp7t3` — *Public registration*, sello temporal del 2 de agosto de 2026
**Documento extenso equivalente:** `06_Experimento/osf_deviations.pdf` (fuente versionada en `06_Experimento/osf_deviations.tex`)

Este archivo es el exigido por el §7 de la guía dentro de `07_Datos/`. Recoge las
desviaciones ya documentadas en `osf_deviations.pdf` (DEV-01, DEV-02, COR-01), la
detectada en la auditoría del 3 de septiembre de 2026 (DEV-03) y la detectada durante la
revisión del manuscrito el 17 de septiembre de 2026 (DEV-04).

Declarar una desviación no invalida el pre-registro. Lo que sí lo invalidaría sería
ejecutar un análisis distinto del registrado y no decirlo.

---

## DEV-03 — El corpus analizado no era el del ERS entregado

| Campo | Contenido |
|---|---|
| **Fecha de detección** | 3 de septiembre de 2026 |
| **Momento** | Después de la ejecución del análisis, durante auditoría técnica del repositorio |
| **Gravedad** | Mayor (afecta a la procedencia del dato de entrada) |
| **Responsable de la corrección** | Pérez Ruiz Carlos Andrés (autor del extractor determinista, commit `4c42bd8`, 2026-09-03) y Quintero Gende Erick Jahir (ejecución final de la regeneración y limpieza del corpus obsoleto, commits `c9e90f0` y `6bc9295`, 2026-09-14) |

**Qué declaraba el protocolo.** Que el detector se ejecutaría sobre los 27 requisitos
funcionales del ERS/SRS v2.0, tomados *verbatim*, sin identificador, nombre, fuente ni
prioridad, tal como los vería el panel ciego.

**Qué se ejecutó realmente.** El detector corrió sobre `rf27.json`, un archivo mantenido
a mano. La comparación mecánica de sus 27 entradas contra los argumentos de la macro
`\rfitem` de `01_ERS/ERS_SRS_2B_v2.0.tex` demostró que **21 de los 27 no coincidían**.
`rf27.json` conservaba la redacción de la Entrega 3 (2A) y no incorporaba las
precisiones añadidas al ERS v2.0.

Ejemplos representativos:

| RF | ERS v2.0 (documento entregado) | `rf27.json` (lo analizado) |
|---|---|---|
| RF-06 | «…margen de merma configurable (valor por defecto: 3 %, rango permitido: 1–8 %)» | «…(brazos, piernas, costillas, lomos, cabezas) y su peso individual» |
| RF-08 | «…(pollo: 3 días; res: 7; cerdo: 5; embutidos: 15) …cuando falte 1 día o menos» | «…(por ejemplo, máximo 3 días para pollo) …cuando esté próximo a vencer» |
| RF-21 | «…en un máximo de 5 minutos. El modo offline se sostiene al menos 8 horas continuas» | «…y sincronizarlas automáticamente al restablecerse la conectividad» |

**Causa raíz.** `rf25.json` se construyó en la Entrega 3 y se congeló. La extensión a 27
fue un *append* puro y honesto —verificado programáticamente—, pero nadie reextrajo los
25 primeros cuando el ERS evolucionó a v2.0. No hubo intención de alterar el corpus:
hubo un artefacto mantenido a mano que se desincronizó de su fuente.

**Mitigación aplicada — cronología real, verificada contra `git log`.**

1. **2026-09-03.** Se escribió `07_Datos/scripts/extraer_rf_desde_tex.py`
   (commit `4c42bd8`), que extrae el corpus directamente del `.tex` entregado. El
   corpus deja de ser un archivo mantenido a mano y pasa a ser una salida reproducible.
2. **2026-09-14.** Se ejecutó `extraer_rf_desde_tex.py` sobre `01_ERS/ERS_SRS_2B_v2.0.tex`
   y se regeneró `rf27.json` con el resultado (commit `c9e90f0`). Verificado de forma
   independiente: correr el extractor de nuevo sobre un clon limpio produce un archivo
   **idéntico byte a byte** al `rf27.json` versionado — no es una edición manual.
3. **2026-09-14.** Se eliminó `07_Datos/scripts/rf25.json` (commit `6bc9295`), el
   artefacto congelado de la Entrega 3 que dio origen a la desviación, ya sin uso una
   vez que `rf27.json` se regenera desde la fuente.
4. **La lógica de `detector_ambiguedad.py` no se modificó en absoluto.** Ni umbrales, ni
   patrones, ni regla de decisión. Corregir el corpus para que sea el declarado es
   reparar una desviación de ejecución; tocar el detector después de ver los resultados
   sería un ajuste post-hoc y no se ha hecho.
5. **2026-09-14.** Se reejecutó el pipeline completo con `python 07_Datos/scripts/run_all.py`
   sobre un clon limpio, de extremo a extremo, sin error.

> **Nota de consistencia:** `06_Experimento/osf_deviations.tex` registra la fecha de esta
> mitigación como «18/09/2026». Esa fecha es posterior a la de hoy y no coincide con el
> historial real de commits (`c9e90f0`, `6bc9295`, ambos del 14/09/2026). Es una errata
> de tecleo — probablemente `14/09` mal escrito como `18/09` — que debe corregirse en el
> `.tex` para que ambos documentos digan la misma fecha real.

**Efecto sobre los resultados — verificado.** Ninguno.

```
Antes  (corpus v1) : detector 0/27 · VP=0 FP=0 FN=4 VN=23 · P=R=F1=0,0000 · κ Fleiss=0,2636
Después(corpus v2.0): detector 0/27 · VP=0 FP=0 FN=4 VN=23 · P=R=F1=0,0000 · κ Fleiss=0,2636
```

Todas las salidas —los cinco JSON/CSV de `resultados/`, las cinco tablas `.tex` y las
cuatro figuras— resultaron **idénticas byte a byte**. Se comprobó por hash SHA-256 de
cada figura PNG.

**Por qué el resultado no cambia.** El umbral de la categoría C2 es «más de 3 conectores
coordinantes». El máximo observado en el corpus v2.0 es **2**. El texto añadido en v2.0
no acerca ningún requisito al umbral. Las categorías C1 y C3 tampoco tienen coincidencia
alguna en ninguna de las dos versiones.

**Consecuencia para el manuscrito.** Ninguna cifra cambia. Lo que cambia es que la
procedencia del corpus es ahora verdadera y verificable por un tercero con una orden.
El `docstring` de `detector_ambiguedad.py` y el `README` del pipeline, que afirmaban
*verbatim* sin que lo fuera, quedan alineados con la realidad.

---

## DEV-04 — La corrección de DEV-03 dejó al panel y al detector evaluando textos distintos

| Campo | Contenido |
|---|---|
| **Fecha de detección** | 17 de septiembre de 2026 |
| **Momento** | Durante la revisión del manuscrito, después de dar DEV-03 por mitigada |
| **Gravedad** | Mayor (afecta a la validez de la comparación, no a las cifras) |
| **Evidencia** | `07_Datos/m1/`, en particular `cronologia_corpus.csv`, `tabla_S1_diferencias_TA_TB.csv` y `resultados_TA/` |

**Qué ocurrió.** DEV-03 sustituyó el corpus por el texto del ERS v2.0 el 14-09-2026
(commit `c9e90f0`). El panel de expertos había clasificado el 31-08-2026, y lo que
clasificó fue la redacción anterior. Al cambiar el corpus no se repitió la clasificación,
así que desde esa fecha las etiquetas humanas y las predicciones del detector
corresponden a **textos distintos**. Llamamos T_A al texto evaluado por el panel y T_B al
del ERS v2.0.

**Alcance, medido.** 21 de los 27 requisitos difieren entre T_A y T_B, y entre ellos están
**los cuatro que el panel marcó como ambiguos** (RF-08, RF-17, RF-21, RF-22). En dos de
ellos la v2.0 elimina precisamente una expresión vaga: «aproximadas» en RF-17 y «próximo
a vencer» en RF-08. Tres personas ajenas al proyecto codificaron los 21 cambios de forma
independiente, con un libro de códigos congelado antes de empezar, y coincidieron por
unanimidad en que esos dos son los únicos casos de eliminación de léxico impreciso.

**Cronología, verificada contra `git log`.**

| Fecha | Hecho |
|---|---|
| 02-08-2026 | Registro OSF; `rf25.json` y el ERS 2A contienen la redacción T_A |
| 31-08-2026 | El panel clasifica 27 ítems con la redacción T_A |
| 01-09-2026 13:43 | Se crea `rf27.json` con T_A (commit `a2fea20`) |
| 01-09-2026 17:46 | El ERS pasa a 2B v2.0 y aparece la redacción T_B (commit `446a828`) |
| 14-09-2026 15:57 | `rf27.json` se sustituye por T_B (commit `c9e90f0`): aquí nace la desviación |

**Mitigación aplicada.**

1. Se congeló el estado previo (etiqueta `m1-estado-inicial`, `07_Datos/m1/hashes_estado_inicial.sha256`).
2. Se reconstruyó T_A por programa desde las plantillas del panel (`m1_01_extraer_TA.py`).
3. Se reconstruyó la clave ítem → RF, que no se conservó, y se validó contra las 81 marcas
   (`m1_02_reconstruir_clave.py`). Se declara como **reconstruida**.
4. Se documentaron las diferencias requisito por requisito (`m1_04_tabla_S1.py`) y se
   codificó su tipo con tres personas externas (`codificacion_S1/`).
5. Se ejecutó el pipeline publicado, **sin modificar ninguna línea**, sobre T_A
   (`m1_07_ruta_A.py`), en un espacio de trabajo temporal.

**Efecto sobre los resultados — verificado.** Ninguno.

```
Sobre T_B (publicado): detector 0/27 · VP=0 FP=0 FN=4 VN=23 · P=R=F1=0,0000 · κ Fleiss=0,2636
Sobre T_A (evaluado) : detector 0/27 · VP=0 FP=0 FN=4 VN=23 · P=R=F1=0,0000 · κ Fleiss=0,2636
```

Los siete artefactos resultaron **idénticos byte a byte**.

**Efecto sobre la interpretación — sí lo hay.** El análisis primario pasa a ser el
realizado sobre T_A, que es el texto que el panel evaluó. Y deja de sostenerse la
afirmación de que el corpus no contiene marcadores: en T_A los hay, pero el inventario no
los reconoce. Incluye `\baproximadamente\b` y no «aproximad[oa]s»; no incluye «próximo a».
Comprobado patrón por patrón sobre T_A: ninguno de los 26 coincide. El 0 de 27 es un
problema de **cobertura léxica del inventario**, no de ausencia de marcadores en el texto.

**Desviación adicional detectada al reconstruir la clave.** El registro OSF declara que el
orden de los requisitos se aleatoriza *para cada evaluador* con una semilla fija. Las tres
plantillas presentan el mismo orden, y no se conservaron ni la semilla ni la clave
original. La clave publicada es una reconstrucción validada, no la original.

**Pendiente.** Reflejar DEV-04 en el registro OSF y en `06_Experimento/osf_deviations.tex`.

---

## DEV-01, DEV-02 y COR-01

Documentadas en `06_Experimento/osf_deviations.pdf`, versión 1.0, y replicadas en la
sección *Deviations from pre-registration* del registro OSF.

`osf_deviations.pdf` se genera desde `06_Experimento/osf_deviations.tex`
(`pdflatex ×2` — sin bibliografía propia), versionado en el repositorio. Verificado en
esta revisión: compila sin errores ni referencias sin resolver, produce un PDF de 4
páginas. Cumple el criterio de piso P2.

---

## Registro de actualización de esta lista

| Fecha | Entrada | Quién | Reflejado en OSF |
|---|---|---|---|
| 2026-09-02 | Redacción inicial de `osf_deviations.pdf` v1.0 (DEV-01, DEV-02, COR-01) | Castro Bajaña Ariel Omar | Sí |
| 2026-09-03 | DEV-03 detectada y extractor escrito | Pérez Ruiz Carlos Andrés | — |
| 2026-09-14 | DEV-03 mitigada: `rf27.json` regenerado, `rf25.json` eliminado, pipeline reejecutado | Quintero Gende Erick Jahir | **Pendiente** |
| 2026-09-17 | DEV-04 detectada: el panel y el detector evaluaron textos distintos | Guerrero-Ulloa Gleiston C. | **Pendiente** |
| 2026-09-17 | DEV-04 mitigada: T_A reconstruido, clave y Tabla S1 publicadas, codificación externa y pipeline reejecutado sobre T_A (`07_Datos/m1/`) | Guerrero-Ulloa Gleiston C. | **Pendiente** |


