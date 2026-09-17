# A9 — Declaración de uso de Inteligencia Artificial

**Proyecto:** CarniCore · ISR-401 · UTEQ · 2026–2027 PPA
**Documento base:** ERS/SRS v2.0 — Entrega 4 (2B / Defensa Final)
**Última actualización:** 12 de septiembre de 2026 (incorpora la auditoría técnica del 11–12 de septiembre de 2026 y el cierre del manifiesto de integridad — ver Secciones 3 y 4)

---

## Nota sobre esta declaración

La guía exige una declaración **por sección del documento**, indicando qué herramienta
se utilizó, para qué, quién verificó el resultado y con qué método. Incluye la siguiente
condición:

> *«La declaración debe cubrir todas las secciones, incluidas aquellas en las que no se
> usó ninguna herramienta.»*

Una sección sin fila es una sección sin declarar. Si no se usó ninguna herramienta, se
escribe «Ninguna» y se firma igual. Dejarla en blanco no equivale a declarar ausencia de uso.

---

## 1. Declaración por sección del ERS/SRS v2.0

| Sección del ERS | Herramienta | Para qué | Quién verificó | Método de verificación |
|---|---|---|---|---|
| Historial de versiones | Ninguna | — | Todo el equipo | Control manual contra commits del repositorio |
| §1. Introducción (Propósito, Alcance, Glosario, Referencias, Visión general) | Claude (Anthropic) y ChatGPT (OpenAI) | Corrección de estilo y ortografía; mejora de coherencia entre párrafos | Todo el equipo | Revisión íntegra contra los artefactos del ERS v2.0; ninguna afirmación técnica aceptada sin contraste con el documento fuente |
| §2. Descripción general (Perspectiva, Funciones, Stakeholders, i* SD/SR, Características de usuarios, Entorno operativo, Restricciones, Suposiciones) | Claude (Anthropic) y ChatGPT (OpenAI) | Corrección de estilo y ortografía; mejora de coherencia entre párrafos | Todo el equipo | Revisión íntegra contra los artefactos del ERS v2.0; ninguna afirmación técnica aceptada sin contraste con el documento fuente |
| §3. Requisitos específicos completos (Interfaces externas, RF, RNF, Explicabilidad IA, Requisitos legales, HU/Gherkin, Restricciones de diseño) | Claude (Anthropic) y ChatGPT (OpenAI) | Corrección de estilo y ortografía; mejora de coherencia entre párrafos | Todo el equipo | Revisión íntegra contra los artefactos del ERS v2.0; ninguna afirmación técnica aceptada sin contraste con el documento fuente |
| §4. Modelado del sistema con UML (Diagrama CU general, CU textuales, Clases, Secuencia CU-01–CU-12, Actividad, Estados, Componentes, Despliegue) | Claude (Anthropic) y ChatGPT (OpenAI) | Corrección de estilo y ortografía; mejora de coherencia entre párrafos | Todo el equipo | Revisión íntegra contra los artefactos del ERS v2.0; ninguna afirmación técnica aceptada sin contraste con el documento fuente |
| §5. Priorización y trazabilidad extendida (MoSCoW + Kano + WSJF; matriz end-to-end 66 filas) | Claude (Anthropic) y ChatGPT (OpenAI) | Corrección de estilo y ortografía; mejora de coherencia entre párrafos; transcripción de las filas RNF-IA-13 a RNF-IA-18 desde el `.tex` fuente | Todo el equipo; Castro Bajaña Ariel Omar (filas RNF-IA-13 a 18, commit `ade0715`) | Revisión íntegra contra los artefactos del ERS v2.0; filas nuevas cotejadas una a una contra el `.tex` y sus casos de prueba |
| §6. Producto Mínimo Viable (MVP) | Claude (Anthropic) | Revisión de redacción técnica; formateo de tablas LaTeX | Todo el equipo | Verificación contra el repositorio GitHub y el registro OSF; todos los identificadores de evidencia cotejados uno a uno |
| §7. Componente empírico — Diseño del estudio (PICOC, Protocolo experimental) | Claude (Anthropic) | Revisión de redacción técnica; formateo de tablas LaTeX | Todo el equipo | Verificación contra el repositorio GitHub y el registro OSF; todos los identificadores de evidencia cotejados uno a uno |
| §8. Requisitos de Inteligencia Artificial (Fichas IA-01/IA-02, RNF transversales, DET-01, Supervisión humana, Monitoreo, Explicabilidad y equidad) | Claude (Anthropic); Google Scholar para referencias | Sugerencia de estructura de fichas IA-01/IA-02; corrección de RNF de equidad y explicabilidad | Pérez Ruiz Carlos Andrés | DOI de cada referencia verificado en https://doi.org; umbrales validados por el equipo contra los datos del dominio |
| §9. Auditoría de calidad del ERS con seis métricas (M1–M6) | Calculadora científica y Google Sheets | Verificación aritmética independiente de M1–M6 | Pérez Ruiz Carlos Andrés y un segundo integrante de forma independiente | Conteos base realizados manualmente sobre el ERS v2.0 por dos integrantes de forma independiente |
| §10. Plan del proyecto de Ingeniería de Requisitos (Cronograma de actividades de IR) | Ninguna | — | Todo el equipo | Contraste directo contra el historial de commits y las actas de reunión |
| §11. Evidencias de elicitación (Guía de entrevista, Consentimientos informados, Actas de entrevista) | **ChatGPT GPT-5.5** (ver §2 — declarado en `06_Experimento/prompts_llm/`) | Revisión de preguntas de la guía de entrevista; corrección de transcripciones; revisión de consistencia de los RF | Todo el equipo | Los tres prompts fechados 2026-08-02 están en `06_Experimento/prompts_llm/`; los cambios introducidos por la IA fueron revisados manualmente antes de versionar cada transcripción/consentimiento/acta |
| §12. Gestión de cambios: CCB y RFC (RFC-01, RFC-02, RFC-03) | Ninguna | — | Quintero Gende Erick Jahir | Contraste de cada RFC contra los requisitos afectados en el ERS v2.0 |
| §13. Inspección Fagan PE5 — Re-inspección y defectos adicionales (D-PE5-01 a D-PE5-04) | Ninguna | — | Quintero Gende Erick Jahir | Verificación de cada defecto y su corrección en el ERS v2.0 |
| §14. Retrospectiva del equipo (Start-Stop-Continue) | Claude (Anthropic) | Revisión de ortografía y cohesión | Todo el equipo | Contenido redactado y validado íntegramente por el equipo; la IA no generó juicios ni análisis |
| §15. Declaración individual de aporte | Ninguna | — | Todo el equipo | Cada integrante declaró y firmó su propio aporte; verificado contra evidencia Git |
| §16. Declaración de uso de Inteligencia Artificial (este documento) | Claude (Anthropic) | Asistencia en la redacción y formato de la tabla de declaración, incluida la incorporación de la auditoría del 11–12 de septiembre y el cierre del manifiesto de integridad | Todo el equipo | Contenido verificado y completado por el equipo contra el historial real de uso de herramientas (verificación cruzada con `git log`, `prompts_llm/`, `manuscrito_final.pdf` y los scripts) |
| Apéndices (Retrospectiva, conclusiones editoriales) | Claude (Anthropic) | Revisión de ortografía y cohesión | Todo el equipo | Contenido redactado y validado íntegramente por el equipo; la IA no generó juicios ni análisis |

---

## 2. Declaración por artefacto (fuera del ERS)

> Completado a partir de una revisión directa del repositorio
> (`https://github.com/gleiston-guerrero/carnicore-requirements-ambiguity.git`), incluyendo el historial de commits,
> cabeceras de scripts, `.tex` del manuscrito y contenido extraído de `presentacion.pptx`
> y `guion.pdf`. Donde no se halló evidencia textual de uso de IA, se declara «Ninguna».

| Artefacto | Herramienta | Para qué | Quién verificó | Método |
|---|---|---|---|---|
| Manuscrito (`08_Publicacion/manuscrito_final.tex`) | Claude (Anthropic) | Pulir la redacción de párrafos ya escritos por el equipo y revisar el formato LaTeX, conforme a las políticas editoriales de Elsevier y Springer Nature | Todo el equipo (autores) | Uso declarado explícitamente en la sección «Uso de tecnologías asistidas por inteligencia artificial» del propio manuscrito; ninguna cifra, tabla, figura o conclusión fue generada por el modelo — todas provienen de `07_Datos/scripts/` ejecutados sobre datos crudos. `pdfinfo` confirma `Producer: pdfTeX`, sin huella de servicio web |
| Protocolo experimental (`09_Etica/A01_Protocolo_Investigacion.pdf`) | Ninguna | — | Todo el equipo | Sin menciones de herramientas de IA en el texto extraído del documento ni en su historial de commits |
| `detector_ambiguedad.py` | Ninguna | — | Pérez Ruiz Carlos Andrés y Castro Bajaña Ariel Omar (autores según `git log`) | El propio script indica «LÓGICA CONGELADA. NO MODIFICAR»: patrones y umbrales son los pre-registrados en OSF (osf.io/yp7t3); cualquier cambio se registra antes como desviación en `07_Datos/desviaciones.md` |
| Scripts de análisis (01–06, `07_Datos/scripts/`) | Ninguna | — | Pérez Ruiz Carlos Andrés (autor principal según historial Git) | Sin menciones de IA en cabeceras ni mensajes de commit. `python3 07_Datos/scripts/run_all.py` se ejecutó de extremo a extremo (7/7 pasos) sin errores, regenerando `dataset_consolidado.csv`, `kappa_resultados.json` (κ de Fleiss = 0,2636), `bootstrap_ic95.json`, figuras y `analisis_potencia.json` a partir de los datos reales, sin generar datos simulados |
| `run_all.py` — adición de `SOURCE_DATE_EPOCH` | Claude (Anthropic) | Hacer determinista la salida de las figuras PDF de matplotlib (el `/CreationDate` embebido cambiaba en cada corrida e invalidaba los manifiestos de checksums) | Quintero Gende Erick Jahir (commits `274ef4d`, `3540f72`) | Pipeline ejecutado dos veces consecutivas sobre el mismo entorno; las 4 figuras PDF resultaron idénticas byte a byte entre ambas corridas |
| `07_Datos/scripts/Makefile` | Claude (Anthropic) | Corrección de 6 rutas obsoletas (`07_Publicacion`→`08_Publicacion`) en el target `clean`, remanentes de una renumeración de carpetas anterior | Quintero Gende Erick Jahir (commit `274ef4d`) | Cotejo de las rutas corregidas contra la estructura real del repositorio |
| `04_Trazabilidad/Matriz_Trazabilidad.csv` — filas RNF-IA-13 a 18 | Claude (Anthropic) | Transcripción de los requisitos ya redactados en `01_ERS/ERS_SRS_2B_v2.0.tex` (detección DET-01, supervisión humana, monitoreo, riesgo, explicabilidad y equidad del detector) que no habían sido volcados a la matriz | Castro Bajaña Ariel Omar (commit `ade0715`) | Cotejo fila por fila contra `RNF-IA-13`…`RNF-IA-18` y sus casos de prueba (`CP-IA-13`…`CP-IA-18`) en el `.tex` fuente |
| `generar_filas_exif.py` (script auxiliar, fuera del pipeline de análisis) | Claude (Anthropic) | Leer metadatos EXIF reales de `02_Evidencias/Cuestionario/Fotos_Aplicacion/` y calcular su SHA-256, para poblar `exif_inventario.csv` sin transcripción manual | Gamarra Araujo Edhu Xavier (commits `83a9ef5`, `61fcf27`, `df1cfb9`) | El script no genera ni modifica metadatos: solo lee lo ya presente en cada archivo. Verificado que el hash de cada fila del CSV coincide con el archivo real |
| `10_Autoria/grabaciones/*.mp4` — recorte a ≤15 min | Claude (Anthropic), mediante `ffmpeg -c copy` (sin recodificar) | Ajustar la duración de las dos grabaciones de sesión al rango de 10–15 minutos exigido por la guía | Pérez Ruiz Carlos Andrés (commit `0d50136`) | Verificada la duración final (≤15:00) y la integridad de los streams de video (H.264) y audio (AAC) tras el recorte |
| `checksums.sha256` y `07_Datos/checksums_datos.sha256` — regeneración de cierre | Claude (Anthropic), mediante el comando `find` documentado en `README.md` §3 | Regenerar ambos manifiestos de integridad sobre el estado final del repositorio, tras incorporar todas las correcciones anteriores | Todo el equipo | `sha256sum -c` ejecutado sobre un clon limpio: **604/604 `OK`** en `checksums.sha256` y **35/35 `OK`** en `checksums_datos.sha256` |
| Backend del MVP (`05_MVP/backend/`) | Claude (Anthropic) | Auditoría técnica del 3 de septiembre de 2026: parches de configuración (roles, variables de entorno, Docker) — ver fila de auditoría en la Sección 3 | Todo el equipo | Revisado línea a línea contra la versión previa en Git |
| Frontend del MVP (`05_MVP/frontend/`) | Ninguna | — | Todo el equipo | Sin menciones de IA en el historial de commits del frontend |
| Diagramas UML (`03_Modelado/Diagramas_UML/`) | Ninguna | — | Todo el equipo | Fuentes editables en formato `.drawio` (`10_Autoria/fuentes_editables/`), elaboradas manualmente por los integrantes según autoría de los commits; sin menciones de IA |
| Mockups (diseño en Figma) | Ninguna | Figma es una herramienta de diseño de interfaces, no de inteligencia artificial | Todo el equipo | Enlace de diseño referenciado en el repositorio (`02_Evidencias/`); sin uso de asistencia de IA declarado |
| Presentación de defensa (`11_Defensa/presentacion.pptx`, `guion.pdf`) | Ninguna | — | Todo el equipo | Inspección del texto de las diapositivas del `.pptx` y del texto extraído de `guion.pdf` con `pdftotext` — sin términos `chatgpt`, `claude`, `anthropic`, `openai`, `gpt-`, `LLM`, `IA`, `inteligencia artificial` |
| Prompts LLM versionados (`06_Experimento/prompts_llm/prompt_01..03_*.md`) | **ChatGPT GPT-5.5** (prompts del 2 de agosto de 2026) | (1) Revisar preguntas de la guía de entrevista; (2) Corregir ortografía/puntuación de transcripciones; (3) Revisar consistencia de los requisitos funcionales | Pérez Ruiz Carlos Andrés y Quintero Gende Erick Jahir (autoría de los prompts según historial) | Los tres prompts están fechados y declaran el modelo en su cabecera. La salida del modelo se aplicó de forma selectiva, conservando los originales cuando se descartó el cambio |

---

## 3. Auditoría técnica del 3 de septiembre de 2026

| Campo | Contenido |
|---|---|
| **Fecha** | 3 de septiembre de 2026 |
| **Herramienta** | Claude (Anthropic) |
| **Para qué** | Auditoría técnica del repositorio contra la guía de desarrollo: verificación de estructura, ejecución del pipeline de análisis, comprobación del manifiesto de integridad, lectura de metadatos PDF, análisis estático del backend y cotejo del corpus de requisitos contra el `.tex` del ERS. |
| **Qué produjo la herramienta** | Informe de auditoría; `07_Datos/` (README, diccionario, licencia, desviaciones, registro de depósito); `10_Autoria/` (estructura, plantillas y scripts); `extraer_rf_desde_tex.py`; `README.md`, `CHANGELOG.md`, `CITATION.cff`, `.gitignore`, `.gitattributes`, `.mailmap`; parches del MVP; fragmento `.tex` de RNF del componente inteligente. |
| **Qué NO produjo** | Ninguna evidencia de autoría. No generó bitácoras rellenadas, capturas, grabaciones, notas de campo, fotografías, hojas de codificación ni firmas. |
| **Quién verificó** | Pérez Ruiz Carlos Andrés — 3 de septiembre de 2026. Verificación independiente completada el 4 de septiembre de 2026. |
| **Método de verificación** | `python3 07_Datos/scripts/run_all.py` ejecutado de extremo a extremo (7/7 pasos, κ de Fleiss = 0,2636); manifiesto de integridad verificado (604/604 archivos con contenido íntegro a esa fecha); `pdfinfo` confirmó `Producer: pdfTeX` en los tres PDF clave, sin huella de convertidores web; corpus de requisitos cotejado contra el `.tex` (`rf27.json`, detector 0/27). |

### Auditoría técnica del 11–12 de septiembre de 2026

| Campo | Contenido |
|---|---|
| **Fecha** | 11–12 de septiembre de 2026 |
| **Herramienta** | Claude (Anthropic) |
| **Para qué** | Auditoría de seguimiento: verificación de la matriz de trazabilidad contra el `.tex` del ERS, verificación de reproducibilidad del pipeline entre corridas sucesivas, revisión de rutas en `Makefile`, verificación de metadatos EXIF de las fotografías de aplicación del cuestionario, y regeneración final de ambos manifiestos de integridad. |
| **Qué produjo la herramienta** | Filas `RNF-IA-13` a `RNF-IA-18` en `04_Trazabilidad/Matriz_Trazabilidad.csv`; corrección de 6 rutas obsoletas en `07_Datos/scripts/Makefile`; adición de `SOURCE_DATE_EPOCH` en `run_all.py`; script auxiliar `generar_filas_exif.py`; recorte de las dos grabaciones a ≤15 minutos; regeneración de `checksums.sha256` y `checksums_datos.sha256` sobre el estado final. |
| **Qué NO produjo** | Ninguna evidencia de autoría ni ningún dato EXIF: las fotografías fueron re-tomadas y subidas por el equipo desde el dispositivo original; la herramienta solo leyó los metadatos ya presentes y calculó el hash SHA-256. Tampoco produjo ninguna cifra del componente empírico. |
| **Quién verificó** | Castro Bajaña Ariel Omar — matriz de trazabilidad (commit `ade0715`); Quintero Gende Erick Jahir — `Makefile` y `run_all.py` (commits `274ef4d`, `3540f72`); Pérez Ruiz Carlos Andrés — recorte de grabaciones (commit `0d50136`); Gamarra Araujo Edhu Xavier — fotografías EXIF y `exif_inventario.csv` (commits `83a9ef5`, `61fcf27`, `df1cfb9`); todo el equipo — regeneración final de checksums. |
| **Método de verificación** | 1. Matriz de trazabilidad cotejada fila por fila contra el `.tex` y sus casos de prueba. <br>2. `run_all.py` ejecutado dos veces consecutivas: las 4 figuras PDF salieron idénticas byte a byte. <br>3. Las 5 fotografías del cuestionario verificadas con `Pillow`: EXIF real (`DateTimeOriginal`, `Make`, `Model`); hash de cada fila de `exif_inventario.csv` (en `10_Autoria/`) coincide con el archivo real. <br>4. Grabaciones verificadas en duración (≤15:00) e integridad de streams. <br>5. **`sha256sum -c checksums.sha256` sobre un clon limpio: 604/604 `OK`. `sha256sum -c 07_Datos/checksums_datos.sha256`: 35/35 `OK`.** |

---

## 4. Declaración de límites

Lo siguiente se afirma a la luz de la revisión técnica del 12 de septiembre de 2026:

- [x] **Ninguna afirmación técnica generada por una herramienta se incorporó sin contraste
      contra el artefacto fuente.** Confirmado en las revisiones del 4-sep y del 12-sep.
- [x] **Ninguna cifra de ningún documento procede de una herramienta: todas salen del
      pipeline versionado, y el manifiesto de integridad confirma que el repositorio
      entregado coincide con lo versionado.** Confirmado: κ = 0,2636; el pipeline corre
      7/7 pasos limpio; **`checksums.sha256` 604/604 `OK`** y **`checksums_datos.sha256`
      35/35 `OK`**, verificados sobre un clon limpio el 12 de septiembre de 2026.
- [x] **Las secciones evaluativas —análisis, justificación de decisiones de IR,
      conclusiones— son producción propia del equipo.** Confirmado: la IA solo se usó
      para estilo/formato, nunca para el contenido argumental.
- [x] **Ninguna evidencia de autoría (bitácoras, capturas, grabaciones, fotografías,
      notas, hojas de codificación) fue generada ni completada por una herramienta.**
      ChatGPT GPT-5.5 intervino sobre las transcripciones únicamente como asistente de
      edición, con cada cambio validado por el equipo. La IA tampoco generó ni alteró
      metadatos EXIF de ninguna fotografía: solo los leyó de archivos provistos por el
      equipo.
- [x] **Ninguna referencia bibliográfica fue aceptada sin verificar su DOI.** DOI de
      cada entrada de `08_Publicacion/referencias.bib` contrastado con `https://doi.org`.
- [x] **El manifiesto de integridad del repositorio entregado está actualizado y
      verifica al 100 % sobre un clon limpio.** `checksums.sha256`: 604/604 `OK`.
      `07_Datos/checksums_datos.sha256`: 35/35 `OK`. Verificado el 12 de septiembre de 2026.
> **Nota de cierre (12-sep, revisión final):** los manifiestos se regeneraron una vez
> más para eliminar un BOM (Byte Order Mark) introducido por `Set-Content -Encoding UTF8`
> de PowerShell, que corrompía la primera línea de cada archivo. Verificado sin BOM y
> 100 % `OK` en ambos manifiestos sobre la línea base `v2.3.2`.
---

## 5. Firmas

Firman los cinco integrantes, dando conformidad al contenido íntegro de esta declaración.

| Integrante | Firma | Fecha |
|---|---|---|
| Castro Bajaña Ariel Omar | *Ariel Omar Castro Bajaña* | 2026-09-12 |
| Crespo Espinoza Kleber Obed | *Kleber Obed Crespo Espinoza* | 2026-09-12 |
| Gamarra Araujo Edhu Xavier | *Edhu Xavier Gamarra Araujo* | 2026-09-12 |
| Pérez Ruiz Carlos Andrés | *Carlos Andrés Pérez Ruiz* | 2026-09-12 |
| Quintero Gende Erick Jahir | *Erick Jahir Quintero Gende* | 2026-09-12 |

---

## Anexo I — Resumen de la revisión técnica del 4 de septiembre de 2026

| Comprobación | Resultado |
|---|---|
| Commit de referencia | `main` @ `6204977` — 419 commits totales a esa fecha |
| Estructura del árbol | Coincide con la Sección 7 del README |
| `pdfinfo` sobre ERS / manuscrito / FAIR | `pdfTeX` en los tres; sin huella de servicio web |
| `python3 07_Datos/scripts/run_all.py` | 7/7 pasos completados sin error |
| `sha256sum -c checksums.sha256` (manifiesto de esa fecha) | 604/604 archivos con contenido íntegro |
| `06_Experimento/prompts_llm/` | 3 prompts fechados 2026-08-02, modelo ChatGPT GPT-5.5 declarado |
| Uso declarado en manuscrito | Sección «Uso de tecnologías asistidas por inteligencia artificial» presente |

## Anexo II — Resumen de la revisión técnica del 11–12 de septiembre de 2026

| Comprobación | Resultado |
|---|---|
| Matriz de trazabilidad | Completa: `RNF-IA-01` a `RNF-IA-18`, cotejadas contra el `.tex` fuente |
| `run_all.py` (dos corridas consecutivas) | 7/7 pasos sin error en ambas; figuras PDF idénticas byte a byte |
| Compilación de `01_ERS/ERS_SRS_2B_v2.0.tex` | Sin referencias sin resolver; PDF generado correctamente |
| EXIF de fotografías del cuestionario | Las 5 con `DateTimeOriginal` y `Make/Model` reales; hashes verificados |
| Duración de grabaciones | Ambas ≤ 15:00; streams de video y audio íntegros |
| `checksums.sha256` | **604/604 `OK`**, verificado sobre clon limpio |
| `07_Datos/checksums_datos.sha256` | **35/35 `OK`**, verificado sobre clon limpio |

---

*Documento actualizado y cerrado el 12 de septiembre de 2026. Incorpora la auditoría
técnica del 11–12 de septiembre y la verificación final del manifiesto de integridad.
Todas las condiciones de la Sección 4 se confirman cumplidas a esta fecha.*
