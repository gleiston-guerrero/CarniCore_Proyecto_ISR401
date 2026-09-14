# CarniCore — Sistema para la gestión integral de un centro cárnico

> \*\*Proyecto Fin de Curso · Ingeniería de Requisitos (ISR-401) · 4.º nivel · Paralelo «A»\*\*
> Universidad Técnica Estatal de Quevedo (UTEQ) · Facultad de Ciencias de la Computación
> Período 2026–2027 PPA · Docente: PhD. Gleiston Cicerón Guerrero Ulloa

**Repositorio:** https://github.com/gleiston-guerrero/CarniCore_Proyecto_ISR401.git

\---

## Tabla de contenidos

1. [Cómo compilar el ERS desde el `.tex`](#1-cómo-compilar-el-ers-desde-el-tex) ← **criterio de piso P2**
2. [Cómo reproducir el análisis empírico](#2-cómo-reproducir-el-análisis-empírico) ← **criterio de piso P6**
3. [Cómo verificar la integridad del repositorio](#3-cómo-verificar-la-integridad-del-repositorio)
4. [Cómo ejecutar el MVP](#4-cómo-ejecutar-el-mvp)
5. [Resumen del sistema](#5-resumen-del-sistema)
6. [Equipo de trabajo](#6-equipo-de-trabajo)
7. [Estructura del repositorio](#7-estructura-del-repositorio)
8. [Componente empírico: qué se midió y qué salió](#8-componente-empírico-qué-se-midió-y-qué-salió)
9. [Depósitos e identificadores persistentes](#9-depósitos-e-identificadores-persistentes)
10. [Ética y protección de datos](#10-ética-y-protección-de-datos)
11. [Estado de la entrega](#11-estado-de-la-entrega)
12. [Licencias y citación](#12-licencias-y-citación)

\---

## 1\. Cómo compilar el ERS desde el `.tex`

**Documento principal:** `01\_ERS/ERS\_SRS\_2B\_v2.0.tex`

### Compilador y dependencias

|Elemento|Valor|
|-|-|
|Motor|**pdfTeX** 3.141592653-2.6-1.40.25|
|Distribución|**TeX Live 2023** (probado en Debian/Ubuntu)|
|Clase|`article`, `11pt`, `a4paper`|
|Bibliografía|**BibTeX** — `\\\\bibliographystyle{plain}`, `\\\\bibliography{referencias}`|
|Archivo `.bib`|`01\_ERS/referencias.bib`|
|Figuras|`01\_ERS/figures/` — todas las referencias `\\\\includegraphics` están resueltas|

**Paquetes:** `inputenc\[utf8]`, `fontenc\[T1]`, `geometry`, `longtable`, `booktabs`,
`array`, `colortbl`, `xcolor`, `graphicx`, `hyperref`, `enumitem`, `titlesec`,
`fancyhdr`, `tabularx`, `multirow`, `amsmath`, `amssymb`, `float`.

En Debian/Ubuntu se cubren con:

```bash
sudo apt-get install texlive-latex-recommended texlive-latex-extra \\
                     texlive-fonts-recommended texlive-lang-spanish
```

### Orden exacto de las órdenes

La bibliografía obliga a cuatro pasadas. Ejecutar **desde `01\_ERS/`**, porque las rutas
de las figuras son relativas a ese directorio:

```bash
cd 01\_ERS
pdflatex ERS\_SRS\_2B\_v2.0.tex
bibtex   ERS\_SRS\_2B\_v2.0
pdflatex ERS\_SRS\_2B\_v2.0.tex
pdflatex ERS\_SRS\_2B\_v2.0.tex
```

Equivalente en una orden:

```bash
cd 01\_ERS \&\& latexmk -pdf ERS\_SRS\_2B\_v2.0.tex
```

El PDF resultante no debe presentar referencias sin resolver (ni `??` ni `\[?]`).
Si aparecen, falta una pasada.

### Publicación del PDF — regla estricta

**El PDF se publica tal como sale de la compilación local.** No se pasa por iLovePDF,
Smallpdf ni ningún otro servicio web: eso deja rastro en los metadatos (`/Producer`) y
rompe la trazabilidad entre la fuente y el entregable.

Si hace falta reducir el tamaño, hágase con herramientas locales, documentando la orden
aquí mismo. Las figuras de consentimientos (JPG multipágina en `01\_ERS/figures/`) son la
principal causa del peso. Opción local, sin servicios externos:

```bash
gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.7 -dPDFSETTINGS=/prepress \\
   -dNOPAUSE -dQUIET -dBATCH \\
   -sOutputFile=ERS\_SRS\_2B\_v2.0\_comprimido.pdf ERS\_SRS\_2B\_v2.0.pdf
```

Comprobación de los metadatos antes de entregar:

```bash
pdfinfo 01\_ERS/ERS\_SRS\_2B\_v2.0.pdf | grep -i producer   # debe decir pdfTeX, no iLovePDF
```

### Otros documentos LaTeX del repositorio

|Documento|Fuente|Orden|
|-|-|-|
|ERS / SRS|`01\_ERS/ERS\_SRS\_2B\_v2.0.tex`|`pdflatex → bibtex → pdflatex ×2`|
|Manuscrito|`08\_Publicacion/manuscrito\_final.tex`|`pdflatex → bibtex → pdflatex ×2`|
|Autoevaluación FAIR|`fair\_assessment.tex` (en la raíz)|`pdflatex ×2`|

> \*\*El manuscrito depende del pipeline.\*\* Incluye las figuras en `.pdf` y las tablas con
> `\\input{tablas/...}`, y esos archivos son \*\*salidas generadas\*\*, no fuentes. Ejecute
> primero `python 07\_Datos/scripts/run\_all.py` y después compile. Si compila antes,
> faltarán las figuras.

> `06\_Experimento/osf\_deviations.pdf` se publica como PDF (no existe fuente `.tex`); se
> edita con cualquier visor/edidor de PDF o se regenera desde un `.tex` si fuera
> necesario volver a redactarlo.

\---

## 2\. Cómo reproducir el análisis empírico

```bash
python -m venv .venv \&\& source .venv/bin/activate     # Windows: .venv\\Scripts\\activate
pip install -r 07\_Datos/scripts/requirements.txt
python 07\_Datos/scripts/run\_all.py
```

Una sola orden regenera, desde los datos crudos y sin intervención manual, todas las
tablas y figuras que aparecen en el manuscrito. Detalle completo en
[`07\_Datos/scripts/README.md`](07_Datos/scripts/README.md); información de contexto
del paquete en [`07\_Datos/registro\_deposito.md`](07_Datos/registro_deposito.md) y
desviaciones en [`07\_Datos/desviaciones.md`](07_Datos/desviaciones.md).

**Ninguna cifra de ningún documento está escrita a mano.** Todas proceden de la salida
de un script. Verificado: el pipeline regenera las cuatro figuras idénticas byte a byte.

\---

## 3\. Cómo verificar la integridad del repositorio

El repositorio incluye un manifiesto `checksums.sha256` (en la raíz) firmado con el
conjunto de archivos versionados. La verificación es estándar con `sha256sum`:

```bash
# desde la raíz del repositorio
sha256sum -c checksums.sha256
```

El comando recorre cada entrada del manifiesto, recalcula el hash y compara con el
registrado. Termina con `OK` por línea si todo verifica; cualquier `FAILED` indica que
un archivo fue modificado fuera de un commit.

> El manifiesto cubre \*\*únicamente\*\* los archivos versionados (los que están en `git`).
> Los archivos cifrados de `02\_Evidencias/00\_Restringido/` \*\*no\*\* entran en
> `checksums.sha256`: su integridad se acredita por separado, mediante los hashes
> registrados en `02\_Evidencias/00\_Restringido/README.md` y contrastados contra los
> contenedores entregados al docente por SGA.

Para regenerar el manifiesto tras un cambio legítimo:

```bash
# sólo sobre los archivos versionados, sin metadatos de git
find . -type f -not -path './.git/\*' -not -path './02\_Evidencias/00\_Restringido/\*.7z' \\
  -exec sha256sum {} \\; | sort -k2 > checksums.sha256
```

\---

## 4\. Cómo ejecutar el MVP

```bash
cd 05\_MVP/Ejecutable/CarniCore
cp backend/.env.example backend/.env      # OBLIGATORIO: sin este paso Docker aborta
# Edite backend/.env y ponga un JWT\_SECRET propio antes de seguir
docker compose up -d
```

* API: http://localhost:4000 · comprobación de vida: `GET /health`
* Semilla de datos de demostración: `docker compose exec backend npm run seed`
* pgAdmin (opcional): `docker compose --profile tools up -d` → http://localhost:5050

> \*\*Las credenciales de demostración no se publican aquí.\*\* Están en
> `backend/.env.example` como valores de ejemplo que \*\*deben cambiarse\*\*, y las de
> usuario de aplicación se generan con la semilla. Publicar contraseñas en el README de
> un repositorio público es un defecto de seguridad, aunque sean de demostración.

**Escenarios de demostración trazados:**

1. **Ingreso y trazabilidad de lote** (RF-01, RF-02, RF-03, RF-11): registrar proveedor →
guía de origen → lote → consultar trazabilidad completa.
2. **Pesaje y vida útil** (RF-04, RF-05, RF-07, RF-08): registrar pesaje → emitir
comprobante → ingresar a cámara → verificar alerta de vida útil.

\---

## 5\. Resumen del sistema

CarniCore digitaliza y da trazabilidad a los procesos operativos críticos de una
distribuidora de productos cárnicos en Pucayacu, La Maná, Cotopaxi, hoy gestionados de
forma manual.

**Problema.** La gestión manual genera inconsistencias en trazabilidad animal, demoras
en reportes regulatorios y pérdida de información entre faenamiento, refrigeración,
despiece y despacho.

**Propuesta de valor.**

* Trazabilidad animal extremo a extremo (lote → canal → corte → cliente), con vista
pública vía QR (RF-25, RF-26)
* Cumplimiento de normativa sanitaria ecuatoriana y de la LOPDP
* Reportería gerencial filtrable por proveedor (RF-27) y por período
* Predicción de demanda (IA-01) y detección de anomalías de cadena de frío (IA-02)

\---

## 6\. Equipo de trabajo

|N.º|Nombres completos|Correo institucional|Rol|ORCID|
|-:|-|-|-|-|
|1|Castro Bajaña Ariel Omar|acastrob@uteq.edu.ec|Líder / Analista líder|[0009-0005-1575-8935](https://orcid.org/0009-0005-1575-8935)|
|2|Gamarra Araujo Edhu Xavier|egamarraa@uteq.edu.ec|Técnico — Modelador UML|[0009-0001-8312-9656](https://orcid.org/0009-0001-8312-9656)|
|3|Crespo Espinoza Kleber Obed|kcrespoe@uteq.edu.ec|Técnico — Elicitación de campo|[0009-0000-9145-1357](https://orcid.org/0009-0000-9145-1357)|
|4|Quintero Gende Erick Jahir|equinterog@uteq.edu.ec|Técnico — Verificador de calidad|[0009-0000-6032-4179](https://orcid.org/0009-0000-6032-4179)|
|5|Pérez Ruiz Carlos Andrés|cperezr3@uteq.edu.ec|Secretario / Documentador|[0009-0003-6741-9391](https://orcid.org/0009-0003-6741-9391)|

> La columna con los números de cédula se retiró de este archivo el 3 de septiembre de
> 2026. Es un dato personal y no tenía ninguna función en un repositorio público. La
> identificación de las personas integrantes queda acreditada por el correo
> institucional y el ORCID.

Aporte individual por persona, con rutas de artefactos e identificadores de commit:
[`10\_Autoria/aporte\_individual.md`](10_Autoria/aporte_individual.md).

\---

## 7\. Estructura del repositorio

```
CarniCore\_Proyecto\_ISR401/
├── README.md · LICENSE · CITATION.cff · CHANGELOG.md
├── checksums.sha256 · fair\_assessment.pdf/.tex
├── .gitignore · .gitattributes · .mailmap
│
├── 01\_ERS/                  ERS/SRS v2.0 (.tex + .pdf) · figures/ · referencias.bib
├── 02\_Evidencias/           Consentimientos, transcripciones, fotos, walkthrough
│   ├── 00\_Restringido/      Inventario y hashes de la zona cifrada (no su contenido)
│   ├── Consentimientos/ · Transcripciones/ · Documentos\_Organizacion/
│   ├── Fotos\_Entorno/ · Validacion\_Walkthrough/ · Codificacion\_Tematica/
│   ├── Member\_checking/     Acta firmada + material de sesión (member checking)
│   └── Cuestionario/{Fotos\_Aplicacion,Respuestas}/
├── 03\_Modelado/             UML en Diagramas\_UML/ (.drawio + .png) · Mockups/ (20)
├── 04\_Trazabilidad/         Matriz\_Trazabilidad.csv · priorizacion\_moscow\_kano.csv
├── 05\_MVP/                  Backend Node/Express + PostgreSQL · frontend · demo
│   └── Ejecutable/CarniCore/ (docker-compose.yml, backend/, frontend/, docs/, video\_demo.mp4)
├── 06\_Experimento/          Protocolo.pdf · osf\_registration.pdf · osf\_deviations.pdf
│   ├── instrumentos/        Cuestionario, guion, consentimiento, rúbrica, panel
│   └── prompts\_llm/         Tres prompts de apoyo al análisis cualitativo
├── 07\_Datos/                PAQUETE DE DATOS (§7 de la guía)
│   ├── datos\_crudos/ · datos\_procesados/ · resultados/
│   ├── scripts/             Cadena numerada (01–06) + run\_all.py + Makefile + requirements.txt
│   ├── diccionario\_datos.csv · LICENSE-DATA.txt
│   ├── registro\_deposito.md · desviaciones.md
│   └── checksums\_datos.sha256 (manifiesto del paquete, separado del general)
├── 08\_Publicacion/          Manuscrito\_final.tex/.pdf · figuras/ · tablas/ · splncs04.bst
│   └── dataset\_zenodo/      README\_dataset.md · ETHICS.md · ANONYMIZATION.md · LICENSE.txt
├── 09\_Etica/                A01–A13 + Adenda + README\_Etica.md + Categoria\_C/
├── 10\_Autoria/              EVIDENCIA DE AUTORÍA (§6 de la guía)
│   ├── aporte\_individual.md · capturas/ · notas\_campo/ · correspondencia/
│   ├── doble\_codificacion/ · fotos\_equipo/ · grabaciones/
│   └── fuentes\_editables/   Class/Component/Context/Deployment/Strategic + Diagramas\_Actividad/ + Diagramas\_Secuencia/
└── 11\_Defensa/              presentacion.pdf/.pptx · guion.pdf · folleto\_una\_hoja.pdf · video\_defensa.mp4
```

> \*\*Los scripts de análisis viven en `07\_Datos/scripts/`.\*\* Es donde los espera la
> rúbrica del §7 de la guía. Las rutas internas son relativas, de modo que el
> repositorio se puede clonar en cualquier directorio y el pipeline funciona sin
> reconfigurar. `06\_Experimento/` conserva protocolo, registro OSF, desviaciones,
> instrumentos y prompts.

\---

## 8\. Componente empírico: qué se midió y qué salió

**Pregunta.** ¿Coincide un detector determinista de patrones léxicos de ambigüedad con
el criterio de un panel de personas expertas sobre los 27 RF de CarniCore?

**Resultado, tal como sale del pipeline:**

|Medida|Valor|
|-|-|
|RF marcados por el detector|**0 de 27**|
|RF ambiguos por consenso experto (≥2 de 3)|4 de 27 (RF-08, RF-17, RF-21, RF-22)|
|Matriz de confusión|VP = 0 · FP = 0 · FN = 4 · VN = 23|
|Precisión / Exhaustividad / F1|0,0000 / 0,0000 / 0,0000|
|κ de Fleiss (3 evaluadores)|0,2636|
|κ de Cohen por pares|0,3478 · 0,3571 · 0,0870|
|McNemar exacta|p = 0,1250 (4 discordantes)|
|κ mínimo detectable con N = 27|0,5230|

**Dos advertencias que acompañan siempre a estas cifras.** Con VP = 0 y FP = 0, la
precisión es 0/0: indefinida en rigor, reportada como 0 por convención. Y el intervalo
de confianza bootstrap de anchura cero es un artefacto de remuestrear una constante, no
una medida de incertidumbre.

**Lectura.** El detector no falló al ejecutarse: es inerte sobre este corpus. El umbral
de conjunciones múltiples es «más de 3 conectores» y el máximo observado es 2; ningún
cuantificador vago de la lista aparece; los 27 requisitos usan la forma activa «El
sistema deberá permitir…». La ambigüedad que las personas expertas sí perciben —y sobre
la que además concuerdan poco, κ = 0,2636— **no es la que capturan los patrones léxicos
superficiales** sobre un corpus redactado con plantilla uniforme. Eso es un hallazgo del
estudio, no un fallo del instrumento. Discusión completa en
[`07\_Datos/scripts/README.md`](07_Datos/scripts/README.md) y, con foco en los números,
en `07\_Datos/resultados/`.

\---

## 9\. Depósitos e identificadores persistentes

|Plataforma|Identificador|Objeto|
|-|-|-|
|GitHub|https://github.com/EdhuXav/CarniCore\_Proyecto\_ISR401|Repositorio|
|OSF|**https://osf.io/yp7t3**|**Registro** previo del protocolo|
|Zenodo|`10.5281/zenodo.22225854`|Paquete de replicación|
|Software Heritage|`swh:1:dir:5741b167af89a201c815b061cc965309d8167069`|Árbol de código|

> \*\*Corrección del 3 de septiembre de 2026.\*\* Las versiones anteriores de este archivo
> citaban `osf.io/wud69`. Ése es el identificador del \*\*proyecto\*\*, no del \*\*registro\*\*.
> Son objetos distintos en OSF: el proyecto es editable en cualquier momento, mientras que
> el registro queda congelado de forma permanente al finalizarse. El registro es
> `osf.io/yp7t3`, con sello \*\*Date Registered\*\* del 2 de agosto de 2026.
>
> \*\*Corrección del 14 de septiembre de 2026.\*\* La nota anterior describía a `wud69` como
> privado, tomando esa afirmación de la v1.0 de `06\_Experimento/osf\_registration.pdf`. Al
> revisar el proyecto directamente se confirmó que también es público, igual que el
> registro. La v2.0 de ese comprobante ya no describe a `wud69` como privado; el motivo por
> el que el comprobante debe anclarse en `yp7t3` y no en `wud69` es la inmutabilidad del
> registro frente al proyecto, no su visibilidad.



**Autoevaluación FAIR:** `fair\_assessment.pdf` (en la raíz), versión 2.1 — **14 de 16
indicadores (87,5 %)**, por encima del mínimo del 60 % que exige el §7.5. No cumplen I2
(vocabulario controlado del corpus) y R4 (estándares de metadatos del dominio), ambos
con responsable y plazo asignados en el propio documento.

> Las versiones anteriores de este README anunciaban «FAIR 100 % (16/16)». Ese dato era
> incorrecto y la propia autoevaluación v2.1 lo corrige.

\---

## 10\. Ética y protección de datos

**Zona pública \[P].** Transcripciones anonimizadas, fotografías sin rostros ni GPS,
respuestas de cuestionario sin columnas identificativas, consentimientos con **nombre,
firma, cédula y correo redactados**.

**Zona restringida \[R].** `02\_Evidencias/00\_Restringido/` — contenedores cifrados
AES-256, entregados al docente por SGA. **No se versionan en el repositorio** (los
`.7z` están en `.gitignore`); lo que sí se versiona es su inventario por pieza y su
hash SHA-256, de modo que su integridad sea verificable sin publicarlos.

**Base legal.** Ley Orgánica de Protección de Datos Personales del Ecuador. Base de
licitud, finalidad, plazo de conservación (24 meses desde el cierre) y responsable del
tratamiento declarados en `09\_Etica/README\_Etica.md` y en el formulario de
consentimiento (`09\_Etica/A03\_Consentimiento\_Informado.pdf`).

**Nomenclatura multimedia:** `AAAA-MM-DD\_TipoParticipante\_ENTR-XX\_Tecnica.ext`. Se usa
el **rol**, nunca el nombre.



\---

## 11\. Estado de la entrega

Todas las casillas fueron comprobadas sobre el repositorio ya corregido (línea base
`v2.3.2`) y confirmadas por el equipo. Verificación firmada en
`10\_Autoria/verificacion\_previa.pdf`.

### Criterios de piso

* \[x] **P1** — PDF con carátula y URL del repositorio subido al SGA; la URL abre sin autenticar
* \[x] **P2** — El PDF se regenera desde el `.tex` siguiendo únicamente la sección 1 de este README
* \[x] **P2 bis** — `fair\_assessment.tex` y `osf\_deviations.pdf` versionados junto a sus PDF
* \[x] **P3** — Ningún archivo de 0 o 1 byte cuyo nombre anuncie evidencia
* \[x] **P4** — Todos los autores del historial son integrantes declarados con correo institucional
* [x] **P5** — Etiqueta anotada publicada y alcanzable: `v2.3.2`
* \[x] **P6** — `07\_Datos/` existe y `python 07\_Datos/scripts/run\_all.py` termina sin error
* \[x] **P7** — `10\_Autoria/` contiene la documentación de autoría con contenido real
* \[x] **P8** — Cada integrante acredita contribución verificable en el repositorio

### Correcciones sobre material existente

* \[x] PDF del ERS republicado sin pasar por servicio web (`pdfinfo` confirma `pdfTeX`, no `iLovePDF`)
* \[x] Consentimientos y figuras del ERS con el nombre redactado; historial purgado
* \[x] Columna de cédulas retirada de este README
* \[x] `02\_Evidencias/00\_Restringido/fichas\_tecnicas.csv` con una fila **por pieza de evidencia**, no por contenedor
* \[x] Los 18 contenedores `.7z`: resueltos (entregados por SGA y declarados aquí)
* \[x] `.mailmap` completado con la salida real de `git log --format='%aN <%aE>' | sort -u`
* \[x] ≥5 fotografías de aplicación del cuestionario con fecha en los metadatos
* \[x] Documentos en `02\_Evidencias/Documentos\_Organizacion/`: **3**, definitivo — la organización no dispone de más documentación institucional que compartir
* \[x] `checksums.sha256` regenerado y verificando al 100 %

### Datos y componente inteligente

* \[x] Corpus regenerado desde el `.tex` y DEV-03 registrado también en OSF
* \[x] RNF de supervisión humana, monitoreo posdespliegue y clasificación de riesgo
incorporados al ERS y a la matriz de trazabilidad (`RNF-IA-14`, `RNF-IA-15`, `RNF-IA-16`)
* \[x] Todo RNF del componente inteligente tiene métrica, unidad, umbral, método de
verificación, responsable y frecuencia de medición
* \[x] Fuentes editables de los diagramas: `10\_Autoria/fuentes\_editables/` y
`03\_Modelado/Diagramas\_UML/` cubren los diagramas en formato `.drawio`

\---

## 12\. Licencias y citación

|Material|Licencia|
|-|-|
|Código fuente (MVP y scripts)|MIT — `LICENSE`|
|ERS/SRS y documentación|CC BY 4.0 — `LICENSE`|
|Paquete de datos `07\_Datos/`|CC BY 4.0 — `07\_Datos/LICENSE-DATA.txt`|
|`02\_Evidencias/00\_Restringido/`|Sin licencia — no se redistribuye|

```bibtex
@software{carnicore\_isr401\_2026,
  author  = {Castro Bajaña, Ariel Omar and Gamarra Araujo, Edhu Xavier and
             Crespo Espinoza, Kleber Obed and Quintero Gende, Erick Jahir and
             Pérez Ruiz, Carlos Andrés},
  title   = {{CarniCore}: Detección automática de patrones de ambigüedad en
             requisitos funcionales --- Paquete de replicación},
  version = {2.0.0},
  year    = {2026},
  doi     = {10.5281/zenodo.22225854},
  url     = {https://github.com/EdhuXav/CarniCore\_Proyecto\_ISR401}
}
```

Metadatos completos en `CITATION.cff`.

\---

*Universidad Técnica Estatal de Quevedo · ISR-401 · 2026–2027 PPA*
