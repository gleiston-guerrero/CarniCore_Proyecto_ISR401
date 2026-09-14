# Desviaciones respecto del protocolo pre-registrado

**Protocolo de referencia:** `06_Experimento/protocolo.pdf`, versión 1.0, 2 de agosto de 2026
**Registro OSF:** `https://osf.io/yp7t3` — *Public registration*, sello temporal del 2 de agosto de 2026
**Documento extenso equivalente:** `06_Experimento/osf_deviations.pdf` (fuente versionada en `06_Experimento/osf_deviations.tex`)

Este archivo es el exigido por el §7 de la guía dentro de `07_Datos/`. Recoge las
desviaciones ya documentadas en `osf_deviations.pdf` (DEV-01, DEV-02, COR-01) y añade
la detectada en la auditoría del 3 de septiembre de 2026 (DEV-03).

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


