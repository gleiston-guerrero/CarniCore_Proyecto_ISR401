# Paquete de replicación — CarniCore

**Título:** Replication package for *"A lexical-syntactic ambiguity detector does not
replicate expert judgement on Spanish functional requirements: a case study in meat
traceability"*

|||
|-|-|
|**DOI**|[10.5281/zenodo.22225854](https://doi.org/10.5281/zenodo.22225854)|
|**Pre-registro OSF**|https://osf.io/yp7t3|
|**Repositorio**|https://github.com/EdhuXav/CarniCore\_Proyecto\_ISR401|
|**Software Heritage**|`swh:1:dir:5741b167af89a201c815b061cc965309d8167069`|
|**Licencia datos**|CC BY 4.0|
|**Licencia código**|MIT|
|**Versión**|2.1 — septiembre de 2026|

\---

## Nota de corrección de la versión 2.1

La versión anterior de este archivo contenía marcadores de posición sin
resolver (`\[cuando haya panel experto:]`, `\[PENDIENTE panel experto]`),
listaba archivos que no existen en el paquete, e indicaba ejecutar
`run\_all.sh`, guion que nunca formó parte del repositorio. Todo eso está
corregido aquí. El panel de expertos **sí se ejecutó** y sus datos forman parte
del paquete.

\---

## Autoría

|Nombre|ORCID|Institución|
|-|-|-|
|Castro Bajaña, Ariel Omar|0009-0005-1575-8935|UTEQ|
|Crespo Espinoza, Kleber Obed|0009-0000-9145-1357|UTEQ|
|Gamarra Araujo, Edhu Xavier|0009-0001-8312-9656|UTEQ|
|Pérez Ruiz, Carlos Andrés|0009-0003-6741-9391|UTEQ|
|Quintero Gende, Erick Jahir|0009-0000-6032-4179|UTEQ|

Supervisión: PhD. Gleiston Cicerón Guerrero Ulloa, UTEQ.

\---

## Descripción del estudio

**RQ1.** ¿Con qué exactitud diagnóstica replica un detector automático de
ambigüedad léxico-sintáctica el consenso de un panel experto sobre los 27
requisitos funcionales de CarniCore?

**RQ2.** ¿Qué grado de acuerdo alcanzan entre sí las personas expertas, y qué
implica para interpretar RQ1?

**Enfoque metodológico:** Enfoque 2 — detección automática de ambigüedad.
**Contexto:** sistema real de trazabilidad cárnica, Pucayacu (La Maná,
Cotopaxi), Ecuador. Dominio no explorado previamente en la literatura de
ambigüedad de requisitos, y en español.

### Resultados principales

|Métrica|Valor|
|-|-:|
|RF marcados por el detector|0 / 27|
|RF marcados por consenso experto (≥2/3)|4 / 27 (RF-08, RF-17, RF-21, RF-22)|
|Matriz de confusión|VP=0, FP=0, FN=4, VN=23|
|Precisión / Exhaustividad / F₁|0,0000 / 0,0000 / 0,0000|
|κ de Cohen por pares|0,3478 · 0,3571 · 0,0870|
|κ de Fleiss|0,2636|
|McNemar exacta|p = 0,1250|

\---

## Contenido del paquete

```
README\_dataset.md              este archivo
ANONYMIZATION.md               procedimiento de seudonimización aplicado
ETHICS.md                      consentimiento informado y LOPDP
LICENSE.txt                    CC BY 4.0 (datos) + MIT (código)

datos/
  rf27.json                    27 RF del ERS/SRS v2.0 (corpus analizado)
  etiquetas\_expertos.csv       clasificación de cada uno de los 3 evaluadores
  dataset\_consolidado.csv      detector + los 3 expertos, una fila por RF
  clasificaciones\_detector.csv salida del detector con la evidencia por categoría

resultados/
  kappa\_resultados.json        κ de Cohen por pares y κ de Fleiss
  matriz\_confusion\_prf1.json   matriz de confusión y métricas
  tabla\_confusion.csv          la misma matriz en formato tabular
  bootstrap\_ic95.json          IC 95 % por bootstrap (10.000 réplicas, semilla 42)
  analisis\_potencia.json       McNemar exacta, κ detectable, N necesario

scripts/
  01\_importar\_datos.py         carga y validación de esquema
  detector\_ambiguedad.py       detector de reglas (3 categorías)
  02\_calcular\_kappa.py         acuerdo inter-evaluador
  03\_matriz\_confusion\_prf1.py  exactitud diagnóstica
  04\_bootstrap\_ic95.py         intervalos de confianza
  05\_generar\_figuras.py        figuras y tablas del manuscrito
  06\_analisis\_potencia.py      análisis de sensibilidad estadística
  run\_all.py                   orquestador de los 7 pasos
  Makefile                     alternativa: make all
  requirements.txt             dependencias

instrumentos/
  guion\_entrevista\_v2.0.pdf
  cuestionario\_v2.0.pdf
  rubrica\_evaluacion\_experta.pdf
  panel\_expertos\_evaluacion.md

transcripciones/               16 transcripciones seudonimizadas (.txt)
respuestas\_cuestionario/
  encuesta\_respuestas.csv      31 respuestas, sin columnas identificativas
prompts\_llm/                   3 prompts documentados con modelo y fecha
```

\---

## Diccionario de datos

### `rf27.json`

|Campo|Tipo|Descripción|
|-|-|-|
|`id`|string|Identificador del requisito, `RF-01` a `RF-27`|
|`nombre`|string|Título breve del requisito|
|`descripcion`|string|Texto del requisito tomado del ERS/SRS v2.0|

### `clasificaciones\_detector.csv`

|Campo|Tipo|Descripción|
|-|-|-|
|`id\_rf`|string|Identificador del requisito|
|`ambiguo\_detector`|int|1 si activa al menos una categoría, 0 si no|
|`categorias\_activadas`|string|Categorías activadas, o `ninguna`|
|`evidencia\_cuantificador\_vago`|string|Términos vagos encontrados (C1)|
|`evidencia\_conjuncion\_multiple`|string|Conectores contados (C2)|
|`evidencia\_voz\_pasiva`|string|Construcción pasiva encontrada (C3)|

### `etiquetas\_expertos.csv`

|Campo|Tipo|Descripción|
|-|-|-|
|`rf\_id`|string|Identificador del requisito|
|`experto\_1`, `experto\_2`, `experto\_3`|int|1 = ambiguo, 0 = no ambiguo, según cada evaluador|

### `dataset\_consolidado.csv`

Une las dos tablas anteriores por `rf\_id`. Es la entrada de los pasos 2 a 4 del
pipeline.

\---

## Cómo reproducir el análisis

```bash
git clone https://github.com/EdhuXav/CarniCore\_Proyecto\_ISR401.git
cd CarniCore\_Proyecto\_ISR401

python -m venv .venv \&\& source .venv/bin/activate
pip install -r 06\_Experimento/scripts\_analisis/requirements.txt

python 06\_Experimento/scripts\_analisis/run\_all.py
```

El pipeline es determinista: semilla fija en 42 y sin llamadas a servicios
externos. Debe reproducir exactamente las cifras de la tabla de resultados de
más arriba. Si no lo hace, algo está mal en el entorno y conviene abrir una
incidencia en el repositorio.

Salidas en `06\_Experimento/resultados/`, `07\_Publicacion/figuras/` y
`07\_Publicacion/tablas/`.

\---

## Limitaciones que conviene conocer antes de reutilizar estos datos

1. **N = 27.** Es la población completa de requisitos del sistema, no una
muestra. El bootstrap cuantifica la sensibilidad a la composición de ese
conjunto concreto, no generaliza a un universo mayor de requisitos.
2. **Solo 4 positivos según el consenso.** La exhaustividad se estima sobre esos
cuatro casos y su intervalo exacto al 95 % llega hasta 0,6024.
3. **Acuerdo bajo del panel.** κ de Fleiss 0,2636. Las etiquetas individuales se
publican precisamente para que otras personas puedan reanalizar con reglas de
consenso distintas de la mayoría simple.
4. **Efecto de la plantilla de redacción.** El corpus se escribió con plantilla
de voz activa y umbrales numéricos, lo que probablemente suprime los patrones
que busca el detector. Los resultados podrían no trasladarse a corpus
heredados.

\---

## Cómo citar

```bibtex
@dataset{carnicore2026replication,
  author    = {Castro Bajaña, Ariel Omar and Crespo Espinoza, Kleber Obed and
               Gamarra Araujo, Edhu Xavier and Pérez Ruiz, Carlos Andrés and
               Quintero Gende, Erick Jahir},
  title     = {Replication package for ``A lexical-syntactic ambiguity detector
               does not replicate expert judgement on Spanish functional
               requirements: a case study in meat traceability''},
  year      = {2026},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.22225854}
}
```

