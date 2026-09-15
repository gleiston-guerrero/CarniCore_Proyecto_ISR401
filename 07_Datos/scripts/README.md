# `07\_Datos/scripts/` — Cadena de análisis reproducible

> \*\*Este directorio se movió.\*\* Antes estaba en `06\_Experimento/scripts\_analisis/`.
> El §7 de la guía exige que la cadena de análisis viva dentro de `07\_Datos/`, y
> ninguna otra carpeta la sustituye. Las rutas internas de los scripts son relativas
> (`Path(\_\_file\_\_).resolve().parents\[1]`), de modo que el traslado \*\*no requirió
> modificar ni una línea de código\*\*: al colgar de `07\_Datos/`, `parents\[1]` pasa a
> ser `07\_Datos/` y las salidas caen donde la guía las pide.

\---

## Ejecución

```bash
pip install -r requirements.txt
python run\_all.py            # o: make all
```

Desde la raíz del repositorio, la orden única declarada en `07\_Datos/README\_datos.md`
es `python 07\_Datos/scripts/run\_all.py`.

\---

## Requisito previo — el dato que este pipeline NO genera

Antes de correr nada debe existir:

```
07\_Datos/datos\_procesados/etiquetas\_expertos.csv
```

con las columnas `rf\_id, experto\_1, experto\_2, experto\_3` (valores 0/1), producidas por
al menos 3 personas expertas clasificando los 27 RF de forma **ciega e independiente**,
según el protocolo pre-registrado. El pipeline no crea, simula ni imputa ese archivo:
si no existe, el paso 2 se detiene con un error explícito.

\---

## Qué hace cada paso

|#|Script|Entrada|Salida|
|-|-|-|-|
|—|`extraer\_rf\_desde\_tex.py`|`01\_ERS/ERS\_SRS\_2B\_v2.0.tex`|`rf27.json`|
|1|`detector\_ambiguedad.py`|`rf27.json`|`clasificaciones\_detector.csv`|
|2|`01\_importar\_datos.py`|etiquetas + clasificaciones|`dataset\_consolidado.csv`|
|3|`02\_calcular\_kappa.py`|dataset consolidado|`kappa\_resultados.json`|
|4|`03\_matriz\_confusion\_prf1.py`|dataset consolidado|`matriz\_confusion\_prf1.json`, `tabla\_confusion.csv`|
|5|`04\_bootstrap\_ic95.py`|dataset consolidado|`bootstrap\_ic95.json` (10 000 réplicas, semilla 42)|
|6|`05\_generar\_figuras.py`|resultados|figuras 01–03 y tablas 01, 03, 04|
|7|`06\_analisis\_potencia.py`|resultados|`analisis\_potencia.json`, figura 04, tabla 05|

Salidas numéricas en `07\_Datos/resultados/`; figuras y tablas del manuscrito en
`07\_Publicacion/figuras/` y `07\_Publicacion/tablas/`.

\---

## El corpus ya no se mantiene a mano

`extraer\_rf\_desde\_tex.py` es nuevo y queda **fuera** de `run\_all.py` a propósito:
regenerar el corpus es una decisión metodológica que se declara como desviación, no un
paso rutinario del análisis.

```bash
python extraer\_rf\_desde\_tex.py --comparar rf27.json   # informa, no escribe
python extraer\_rf\_desde\_tex.py --salida rf27.json     # regenera el corpus
```

**Por qué existe.** Hasta el 3 de septiembre de 2026, este README y el `docstring` del
detector afirmaban que `rf27.json` contenía los 27 RF *verbatim* del ERS v2.0. La
comparación mecánica contra el `.tex` demostró que **21 de los 27 no coincidían**:
`rf27.json` conservaba la redacción de la Entrega 3 (2A). El corpus analizado no era el
documento entregado. Documentado como **DEV-03** en `07\_Datos/desviaciones.md`.

rf25.json → rf27.json *fue un *append puro** —verificado programáticamente, los 25
primeros eran idénticos—. El defecto no estaba en la extensión, sino en que los 25
heredados nunca se reextrajeron cuando el ERS evolucionó. rf25.json se eliminó el
14/09/2026 al mitigar DEV-03, una vez cumplida su función como prueba documental (ver
07_Datos/desviaciones.md).

\---

## Regla de consenso experto

Mayoría simple: un RF se considera ambiguo según el panel si **≥2 de 3** expertos lo
marcaron. Fijada en `consenso\_mayoria` de `03\_matriz\_confusion\_prf1.py` y en
`04\_bootstrap\_ic95.py`. Si el protocolo pre-registrado define otra regla, ajústese la
función para que coincida con lo declarado — **nunca al revés**.

\---

## Reglas de detección: congeladas

Los patrones, umbrales y regla de decisión de `detector\_ambiguedad.py` son los del
protocolo pre-registrado, idénticos a los de la Entrega 3 (2A). **No se ajustan después
de ver los resultados del panel.** Eso invalidaría la comparación pre-registrada.

Corregir el corpus para que sea el declarado (DEV-03) **no es** un ajuste de la lógica:
es reparar una desviación de ejecución. La lógica no se tocó, y se verificó que la
corrección no altera ningún resultado.

\---

## Sobre el resultado 0/27 — leer antes de interpretar las métricas

El detector no activa ninguna categoría. Diagnóstico verificado patrón por patrón:

|Categoría|Activaciones|Causa|
|-|-:|-|
|C1 — Cuantificadores vagos|0/27|Ninguno de los 26 patrones aparece en el corpus|
|C2 — Conjunciones múltiples|0/27|Umbral `>3`; el máximo del corpus es **2**|
|C3 — Voz pasiva sin agente|0/27|Forma activa uniforme «El sistema deberá permitir…»|

Con VP = 0 y FP = 0, la precisión es 0/0: **indefinida en rigor**, reportada como 0 por
convención. El IC bootstrap de anchura cero es artefacto de remuestrear una constante,
**no** una medida de incertidumbre. Ambas advertencias deben acompañar a las cifras
allí donde se publiquen. Discusión completa en `07\_Datos/README\_datos.md`, sección 4.

\---

## Reproducibilidad verificada

Ejecutado en árbol limpio con dependencias recién instaladas, el pipeline regenera las
cuatro figuras del manuscrito **idénticas byte a byte** (hash SHA-256 comprobado) y las
cinco tablas `.tex` sin diferencias. Ninguna cifra del manuscrito está escrita a mano.

Nota: las salidas CSV se escriben con CRLF. `.gitattributes` (raíz) las marca como
`-text` para que Git no las normalice y su hash sea estable entre máquinas.

\---

## Limpieza

```bash
make clean
```

Borra sólo los artefactos generados. Nunca toca `etiquetas\_expertos.csv`, que es dato
crudo real, ni `rf25.json`.

