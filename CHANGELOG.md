# Changelog

Todas las modificaciones relevantes de este proyecto se documentan aquí.
El formato sigue [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/)
y el versionado sigue [Versionado Semántico](https://semver.org/lang/es/).

Correspondencia entre versiones y entregas del PFC:

|Versión|Entrega|Semana|
|-|-|-|
|0.1.0|Entrega 1 (1A)|4|
|0.5.0|Entrega 2 (1B)|10|
|1.0.0|Entrega 3 (2A)|13|
|2.0.0|Entrega 4 (2B / Defensa)|17|
|2.1.0|Correcciones para el examen final|19|
|2.2.0|Cierre de pendientes (member checking, zona de evidencia)|19|
|2.2.1|Corrección de metadatos, consentimientos y estabilidad de checksums|19|
|2.3.0|Reproducibilidad de figuras y actualización de trazabilidad|19|
|2.3.1|Estabilización de manifiestos de integridad (BOM/EOL)|19|
|2.3.2|Manifiestos finales sin autorreferencia|19|
|2.4.0|Correcciones del examen suspenso (guía del 18/09/2026)|20|
|2.4.1|Correcciones de contenido tras informe docente del 16/09/2026|20|

---

## [2.4.1] — 2026-09-16 — Correcciones de contenido tras informe de evaluación

> Responde al informe de evaluación del examen suspenso (revisión docente del 16/09/2026,
> 18:18 Ecuador), que encontró que el ERS y la matriz cumplían el conteo mecánico de la guía
> pero no el contenido exigido, y que esta misma entrada del CHANGELOG (entonces 2.4.0)
> afirmaba cosas que el repositorio desmentía. Etiqueta anotada `v2.4.0` **ya creada** sobre
> el commit `785b86d`; ver "Pendiente real" al final de esta entrada para la etiqueta de
> cierre sobre el commit final, posterior a esta corrección.

### Corregido

* **Los 12 casos de uso del ERS, contenido real (no solo conteo).** El informe encontró que
  CU-07, CU-09 y CU-10 no tenían una excepción propia con poscondición (estaba embebida sin
  estructura dentro del flujo principal), y que cinco flujos se disparaban bajo una condición
  que la propia precondición del caso de uso ya excluía (CU-01, CU-02, CU-08, CU-11, CU-12).
  Se dio a CU-07, CU-09 y CU-10 su excepción en bloque propio, con disparo y poscondición; se
  relajaron las cinco precondiciones contradictorias; y se incorporó la georreferencia de
  RF-17 como segundo flujo alternativo propio de CU-01, que antes solo la mencionaba dentro
  del flujo principal sin especificarla. `01_ERS/ERS_SRS_2B_v2.0.tex` recompilado (142
  páginas). (Gamarra Araujo Edhu Xavier; Quintero Gende Erick Jahir)
* **Matriz de trazabilidad, huecos de HU/CA.** De las 24 filas nuevas de flujos y excepciones,
  12 no tenían historia de usuario ni criterio de aceptación. Se completaron reutilizando la
  HU/CA del caso de uso base donde existía, y se crearon **HU-05** y **HU-12** —con su
  Dado/Cuando/Entonces— para CU-05 y CU-11, que no tenían historia de usuario propia.
  (Quintero Gende Erick Jahir)
* **Tabla de trazabilidad interna del ERS desincronizada de la matriz externa.** La Sección 5
  del ERS seguía en 60 filas y sin columna `Flujo`, aunque `04_Trazabilidad/Matriz_Trazabilidad.csv`
  ya tenía 90. Se sincronizó a 84 filas (60 base/IA + 24 de flujos y excepciones), con columna
  `Flujo` añadida, y se agregó la entrada de historial de versiones v2.1 del propio ERS
  documentando el cambio. (Gamarra Araujo Edhu Xavier)
* **La entrada `[2.4.0]` de este mismo archivo afirmaba cosas que el repositorio desmentía,
  señalado en la revisión docente del 16/09/2026:** decía "Pendiente de etiquetar" cuando la
  etiqueta `v2.4.0` ya existía; atribuía a Pérez Ruiz Carlos Andrés la regeneración de
  `checksums_datos.sha256` y de `checksums.sha256` sin BOM, cuando su último commit es del
  12/09 y esos cambios los hicieron Quintero Gende Erick Jahir (`db51466`, `4142f7b`) y
  Gamarra Araujo Edhu Xavier (`785b86d`, `1e3c1f8`, `27371b0`); y daba como ejemplo de flujo
  del ERS "proveedor sin georreferencia", que ningún flujo trata (el flujo real es el caso
  contrario: georreferencia sí registrada). Las tres afirmaciones se corrigieron directamente
  en la entrada `[2.4.0]` de arriba, en vez de dejarlas y solo señalarlas aquí.
* **`README.md`, ítem P6 y oración truncada.** Al declarar `v2.4.0` como línea base vigente se
  perdió por error la línea de cierre de la oración de verificación (`10_Autoria/verificacion_previa.pdf`)
  y el criterio de piso **P6** completo, quedando **P5** duplicado en su lugar. Restaurados
  ambos. (Gamarra Araujo Edhu Xavier)

### Añadido

* **Retrospectiva del equipo, reescrita.** `10_Autoria/retrospectiva_equipo.md` tenía
  instrucciones de plantilla sin resolver ("actualizar a la fecha real...", "sustituir o
  ampliar esta sección..."), atribuía a Pérez Ruiz Carlos Andrés la regeneración final de
  manifiestos y el CHANGELOG sin tener commits en esta fase, y sus cinco firmas las había
  escrito una sola persona en un único commit. Reescrita sin texto de plantilla, con autoría
  verificada contra `git log`, y con una firma por commit: Gamarra Araujo Edhu Xavier y
  Quintero Gende Erick Jahir firmaron cada uno el suyo. El documento declara además, con base
  en el mismo corte que usa el informe docente (14/09/2026), que Castro Bajaña Ariel Omar,
  Crespo Espinoza Kleber Obed y Pérez Ruiz Carlos Andrés no tienen commits en esta fase de
  cierre y por eso no firman, sin que eso altere su participación ya registrada en el resto
  del historial. (Gamarra Araujo Edhu Xavier; Quintero Gende Erick Jahir)
* **`10_Autoria/aporte_individual.md` actualizado** con los commits del cierre por integrante.
  (Quintero Gende Erick Jahir)
* **`10_Autoria/bitacora_sesiones.csv` completada** con las sesiones del 15 y 16 de septiembre,
  que faltaban. (Quintero Gende Erick Jahir)
* **Fotografías del entorno reemplazadas** (`10_Autoria/fotos_equipo/`): las seis del 02/08 se
  retiraron y se agregaron ocho nuevas del 15/09, con `exif_inventario.csv` regenerado a partir
  de los metadatos reales de las fotos vigentes. (Quintero Gende Erick Jahir; Gamarra Araujo
  Edhu Xavier)
* **`declaracion_uso_ia.md`** corregido tras el reemplazo de `exif_inventario.csv` para que su
  referencia siga apuntando al archivo vigente. (Gamarra Araujo Edhu Xavier)

### Pendiente real (requiere acción adicional del equipo antes del corte)

* **Nueva etiqueta anotada de cierre** sobre el commit final, posterior a esta entrada del
  CHANGELOG. La etiqueta `v2.4.0` existe pero apunta a `785b86d`, anterior a las correcciones
  de contenido de §4 y §16 documentadas arriba; por la regla de dependencia de la guía, su
  estado efectivo queda congelado al estado de lo que etiqueta. Se propone `v2.4.1` para la
  nueva etiqueta, en consistencia con esta entrada.
* Regenerar `checksums.sha256` y `checksums_datos.sha256` una vez más después de comitear esta
  entrada, y antes de crear `v2.4.1`.

---

## [2.4.0] — 2026-09-15 — Correcciones del examen suspenso

> Responde a la guía de cierre y rúbrica del examen suspenso (verificación docente del
> 15/09/2026, corte 18/09/2026 23:55). Etiqueta anotada `v2.4.0` creada sobre el commit
> `785b86d` (ver entrada `[2.4.1]` para las correcciones de contenido posteriores).

### Corregido

* **DEV-03 — corpus del detector desincronizado del ERS.** `07_Datos/scripts/rf27.json`
  conservaba la redacción de la Entrega 3 (2A) en 21 de los 27 requisitos, en vez del ERS
  v2.0 entregado. Se regeneró de forma determinista con `extraer_rf_desde_tex.py` y se
  reejecutó el pipeline completo sobre un clon limpio, confirmando que ninguna cifra
  publicada cambia. El histórico `rf25.json`, que había servido de prueba documental de la
  desviación, se eliminó una vez cumplida su función; todas las referencias a él en
  `README_dataset.md`, `manuscrito_final.tex` y `scripts/README.md` se corrigieron o
  retiraron. Documentado en `07_Datos/desviaciones.md`.
  (Quintero Gende Erick Jahir; Gamarra Araujo Edhu Xavier)
* **`checksums_datos.sha256` desincronizado.** `registro_deposito.md` y `scripts/README.md`
  se habían editado después de firmar el manifiesto de datos. Regenerado tras confirmar que
  el contenido de ambos archivos ya era correcto. (Quintero Gende Erick Jahir)
* **`checksums.sha256` con BOM en la primera línea.** El BOM al inicio del archivo hacía que
  `sha256sum -c` reportara esa línea como mal formada y la omitiera silenciosamente de la
  verificación, sin comprobar ese archivo. Regenerado sin BOM y con terminador de línea LF
  puro en las 625 entradas; `sha256sum -c checksums.sha256 --quiet` ahora no imprime nada.
  (Gamarra Araujo Edhu Xavier)
* **URL canónica del repositorio.** Corregida en `CITATION.cff`, `README.md`,
  `registro_deposito.md` y `10_Autoria/aporte_individual.md` tras el cambio de propietario
  del repositorio. (Gamarra Araujo Edhu Xavier; Quintero Gende Erick Jahir)
* **Identificador de `osf_registration`.** Corregido en `.tex`, recompilado el `.pdf` y
  actualizada la figura `osf_detalle_registro.png`. (Crespo Espinoza Kleber Obed; Castro
  Bajaña Ariel Omar)
* **Fecha errónea en `osf_deviations.tex`** (18/09 → 14/09); PDF recompilado. (Gamarra
  Araujo Edhu Xavier; Quintero Gende Erick Jahir)
* **Desviación de numeración de carpetas documentada.** La carpeta de ética es `09_Etica` y
  la de defensa `11_Defensa`, no `08_Etica`/`09_Defensa` como en la numeración original de la
  guía; la diferencia viene de haber insertado `07_Datos` (SES-008, 03/09) y `10_Autoria`
  (SES-009, 04/09) en la secuencia. Se documenta explícitamente en `README.md` §7 en vez de
  renumerar, para no romper las rutas ya versionadas en scripts, checksums y el propio ERS.
  (Ver README.md)

### Añadido

* **Flujo alternativo y excepción en los 12 casos de uso del ERS** (CU-01 a CU-12), exigidos
  por ISO/IEC/IEEE 29148 para especificar el comportamiento cuando el flujo principal no se
  cumple (arete inexistente, pesaje fuera de rango, georreferencia del proveedor, caducidad
  vencida, entre otros). `01_ERS/ERS_SRS_2B_v2.0.tex` recompilado.
  (Quintero Gende Erick Jahir: CU-01 a CU-06; Gamarra Araujo Edhu Xavier: CU-07 a CU-12)
* **Columna `Flujo` en la matriz de trazabilidad** y 24 filas nuevas (un flujo alternativo y
  una excepción por cada CU), que la amplían de 66 a 90 filas. Corregida además la fila
  huérfana de RF-17 (antes forzaba `"CU-01 alt."` en la columna `CU`; ahora `CU-01` con
  `Flujo = Alternativo`), cerrando el hallazgo D-PE5-02 de completitud.
  (Quintero Gende Erick Jahir)
* **`10_Autoria/retrospectiva_equipo.md`**: retrospectiva del equipo con resumen del
  desarrollo, distribución real de commits por integrante (contada sobre `git log`, no sobre
  `aporte_individual.md`) y lecciones aprendidas sobre reproducibilidad y mantenimiento del
  corpus.
* **Comprobante externo del registro previo.** Depositada la consulta pública a la API de
  OSF para el registro `yp7t3` (`06_Experimento/registro_previo/consulta.json` y
  `registro_osf.pdf`), con fecha de registro anterior al panel de expertos.
  (Quintero Gende Erick Jahir)

### Cierre de esta versión

* Etiqueta anotada `v2.4.0` creada y publicada sobre el último commit de esta entrada
  (`785b86d`). Las correcciones de contenido encontradas en la revisión docente posterior se
  documentan en la entrada `[2.4.1]`.

---

## [2.3.2] — 2026-09-12 — Manifiestos finales sin autorreferencia

### Corregido

* Referencia al tag `v2.3.2` sin hash embebido en el propio manifiesto, para evitar que el
  manifiesto se autorreferencie y quede inestable.
* EOL de `checksums.sha256`/`checksums_datos.sha256` forzado a LF explícito, sin depender del
  `Environment.NewLine` del sistema operativo que los genera.
* `exif_inventario.csv` renormalizado a LF.
* `declaracion_uso_ia.md` y `README.md` actualizados.
* Manifiestos regenerados desde un clon limpio, sin BOM ni residuos de EOL.

(Pérez Ruiz Carlos Andrés)

---

## [2.3.1] — 2026-09-12 — Estabilización de manifiestos de integridad (BOM/EOL)

### Corregido

* BOM en `checksums.sha256`/`checksums_datos.sha256` corregido (causaba que `sha256sum -c`
  reportara la primera línea como mal formada).
* Manifiestos regenerados desde un clon limpio y, luego, tras una corrección final de
  `README.md`.

(Pérez Ruiz Carlos Andrés)

---

## [2.3.0] — 2026-09-12 — Reproducibilidad de figuras y actualización de trazabilidad

### Corregido

* Ruta obsoleta en `07_Datos/scripts/Makefile`. (Quintero Gende Erick Jahir)
* Reproducibilidad de `05_generar_figuras.py` fijada (parámetros de render deterministas).
  (Quintero Gende Erick Jahir)
* Imágenes de evidencia del encuestado corregidas; `exif_inventario.csv` actualizado.
  (Gamarra Araujo Edhu Xavier)
* Grabaciones de la sesión de verificación recortadas a ≤ 15 minutos, según exige la guía.
  (Pérez Ruiz Carlos Andrés)
* `declaracion_uso_ia.md` actualizado. (Pérez Ruiz Carlos Andrés)

### Cambiado

* Matriz de trazabilidad actualizada. (Castro Bajaña Ariel Omar)
* Manifiestos de integridad regenerados sobre el estado final del repositorio.
  (Pérez Ruiz Carlos Andrés)

---

## [2.2.1] — 2026-09-09 — Corrección de metadatos, consentimientos y estabilidad de checksums

### Corregido

* Sigla del equipo en `registro_deposito.md` (AHMRV → CCGaPQ) y referencia `run_all.sh` →
  `run_all.py`. (Pérez Ruiz Carlos Andrés)
* Metadato `pdftitle` del `ERS_SRS_2B_v2.0.tex` corregido para mejorar la indexación en
  Zenodo; PDF recompilado. (Pérez Ruiz Carlos Andrés)
* Salidas del pipeline forzadas a LF (`csv.DictWriter` con `lineterminator`, `newline=''` en
  `open()`/`write_text()`) y renormalizadas según `.gitattributes`, para que los hashes sean
  estables entre sistemas operativos. (Pérez Ruiz Carlos Andrés)
* `checksums.sha256` y `checksums_datos.sha256` regenerados varias veces hasta estabilizarse
  sin BOM y con LF puro sobre un clon limpio. (Pérez Ruiz Carlos Andrés)

### Añadido

* Consentimientos anonimizados actualizados: ENTR-01, ENTR-02, ENTR-03, ENTR-11, ENTR-12-13
  y otros. (Quintero Gende Erick Jahir; Gamarra Araujo Edhu Xavier; Castro Bajaña Ariel Omar)
* `09_Defensa/verificacion_previa.pdf` con la verificación previa de la entrega.
  (Crespo Espinoza Kleber Obed; Pérez Ruiz Carlos Andrés)
* Checklist de entrega actualizado en `README.md`; nota de hash de contenedor actualizada en
  `fichas_tecnicas.csv`. (Pérez Ruiz Carlos Andrés)
* Bitácora de sesiones y `aporte_individual.md` regenerados con los commits nuevos.
  (Crespo Espinoza Kleber Obed)

---

## [2.2.0] — 2026-09-05 — Sesión de member checking, corrección de zona de evidencia y cierre de pendientes

### Añadido

* **Sesión de member checking realizada.** Sesión grupal de verificación de interpretación de
  resultados con participantes ENTR-05, ENTR-11 y ENTR-14 (2026-09-04). Depositados: acta
  firmada y material de presentación en `02_Evidencias/Member_checking/`, y el video de la
  sesión cifrado como `17-evidencias_restringidas.7z` con su fila correspondiente en
  `fichas_tecnicas.csv`.
* **Correspondencia con la organización (A8).** Depositadas las solicitudes fechadas de
  sesión de member checking y de documentos adicionales en `10_Autoria/correspondencia/`; las
  respuestas de la organización quedaron adjuntas dentro de esos mismos documentos.

### Corregido — hallazgo crítico de zona de evidencia

* **Videos de walkthrough retirados de la zona pública.** Los tres videos de evidencia de
  walkthrough (`01_evidencia_walkthrough_no_tecnico.mp4`, `01_evidencia_walkthrough_tecnico.mp4`,
  `02_evidencia_walkthrough_tecnico.mp4`) estaban en `02_Evidencias/Validacion_Walkthrough/`
  sin cifrar, con rostros de personas participantes claramente identificables. Esto
  incumplía la Sección 3 de la guía, que exige que la grabación de cada sesión de validación
  vaya en la zona restringida cifrada [R] y que solo el acta enmascarada sea pública [P]. Se
  comprimieron los tres videos con AES-256 en `18-evidencias_restringidas.7z`, se retiraron
  de la carpeta pública, y se agregaron las tres filas correspondientes
  (`WALKTHROUGH-NO-TEC-01`, `WALKTHROUGH-TEC-01`, `WALKTHROUGH-TEC-02`) a
  `fichas_tecnicas.csv`.
* **Pendiente de este mismo hallazgo:** los tres archivos ya retirados siguen existiendo en
  commits anteriores del historial de git (`ee59f8e` y posteriores). Retirarlos de la carpeta
  no los elimina del historial; se requiere `git filter-repo` seguido de `push --force` y
  re-clonado por parte de todo el equipo antes de considerar este punto cerrado.

### Pendiente real de esta versión (resuelto en versiones posteriores, ver arriba)

* ~~Etiqueta anotada de línea base (`git tag -a`), publicada en el remoto.~~ Resuelto: v2.2.1
  en adelante sí quedaron etiquetadas; falta la etiqueta de cierre de v2.4.0 (ver el inicio
  de este archivo).
* ~~`checksums.sha256` y `07_Datos/checksums_datos.sha256`: regenerar como último paso.~~
  Resuelto en v2.2.1 y siguientes.
* Purgar del historial de git los tres videos de walkthrough retirados en esta versión
  (`git filter-repo` + `push --force` + re-clonado del equipo). **Sigue pendiente.**
* 2 documentos adicionales de la organización en `02_Evidencias/Documentos_Organizacion/`
  (hay 3, se piden 5). **Sigue pendiente.**
* Nombre completo de la persona participante sin enmascarar en las actas de
  `02_Evidencias/Validacion_Walkthrough/*.pdf` (dato identificable en zona pública; el rostro
  y la voz ya se resolvieron al mover los videos). **Sigue pendiente, prioridad baja.**

---

## [2.1.0] — 2026-09-04 — Correcciones para el examen final

Versión que responde al informe docente del 1 de septiembre de 2026.

### Corregido

* **Manuscrito: se reportan los resultados reales.** La versión 2.0.0 declaraba en DEV-01 que
  la fase comparativa contra el panel experto no se había ejecutado, y reportaba que el
  detector marcó 1 de 27 requisitos (3,7 %) atribuyendo la activación a RF-27 por el término
  *correspondientes*. Las tres afirmaciones eran incorrectas. El panel se ejecutó, sus
  etiquetas estaban versionadas y el detector marcó **0 de 27**. El texto citado no existe en
  RF-27. Ver `06_Experimento/osf_deviations.pdf`, apartado COR-01.
* **Manuscrito: plantilla oficial.** Se sustituyó `\documentclass{article}` por
  `\documentclass[runningheads]{llncs}`, la clase oficial de Springer LNCS exigida por el
  criterio C7 y el gatekeeper G2.
* **`splncs04.bst` reparado.** El archivo del repositorio invocaba las funciones
  `new.block.checkb`, `new.sentence.checka` y `new.sentence.checkb` sin definirlas, lo que
  hacía abortar a BibTeX con 52 errores. Se añadieron las tres definiciones.
* **`checksums.sha256` regenerado.** De las 86 entradas anteriores fallaban 7: dos rutas
  heredadas de la Entrega 3 (`01_ERS/main.tex` y `01_ERS/figura/istar_SD.svg`) ya no existían
  y cinco archivos tenían hash distinto del declarado. Además el manifiesto no cubría ningún
  archivo multimedia. El nuevo manifiesto tiene 468 entradas, incluye los 22 archivos
  multimedia y contenedores, y verifica sin error.
* **Identificador del registro OSF corregido.** Los documentos citaban `osf.io/wud69`, que es
  el identificador del *proyecto*. El identificador del *registro* es `osf.io/yp7t3`, y es
  público desde su creación. Se propagó el identificador correcto a los seis documentos donde
  aparecía. Con ello el indicador FAIR A4 pasa a cumplido.
* **Autoevaluación FAIR corregida.** La versión anterior se adjudicaba 16/16 indicadores
  (100 %) mientras el manifiesto de integridad fallaba. La nueva evaluación reconoce 14/16
  (87,5 %) y detalla los dos indicadores no cumplidos con su plan de subsanación.
* **`README.md`**: se eliminó la afirmación de 90 respuestas del cuestionario (el CSV tiene
  31), la insignia de FAIR 100 % y la marca de reproducibilidad del pipeline sobre las
  figuras del manuscrito, que hasta ahora no era cierta.
* **`README_dataset.md`**: se eliminaron los marcadores de posición «[cuando haya panel
  experto]» y «[PENDIENTE panel experto]», se corrigió el listado de archivos (varios no
  existían) y se sustituyó `run_all.sh` por `run_all.py`.
* **`fichas_tecnicas.csv`**: se corrigió la nota de ENTR-15, que afirmaba haber verificado
  manualmente una duración distinta a la de ENTR-14. Los dos vídeos son el mismo archivo
  (idéntico tamaño e idéntico CRC32). Ver
  `02_Evidencias/00_Restringido/INCIDENCIA_ENTR14_ENTR15.md`.

### Añadido

* `06_Experimento/scripts_analisis/05_generar_figuras.py`: genera todas las figuras y tablas
  de resultados del manuscrito desde los artefactos del pipeline. Cierra la causa raíz del
  error del manuscrito: ya no es posible que documento y datos diverjan sin que se note.
* `06_Experimento/scripts_analisis/06_analisis_potencia.py`: cálculo de potencia explícito
  exigido por el criterio C6 (McNemar exacta, κ mínimo detectable, N necesario, IC exacto de
  la exhaustividad).
* `06_Experimento/osf_deviations.pdf` y `.tex`: documento de desviaciones respecto del
  pre-registro, ausente en la entrega anterior.
* `herramientas/regenerar_checksums.sh`: regenera y verifica el manifiesto.
* `herramientas/verificar_dois.py`: verifica cada DOI del `.bib` contra Crossref y propone
  candidatos para las entradas sin DOI.
* `herramientas/enmascarar_consentimientos.py`: instrumento para cubrir nombre, firma y
  correo en las copias públicas de los consentimientos.
* `02_Evidencias/Codificacion_Tematica/curva_saturacion.py` y su plantilla de datos, para
  producir la curva a partir de la codificación real del equipo.
* `.mailmap`: consolida las identidades duplicadas de Git de dos integrantes.
* `09_Defensa/guion_defensa_v2.md`: guion de 25 minutos con reparto equitativo y el contenido
  de las siete láminas del componente empírico que faltaban.
* `resumen_modificaciones.md`: informe detallado de esta versión.
* Bibliografía ampliada de 18 a 62 entradas.
* Figuras 03 (acuerdo inter-evaluador) y 04 (curva de potencia), y tablas 03, 04 y 05, todas
  generadas por script.

### Cambiado

* Destino de publicación: de REFSQ 2027 Research Previews (8 páginas) a REFSQ 2027 track
  Research (15 páginas). El manuscrito corregido no cabe en ocho páginas con el trabajo
  relacionado ampliado, el análisis de sensibilidad y las ocho amenazas a la validez.
* Título del manuscrito, para que refleje el hallazgo real.
* `run_all.py` y `Makefile`: el pipeline pasa de 5 a 7 pasos.
* `CITATION.cff`: versión 2.1.0 y eliminación del texto de marcador de posición sobre el DOI.

---

## [2.0.0] — 2026-09-01 — Entrega 4 (2B / Defensa Final)

### Añadido

* ERS/SRS v2.0 definitivo unificado (135 páginas) con las observaciones de la Entrega 3
  resueltas, incorporando RF-26 y RF-27.
* Tercera ronda de trabajo de campo: entrevistas ENTR-06 a ENTR-16.
* Panel de tres personas expertas: rúbrica, plantillas anonimizadas y
  `etiquetas_expertos.csv`.
* Pipeline de análisis: `01_importar_datos.py`, `detector_ambiguedad.py`,
  `02_calcular_kappa.py`, `03_matriz_confusion_prf1.py`, `04_bootstrap_ic95.py`,
  `run_all.py`, `Makefile` y `requirements.txt`.
* Depósito Zenodo con DOI persistente y archivado en Software Heritage.
* `09_Defensa/` con presentación, guion, vídeo y folleto de una hoja.
* `fair_assessment.pdf`, `CITATION.cff` v2.0.0 y `LICENSE` con alcance explícito.

### Cambiado

* Matriz de trazabilidad ampliada a 60 filas.
* MVP: backend Node/Express/Sequelize con 15 controladores y `docker-compose`.

---

## [1.0.0] — 2026-08-02 — Entrega 3 (2A)

### Añadido

* ERS/SRS completo con 25 RF y 15 RNF.
* Protocolo experimental del Enfoque 2 y su registro en OSF (`wud69`).
* Segunda ronda de campo: entrevistas ENTR-01 a ENTR-05 y cuestionario.
* Paquete ético A01–A13 y `Adenda_Segunda_Ronda.pdf`.
* Borrador del manuscrito: introducción, trabajo relacionado y metodología.
* Modelado UML y primeros mockups.

---

## [0.5.0] — 2026-06 — Entrega 2 (1B)

### Añadido

* ERS/SRS parcial con la primera ronda de trabajo de campo.
* Identificación de interesados y catálogo inicial de requisitos.
* Primeros diagramas de contexto y de casos de uso.

---

## [0.1.0] — 2026-05 — Entrega 1 (1A)

### Añadido

* Conformación del equipo, asignación de roles y plan de trabajo.
* Identificación del sistema real y del cliente.
* Elicitación inicial y aval institucional.
* Estructura base del repositorio.
